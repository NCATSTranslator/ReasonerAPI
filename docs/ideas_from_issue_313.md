# Thoughts on Merging

Combining the results of two translator services to the same query highlights several areas by which translator results could be made more interpretable through better merging of the seemingly equivalent information. This documents some initial thoughts and a rough first pass at potential changes.

____
## Merging Knowledge Graph Nodes
Knowledge graph nodes can be simply and effecitvely merged. 
* Each identifier is normalized to a the identifier
* Attributes can be concatenated.

This simple technique is powered by the following assumptions
* Nodes can be uniquely identified by the normalized identifier
* Node attributes are an unodered list that can be concatenated without loss of information.

## Merging Knowledge Graph Edges
Knowledge graph edges currently store both EPC data and other information as a list of edge attributes. Due to the inclusion of EPC data it has been decided that edges with unique lines of EPC should not be combined, because the list of edge attributes has asigned meaning to the order of the list.

A more flexible edge attribute definition may permit the merging of knowledge graph edges. Merging knowledge graph edges would increase the overlap (equivalence, see below) of results, thereby producing more intepretable translator output.

### Equivalence
Currently it is assumed that edges are equivalent if and only if the following are equivalent
* The identifier of the subject
* The predicate 
* The identifier of the object
* The list of attribute information (including order)

As it is unlikely that the the list of attributes will match with any otherwise similar edges, knowledge graph edge merging rarely occurs. If instead we remove the final constraint and encode attribute list information in a combinable manner we can combine to edges. Consider the following edges

```json
{
  "edges": {
    "edge1a": {
      "subject": "PUBCHEM.COMPOUND:126806",
      "predicate": "biolink:treats",
      "object": "MONDO:0005148",
      "attributes": attr1a,
    },
    "edge1b": {
      "subject": "PUBCHEM.COMPOUND:126806",
      "predicate": "biolink:treats",
      "object": "MONDO:0005148",
      "attributes": attr1b,
    }
  }
}
```

These could be combined by making attribute information a dictionary with source identifiers.

```json
{
  "edges": {
    "edge1": {
      "subject": "PUBCHEM.COMPOUND:126806",
      "predicate": "biolink:treats",
      "object": "MONDO:0005148",
      "attributes": {
        "edge1a_provider_id": attr1a,
        "edge1b_provider_id": attr1b
      }
    }
  }
}
```

This newly formed edge can be used in results, making subsequent results more similar.

There are several outstanding questions regarding the source and standardization of edge provider keys, but those can likely be solved using infores. If we assume that any knowledge edge producer will attach attributes with a given key, the underlying attributes should be able to be concatenate if multiples occur.

```json
{
  "edges": {
    "edge1a": {
      "subject": "PUBCHEM.COMPOUND:126806",
      "predicate": "biolink:treats",
      "object": "MONDO:0005148",
      "attributes": attr1a,
    },
    "edge1a_different": {
      "subject": "PUBCHEM.COMPOUND:126806",
      "predicate": "biolink:treats",
      "object": "MONDO:0005148",
      "attributes": attr1a_different,
    }
  }
}
```

becomes

```json
{
  "edges": {
    "edge1a": {
      "subject": "PUBCHEM.COMPOUND:126806",
      "predicate": "biolink:treats",
      "object": "MONDO:0005148",
      "attributes": {
        "edge1a_provider_id": attr1a + attr1a_different
    }
  }
}
```

___
## Merging Results

### Equivalence
Results will be considered equivalent if
* The set of node binding ids attached to each q-node are equal
* The set of edge binding ids attached to each q-edge are equal

### Merging

When merging nodes we want to retain the unique information from two lines of reasoning. This includes
* The list of node binding attributes
* The list of edge binding attributes
* score
* any other top level meta data that is currently not standardized but is in use

Consider the following two answers
```json
[
  {
    "node_bindings": {
      "drug": [
        {
          "id": "PUBCHEM.COMPOUND:126806",
          "attributes": result1_drug_attrs
        }
      ],
      "type-2 diabetes": [
        {
          "id": "MONDO:0005148",
          "attributes": result1_diabetes_attrs
        }
      ]
    },
    "edge_bindings": {
      "treats": [
        {
          "id": "6a0dbdfc163c",
          "attributes": result1_treats_attrs
        }
      ]
    },
    "score": result1_score,
    "additional_info": result1_additional_info
  },
  {
    "node_bindings": {
      "drug": [
        {
          "id": "PUBCHEM.COMPOUND:126806",
          "attributes": result2_drug_attrs
        }
      ],
      "type-2 diabetes": [
        {
          "id": "MONDO:0005148",
          "attributes": result2_diabetes_attrs
        }
      ]
    },
    "edge_bindings": {
      "treats": [
        {
          "id": "6a0dbdfc163c",
          "attributes": result2_treats_attrs
        }
      ]
    },
    "score": result2_score,
    "additional_info": result2_additional_info
  }
]
```

To combine we must unnest node and edge binding attributes from the node and edge bindings and we must nest top level properties, score and additional_info, behind a layer. One potential option is:

```json
[
  {
    "node_bindings": {
      "drug": ["PUBCHEM.COMPOUND:126806"],
      "type-2 diabetes": ["MONDO:0005148"]
    },
    "edge_bindings": {
      "treats": ["6a0dbdfc163c"],
    },
    "analysis": {
      "result1_producer_id": {
        "node_binding_attributes": {
          "drug": {
            "PUBCHEM.COMPOUND:126806": result1_drug_attrs
          },
          "type-2 diabetes": {
            "MONDO:0005148": result1_diabetes_attrs
          }
        },
        "edge_binding_attributes": {
          "treats": {
            "6a0dbdfc163c":  result1_treats_attrs
          }
        },
        "score": results1_score,
        "additional_info": results1_additional_info
      },
      "result2_producer_id": {
        "node_binding_attributes": {
          "drug": {
            "PUBCHEM.COMPOUND:126806": result2_drug_attrs
          },
          "type-2 diabetes": {
            "MONDO:0005148": result2_diabetes_attrs
          }
        },
        "edge_binding_attributes": {
          "treats": {
            "6a0dbdfc163c":  result2_treats_attrs
          }
        },
        "score": results2_score,
        "additional_info": results2_additional_info
      },
    }
  }
]
```

All details that must be combined together are contained within a new top level key "analysis" for example. Each result producer has an identifier that can be used as a key within a dictionary, all producer's specific information is contained benethe this key.

Result producer keys may not correspond uniquely to ARAs or groups, in the event that a single ARA would like to provide information on distinct lines of reasoning. For instance, a single ARA may utilize two different algorithms to preset two different scores, so differentiating between the two would be necessary. 

Additional result producer information may need to become standardized to better support understanding of the merged message.
