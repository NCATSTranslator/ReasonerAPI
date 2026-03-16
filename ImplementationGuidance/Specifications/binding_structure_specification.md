# Result Binding Format

These 3 kinds of bindings in Results share a common format: 
- `Result.node_bindings`
- `Result.analyses.edge_bindings`
- `Result.analyses.path_bindings`

```json
...
"<node/edge/path>_bindings": {
  "key1": {
    "ids": ["<CURIE/EdgeID/AuxGraphID>"]
  },
  "key2": {
    "ids": ["<CURIE/EdgeID/AuxGraphID>"]
  }
},
...
```

These structures hold the mapping (binding) of QueryGraph elements to matching KnowledgeGraph elements in an answer. 

Common details:
* `node_bindings` is required in `Result`; at least 1 of `["edge_bindings", "path_bindings"]` is required in an `Analysis`
* `<node/edge/path>_bindings` are `minProperties: 1`; AKA when these fields are present, they MUST contain data
* The keys in `<node/edge/path>_bindings` MUST be the same as the keys in the corresponding QueryGraph objects (`QueryGraph.<nodes/edges/paths>`)
* `ids` is required with `minItems: 1`. The items are the IDs of the matching KnowledgeGraph elements (`<Nodes/Edges/path AuxiliaryGraphs>`), and multiple items MAY be bound to a single key for one result/answer. 
* A `<Node/Edge/Path>Binding` currently MAY include other (undefined) properties besides `ids`. This is to support potential future dev work. 

Notes:
- `NodeBinding.query_id` from older TRAPI versions is obsolete and SHOULD NOT be used. 
- `Analysis` currently allows both `edge_bindings` and `path_bindings` within the same object (for experimental dev use only)


## Examples

### Results with edge bindings

```json
{
  "node_bindings": {
    "n0": { "ids": ["NCBIGene:1234"] },
    "n1": { "ids": ["MONDO:1234"] }
  },
  "analyses": [
    {
      "resource_id": "infores:retriever",
      "edge_bindings": {
        "e0": { "ids": ["edge-1234-1234-1234-1234"] }
      }
    }
  ]
}
```

Multiple nodes/edges bound to a key:

```json
{
  "node_bindings": {
    "nA": { "ids": ["CHEBI:1234"] },
    "nI": { "ids": ["NCBIGene:5555", "NCBIGene:7777"]
    },
    "nB": { "ids": ["MONDO:111"] }
  },
  "analyses": [
    {
      "resource_id": "infores:retriever",
      "edge_bindings": {
        "e1": { "ids": ["e1_A", "e1_B"] },
        "e2": { "ids": ["e2_A", "e2_B"] }
      }
    }
  ]
}
```

### Result with path bindings

```json
{
  "node_bindings": {
    "n0": { "ids": ["CHEBI:4567"] },
    "n1": { "ids": ["MONDO:4567"] }
  },
  "analyses": [
    {
      "resource_id": "infores:shepherd-aragorn",
      "path_bindings": {
        "p0": { "ids": ["auxGraph-4567-4567-4567-4567"] }
      }
    }
  ]
}
```
