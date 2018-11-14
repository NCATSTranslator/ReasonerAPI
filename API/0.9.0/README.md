# NCATS Translator Reasoners API
This API specification represents a version 0.9.0 draft of the NCATS Translator Reasoners API.
It is intended that the various reasoner tools will support this API so that remote calls to
any of the reasoners may be made using the same API with the same result format, which will
facilitate comparison among reasoners and chaining of queries to different reasoners to
achieve an aggregated result.

## Previous versions
- Previous and potentially newer versions of the draft standard may be found at https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI/tree/master/API

## Notes
- The target output is intended to be JSON-LD


# WARNING: This markdown file has not yet been updated to version 0.9.0.! The .yaml file and the .pptx file are in sync and represent 0.9.0, but the below doc has not yet caught up! In process...



# INPUT Specification
Below is a description of the elements of the JSON formatted input to the /query endpoint.
Note that at present all parameters are optional and the endpoint handler will look at what
is provided and decide if it can proceed with the input given.

## Top level (Query class)
- **max_results** - integer - Maximum number of individual results to return
- **page_size** - integer - Split the results into pages with this number of results each
- **page_number** - integer - Page number of results when the number of results exceeds the page_size

- **bypass_cache** - string - Set to 'true' in order to bypass any possible cached response and try to answer the query over again
- **asynchronous** - string - Set to 'true' in order to receive an incomplete message_id if the query will take a while. Client can then periodically request that message_id for a status update and eventual complete message
- **reasoner_ids** - array - List of reasoners to consult for the query (intended for support for an endpoint that can forward a query to one or more of the registered Translator Reasoners and further process the result for the user)

- **query_message** - object - Message object that represents the query to be answered
- **previous_message_processing_plan** - object - Container for one or more Message objects or identifiers for one or more Messages along with a processing plan for how those messages should be processed and returned






# OUTPUT Specification
Below is a description of the elements of the JSON formatted output.

