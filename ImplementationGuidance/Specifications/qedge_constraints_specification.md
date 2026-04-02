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
* If a specified value has descendants (ex: `activity_or_abundance`), the tool MUST treat those descendants (ex: `abundance`, `expression`, etc.) as if they were included using an `OR` relationship (i.e. "hierarchy expansion"). Links: [hierarchy for aspect-qualifier values](https://biolink.github.io/biolink-model/aspects.html), [enums](https://biolink.github.io/biolink-model/#enumerations) for qualifier values

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
  * Note that KnowledgeGraph Edges have only 1 value each in their `knowledge_level`/`agent_type` fields.
* The `values` MUST be valid, from the corresponding biolink enum for the property ([knowledge_level](https://biolink.github.io/biolink-model/KnowledgeLevelEnum/), [agent_type](https://biolink.github.io/biolink-model/AgentTypeEnum/))
* If a specified value has descendants (ex: `automated_agent`), the tool MUST treat those descendants (ex: `text_mining_agent`, etc.) as if they were included in the `values` array (i.e. "hierarchy expansion"). 

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

Attribute constraints are presented as a list of attribute constraint objects. Each attribute constraint object constrains a specific attribute type. Multiple attribute constraints together represent an AND relationship, such that all attribute constraints must be met.

Every attribute constraint must supply a `name`, `id`, `value`, and `operator`:

- `name`: For human use, this just specifies the intent of the constraint.
- `id`: This targets the constraint to attributes with a specific `attribute_type_id`.
- `value`: Provides a value with which the targeted attribute must agree.
- `operator`: Provides the relationship to the `value` that targeted attributes must fulfill.

Additionally, `not` allows the operator relationship to be inverted.

### `===` "Strict equality"

In the most simple case, the operator `===` requires that edges must have an attribute exactly matching the given value:

```json
{
    "name": "Must have the exact given publication list",
    "id": "biolink:publications",
    "operator": "===",
    "value": ["PMID:1234", "PMID:4567"]
}
```

would only allow edges that have the `attribute_type_id` 'biolink:publications', where the attribute value is exactly `["PMID:1234", "PMID:4567"]`.

`"not": true` would make this operator mean 'not exactly equal to'.

Other operators exist which provide specific expressions, detailed below:

### `==` "Equals"

The operator `==` means 'is equal to'. `not` would make this operator mean 'not equal to, in any comparison.'

### `>` "Greater than"

The operator `>` means "greater than". `not` makes this operator mean `<=` 'less than or equal to' for all comparisons.

### `<` "Less than"

The operator `<` means "less than". `not` makes this operator mean `>=` 'greater than or equal to' for all comparisons.

### `matches` "Matches by regular expression"

The operator `matches` invokes a regular expression for the comparison, using python-like regex syntax. `not` means that no regex match is found for all comparisons.

### List-wise comparison

When either the constraint value, or the value of the targeted attribute, is a list, comparisons are made against each item of the list. The operators `==`, `>`, `<`, and `matches` all are compared list-wise. Using `==` as an example, where constraint value == attribute value:

In the most basic case, simple equality satisfies the operator:

- `1 == 1` constraint met!
- `1 == 2` constraint failed.

However, if the constraint value is a list, each item in the list is compared against the attribute value. Any successful comparison means the constraint is met:

- `[1, 2, 3] == 1` constraint met! (1 == 1)
- `[1, 2, 3] == 2` constraint met! (2 == 2)
- `[1, 2, 3] == 3` constraint met! (3 == 3)
- `[1, 2, 3] == 4` constraint failed.

Similarly, if the attribute value is a list, each item is compared against the constraint. Any successful comparison means the constraint is met:

- `1 == [1, 2, 3]` constraint met! (1 == 1)
- `2 == [1, 2, 3]` constraint met! (2 == 2)
- `3 == [1, 2, 3]` constraint met! (3 == 3)
- `4 == [1, 2, 3]` constraint failed.

Finally, both may be lists, in which case every pair must be compared. Any pair that meets the constraint means the constraint is satisfied:

- `[1, 2, 3] == [3, 4, 5]` constraint met! (3 == 3)
- `[1, 2, 3] == [4, 6, 6]` constraint failed.

The only operator for which this behavior is not held is `===` (strict equality), it exists to allow exact list comparison.


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
