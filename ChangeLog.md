# Change Log  1.6.0-beta (2025-06-06) -> 2.0.0-dev (2026-03-25)

1. QEdge Constraints Refactor (see [migration guide entry](https://github.com/NCATSTranslator/ReasonerAPI/blob/2.0-migration-guide-plus/ImplementationGuidance/MigrationGuides/MigrationAndImplementationGuide2-0.md#1-qedge-constraints-refactor))
- QEdge.attribute_constraints has been removed and replaced with QEdge.constraints, which is an object that can contain constraints for knowledge_level, agent_type, sources, attributes, and qualifiers
- The new 'sources' constraint has ALLOW and DENY constructs with an optional 'primary_only' flag

2. Add Query.parameters to contain existing log_level and bypass_cache parameters and add timeout query parameter (see [migration guide entry](https://github.com/NCATSTranslator/ReasonerAPI/blob/2.0-migration-guide-plus/ImplementationGuidance/MigrationGuides/MigrationAndImplementationGuide2-0.md#2-new-queryresponse-parameters))

3. Binding Structure Changes (NodeBinding/EdgeBinding/PathBinding) (see [migration guide entry](https://github.com/NCATSTranslator/ReasonerAPI/blob/2.0-migration-guide-plus/ImplementationGuidance/MigrationGuides/MigrationAndImplementationGuide2-0.md#3-binding-structure-changes-nodeedgepath))
- <node/edge/path>_bindings are now minProperties: 1 (i.e. when these fields are present, they MUST contain data)
- `id` properties renamed to `ids` and is now a list
- `ids` arrays are minItems: 1 (this property is required)
- `attributes` property completely removed
- `query_id` was removed from NodeBinding (obsolete with the current subclassing behavior)
- Each binding is now an object containing only `ids` (which contains is a list), instead of a list of objects each with `id` and `attributes`

4. KL/AT turned into top-level Edge properties, now required (see [migration guide entry](https://github.com/NCATSTranslator/ReasonerAPI/blob/2.0-migration-guide-plus/ImplementationGuidance/MigrationGuides/MigrationAndImplementationGuide2-0.md#4-klat-turned-into-top-level-edge-properties-now-required))
- Edge.knowledge_level and Edge.agent_type are now required Edge properties instead of being located within 'attributes'

5. Add COLLATE option to QNode.set_interpretation enum (see [migration guide entry](https://github.com/NCATSTranslator/ReasonerAPI/blob/2.0-migration-guide-plus/ImplementationGuidance/MigrationGuides/MigrationAndImplementationGuide2-0.md#5-add-collate-option-to-qnodeset_interpretation))

6. null is no longer a valid value in queries and responses (see [migration guide entry](https://github.com/NCATSTranslator/ReasonerAPI/blob/2.0-migration-guide-plus/ImplementationGuidance/MigrationGuides/MigrationAndImplementationGuide2-0.md#6-null-is-no-longer-a-valid-value-in-queries-and-responses))
- Remove `nullable: true/false` designations for all properties. Properties with no data must now be *absent* from TRAPI JSON rather than allowed to be present but with a null value

7. Many optional properties set to <minItems/minProperties>: 1 
- Empty lists are no longer permitted to say "no data". "No data" is now expressed with an absent property
- ****** list them

8. Remove AuxiliaryGraph.attributes property

9. The following properties changed to not-required
- `Nodes.attributes` (to reduce bloat)
- `QueryGraph.edges` and `QueryGraph.paths` (to accommodate queries with only nodes) (e.g. "what are the attributes of CURIE:123?")
- `KnowledgeGraph.edges` (to accommodate queries with only nodes)
- `Result.analyses` (to accommodate queries with only nodes)

10. Analysis is technically allowed to have both edge and path bindings (experimental use)

11. YAML specification document5 migrated from OpenAPI 3.0.1 to OpenAPI 3.1.2
- All `example` attributes become `examples` in OpenAPI 3.1.2

12. BaseQueryGraph and BaseAnalysis base classes removed in favor of single QueryGraph and Analysis classes that support both pathfinder and regular queries





# Change Log TRAPI 1.5.0 (2024-05-26) -> 1.6.0-beta (2025-06-06)

- TBD

# Change Log TRAPI 1.4.0 (2023-06-23) -> 1.5.0 (2024-05-26)

https://github.com/NCATSTranslator/ReasonerAPI/compare/v1.4.0...1.5
  
- Add x-trapi pathfinderquery: true/false
  https://github.com/NCATSTranslator/ReasonerAPI/pull/487/files
  
- Add x-trapi multicuriequery: true/false
  https://github.com/NCATSTranslator/ReasonerAPI/pull/488/files
  
- Fix minor syntax errors
  https://github.com/NCATSTranslator/ReasonerAPI/pull/485/files
  
- Update knowledge_level_agent_type_specification.md
  https://github.com/NCATSTranslator/ReasonerAPI/pull/486/files
  
- Add QNode.member_ids
  https://github.com/NCATSTranslator/ReasonerAPI/pull/481/files
  
- Change workflow schema to https and version 1.3.5
  https://github.com/NCATSTranslator/ReasonerAPI/commit/aeddb4323ed9fd5aead5986c5e5ffbab167e6524
  https://github.com/NCATSTranslator/ReasonerAPI/commit/1fdd0351c8edfb59d8fcf52dfe387f5547f1fc27
  https://github.com/NCATSTranslator/ReasonerAPI/commit/6c4215a92a5895cdb9062124700a5c84b5e1c249
  
- Revert OneOf to additionalProperties (TRAPI 1.4.2 correction)
  https://github.com/NCATSTranslator/ReasonerAPI/commit/795b13836bde2042687cbd7927f10e6dbee923e1
  https://github.com/NCATSTranslator/ReasonerAPI/commit/98077dd71f6c582ff71ac32719c708c118132245

- Make Query.message a oneOf $ref and nullable false
  https://github.com/NCATSTranslator/ReasonerAPI/commit/1f9a9828a1dbeb146bb34de9b8bda2277895b985

- Fix ambiguiities in Response
  https://github.com/NCATSTranslator/ReasonerAPI/commit/55ccfdfa9a9988a1f271dd28708c9ade0fc347bf

- convert to oneOf with -
  https://github.com/NCATSTranslator/ReasonerAPI/commit/505ddb954310eab37d58d37be881006751dda5e2

- Fix EdgeBinding and AuxGraph
  https://github.com/NCATSTranslator/ReasonerAPI/commit/91cd63b174b81d6d7629ae478f0a8d4eb4bd60ec

- Insert missing dashes at lines 267 and 320
  https://github.com/NCATSTranslator/ReasonerAPI/commit/c17fe1be1dbc131800cfab444a7b739b8b75a3cc
  https://github.com/NCATSTranslator/ReasonerAPI/commit/ffb2fedf1a8788e75714e9f140afee936feba060

- Make attributes required with minItems 0
  https://github.com/NCATSTranslator/ReasonerAPI/commit/e5f52be4f47391e8f3496dcfc538c0764a5824b3

- Make Query.message a oneOf $ref and nullable false
  https://github.com/NCATSTranslator/ReasonerAPI/commit/cc2b67d1c5f93dd62c934080c11607a2e15c5100

- Fix EdgeBinding and AuxGraph
  https://github.com/NCATSTranslator/ReasonerAPI/commit/6d5bfdb7cff85a216df3830fce36a63db22976d3

- Set_interpretation and is_set changes
  https://github.com/NCATSTranslator/ReasonerAPI/pull/475/files

- Add bypass_cache
  https://github.com/NCATSTranslator/ReasonerAPI/pull/473/files
  Implementation note: bypass_cache MUST be passed down to downstream queries: ARS -> ARAs -> KP2 -> NodeNorm

- Clarify minItems 1 for Attributes
  https://github.com/NCATSTranslator/ReasonerAPI/pull/472/files

- Clarify NodeBinding
  https://github.com/NCATSTranslator/ReasonerAPI/pull/468/files

- Make Message.Results minItems 0
  https://github.com/NCATSTranslator/ReasonerAPI/pull/464/files

- Make logs minItems: 1
  https://github.com/NCATSTranslator/ReasonerAPI/pull/466/files

- Clarify Result
  Not yet merged. Abrar checking on a potential snag
  https://github.com/NCATSTranslator/ReasonerAPI/pull/467/files

Documentation updates:

- Update retrieval_provenance_specification
  https://github.com/NCATSTranslator/ReasonerAPI/commit/78dafcf07f33dc0511e8a18c7f801fd68226d73e
  https://github.com/NCATSTranslator/ReasonerAPI/commit/4d3e457b7e46425548cf855562127e67de2757e5

- Update supporting_publications_specification
  https://github.com/NCATSTranslator/ReasonerAPI/commit/b856d79c4df1fe2dbba937ddb339019958cb1150

Minor updates during the beta phase:

- Pending









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

- Version v1.4.0-beta2 was corrupted somehow and should not be used. It is replaced by v1.4.0-beta3


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
