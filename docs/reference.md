# Translator Reasoner API

## Components

#### Query [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L105:L127)

The Query class is used to package a user request for information. A Query object consists of a required Message object with optional additional properties. Additional properties are intended to convey implementation-specific or query-independent parameters. For example, an additional property specifying a log level could allow a user to override the default log level in order to receive more fine-grained log information when debugging an issue.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
message | [Message](#message) | **REQUIRED**. The query Message is a serialization of the user request. Content of the Message object depends on the intended TRAPI operation. For example, the fill operation requires a non-empty query_graph field as part of the Message, whereas other operations, e.g. overlay, require non-empty results and knowledge_graph fields.

#### Response [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L128:L164)

The Response object contains the main payload when a TRAPI query endpoint interprets and responds to the submitted query successfully (i.e., HTTP Status Code 200). The message property contains the knowledge of the response (query graph, knowledge graph, and results). The status, description, and logs properties provide additional details about the response.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
message | [Message](#message) | **REQUIRED**. Contains the knowledge of the response (query graph, knowledge graph, and results).
status | `string` | One of a standardized set of short codes, e.g. Success, QueryNotTraversable, KPsNotAvailable
description | `string` | A brief human-readable description of the outcome
logs | [[LogEntry](#logentry)] | Log entries containing errors, warnings, debugging information, etc

#### Message [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L165:L198)

The message object holds the main content of a Query or a Response in three properties: query_graph, results, and knowledge_graph. The query_graph property contains the query configuration, the results property contains any answers that are returned by the service, and knowledge_graph property contains lists of edges and nodes in the thought graph corresponding to this message. The content of these properties is context-dependent to the encompassing object and the TRAPI operation requested.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
results | [[Result](#result)] | List of all returned Result objects for the query posed
query_graph | [QueryGraph](#querygraph) | QueryGraph object that contains a serialization of a query in the form of a graph
knowledge_graph | [KnowledgeGraph](#knowledgegraph) | KnowledgeGraph object that contains lists of nodes and edges in the thought graph corresponding to the message

#### LogEntry [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L199:L237)

The LogEntry object contains information useful for tracing and debugging across Translator components.  Although an individual component (for example, an ARA or KP) may have its own logging and debugging infrastructure, this internal information is not, in general, available to other components. In addition to a timestamp and logging level, LogEntry includes a string intended to be read by a human, along with one of a standardized set of codes describing the condition of the component sending the message.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
timestamp | `string` | Timestamp in ISO 8601 format
level | `string` | Logging level
code | `string` | One of a standardized set of short codes e.g. QueryNotTraversable, KPNotAvailable, KPResponseMalformed
message | `string` | A human-readable log message

#### Result [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L238:L276)

A Result object specifies the nodes and edges in the knowledge graph that satisfy the structure or conditions of a user-submitted query graph. It must contain a NodeBindings object (list of query graph node to knowledge graph node mappings) and an EdgeBindings object (list of query graph edge to knowledge graph edge mappings).

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
node_bindings | Map[`string`, [[NodeBinding](#nodebinding)]] | **REQUIRED**. The dictionary of Input Query Graph to Result Knowledge Graph node bindings where the dictionary keys are the key identifiers of the Query Graph nodes and the associated values of those keys are instances of NodeBinding schema type (see below). This value is an array of NodeBindings since a given query node may have multiple knowledge graph Node bindings in the result.
edge_bindings | Map[`string`, [[EdgeBinding](#edgebinding)]] | **REQUIRED**. The dictionary of Input Query Graph to Result Knowledge Graph edge bindings where the dictionary keys are the key identifiers of the Query Graph edges and the associated values of those keys are instances of EdgeBinding schema type (see below). This value is an array of EdgeBindings since a given query edge may resolve to multiple knowledge graph edges in the result.

#### NodeBinding [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L277:L290)


##### Fixed Fields

Field Name | Type | Description
---|:---:|---
id | [CURIE](#curie) | **REQUIRED**. An instance of NodeBinding is a single KnowledgeGraph Node mapping, identified by the corresponding 'id' object key identifier of the Node within the Knowledge Graph. Instances of NodeBinding may include extra annotation (such annotation is not yet fully standardized).

#### EdgeBinding [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L291:L304)

A instance of EdgeBinding is a single KnowledgeGraph Edge mapping, identified by the corresponding 'id' object key identifier of the Edge within the Knowledge Graph. Instances of EdgeBinding may include extra annotation (such annotation is not yet fully standardized).

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
id | `string` | **REQUIRED**. The key identifier of a specific KnowledgeGraph Edge.

#### KnowledgeGraph [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L305:L332)

The knowledge graph associated with a set of results. The instances of Node and Edge defining this graph represent instances of biolink:NamedThing (concept nodes) and biolink:Association (relationship edges) representing (Attribute) annotated knowledge returned from the knowledge sources and inference agents wrapped by the given TRAPI implementation.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
nodes | Map[`string`, [Node](#node)] | **REQUIRED**. Dictionary of Node instances used in the KnowledgeGraph, referenced elsewhere in the TRAPI output by the dictionary key.
edges | Map[`string`, [Edge](#edge)] | **REQUIRED**. Dictionary of Edge instances used in the KnowledgeGraph, referenced elsewhere in the TRAPI output by the dictionary key.

#### QueryGraph [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L333:L360)

A graph representing a biomedical question. It serves as a template for each result (answer), where each bound knowledge graph node/edge is expected to obey the constraints of the associated query graph element.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
nodes | Map[`string`, [QNode](#qnode)] | **REQUIRED**. The node specifications. The keys of this map are unique node identifiers and the corresponding values include the constraints on bound nodes.
edges | Map[`string`, [QEdge](#qedge)] | **REQUIRED**. The edge specifications. The keys of this map are unique edge identifiers and the corresponding values include the constraints on bound edges, in addition to specifying the subject and object QNodes.

#### QNode [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L361:L397)

A node in the QueryGraph used to represent an entity in a query. If a CURIE is not specified, any nodes matching the category of the QNode will be returned in the Results.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
id | [CURIE](#curie) \| [[CURIE](#curie)] | CURIE identifier for this node
category | [BiolinkEntity](#biolinkentity) \| [[BiolinkEntity](#biolinkentity)] | 
is_set | `boolean` | Boolean that if set to true, indicates that this QNode MAY have multiple KnowledgeGraph Nodes bound to it within each Result. The nodes in a set should be considered as a set of independent nodes, rather than a set of dependent nodes, i.e., the answer would still be valid if the nodes in the set were instead returned individually. Multiple QNodes may have is_set=True. If a QNode (n1) with is_set=True is connected to a QNode (n2) with is_set=False, each n1 must be connected to n2. If a QNode (n1) with is_set=True is connected to a QNode (n2) with is_set=True, each n1 must be connected to at least one n2.

#### QEdge [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L398:L443)

An edge in the QueryGraph used as an filter pattern specification in a query. If optional predicate or relation properties are not specified, they are assumed to be wildcard matches to the target knowledge space. If specified, the ontological inheritance hierarchy associated with the terms provided is assumed, such that edge bindings returned may be an exact match to the given QEdge predicate or relation term ('class'), or to a term which is a subclass of the QEdge specified term.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
predicate | [BiolinkPredicate](#biolinkpredicate) \| [[BiolinkPredicate](#biolinkpredicate)] | 
relation | `string` | Query constraint against the relationship type term of this edge, as originally specified by, or curated by inference from, the original external source of knowledge. Note that this should often be specified as predicate ontology term CURIE, although this may not be strictly enforced.
subject | `string` | **REQUIRED**. Corresponds to the map key identifier of the subject concept node anchoring the query filter pattern for the query relationship edge.
object | `string` | **REQUIRED**. Corresponds to the map key identifier of the object concept node anchoring the query filter pattern for the query relationship edge.

#### Node [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L444:L469)

A node in the KnowledgeGraph which represents some biomedical concept. Nodes are identified by the keys in the KnowledgeGraph Node mapping.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
name | `string` | Formal name of the entity
category | [BiolinkEntity](#biolinkentity) \| [[BiolinkEntity](#biolinkentity)] | 
attributes | [[Attribute](#attribute)] | A list of attributes describing the node

#### Attribute [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L470:L514)

Generic attribute for a node or an edge that expands key-value pair concept by including a type of this attribute from a suitable ontology, a source of this attribute, and (optionally) a url with additional information about this attribute.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
name | `string` | Human-readable name or label for the attribute. If appropriate, should be the name of the semantic type term.
value | any | **REQUIRED**. Value of the attribute. May be any data type, including a list.
type | [CURIE](#curie) | **REQUIRED**. CURIE of the semantic type of the attribute. For properties defined by the Biolink model this should be a biolink CURIE, otherwise, if possible, from the EDAM ontology. If a suitable identifier does not exist, enter a descriptive phrase here and submit the new type for consideration by the appropriate authority.
url | `string` | Human-consumable URL to link out and provide additional information about the attribute (not the node or the edge).
source | `string` | Source of the attribute, preferably as a CURIE prefix.

#### Edge [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L515:L555)

A specification of the semantic relationship linking two concepts that are expressed as nodes in the knowledge "thought" graph resulting from a query upon the underlying knowledge source.

##### Fixed Fields

Field Name | Type | Description
---|:---:|---
predicate | any | 
relation | `string` | The relationship type term of this edge, originally specified by, or curated by inference from, the original source of knowledge. This should generally be specified as predicate ontology CURIE.
subject | [CURIE](#curie) | **REQUIRED**. Corresponds to the map key CURIE of the subject concept node of this relationship edge.
object | [CURIE](#curie) | **REQUIRED**. Corresponds to the map key CURIE of the object concept node of this relationship edge.
attributes | [[Attribute](#attribute)] | A list of additional attributes for this edge

#### BiolinkEntity [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L556:L566)

Compact URI (CURIE) for a Biolink class, biolink:NamedThing or a child thereof. The CURIE must use the prefix 'biolink:' followed by the PascalCase class name.

`string` (pattern: `^biolink:[A-Z][a-zA-Z]*$`)

##### Example

```json
"biolink:PhenotypicFeature"
```

#### BiolinkPredicate [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L567:L578)

CURIE for a Biolink 'predicate' slot, taken from the Biolink slot ('is_a') hierarchy rooted in biolink:related_to (snake_case). This predicate defines the Biolink relationship between the subject and object nodes of a biolink:Association defining a knowledge graph edge.

`string` (pattern: `^biolink:[a-z][a-z_]*$`)

##### Example

```json
"biolink:interacts_with"
```

#### CURIE [↗](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L579:L588)

A Compact URI, consisting of a prefix and a reference separated by a colon, such as UniProtKB:P00738. Via an external context definition, the CURIE prefix and colon may be replaced by a URI prefix, such as http://identifiers.org/uniprot/, to form a full URI.

`string`