## Top level (Message class)
- **context** - URI - URL of the JSON-LD context file of this document. An actual context file remains yet been developed.
- **type** - string - Type definition of this message object. Should always be "medical_translator_query_result"
- **id** - URI - URI of this message if it is persisted somewhere.
- **reasoner_id** - string - String identifier of the reasoner providing the response ("RTX", "Robokop", "Indigo", "Integrator", etc.)
- **tool_version** - string - The version string of the reasoning tool that provided this response.
- **schema_version** - string - The API standard will likely evolve over time. This encodes the schema version used in this response.
- **datetime** - datetime - The datetime stamp when this response was provided to a user.
- **n_results** - int - Total number of results in the message (which may be less than what is returned if limits were placed on the results to return)
- **message_code** - string - A terse code indicating success or error message for the query overall. OK is normal completion. Available error codes are not yet defined. These probably should be mapped to HTTP error codes in the YAML or entirely replaced by YAML-defined error codes.
- **code_description** - string - A detailed message from the Reasoning Tool to the user about degree of success of answering the query. If there are no results returned, then this message should detail why there are no results. If there are results returned, the Reasoning Tool may still provide some commentary to the user about how act of addressing the query result went. This is NOT intended to describe and answer/result, but rather just for the Reasoning Tool to provide information external to any specific result to the user.
- **original_question** - string - The exact text question that the original user provided to the reasoning tool
- **restated_question** - string - A restatement of the question that the reasoning tool understood and is answering with this response. This may not match the intent of the original_question_text.
- **query_type_id** - string - The query type id if one is known for the query/response (as defined in https://docs.google.com/spreadsheets/d/1Gna_yCbHj14Brp-8GBY50Mq36nwKGl5T5z4REUQQsfw/edit)
- **terms** - object - A dict/hash/object of the terms needed to convert the referenced **query_type_id** into a specific instance of a question. For example: "{ 'disease': 'malaria' }"
- **query_options** - object - Dict of options that can be sent with the query. Options are tool specific and not stipulated here
- **table_column_names** - array - List of column names that corresponds to the row_data for each result. Example: '[ "chemical_substance.name", "chemical_substance.id" ]'
- **results** - array - A response from a tool may contain multiple results, where a result is an independent potential answer to the query.
- **query_graph** - object - Some reasoners may not work from an English text question, but may begin with a series of notes or node types. This section is intended to encode such a beginning. It is still not completely specified. There is some initial work on this in the QuerySpecification doc in the NCATS Hackathon 44/51 folder. To be fleshed out later with appropriate input from groups who want this functionality.
- **knowledge_graph** - object - KnowledgeGraph object that contains all the nodes and edges referenced in any of the possible answers to the query
- **remote_knowledge_graph** - object - Connection information for a remote knowledge graph that is a substitute for local KnowledgeGraph contained in this Message


## Result (each object within results)
- **id** - URI - URI of this specific result if it is persisted somewhere.
- **description** - string - A free text field describing this result (answer to the query).
- **essence** - string - A single string that is the terse essence of the result (useful for simple answers)
- **essence_type** - string - A Translator bioentity type of the essence
- **row_data** - array - An arbitrary list of values that captures the essence of the result that can be turned into a tabular result across all answers (each result is a row) for a user that wants tabular output
- **score** - number - Any type of score associated with this result (highest confidence)
- **score_name** - string - Name for the score (e.g. "Jaccard distance")
- **score_direction** - string - Sorting indicator for the score: one of higher_is_better or lower_is_better
- **confidence** - float - A numerical confidence score for this result, where 1.0 denotes the highest confidence and 0.0 denote no confidence.
- **result_type** - string - One of several possible result types: 'individual query answer', 'neighborhood graph', 'type summary graph'
- **result_group** - integer - An integer group number for results for use in cases where several results should be grouped together. Also useful to control sorting ascending. The intended use for this is when multiple reasoner outputs are merged with similar answers grouped together.
- **result_group_similarity_score** - number - A score that denotes the similarity of this result to other members of the result_group
- **reasoner_id** - string - String identifier of the reasoner providing the response ("RTX", "Robokop", "Indigo", "Integrator", etc.)
- **result_graph** - object - A serialization of a KnowledgeGraph object, which is a thought pattern or graph path for this result (answer to the query).
- **knowledge_map** - object - Lookup dict that maps QNode and QEdge identifiers in the QueryGraph to Node and Edge identifiers in the KnowledgeGraph

## KnowledgeGraph (a container for nodes and edges)
- **node_list** - array - An array container for multiple node objects in arbitrary order
- **edge_list** - array - an array container for multiple edge objects in arbitrary order

## Node (each object within nodes{})
- **id** - string - CURIE corresponding to the bioentity
- **uri** - URI - Full URI corresponding to the bioentity
- **name** - string - bioentity name of the node
- **type** - array - bioentity types of the node, as defined by the KG standard
- **description** - Full 1+ sentence description/definition of the bioentity
- **symbol** - string - Equivalent symbol for this bioentity. This is most common with the protein or gene bioentity types, but other types may also have symbols or abbreviations
- **node_attributes** - array - container for a series of node_property objects

## NodeAttribute (each object within node_attributes)
- **type** - string - controlled type of the property
- **name** - string - name of the node property
- **value** - any - value associate with the name and type
- **url** - URI - URL associated with this node property

## Edge (each object within edges)
- **id** - string - Local identifier for this node which is unique within this KnowledgeGraph, and perhaps within the source reasoner's knowledge graph
- **type** - string - controlled edge type / predicate from the KG standard minimum list
- **relation** - string - controlled edge type / predicate from the KG standard maximal list
- **source** - string - id of the source node
- **target** - string - id of the target node
- **is_defined_by** - string - A CURIE/URI for the translator group that made the KG
- **defined_datetime** - string - Datetime at which the KG builder/updater pulled the information from the original source. Used as a freshness indicator.
- **provided_by** - string - A CURIE/URI for the knowledge source that defined this edge
- **confidence** - float - Confidence metric for this relationship/assertion/edge. 1.0 indicates the highest confidence. 0.0 indicates no confidence. The confidence may come directly from a knowledge source, or may come from come from the KG builder or even Reasoning Tool based on other contextual information. (NOTE: This is not in the KG standard, but is being proposed as an addition there)
- **publications** - array - Array of CURIEs for publications associated with this edge
- **evidence_type** - string - A CURIE/URI for class of evidence supporting the statement made in an edge - typically a class from the ECO ontology (e.g. ECO:0000220)
- **qualifiers** - string - Terms representing qualifiers that modify or qualify the meaning of the statement made in an edge
- **negated** - boolean - Boolean that if set to true, indicates the edge statement is negated i.e. is not true
- **edge_attributes** - array - A list of additional attributes for this edge

## EdgeAttribute (each object within a edge_attributes)
- **type** - string - controlled type of the property
- **name** - string - name of the edge property
- **value** - any - value associate with the name and type
- **url** - URI - URL associated with this edge property

