# NCATS Translator Reasoners API
This API specification represents a version 0.8.0 draft of the NCATS Translator Reasoners API.
It is intended that the various reasoner tools will support this API so that remote calls to
any of the reasoners may be made using the same API with the same result format, which will
facilitate comparison among reasoners and chaining of queries to different reasoners to
achieve an aggregated result.

## Previous versions
- Previous versions of the draft standard may be found at https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI/tree/master/API
- Early Google-doc based discussion may be found at https://drive.google.com/drive/folders/1kTIW6W7sLdSAhH9qBBeSAEZ4ouAViI4x
- Emerging KG Standard: https://docs.google.com/document/d/1TrvqJPe_HwmRJ5HCwZ7fsi9_mwGcwLOZ53Fnjo8Sh4E/edit#

## Notes
- The target output is intended to be JSON-LD

# Specification
Below is a description of the elements of the JSON format.

## Top level (Response)
- *context* - URI - URL of the JSON-LD context file of this document. An actual context file remains yet been developed.
- id - URI - URI of this Reasoning Tools response if it is persisted somewhere.
- type - text - Type definition of this response object.
- schema_version - text - The API standard will likely evolve over time. This encodes the schema version used in this response.
- tool_version - text - The version string of the reasoning tool that provided this response.
- datetime - datetime - The datetime stamp when this response was provided to a user.
- original_question_text - text - The exact string that the original user provided to the reasoning tool
- restated_question_text - text - A restatement of the question that the reasoning tool understood and is answering with this response. This may not match the intent of the original_question_text.
- query_template - object - Some reasoners may not work from an English text question, but may begin with a series of notes or node types. This section is intended to encode such a beginning. It is still not completely specified. There is some initial work on this in the QuerySpecification doc in the NCATS Hackathon 44/51 folder. To be fleshed out later with appropriate input from groups who want this functionality.
- result_code - text - A terse code indicating success or error message for the query overall. OK is normal completion. Available error codes are not yet defined. These probably should be mapped to HTTP error codes in the YAML or entirely replaced by YAML-defined error codes.
- message - text - A detailed message from the Reasoning Tool to the user about degree of success of answering the query. If there are no results returned, then this message should detail why there are no results. If there are results returned, the Reasoning Tool may still provide some commentary to the user about how act of addressing the query result went. This is NOT intended to describe and answer/result, but rather just for the Reasoning Tool to provide information external to any specific result to the user.
- result_list - array - A response from a tool may contain multiple results, where a result is an independent potential answer to the query.

## result (each object within result_list)
- id - URI - URI of this specific result if it is persisted somewhere.
- text - text - A free text field describing this result (answer to the query).
- confidence - float - A numerical confidence score for this result, where 1.0 denotes the highest confidence and 0.0 denote no confidence.
- result_graph - object - A serialization of the thought pattern or graph path for this result (answer to the query).

##result_graph (a container for nodes and edges)
- node_list - array - An array container for multiple node objects in arbitrary order
- edge_list - array - an array container for multiple edge objects in arbitrary order

## node (each object within node_list)
- id - text - CURIE corresponding to the bioentity
- category - text - bioentity type of the node, as defined by the KG standard
- name - text - bioentity name of the node
- uri - URI - Full URI corresponding to the bioentity
- description - Full 1+ sentence description/definition of the bioentity
- symbol - text - Equivalent symbol for this bioentity. This is most common with the protein or gene bioentity types, but other types may also have symbols or abbreviations
- node_property_list - array - container for a series of node_property objects

## node_property (each object within a node_property_list)
- type - text - controlled type of the property
- name - text - name of the node property
- value - any - value associate with the name and type
- uri - URI - potential URI or URL associated with this node property

## edge (each object within edge_list)
- predicate - text - controlled edge type / predicate from the KG standard
- subject - text - id of the subject node
- object - text - id of the object node
- is_defined_by - text - Tag of the Reasoning Tool group that built the KG from this this edge is derived
- provided_by - text - Tag of the original knowledge source that is credited with this edge/relationship in the KG   (NOTE: This is from the KG standard, but is redundant to the origin_list below, and may be removed!)
- confidence - float - Confidence metric for this relationship/assertion/edge. 1.0 indicates the highest confidence. 0.0 indicates no confidence. The confidence may come directly from a knowledge source, or may come from come from the KG builder or even Reasoning Tool based on other contextual information. (NOTE: This is not in the KG standard, but is being proposed as an addition there)
- edge_property_list - array - container for a series of edge_property objects
- origin_list - array - container for a series of origin objects

## edge_property (each object within an edge_property_list)
- type - text - controlled type of the property
- name - text - name of the edge property
- value - any - value associate with the name and type
- uri - URI - potential URI or URL associated with this edge property

