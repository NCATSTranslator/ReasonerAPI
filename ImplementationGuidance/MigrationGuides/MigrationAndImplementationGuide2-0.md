# TRAPI 2.0 Migration Guide

This guide lays out the format and functionality changes for queries and responses in TRAPI 2.0.0 (compared to 1.6.0-beta).

TRAPI 2.0 includes many breaking changes, new/reintroduced functionality, and format changes designed to slim down TRAPI messages. This guide provides before-after examples to illustrate the more complex changes and a list for the other important changes (mainly formatting).  


## Changes with before-after examples


### 1. QEdge Constraints Refactor

#### BEFORE

In 1.6.0-beta, you could include `attribute_constraints` and `qualifier_constraints` on QEdges. If you wanted to only include or exclude specific knowledge_level/agent_type (KL/AT) values, you'd use `attribute_constraints` because KL/AT are stored in Edge `attributes`. If you wanted to only include or exclude specific sources (infores), you may have used `attribute_constraints`. BUT this format no longer makes sense after we moved source info out of Edge `attributes` into its own top-level property `sources` several versions ago (1.4.0-beta). 

<details><summary>A QEdge in 1.6.0-beta with all of these constraints would look like this (click to expand)
</summary>
<p>

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

</p>
</details> 

#### AFTER

In 2.0, there is instead one property on a QEdge, `constraints`, that holds all the types of constraints, organized by key. There are 5 keys currently specified:

* `knowledge_level`: we moved KL/AT out of Edge `attributes` and into its own top-level properties on an Edge (see #4), so they need corresponding separate constraints. This constraint is an object with two keys: `behavior` (`ALLOW` or `DENY`) and `values` (an array of strings). 
   * `ALLOW` means "ANY (at least 1) of the `values` MUST be in the matched Edge's corresponding property". 
   * `DENY` means "ALL of the `values` MUST NOT be in the matched Edge's corresponding property". 
* `agent_type`: see above (KL)
   * FYI: if a specified value has descendants (ex: `automated_agent`), the tool MUST treat those descendants (ex: `text_mining_agent`, etc.) as if they were included in the `values` array (aka "hierarchy expansion").
* `sources`: this constrains the Edge `sources`. It has the same keys as KL/AT (`behavior`, `values`) plus the optional `primary_only` (if true, the constraint ONLY applies to the `primary_knowledge_source`). 
* `attributes`: minItems 1, otherwise the same as previous `attribute_constraints`
* `qualifiers`: simplified format to an array of objects but preserved previous behavior. Each object represents a qualifier-set, and multiple objects/sets have an `OR` relationship. Within an object, the keys are the "qualifier-type-ids" and their values are the "qualifier values". Multiple key/value pairs in one object/set have an `AND` relationship. 

<details><summary>The same QEdge in 2.0 would look like this (click to expand)</summary>
<p>

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

</p>
</details> 

<br>

<details><summary>This example Edge (not real!) would fulfill the constraints. Its properties are put in same order as constraints for easy comparison (click to expand)</summary>
<p>

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

</p>
</details> 


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


### 4. KL/AT turned into top-level Edge properties, now required 

In 1.6.0-beta, `knowledge_level` and `agent_type` are stored in `Edge.attributes`, which is not a required property. However, for several years the Translator Consortium has actually required KL/AT on Edges. 

In 2.0, they are now top-level properties that are required on an `Edge`. The way to constrain them in queries has also changed (own keys under `QEdge.constraints`) - see #1 for details.

Example snippet of an `Edge` in 2.0, showing the top-level KL/AT:

```json
{
    "subject": "NCBIGene:1234",
    "object": "MONDO:1234",
    "predicate": "biolink:associated_with",
    "agent_type": "data_analysis_pipeline",    // top-level properties!
    "knowledge_level": "statistical_association",
    "sources": [...],
}
```


### 5. Add `COLLATE` option to `QNode.set_interpretation`

In 2.0, `COLLATE` is an option that is only allowed on QNodes with no `ids` set and indicates that multiple matching nodes MUST be collated into a single Result, rather than put into separate Results. This restores some of the `QNode.is_set` behavior that was removed in 1.5.0 (don't confuse with **Node**.is_set!). 

When `COLLATE` is set, `QNode.member_ids` must not be used.

Example scenario:

For the query `Drug -interacts_with-> Gene -causes-> Diabetes`, if `Drug A` has matching paths to `Diabetes` through Genes A, B, and C, 3 results could be generated:
* `Drug A -interacts_with-> Gene A -causes-> Diabetes`
* `Drug A -interacts_with-> Gene B -causes-> Diabetes`
* `Drug A -interacts_with-> Gene C -causes-> Diabetes`

But if COLLATE was set on the Gene QNode as `Drug -interacts_with-> Gene (set_interpretation: COLLATE) -causes-> Diabetes`, in that scenario only 1 result should be generated:
* `Drug A -interacts_with-> Gene [A, B, C] -causes-> Diabetes`

The `node_bindings.[Gene QNode].ids` would include Genes A, B, and C. The edge_bindings would be collated accordingly. 


## Other Changes

1. `null` is no longer a valid value in queries and responses. To convey "no data", omit the field or use an empty array/object if the schema allows (doesn't set `minProperties`/`minItems`). However, unless the field's description explicitly states that the empty array/object should be used, we strongly encourage omitting fields instead to reduce needless bloat. Examples:
   * `Message.knowledge_graph` should omitted, not be set to `null`, when there is no data (ex: a query, or a response with no data found).
   * `Message.results` should not be set to `null` when there is no data. Its description states when it should be omitted (when not expected, like a query) VS an empty array (when it is expected and there's no data, like a response).
2. For many optional array and object properties, `minItems`/`minProperties` was set to 1. This was to reduce bloat (only include the field if there's data). See the Changelog for the list of changed properties.
3. `AuxiliaryGraph.attributes` was removed. It was previously required, but never used and its empty arrays bloated responses.
4. These properties were changed to not required:
   * `Nodes.attributes`
   * `QueryGraph` `edges` and `paths`: to accommodate queries with only nodes
   * `KnowledgeGraph.edges`: same reason as above
   * `Result.analyses`: same reason as above
5. Analysis allows edge_bindings and path_bindings to be present together (for experimental use only, small change introduced when simplifying schema classes)


## Full Example: 1.6.0-beta Response

```json
// TODO: full-size 1.6.0-beta response example
```

## Full Example: 2.0 Response

```json
// TODO: full-size 2.0 response example
```
