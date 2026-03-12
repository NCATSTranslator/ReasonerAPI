# TRAPI 2.0 Migration Guide

This guide lays out the format and functionality changes for queries and responses in TRAPI 2.0.0 (compared to 1.6.0-beta).

TRAPI 2.0 includes many breaking changes, new/reintroduced functionality, and format changes designed to slim down TRAPI messages. This guide provides before-after examples to illustrate the more complex changes and a list for the other important changes (mainly formatting).  


## Changes with before-after examples


### 1. QEdge Constraints Refactor

#### BEFORE

In 1.6.0-beta, you could include `attribute_constraints` and `qualifier_constraints` on QEdges. If you wanted to only include or exclude specific knowledge_level/agent_type (KL/AT) values, you'd use `attribute_constraints` because KL/AT are stored in Edge `attributes`. If you wanted to only include or exclude specific sources (infores), you may have used `attribute_constraints`. BUT this format no longer makes sense after we moved source info out of Edge `attributes` into its own top-level property `sources` several versions ago (1.4.0-beta). 

A QEdge in 1.6.0-beta with all of these constraints would look like this:

```json
{
    "subject": "n0",
    "object": "n1",
    "attribute_constraints": [
        {
            "id": "biolink:agent_type",    // AT constraint
            "name": "agent type",
            "operator": "==",
            "value": "automated_agent"
        },
        {
            "id": "biolink:knowledge_source",    // source constraint: not semmeddb
            "name": "special key to query on sources info",
            "not": true,
            "operator": "==",
            "value": "infores:semmeddb"    // str or array of str
        },
        {
            "id": "biolink:z_score",    // regular attribute constraint
            "name": "z-score",
            "operator": ">",
            "value": 5
        }
    ],
    "qualifier_constraints": [
        {
            "qualifier_set": [
                {
                    "qualifier_type_id": "biolink:subject_aspect_qualifier",
                    "qualifier_value": "activity_or_abundance"
                }
            ]
        }
    ]
}
```

#### AFTER

In 2.0, there is instead one property on a QEdge, `constraints`, that holds all the types of constraints, organized by key. There are 5 keys currently specified:

* `knowledge_level`: we moved KL/AT out of Edge `attributes` and into its own top-level properties on an Edge, so they need corresponding separate constraints. This constraint is an object with two keys: `behavior` (`ALLOW` or `DENY`) and `values` (an array of strings). 
   * `ALLOW` means "ANY (at least 1) of the `values` MUST be in the matched Edge's corresponding property". 
   * `DENY` means "ALL of the `values` MUST NOT be in the matched Edge's corresponding property". 
* `agent_type`: see above (KL)
   * FYI: if a specified value has descendants (ex: `automated_agent`), the tool MUST treat those descendants (ex: `text_mining_agent`, etc.) as if they were included in the `values` array (aka "hierarchy expansion").
* `sources`: this constrains the Edge `sources`. It has the same keys as KL/AT (`behavior`, `values`) plus the optional `primary_only` (if true, the constraint ONLY applies to the `primary_knowledge_source`). 
* `attributes`: minItems 1, otherwise the same as previous `attribute_constraints`
* `qualifiers`: simplified format to an array of objects but preserved previous behavior. Each object represents a qualifier-set, and multiple objects/sets have an `OR` relationship. Within an object, the keys are the "qualifier-type-ids" and their values are the "qualifier values". Multiple key/value pairs in one object/set have an `AND` relationship. 

The same QEdge in 2.0 would look like this: 

```json
{
    "subject": "n0",
    "object": "n1",
    "constraints": {
        "agent_type": {    // AT constraint
            "behavior": "ALLOW",
            "values": ["automated_agent"]
        },
        "sources": {    // source constraint: not semmeddb
            "behavior": "DENY",
            "values": ["infores:semmeddb"]
        },
        "attributes": [
            {
                "id": "biolink:z_score",    // regular attribute constraint
                "name": "z-score",
                "operator": ">",
                "value": 5
            }
        ],
        "qualifiers": [
            // one qualifier set
            {
                "biolink:subject_aspect_qualifier": "activity_or_abundance"
            }
        ]
    }
}
```

This example Edge (not real!) would fulfill the constraints (properties put in same order as constraints for easy comparison):


```json
{
    "subject": "NCBIGene:1234",
    "object": "MONDO:1234",
    "predicate": "biolink:associated_with",
    "agent_type": "data_analysis_pipeline",    // matches AT constraint: this is a child of automated_agent
    "knowledge_level": "statistical_association",
    "sources": [    // matches source constraint: not semmeddb
        {
            "resource_id": "infores:diseases",
            "resource_role": "primary_knowledge_source"
        }
    ],
    "attributes": [
        {
            "attribute_type_id": "biolink:z_score",    // matches attrib constraint: >5
            "value": 6.435
        }
    ],
    "qualifiers": [
        {
            "qualifier_type_id": "biolink:subject_direction_qualifier",
            "qualifier_value": "decreased"
        },
        {
            "qualifier_type_id": "biolink:subject_aspect_qualifier",    // matches qualifier constraint
            "qualifier_value": "activity_or_abundance"
        },
        {
            "qualifier_type_id": "biolink:qualified_predicate",
            "qualifier_value": "biolink:causes"
        }
    ]
}
```


### 2. New Query/Response Parameters

#### BEFORE

In 1.6.0-beta, `log_level` and `bypass_cache` were top-level properties in `Query` and `AsyncQuery`. 

A query with them would look like this: 

```json
// TO-DO: snippet of a query - include those two, message {...}. Don't include custom param like data tier? 
```

#### AFTER

