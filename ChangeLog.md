# Change Log TRAPI 1.3 (2022-09-01) -> 1.4-beta (2023-03-23)

https://github.com/NCATSTranslator/ReasonerAPI/compare/v1.3.0...1.4
  
- Edge.predicate switched to nullable false and made required, Edge.subject and Edge.object switched to nullable false
  https://github.com/NCATSTranslator/ReasonerAPI/pull/377/files

- External workflow schema updated from version 1.0.0 to version 1.3.2 
  https://github.com/NCATSTranslator/ReasonerAPI/pull/365/files
  
- Node.categories clarified that they SHOULD be Biolink Model categories and MUST NOT be of type 'abstract' or 'mixin'. 'deprecated' categories SHOULD also be avoided.
  https://github.com/NCATSTranslator/ReasonerAPI/pull/383/files

- In MetaKnowledgeGraph component, added MetaEdge.qualifiers as list of new MetaQualifier types
  https://github.com/NCATSTranslator/ReasonerAPI/pull/387/files
 
- Add /async_query_status/{job_id} endpoint
  https://github.com/NCATSTranslator/ReasonerAPI/pull/395/files
  
- Constrain Qualifier.qualifier_type_id to be a biolink CURIE
  https://github.com/NCATSTranslator/ReasonerAPI/pull/391/files
 
- Encoding extra supporting graph information in TRAPI
  This is a complex breaking change that moves Result.edge_bindings into Result.analyses which link to AuxiliaryGraph objects
  https://github.com/NCATSTranslator/ReasonerAPI/pull/389/files

- Enhance encoding of EPC retrieval sources by adding Edge.sources as list of RetrievalSource items (required, minItems: 1)
  https://github.com/NCATSTranslator/ReasonerAPI/pull/393/files

- Switch all cases of "allOf" to "oneOf" to be compatible with actual schema semantics and TRAPI (JSONSchema) validation
  https://github.com/NCATSTranslator/ReasonerAPI/pull/403/files

- New properties Response.schema_version and Response.biolink_version to aid in TRAPI (JSONSchema) validation
  https://github.com/NCATSTranslator/ReasonerAPI/pull/405/files

Minor updates during the beta phase:

- Everyone should be tagging at 1.4.0: https://github.com/NCATSTranslator/ReasonerAPI/pull/419/files

- Change RetrievalSource.resource and upstream_resources to RetrievalSource.resource_id and upstream_resource_ids for consistency:
  https://github.com/NCATSTranslator/ReasonerAPI/pull/418/files

- Change Analysis.reasoner_id to Analysis.resource_id


# Change Log TRAPI 1.2 -> 1.3

https://github.com/NCATSTranslator/ReasonerAPI/compare/v1.2.0...1.3
  
- Add test_data_location in x-trapi
  https://github.com/NCATSTranslator/ReasonerAPI/pull/339/files

- Add flag for knowledge_type flag for Creative Mode
  https://github.com/NCATSTranslator/ReasonerAPI/pull/331/files

- Add support for Qualifiers in KGs and queries
  https://github.com/NCATSTranslator/ReasonerAPI/pull/330/files

- Add knowledge_types support to /meta_knowledge_graph
  https://github.com/NCATSTranslator/ReasonerAPI/pull/333/files

- Add === operator to Constraint
  https://github.com/NCATSTranslator/ReasonerAPI/commit/875112b7a349c9f8e89bb5660725af5c895c9a24

- Clarified meaning of batch_size_limit
  https://github.com/NCATSTranslator/ReasonerAPI/commit/ad3c16a3ecc085cc041b0ebbeeb7f0803e054fd0

- Misc documentation fixes

- Add NodeBinding.query_id property. Optional but a substantial change to current practice
  https://github.com/NCATSTranslator/ReasonerAPI/commit/dc6e864af5e498f7e420318b16be7d4a2f9a03ef

- Clarification on expectations for /meta_knowledge_graph for KPs and ARAs
  https://github.com/NCATSTranslator/ReasonerAPI/commit/e2ed87aa4f02dac55dcbd8eac7e190b8c188fbdd

- Permit unlimited recursion of attributes
  https://github.com/NCATSTranslator/ReasonerAPI/commit/6ec8ea28f3262ac163803622017bb651a4adac33

- Added NodeBinding.Attributes

- Clarification on how to properly to specify KP "allowlist"s and "denylist"s via constraints
  https://github.com/NCATSTranslator/ReasonerAPI/commit/82218fc86be74755ec1ffa9b8679eac0075df364

- Clarification on previously-agreed handling of QNode and QEdge additional properties
  https://github.com/NCATSTranslator/ReasonerAPI/commit/85fefd44925652a5b2e9648fef1d6c70c5099ea9


# Change Log TRAPI 1.1 -> 1.2
- /predicates endpoint is REMOVED
  https://github.com/NCATSTranslator/ReasonerAPI/pull/261/files

- Removed all 'relation' properties in Edge, QEdge, MetaEdge

- /meta_knowledge_graph allows optional attributes[] property (encouraged but not required)
  https://github.com/NCATSTranslator/ReasonerAPI/pull/259/files

- Add support for workflow and operations v1.0.0 (encouraged but not yet required)
  https://github.com/NCATSTranslator/ReasonerAPI/pull/262/files

- /asyncquery endpoint added (recommended but not required)
  https://github.com/NCATSTranslator/ReasonerAPI/pull/255/files
  https://github.com/NCATSTranslator/ReasonerAPI/pull/263/files

- Add result.score (highly encouraged but not required)
  https://github.com/NCATSTranslator/ReasonerAPI/pull/247/files

- /meta_knowledge_graph should only include specific relationships, not ancestor-inferred relationships (policy clarification)

- Add one level of subattributes to Attribute
  https://github.com/NCATSTranslator/ReasonerAPI/pull/268/files

- Add attributes[] to EdgeBinding to complement Edge and Node
  https://github.com/NCATSTranslator/ReasonerAPI/pull/269/files

- QNode.constraints and QEdge.constraints no longer nullable. Now use empty list as default instead of null
  https://github.com/NCATSTranslator/ReasonerAPI/pull/286/files


# Change Log TRAPI 1.0 -> 1.1
- Many changes to "info" template at top. Please refresh to the latest template
- info.version is now your API version not TRAPI version
- x-trapi now contains the official TRAPI version
- x-translator now contains mandatory metadata
- Remove tag "reasoner". Add tag "trapi"
- /predicates endpoint is marked deprecated
- New /meta_knowledge_graph endpoint replaces /predicates endpoint. Note that counts are optional as defined in extended schema
- log_level property in Query specifies desired logging level in Response
- QNode.id pluralized to ids and changed from CURIE or array of CURIEs to just array of CURIEs with array length > 0
- QNode.category pluralized to categories and changed from BiolinkEntity or array of BiolinkEntitys to just array of BiolinkEntitys with array length > 0
- QNode.predicate pluralized to predicates and changed from BiolinkPredicate or array of BiolinkPredicates to just array of BiolinkPredicates with array length > 0
- Attribute class extended and properties renamed
- QNode.constraints and QEdge.constraints as array of Constraint added
