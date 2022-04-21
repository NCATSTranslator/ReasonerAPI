# QueryGraph Implementation Rules:

The following rules MUST be applied by implementers of TRAPI endpoints.
The rules are organized by class and property.

The terms MUST, SHOULD, MAY are used as defined in RFC 2119  https://tools.ietf.org/html/rfc2119 

## /asyncquery
- Knowledge Providers (KPs) MAY implement /asyncquery
- Autonomous Reasoning Agents (ARAs) SHOULD implement /asyncquery
- The /asyncquery endpoint SHOULD be left in an OpenAPI definition for a TRAPI endpoint even if
  if it is not implemented, since it is part of the TRAPI core schema
- Each TRAPI server MUST indicate with true or false if the /asyncquery endpoint is implemented
  by the server via the x-trapi asyncquery property as found in the TRAPI core schema template.

## QNode.ids
- MAY be null, or MAY be missing. The meaning is the same.
- MUST NOT be an empty array (#199)
- If more than one element is present, the elements MUST be treated in the sense of an "or" list.
  This effectively creates a simple batch query mechanism.
- The list SHOULD NOT be used by the client to provide equivalent CURIEs to the server
- If the server considers a subset of items in the list as equivalent CURIEs,
  the server SHOULD merge the subset into a single KnowledgeGraph Node

## QNode.categories
- MAY be null, or MAY be missing. The meaning is the same: matching Nodes may be any category
- If QNode.categories is [ 'biolink:NamedThing' ], it means matching Nodes may be any category
  (any descendent biolink category NamedThing)
- MUST NOT be an empty array (#199)
- If more than one element is present, the elements MUST be treated in the sense of an "or" list.
  Matching Nodes may be any of the listed QNode.categories
- Biolink category descendents do not need to be specified separately. Queries MUST automatically
  match descendents. (e.g. QNode.categories is [ 'biolink:BiologicalEntity' ], then the KP MUST return
  Nodes with category biolink:Protein and biolink:Disease if present)
- IF a QNode has non-null QNode.ids (CURIEs), the client SHOULD NOT provide QNode.categories, and
  the server SHOULD NOT require that categories are provided to function, and the server MAY provide
  different answers for different provided categories.

## QEdge.predicates
- MAY be null, or MAY be missing. The meaning is the same.
- MUST NOT be an empty array (#199)
- If more than one element is present, the elements MUST be treated in the sense of an "or" list.
  Matching Edges may be any of the listed QEdge.predicates. 
  This effectively creates a simple batch query mechanism where the response may contain multiple
  edges, where each one matches at least one of the specified QEdge.predicates.
- Biolink predicate descendents do not need to be specified separately. Queries MUST automatically
  match descendents. (e.g. QEdge.predicates is [ 'biolink:regulates' ], then the KP MUST return
  Edges with biolink:positively_regulates and biolink:negatively_regulates if present)

## QNode.xxxxx
- Server SHOULD generate a warning and MAY continue

## QEdge.xxxxx
- Server SHOULD generate a warning and MAY continue

## QNode.constraints
- If a KP server receives any QNode.constraints, if it does not support all of them,
  it MUST immediately respond with an error Code "UnsupportedConstraint" and list all constraint
  names that it does not support.
- If an ARA server receives any QNode.constraints, it MUST perform one of the following:
  - Relay all constraints to its KP(s) to satisfy
  - Withhold one or more constraints from its KP queries and satisfy those constraints itself
- An ARA server MUST ensure that all constraints are satisifed by either trusting its KPs to satisfy them
  or by performing the constraints itself. If the ARA cannot ensure this,
  it MUST immediately respond with an error Code "UnsupportedConstraint" and list all constraint
  names that it does not support.

## info.x-trapi.batch_size_limit
- This batch size limit refers to the maximum length of any single QNode.ids list. The limit
  applies to the length of the list as supplied by the client, with the understanding that the server
  may further expand the list via descendant inference. If the descendant expansion becomes too
  large (e.g., if the client specified `MONDO:0000001: disease or disorder`), the server SHOULD
  return a runtime error gracefully.

## Specifying permitted and excluded KPs to an ARA
- The proper syntax for specifying or excluding specific KPs to consult to an ARA MUST be done
  via a `constraint` on a QEdge. The following is a complete Query example that disallows the
  use of SemMedDB:

```
{
  "message": {
    "query_graph": {
      "edges": {
        "e01": {
          "object": "n0",
          "subject": "n1",
          "predicates": [
            "biolink:entity_negatively_regulates_entity"
          ],
          "constraints": [
            {
              "id": "biolink:knowledge_source",
              "name": "knowledge source",
              "value": "infores:semmeddb",
              "not": true,
              "operator": "=="
            }
          ]
        }
      },
      "nodes": {
        "n0": {
          "ids": [
            "NCBIGene:23221"
          ],
          "categories": [
            "biolink:Gene"
          ]
        },
        "n1": {
          "categories": [
            "biolink:Gene"
          ]
        }
      }
    }
  }
}
```

A general "allowlist" SHOULD look like this:
```
      "constraints": [
        {
          "id": "biolink:knowledge_source",
          "name": "knowledge source",
          "value": [
            "infores:rtx-kg2",
            "infores:biothings-explorer",
          ],
          "operator": "=="
        }
      ],
```

(when the value is a list, the "==" operator works like a SQL "IN" clause, as clearly documented in the TRAPI yaml)

Here is what a general "denylist" should look like:
```
      "constraints": [
        {
          "id": "biolink:knowledge_source",
          "name": "knowledge source",
          "value": [
            "infores:rtx-kg2",
            "infores:biothings-explorer",
          ],
          "not": true,
          "operator": "=="
        }
      ],
```

(when the value is a list, the "==" operator combined with ' "not": true ' works like a SQL "NOT IN" clause, as clearly documented in the TRAPI yaml)

