# QEdge Constraints Specification

The `QEdge` property `constraints` holds query-constraints on other Edge fields besides the main triple (`subject`, `predicate`, `object`). It and its keys should only be present when there's a constraint (`minProperties`/`minItems`: 1).

 There are 5 keys/Edge fields currently specified:
* `qualifiers`
* `knowledge_level`
* `agent_type`
* `sources`
* `attributes`

The keys have an `AND` relationship (all must be met by a matched Edge). 


## Qualifiers

* Each object represents a qualifier-set, and multiple objects/sets have an `OR` relationship.
* Within an object, the keys are the "qualifier-type-ids" and their values are the "qualifier values". Multiple key/value pairs in one object/set have an `AND` relationship. 
* If a specified value has descendants (ex: `activity_or_abundance`), the tool MUST treat those descendants (ex: `abundance`, `expression`, etc.) as if they were included using an `OR` relationship (aka "hierarchy expansion"). 

Example: the matched Edge's qualifier set should include either:
* `causes` + `decreased` (or its child `downregulated`) + `activity_or_abundance` (or 1 of its descendants)
* `vaccine_antigen` (current modeling doesn't include other qualifiers)

```json
"qualifiers": [  // each object is a qualifier-set, OR behavior between them
      {  // AND behavior for elements within an object
        "biolink:qualified_predicate": "causes",
        "biolink:object_direction_qualifier": "decreased",
        "biolink:object_aspect_qualifier": "activity_or_abundance"
      },
      {
        "biolink:causal_mechanism_qualifier": "vaccine_antigen",
      }
   ]
```


## Knowledge Level / Agent Type (KL/AT)

* two required keys: `behavior` (`ALLOW` or `DENY`) and `values` (an array of strings)
* `ALLOW` means "ANY (at least 1) of the `values` MUST be in the matched Edge's corresponding property". `DENY` means "ALL of the `values` MUST NOT be in the matched Edge's corresponding property".
  * Note that KnowledgeGraph Edges have only 1 value each in their `knowledge_graph`/`agent_type` fields.
* The `values` MUST be valid, from the corresponding biolink enum for the property.
* If a specified value has descendants (ex: `automated_agent`), the tool MUST treat those descendants (ex: `text_mining_agent`, etc.) as if they were included in the `values` array (aka "hierarchy expansion"). 

```json
"<knowledge_level/agent_type>": {
    "behavior": "<ALLOW/DENY>",
    "values": ["xxxx", "yyyy"]
}
```

### Examples:

The matched Edge's `knowledge_level` should be either `text_co_occurrence` or `not_provided` (currently used for text-mined edges). 

```json
"knowledge_level": {
    "behavior": "ALLOW",
    "values": ["text_co_occurrence", "not_provided"]
}
```

The matched Edge's `agent_type` should NOT be `not_provided` or `automated_agent` or any of `automated_agent`'s descendants.

```json
"agent_type": {
    "behavior": "DENY",
    "values": ["not_provided", "automated_agent"]
}
```


## Sources

This constrains the infores CURIEs in the matched Edge's `sources` (`RetrievalSource.resource_id`). It has the same format as KL/AT plus the optional field `primary_only`:

* if set to `true`: the constraint only applies to the `primary_knowledge_source` (there's only 1 `RetrievalSource` with this `resource_role` per Edge)
* if set to `false` or not present (default): the constraint applies to the entire set of RetrievalSources in `sources`

Notes:
* should do only on a resource level, not a tool/Translator database level (ex: shouldn't use the infores for Tiers, Retriever, or an ARA)
* Note on value descendants doesn't apply (no hierarchy for infores) 

### Examples:

The matched Edge's `sources` should include a RetrievalSource with the resource_id `infores:chembl` or `infores:dgidb`. The resource_role of the matching RetrievalSource doesn't matter. 

```json
"sources": {
    "behavior": "ALLOW",
    "values": ["infores:chembl", "infores:dgidb"]
}
```

The matched Edge's `primary_knowledge_source` should NOT be `infores:semmeddb` or `infores:text-mining-provider-targeted`. 

```json
"sources": {
    "behavior": "DENY",
    "values": ["infores:semmeddb", "infores:text-mining-provider-targeted"],
    "primary_only": true
}
```


## Attributes

Format didn't change in TRAPI 2.0, see docs for details. 


## Full Examples

<details><summary>QEdge with 4/5 constraint types, no KL (click to expand)</summary>
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

<details><summary>This example Edge (not real!) would fulfill those constraints. Its properties are put in same order as constraints for easy comparison (click to expand)</summary>
<p>

```json
{
    "subject": "NCBIGene:1234",
    "object": "MONDO:1234",
    "predicate": "biolink:associated_with",
    "agent_type": "data_analysis_pipeline",    // matches AT constraint: this is a child of automated_agent
    "knowledge_level": "text_co_occurrence",
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

<br>

[Response with all 5 kinds of constraints on QEdges](../DataExamples/2-0_example_response.json)