In 2.0, these are moved under a new top-level property `parameters` (their behavior is otherwise kept the same). `parameters` also includes a new parameter/property `timeout`, so a client can state how long they will wait for a response.

Tools can also use the new `parameters` property to hold undefined query-time parameters that affect overall behavior of the server in query execution, like specifying data-tier in the Translator ecosystem. 

`parameters` has also been added to `Response`; the server receiving a Query/AsyncQuery with `parameters` MUST echo them in its Response. If there is a conflict between the `parameters` and the server's capabilities, the server SHOULD return HTTP `409`.

A query with the same parameters (plus timeout and custom data-tier) would look like this:

```json
// TO-DO: AFTER snippet + timeout and custom data-tier
```


### 3. Binding Structure Changes (Node/Edge/Path)

#### BEFORE 

In 1.6.0-beta, the 3 kinds of bindings have this format: 

```json
...
"<node/edge/path>_bindings": {
          "key1": [
            {
              "id": "<CURIE/EdgeID/AuxGraphID>",
              "attributes": []
            }
          ],
          "key2": [
            {
              "id": "<CURIE/EdgeID/AuxGraphID>",
              "attributes": []
            }
          ]
        },
...
```

Details:
* `attributes` were required for `NodeBinding` and `EdgeBinding`, not defined/included in `PathBinding`
* NodeBinding had the optional property `query_id`, which supported an older implementation of subclassing.

<details><summary>Example result with node/edge bindings</summary>
<p>

```json
{
    "node_bindings": {
        "n0": [
            {
                "id": "NCBIGene:1234",
                "attributes": []
            }
        ],
        "n1": [
            {
                "id": "MONDO:1234",
                "attributes": []
            }
        ]
    },
    "analyses": [
        {
            "resource_id": "infores:retriever",
            "edge_bindings": {
                "e0": [
                    {
                        "id": "edge-1234-1234-1234-1234",
                        "attributes": []
                    }
                ]
            }
        }
    ]
}
```

</p>
</details> 

<details><summary>Example result with node/path bindings</summary>
<p>

```json
{
    "node_bindings": {
        "n0": [
            {
                "id": "CHEBI:4567",
                "attributes": []
            }
        ],
        "n1": [
            {
                "id": "MONDO:4567",
                "attributes": []
            }
        ]
    },
    "analyses": [
        {
            "resource_id": "infores:aragorn-shepherd",
            "path_bindings": {
                "p0": [
                    {
                        "id": "auxGraph-4567-4567-4567-4567"
                    }
                ]
            }
        }
    ]
}
```

</p>
</details> 

#### AFTER

In 2.0, the format is simplified:

```json
"<node/edge/path>_bindings": {
          "key1": {
            "ids": ["<CURIE/EdgeID/AuxGraphID>"]
          }
          "key2": {
            "ids": ["<CURIE/EdgeID/AuxGraphID>"]
          }
        },
```

Changes:
* `node/edge/path>_bindings` are now `minProperties: 1` (AKA when these fields are present, they MUST contain data) 
* `ids` arrays are `minItems: 1` (this property is still required)
* `attributes` were removed from NodeBinding/EdgeBinding (were never used, empty arrays bloated responses)
* `query_id` was removed from NodeBinding (obsolete with the current subclassing behavior)

<details><summary>Same node/edge bindings result, converted to 2.0</summary>
<p>

```json
{
    "node_bindings": {
        "n0": {
            "ids": ["NCBIGene:1234"]
        },
        "n1": {
            "ids": ["MONDO:1234"]
        }
    },
    "analyses": [
        {
            "resource_id": "infores:retriever",
            "edge_bindings": {
                "e0": {
                    "ids": ["edge-1234-1234-1234-1234"]
                }
            }
        }
    ]
}
```

</p>
</details>

<details><summary>Same node/path bindings result, converted to 2.0</summary>
<p>

```json
{
    "node_bindings": {
        "n0": {
            "ids": ["CHEBI:4567"]
        },
        "n1": {
            "ids": ["MONDO:4567"]
        }
    },
    "analyses": [
        {
            "resource_id": "infores:aragorn-shepherd",
            "path_bindings": {
                "p0": {
                    "ids": ["auxGraph-4567-4567-4567-4567"]
                }
            }
        }
    ]
}
```

</p>
</details>


## 4. Edge Output Now Requires `knowledge_level` and `agent_type`

TRAPI 2.0 requires both fields on `Edge` in addition to existing required edge fields.

```json
// TODO: Insert old/new Edge snippet showing required knowledge_level and agent_type
```

## 5. `QNode.set_interpretation` Adds `COLLATE`

TRAPI 2.0 adds `COLLATE` to `set_interpretation`, with updated expectations for `member_ids`.

```json
// TODO: Insert QNode example using COLLATE and a separate MANY/ALL example using member_ids
```



## Other Changes
A. `nullable` lines are removed in TRAPI 2.0, consistent with OpenAPI 3.1 and JSON Schema handling of nullability. This means `null` is generally not valid unless the schema explicitly allows it. For fields that are not required, clients should omit the field instead of sending `null`. For required fields, clients must send a value that matches the declared type. Parsers and validators should be updated to treat omitted and `null` values differently.
B. minItems/minProperties set to 1. Explanation: "if present, must have data - at least 1 element"
C. AuxiliaryGraph.attributes removed (previously required)
D. Changed to not required
E. Analysis allows both EdgeBinding and PathBinding (for experimental use only, small change introduced when simplifying schema classes)


## Large Example: 1.6.0-beta Response (+Query)

```json
// TODO: Insert full-size TRAPI 1.6.0-beta response example
```

## Large Example: 2.0 Response (+Query)

```json
// TODO: Insert full-size TRAPI 2.0 response example
```
