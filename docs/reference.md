# Translator Reasoner API

## Components

#### Query [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L211:L250)

The Query class is used to package a user request for information. A Query object consists of a required Message object with optional additional properties. Additional properties are intended to convey implementation-specific or query-independent parameters. For example, an additional property specifying a log level could allow a user to override the default log level in order to receive more fine-grained log information when debugging an issue.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
message | [Message](#message-) | **REQUIRED**. The query Message is a serialization of the user request. Content of the Message object depends on the intended TRAPI operation. For example, the fill operation requires a non-empty query_graph field as part of the Message, whereas other operations, e.g. overlay, require non-empty results and knowledge_graph fields.
log_level | any | The least critical level of logs to return
workflow | any | List of workflow steps to be executed.
submitter | `string` | Any string for self-identifying the submitter of a query. The purpose of this optional field is to aid in the tracking of the source of queries for development and issue resolution.

#### AsyncQuery [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L251:L299)

The AsyncQuery class is effectively the same as the Query class but it requires a callback property.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
callback | `string` | **REQUIRED**. Upon completion, this server will send a POST request to the callback URL with `Content-Type: application/json` header and request body containing a JSON-encoded `Response` object. The server MAY POST `Response` objects before work is fully complete to provide interim results with a Response.status value of 'Running'. If a POST operation to the callback URL does not succeed, the server SHOULD retry the POST at least once.
message | [Message](#message-) | **REQUIRED**. The query Message is a serialization of the user request. Content of the Message object depends on the intended TRAPI operation. For example, the fill operation requires a non-empty query_graph field as part of the Message, whereas other operations, e.g. overlay, require non-empty results and knowledge_graph fields.
log_level | any | The least critical level of logs to return
workflow | any | List of workflow steps to be executed.
submitter | `string` | Any string for self-identifying the submitter of a query. The purpose of this optional field is to aid in the tracking of the source of queries for development and issue resolution.

#### Response [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L300:L341)

The Response object contains the main payload when a TRAPI query endpoint interprets and responds to the submitted query successfully (i.e., HTTP Status Code 200). The message property contains the knowledge of the response (query graph, knowledge graph, and results). The status, description, and logs properties provide additional details about the response.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
message | [Message](#message-) | **REQUIRED**. Contains the knowledge of the response (query graph, knowledge graph, and results).
status | `string` | One of a standardized set of short codes, e.g. Success, QueryNotTraversable, KPsNotAvailable
description | `string` | A brief human-readable description of the outcome
logs | [[LogEntry](#logentry-)] | Log entries containing errors, warnings, debugging information, etc
workflow | any | List of workflow steps that were executed.

#### Message [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L342:L377)

The message object holds the main content of a Query or a Response in three properties: query_graph, results, and knowledge_graph. The query_graph property contains the query configuration, the results property contains any answers that are returned by the service, and knowledge_graph property contains lists of edges and nodes in the thought graph corresponding to this message. The content of these properties is context-dependent to the encompassing object and the TRAPI operation requested.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
results | [[Result](#result-)] | List of all returned Result objects for the query posed. The list SHOULD NOT be assumed to be ordered. The 'score' property,
 if present, MAY be used to infer result rankings.
query_graph | any | QueryGraph object that contains a serialization of a query in the form of a graph
knowledge_graph | any | KnowledgeGraph object that contains lists of nodes and edges in the thought graph corresponding to the message

#### LogEntry [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L378:L411)

The LogEntry object contains information useful for tracing and debugging across Translator components.  Although an individual component (for example, an ARA or KP) may have its own logging and debugging infrastructure, this internal information is not, in general, available to other components. In addition to a timestamp and logging level, LogEntry includes a string intended to be read by a human, along with one of a standardized set of codes describing the condition of the component sending the message.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
timestamp | `string` | Timestamp in ISO 8601 format
level | any | 
code | `string` | One of a standardized set of short codes e.g. QueryNotTraversable, KPNotAvailable, KPResponseMalformed
message | `string` | A human-readable log message

#### LogLevel [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L412:L419)

Logging level

`string`

one of:
* ERROR
* WARNING
* INFO
* DEBUG

#### Result [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L420:L467)

A Result object specifies the nodes and edges in the knowledge graph that satisfy the structure or conditions of a user-submitted query graph. It must contain a NodeBindings object (list of query graph node to knowledge graph node mappings) and an EdgeBindings object (list of query graph edge to knowledge graph edge mappings).

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
node_bindings | Map[`string`, [[NodeBinding](#nodebinding-)]] | **REQUIRED**. The dictionary of Input Query Graph to Result Knowledge Graph node bindings where the dictionary keys are the key identifiers of the Query Graph nodes and the associated values of those keys are instances of NodeBinding schema type (see below). This value is an array of NodeBindings since a given query node may have multiple knowledge graph Node bindings in the result.
edge_bindings | Map[`string`, [[EdgeBinding](#edgebinding-)]] | **REQUIRED**. The dictionary of Input Query Graph to Result Knowledge Graph edge bindings where the dictionary keys are the key identifiers of the Query Graph edges and the associated values of those keys are instances of EdgeBinding schema type (see below). This value is an array of EdgeBindings since a given query edge may resolve to multiple knowledge graph edges in the result.
score | `number` | A numerical score associated with this result indicating the relevance or confidence of this result relative to others in the returned set. Higher MUST be better.

#### NodeBinding [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L468:L505)

An instance of NodeBinding is a single KnowledgeGraph Node mapping, identified by the corresponding 'id' object key identifier of the Node within the Knowledge Graph. Instances of NodeBinding may include extra annotation in the form of additional properties. (such annotation is not yet fully standardized).

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
id | [CURIE](#curie-) | **REQUIRED**. The CURIE of a Node within the Knowledge Graph.
query_id | [CURIE](#curie-) | An optional property to provide the CURIE in the QueryGraph to which this binding applies. If the bound QNode does not have an an 'id' property or if it is empty, then this query_id MUST be null or absent. If the bound QNode has one or more CURIEs as an 'id' and this NodeBinding's 'id' refers to a QNode 'id' in a manner where the CURIEs are different (typically due to the NodeBinding.id being a descendant of a QNode.id), then this query_id MUST be provided. In other cases, there is no ambiguity, and this query_id SHOULD NOT be provided.
attributes | [[Attribute](#attribute-)] | A list of attributes providing further information about the node binding. This is not intended for capturing node attributes and should only be used for properties that vary from result to result.

#### EdgeBinding [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L506:L529)

A instance of EdgeBinding is a single KnowledgeGraph Edge mapping, identified by the corresponding 'id' object key identifier of the Edge within the Knowledge Graph. Instances of EdgeBinding may include extra annotation (such annotation is not yet fully standardized).

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
id | `string` | **REQUIRED**. The key identifier of a specific KnowledgeGraph Edge.
attributes | [[Attribute](#attribute-)] | A list of attributes providing further information about the edge binding. This is not intended for capturing edge attributes and should only be used for properties that vary from result to result.

#### KnowledgeGraph [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L530:L557)

The knowledge graph associated with a set of results. The instances of Node and Edge defining this graph represent instances of biolink:NamedThing (concept nodes) and biolink:Association (relationship edges) representing (Attribute) annotated knowledge returned from the knowledge sources and inference agents wrapped by the given TRAPI implementation.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
nodes | Map[`string`, [Node](#node-)] | **REQUIRED**. Dictionary of Node instances used in the KnowledgeGraph, referenced elsewhere in the TRAPI output by the dictionary key.
edges | Map[`string`, [Edge](#edge-)] | **REQUIRED**. Dictionary of Edge instances used in the KnowledgeGraph, referenced elsewhere in the TRAPI output by the dictionary key.

#### QueryGraph [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L558:L585)

A graph representing a biomedical question. It serves as a template for each result (answer), where each bound knowledge graph node/edge is expected to obey the constraints of the associated query graph element.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
nodes | Map[`string`, [QNode](#qnode-)] | **REQUIRED**. The node specifications. The keys of this map are unique node identifiers and the corresponding values include the constraints on bound nodes.
edges | Map[`string`, [QEdge](#qedge-)] | **REQUIRED**. The edge specifications. The keys of this map are unique edge identifiers and the corresponding values include the constraints on bound edges, in addition to specifying the subject and object QNodes.

#### QNode [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L586:L629)

A node in the QueryGraph used to represent an entity in a query. If a CURIE is not specified, any nodes matching the category of the QNode will be returned in the Results.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
ids | [[CURIE](#curie-)] | CURIE identifier for this node
categories | [[BiolinkEntity](#biolinkentity-)] | **QNode** categories should be Biolink Model categories and are allowed to be of type `abstract` or `mixin` (only in QGraphs). Use of `deprecated` categories should be avoided.
is_set | `boolean` | Boolean that if set to true, indicates that this QNode MAY have multiple KnowledgeGraph Nodes bound to it within each Result. The nodes in a set should be considered as a set of independent nodes, rather than a set of dependent nodes, i.e., the answer would still be valid if the nodes in the set were instead returned individually. Multiple QNodes may have is_set=True. If a QNode (n1) with is_set=True is connected to a QNode (n2) with is_set=False, each n1 must be connected to n2. If a QNode (n1) with is_set=True is connected to a QNode (n2) with is_set=True, each n1 must be connected to at least one n2.
constraints | [[AttributeConstraint](#attributeconstraint-)] | A list of contraints applied to a query node. If there are multiple items, they must all be true (equivalent to AND)

#### QEdge [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L630:L700)

An edge in the QueryGraph used as a filter pattern specification in a query. If the optional predicate property is not specified, it is assumed to be a wildcard match to the target knowledge space. If specified, the ontological inheritance hierarchy associated with the term provided is assumed, such that edge bindings returned may be an exact match to the given QEdge predicate term, or to a term that is a descendant of the QEdge predicate term.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
knowledge_type | `string` | Indicates the type of knowledge that the client wants from the server between the subject and object. If the value is 'lookup', then the client wants direct lookup information from knowledge sources. If the value is 'inferred', then the client wants the server to get creative and connect the subject and object in more speculative and non-direct-lookup ways. If this property is absent or null, it MUST be assumed to mean 'lookup'. This feature is currently experimental and may be further extended in the future.
predicates | [[BiolinkPredicate](#biolinkpredicate-)] | This should be a Biolink Model predicate and is allowed to be of type `abstract` or `mixin` (only in QGraphs). Use of `deprecated` predicates should be avoided.
subject | `string` | **REQUIRED**. Corresponds to the map key identifier of the subject concept node anchoring the query filter pattern for the query relationship edge.
object | `string` | **REQUIRED**. Corresponds to the map key identifier of the object concept node anchoring the query filter pattern for the query relationship edge.
attribute_constraints | [[AttributeConstraint](#attributeconstraint-)] | A list of attribute contraints applied to a query edge. If there are multiple items, they must all be true (equivalent to AND)
qualifier_constraints | [[QualifierConstraint](#qualifierconstraint-)] | A list of QualifierConstraints that provide nuance to the QEdge. If multiple QualifierConstraints are provided, there is an OR relationship between them. If the QEdge has multiple predicates or if the QNodes that correspond to the subject or object of this QEdge have multiple categories or multiple curies, then qualifier_constraints MUST NOT be specified because these complex use cases are not supported at this time.

#### Node [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L701:L724)

A node in the KnowledgeGraph which represents some biomedical concept. Nodes are identified by the keys in the KnowledgeGraph Node mapping.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
name | `string` | Formal name of the entity
categories | [[BiolinkEntity](#biolinkentity-)] | These should be Biolink Model categories and are **_NOT_** allowed to be of type `abstract` or `mixin`. Returning `deprecated` categories should also be avoided.
attributes | [[Attribute](#attribute-)] | A list of attributes describing the node

#### Attribute [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L725:L810)

Generic attribute for a node or an edge that expands the key-value pair concept by including fields for additional metadata. These fields can be used to describe the source of the statement made in a key-value pair of the attribute object, or describe the attribute's value itself including its semantic type, or a url providing additional information about it. An attribute may be further qualified with sub-attributes (for example to provide confidence intervals on a value).

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
attribute_type_id | [CURIE](#curie-) | **REQUIRED**. The 'key' of the attribute object, holding a CURIE of an ontology property defining the attribute (preferably the CURIE of a Biolink association slot). This property captures the relationship asserted to hold between the value of the attribute, and the node or edge from  which it hangs. For example, that a value of '0.000153' represents a p-value supporting an edge, or that a value of 'ChEMBL' represents the original source of the knowledge expressed in the edge.
original_attribute_name | `string` | The term used by the original source of an attribute to describe the meaning or significance of the value it captures. This may be a column name in a source tsv file, or a key in a source json document for the field in the data that held the attribute's value. Capturing this information  where possible lets us preserve what the original source said. Note that the data type is string' but the contents of the field could also be a CURIE of a third party ontology term.
value | any | **REQUIRED**. Value of the attribute. May be any data type, including a list.
value_type_id | any | CURIE describing the semantic type of an  attribute's value. Use a Biolink class if possible, otherwise a term from an external ontology. If a suitable CURIE/identifier does not exist, enter a descriptive phrase here and submit the new type for consideration by the appropriate authority.
attribute_source | `string` | The source of the core assertion made by the key-value pair of an attribute object. Use a CURIE or namespace designator for this resource where possible.
value_url | `string` | Human-consumable URL linking to a web document that provides additional information about an  attribute's value (not the node or the edge fom which it hangs).
description | `string` | Human-readable description for the attribute and its value.
attributes | [[Attribute](#attribute-)] | A list of attributes providing further information about the parent attribute (for example to provide provenance information about the parent attribute).

#### Edge [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L811:L851)

A specification of the semantic relationship linking two concepts that are expressed as nodes in the knowledge "thought" graph resulting from a query upon the underlying knowledge source.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
predicate | any | These should be Biolink Model predicate terms and are **_NOT_** allowed to be of type `abstract` or `mixin`. Returning `deprecated` predicate terms should also be avoided.
subject | [CURIE](#curie-) | **REQUIRED**. Corresponds to the map key CURIE of the subject concept node of this relationship edge.
object | [CURIE](#curie-) | **REQUIRED**. Corresponds to the map key CURIE of the object concept node of this relationship edge.
attributes | [[Attribute](#attribute-)] | A list of additional attributes for this edge
qualifiers | [[Qualifier](#qualifier-)] | A set of Qualifiers that act together to add nuance or detail to the statement expressed in an Edge.

#### Qualifier [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L852:L877)

An additional nuance attached to an assertion

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
qualifier_type_id | `string` | **REQUIRED**. The category of the qualifier, drawn from a hierarchy of qualifier slots in the Biolink model (e.g. subject_aspect, subject_direction, object_aspect, object_direction, etc).
qualifier_value | `string` | **REQUIRED**. The value associated with the type of the qualifier, drawn from a set of controlled values by the type as specified in the Biolink model (e.g. 'expression' or 'abundance' for the qualifier type 'subject_aspect', etc).

#### QualifierConstraint [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L878:L900)

Defines a query constraint based on the qualifier_types and qualifier_values of a set of Qualifiers attached to an edge. For example, it can constrain a "ChemicalX - affects - ?Gene" query to return only edges where ChemicalX specifically affects the 'expression' of the Gene, by constraining on the qualifier_type "object_aspect" with a qualifier_value of "expression".

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
qualifier_set | [[Qualifier](#qualifier-)] | **REQUIRED**. A set of Qualifiers that serves to add nuance to a query, by constraining allowed values held by Qualifiers on queried Edges.

#### BiolinkEntity [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L901:L911)

Compact URI (CURIE) for a Biolink class, biolink:NamedThing or a child thereof. The CURIE must use the prefix 'biolink:' followed by the PascalCase class name.

`string` (pattern: `^biolink:[A-Z][a-zA-Z]*$`)

##### Example

```json
"biolink:PhenotypicFeature"
```

#### BiolinkPredicate [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L912:L923)

CURIE for a Biolink 'predicate' slot, taken from the Biolink slot ('is_a') hierarchy rooted in biolink:related_to (snake_case). This predicate defines the Biolink relationship between the subject and object nodes of a biolink:Association defining a knowledge graph edge.

`string` (pattern: `^biolink:[a-z][a-z_]*$`)

##### Example

```json
"biolink:interacts_with"
```

#### CURIE [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L924:L933)

A Compact URI, consisting of a prefix and a reference separated by a colon, such as UniProtKB:P00738. Via an external context definition, the CURIE prefix and colon may be replaced by a URI prefix, such as http://identifiers.org/uniprot/, to form a full URI.

`string`
#### MetaKnowledgeGraph [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L934:L960)

Knowledge-map representation of this TRAPI web service. The meta knowledge graph is composed of the union of most specific categories and predicates for each node and edge.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
nodes | Map[`string`, [MetaNode](#metanode-)] | **REQUIRED**. Collection of the most specific node categories provided by this TRAPI web service, indexed by Biolink class CURIEs. A node category is only exposed here if there is node for which that is the most specific category available.
edges | [[MetaEdge](#metaedge-)] | **REQUIRED**. List of the most specific edges/predicates provided by this TRAPI web service. A predicate is only exposed here if there is an edge for which the predicate is the most specific available.

#### MetaNode [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L961:L984)

Description of a node category provided by this TRAPI web service.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
id_prefixes | [`string`] | **REQUIRED**. List of CURIE prefixes for the node category that this TRAPI web service understands and accepts on the input.
attributes | [[MetaAttribute](#metaattribute-)] | Node attributes provided by this TRAPI web service.

#### MetaEdge [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L985:L1027)

Edge in a meta knowledge map describing relationship between a subject Biolink class and an object Biolink class.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
subject | [BiolinkEntity](#biolinkentity-) | **REQUIRED**. Subject node category of this relationship edge.
predicate | [BiolinkPredicate](#biolinkpredicate-) | **REQUIRED**. Biolink relationship between the subject and object categories.
object | [BiolinkEntity](#biolinkentity-) | **REQUIRED**. Object node category of this relationship edge.
knowledge_types | [`string`] | A list of knowledge_types that are supported by the service. If the knowledge_types is null, this means that only 'lookup' is supported. Currently allowed values are 'lookup' or 'inferred'.
attributes | [[MetaAttribute](#metaattribute-)] | Edge attributes provided by this TRAPI web service.

#### MetaAttribute [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L1028:L1065)


##### Fixed Fields

Field Name | Type | Description
---|:---:|---
attribute_type_id | [CURIE](#curie-) | **REQUIRED**. Type of an attribute provided by this TRAPI web service (preferably the CURIE of a Biolink association slot)
attribute_source | `string` | Source of an attribute provided by this TRAPI web service.
original_attribute_names | [`string`] | Names of an the attribute as provided by the source.
constraint_use | `boolean` | Indicates whether this attribute can be used as a query constraint.
constraint_name | `string` | Human-readable name or label for the constraint concept. Required whenever constraint_use is true.

#### AttributeConstraint [?](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L1066:L1157)

Generic query constraint for a query node or query edge

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
id | any | **REQUIRED**. CURIE of the concept being constrained. For properties defined by the Biolink model this SHOULD be a biolink CURIE. otherwise, if possible, from the EDAM ontology. If a suitable CURIE does not exist, enter a descriptive phrase here and submit the new type for consideration by the appropriate authority.
name | `string` | **REQUIRED**. Human-readable name or label for the constraint concept. If appropriate, it SHOULD be the term name of the CURIE used as the 'id'. This is redundant but required for human readability.
not | `boolean` | 
operator | `string` | **REQUIRED**. Relationship between the database value and the constraint value for the specified id. The operators ==, >, and < mean is equal to, is greater than, and is less than, respectively. The 'matches' operator indicates that the value is a regular expression to be evaluated. If value is a list type, then at least one evaluation must be true (equivalent to OR). This means that the == operator with a list acts like a SQL 'IN' clause. If the value of the compared attribute is a list, then comparisons are performed between each of the constraint values and each of the attribute values, and any one true evaluation counts as an overall true (e.g., [1,2,3] == [6,7,2] is true). The == operator is therefore a broad interpretation of inclusion. The '===' operator requires that the constraint value and the attribute value be the same data type, length, content, and order (e.g. only [1,2,3] === [1,2,3]). The 'not' property negates the operator such that not and == means 'not equal to' (or 'not in' for a list), and not > means <=, and not < means >=, not matches means does not match, and not === means the match between the constraint and attribute values are not exact. The '==' operator SHOULD NOT be used in a manner that describes an "is a" subclass relationship for the parent QNode.
value | any | **REQUIRED**. Value of the attribute. May be any data type, including a list. If the value is a list and there are multiple items, at least one comparison must be true (equivalent to OR) unless the '===' operator is used. If 'value' is of data type 'object', the keys of the object MAY be treated as a list. A 'list' data type paired with the '>' or '<' operators will encode extraneous comparisons, but this is permitted as it is in SQL and other languages.
unit_id | any | CURIE of the units of the value or list of values in the 'value' property. The Units of Measurement Ontology (UO) should be used if possible. The unit_id MUST be provided for (lists of) numerical values that correspond to a quantity that has units.
unit_name | any | Term name that is associated with the CURIE of the units of the value or list of values in the 'value' property. The Units of Measurement Ontology (UO) SHOULD be used if possible. This property SHOULD be provided if a unit_id is provided. This is redundant but recommended for human readability.
