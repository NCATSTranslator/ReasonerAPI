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
