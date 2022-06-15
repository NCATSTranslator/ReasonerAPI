# Change Log TRAPI 1.2 -> 1.3

https://github.com/NCATSTranslator/ReasonerAPI/compare/v1.2.0...1.3
  
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
