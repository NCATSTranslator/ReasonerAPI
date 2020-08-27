# Translator Reasoner API

This API specification represents a version 0.9.3-dev draft of the Translator Reasoner API.
Previous releases (e.g. 0.9.2, 0.9.1) are tagged.
It is intended that NCATS Translator ARS, Autonomous Reasoning Agents (ARAs), and Knowledge Providers (KPs)
will support this API so that remote calls to
any of these services (and other related Translator resources) may be made using the same API
with the same result format, which will
facilitate comparison among reasoners and chaining of queries to different reasoners to
achieve an aggregated result.

## The Core and Extended
- The `master` branch contains the core schema, a minimal schema that all implementations must have code to handle
- The `extended` branch contains extensions to the schema that enable the encoding of substantially more information,
  but clients and servers are not required to implement handling for these items.

## Previous versions
- Previous versions of the draft standard may be found at https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI/tree/7205051d69e50d2c8137d88598346e185f920ea4/API

## Notes
- The following documentation is now badly out of date, but generally reflects the year-old state of the `extended` schema
- The target output is intended to be JSON-LD
- Updated 2019-03-08

# INPUT Specification
Below is a description of the elements of the JSON formatted input to the /query endpoint.
Note that at present all parameters are optional and the endpoint handler will look at what
is provided and decide if it can proceed with the input given.

## Top level (Query class)
- **bypass_cache** - string - Set to true in order to bypass any possible cached message and try to answer the query over again (e.g.:  "true")                                             
- **asynchronous** - string - Set to true in order to receive an incomplete message_id if the query will take a while. Client can then periodically request that message_id for a status update and eventual complete message (e.g.:  "false")                                                                                                                                          
- **max_results** - integer - Maximum number of individual results to return (e.g.:  100)                                                                                                   
- **page_size** - integer - Split the results into pages with this number of results each (e.g.:  20)                                                                                       
- **page_number** - integer - Page number of results when the number of results exceeds the page_size (e.g.:  1)                                                                            
- **reasoner_ids** - array - List of reasoners to consult for the query (e.g.:  [ "RTX", "Robokop" ])                                                                                       
- **query_message** - object - Message object that represents the query to be answered (e.g.: ) which contains a [query graph representing the structure of a query](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI/blob/master/API/TranslatorReasonersAPI.yaml#L664).                                                                                           
- **previous_message_processing_plan** - object - Container for one or more Message objects or identifiers for one or more Messages along with a processing plan for how those messages should be processed and returned (e.g.: ).                                                                                                                                                  
## PreviousMessageProcessingPlan
- **previous_message_uris** - array - List of URIs for Message objects to fetch and process (e.g.:  [ "https://rtx.ncats.io/api/rtx/v1/message/300" ])
- **previous_messages** - array - List of Message objects to process (e.g.: ) similar to the ones referenced by **query_message** above, containing a [query graph object representing the structure of a query](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI/blob/master/API/TranslatorReasonersAPI.yaml#L664).
- **processing_actions** - array - List of order-dependent actions to guide what happens with the Message object(s) (e.g.:  [ "mod45filter", "redirect2RTX" ])
- **options** - object - Dict of options that apply during processing in an order independent fashion (e.g.:  [ "topNMostFrequent" ])



# OUTPUT Specification
Below is a description of the elements of the JSON formatted output.

## Top level (Message class)
- **context** - string - JSON-LD context URI (e.g.:  "https://rtx.ncats.io/ns/translator.jsonld")
- **type** - string - Entity type of this message (e.g.:  "translator_reasoner_message")
- **id** - string - URI for this message (e.g.:  "https://rtx.ncats.io/api/rtx/v1/message/123")
- **reasoner_id** - string - Identifier string of the reasoner that provided this message (one of RTX, Robokop, Indigo, Integrator, etc.) (e.g.:  "reasoner")
- **tool_version** - string - Version label of the tool that generated this message (e.g.:  "RTX 0.5.0")
- **schema_version** - string - Version label of this JSON-LD schema (e.g.:  "0.9.0")
- **datetime** - string - Datetime string for the time that this message was generated (e.g.:  "2018-01-09 12:34:45")
- **n_results** - integer - Total number of results from the query (which may be less than what is returned if limits were placed on the number of results to return) (e.g.:  42)
- **message_code** - string - Set to OK for success, or some other short string to indicate and error (e.g., KGUnavailable, TermNotFound, etc.) (e.g.:  "OK")
- **code_description** - string - Extended description denoting the success or mode of failure in the generation of the message (e.g.:  "9 results found")
- **table_column_names** - array - List of column names that corresponds to the row_data for each result (e.g.:  [ "chemical_substance.name", "chemical_substance.id" ])
- **original_question** - string - The original question text typed in by the user (e.g.:  "what proteins are affected by sickle cell anemia")
- **restated_question** - string - A precise restatement of the question, as understood by the Translator, for which the answer applies. The user should verify that the restated question matches the intent of their original question (it might not). (e.g.:  "Which proteins are affected by sickle cell anemia?")
- **query_type_id** - string - The query type id if one is known for the query/message (as defined in https://docs.google.com/spreadsheets/d/18zW81wteUfOn3rFRVG0z8mW-ecNhdsfD_6s73ETJnUw/edit#gid=1742835901 ) (e.g.:  "Q2")
- **terms** - object - Dict of terms needed by the specific query type (e.g.: )
- **query_options** - object - Dict of options that can be sent with the query. Options are tool specific and not stipulated here (e.g.:  "{coalesce=True,threshold=0.9}")
- **results** - array - List of all returned potential answers for the query posed (e.g.: )
- **query_graph** - object - QueryGraph object that contains a serialization of a query in the form of a graph (e.g.: )
- **knowledge_graph** - object - KnowledgeGraph object that contains all the nodes and edges referenced in any of the possible answers to the query (e.g.: ) **OR** a RemoteKnowledgeGraph object that contains connection information for a remote knowledge graph that is a substitute for local KnowledgeGraph contained in this Message (e.g.: )


## Result (each object within results)
- **id** - string - URI for this message (e.g.:  "https://rtx.ncats.io/api/rtx/v1/result/234")
- **description** - string - A free text description of this result answer from the reasoner (e.g.:  "The genetic condition sickle cell anemia may provide protection\)
- **essence** - string - A single string that is the terse essence of the result (useful for simple answers) (e.g.:  "ibuprofen")
- **essence_type** - string - A Translator bioentity type of the essence (e.g.:  "drug")
- **row_data** - array - An arbitrary list of values that captures the essence of the result that can be turned into a tabular result across all answers (each result is a row) for a user that wants tabular output (e.g.:  [ "ibuprofen", "CHEMBL:CHEMBL521" ])
- **score** - number - Any type of score associated with this result (e.g.:  163.233)
- **score_name** - string - Name for the score (e.g.:  "Jaccard distance")
- **score_direction** - string - Sorting indicator for the score: one of higher_is_better or lower_is_better (e.g.:  "lower_is_better")
- **confidence** - number - Confidence metric for this result, a value between (inclusive) 0.0 (no confidence) and 1.0 (highest confidence) (e.g.:  0.9234)
- **result_type** - string - One of several possible result types: 'individual query answer', 'neighborhood graph', 'type summary graph' (e.g.:  "individual query answer")
- **result_group** - integer - An integer group number for results for use in cases where several results should be grouped together. Also useful to control sorting ascending. (e.g.:  "1")
- **result_group_similarity_score** - number - A score that denotes the similarity of this result to other members of the result_group (e.g.:  0.95)
- **reasoner_id** - string - Identifier string of the reasoner that provided this result (e.g., RTX, Robokop, Indigo, Integrator) (e.g.:  "RTX")
- **result_graph** - object - A graph that describes the thought pattern of this result (i.e. answer to the query) (e.g.: )
- **node_bindings** - object - Lookup dict that maps QNode (internal) identifiers in the QueryGraph to Node identifiers (CURIEs) in the KnowledgeGraph (e.g.: { "n00": [ "HP:0001878" ] })
- **edge_bindings** - object - Lookup dict that maps QEdge (internal) identifiers in the QueryGraph to Edge (internal) identifiers in the KnowledgeGraph (e.g.: { "e00": [ "0001" ] })

## KnowledgeGraph
- **nodes** - array - List of nodes in the KnowledgeGraph (e.g.: )
- **edges** - array - List of edges in the KnowledgeGraph (e.g.: )

## RemoteKnowledgeGraph
- **url** - string - URL that provides programmatic access to the remote knowledge graph (e.g.:  "http://robokop.renci.org/api/kg")
- **credentials** - object - Credentials needed for programmatic access to the remote knowledge graph (e.g.: )

## Credentials
- **username** -  string - Username needed for programmatic access to the remote knowledge graph (e.g.: )
- **password** -  string - Password needed for programmatic access to the remote knowledge graph (e.g.: )

## QueryGraph
- **nodes** - array - List of nodes in the QueryGraph (e.g.: )
- **edges** - array - List of edges in the QueryGraph (e.g.: )

## QNode
- **node_id** - string - QueryGraph internal identifier for this QNode. Recommended form: n00, n01, n02, etc. (e.g.:  "n00")
- **curie** - string - CURIE identifier for this node (e.g.:  "OMIM:603903")
- **type** - string - Entity type of this node (e.g., protein, disease, etc.) (e.g.:  "disease")

## QEdge
- **edge_id** - string - QueryGraph internal identifier for this QEdge. Recommended form: e00, e01, e02, etc. (e.g.:  "e00")
- **type** - string - Higher-level relationship type of this edge (e.g.:  "affects")
- **relation** - string - Lower-level relationship type of this edge (e.g.:  "upregulates")
- **source_id** - string - Corresponds to the @id of source node of this edge (e.g.:  "https://omim.org/entry/603903")
- **target_id** - string - Corresponds to the @id of target node of this edge (e.g.:  "https://www.uniprot.org/uniprot/P00738")
- **negated** - boolean - Boolean that if set to true, indicates the edge statement is negated i.e. is not true (e.g.:  "true")

## Node
- **id** - string - CURIE identifier for this node (e.g.:  "OMIM:603903")
- **uri** - string -  URI identifier for this node (e.g.:  "https://www.uniprot.org/uniprot/P00738")
- **name** - string - Formal name of the entity (e.g.:  "Haptoglobin")
- **type** - array - Entity type of this node (e.g., protein, disease, etc.) (e.g.:  [ "protein" ])
- **description** - string - One to three sentences of description/definition of this entity (e.g.:  "Haptoglobin captures, and combines with free plasma hemoglobin...")
- **symbol** - string - Short abbreviation or symbol for this entity (e.g.:  "HP")
- **node_attributes** - array - A list of arbitrary attributes for the node (e.g.: )

## NodeAttribute
- **type** - string - Entity type of this attribute (e.g.:  "article")
- **name** - string - Formal name of the attribute (e.g.:  "Wikipedia article")
- **value** - string - Value of the attribute (e.g.:  "7.23e-12")
- **url** - string - A URL corresponding to this attribute (e.g.:  "https://en.wikipedia.org/wiki/Malaria")

## Edge
- **id** - string - Local identifier for this node which is unique within this KnowledgeGraph, and perhaps within the source reasoner's knowledge graph (e.g.:  "553903")
- **type** - string - Higher-level relationship type of this edge (e.g.:  "affects")
- **relation** - string - Lower-level relationship type of this edge (e.g.:  "upregulates")
- **source_id** - string - Corresponds to the @id of source node of this edge (e.g.:  "https://omim.org/entry/603903")
- **target_id** - string - Corresponds to the @id of target node of this edge (e.g.:  "https://www.uniprot.org/uniprot/P00738")
- **is_defined_by** - string - A CURIE/URI for the translator group that made the KG (e.g.:  "reasoner")
- **defined_datetime** - string - Datetime at which the KG builder/updater pulled the information from the original source. Used as a freshness indicator. (e.g.:  "2018-11-03 15:34:23")
- **provided_by** - string - A CURIE/URI for the knowledge source that defined this edge (e.g.:  "OMIM")
- **confidence** - number - Confidence metric for this edge, a value between (inclusive) 0.0 (no confidence) and 1.0 (highest confidence) (e.g.:  0.99)
- **weight** - number - Weight metric for this edge, with no upper bound. Perhaps useful when formal confidence metrics are not available (e.g.:  0.99)
- **publications** - array - List of CURIEs for publications associated with this edge (e.g.:  [ "PMID:12345562" ])
- **evidence_type** - string - A CURIE/URI for class of evidence supporting the statement made in an edge - typically a class from the ECO ontology (e.g.:  "ECO:0000220")
- **qualifiers** - string - Terms representing qualifiers that modify or qualify the meaning of the statement made in an edge (e.g.:  "ECO:0000220")
- **negated** - boolean - Boolean that if set to true, indicates the edge statement is negated i.e. is not true (e.g.:  "true")
- **edge_attributes** - array - A list of additional attributes for this edge (e.g.: )

## EdgeAttribute
- **type** - string - Entity type of this attribute (e.g.:  "localization")
- **name** - string - Formal name of the attribute (e.g.:  "Cell type limitation")
- **value** - string - Value of the attribute. While all attributes should have a name, many will not have a value (e.g.:  "MFC cells")
- **url** - string - A URL corresponding to this attribute (e.g.:  "https://www.ncbi.nlm.nih.gov/pubmed/29309293")

## Feedback
- **id** - string - URI for this feedback item (e.g.:  "https://rtx.ncats.io/api/rtx/v1/result/234/feedback/56")
- **result_id** - string - URI for the result that this feedback corresponds to (e.g.:  "https://rtx.ncats.io/api/rtx/v1/result/234")
- **expertise_level_id** - integer - Integer identifier of the claimed expertise level (e.g.:  "1")
- **rating_id** - integer - Integer identifier of the applied rating (e.g.:  "1")
- **commenter_id** - integer - Integer identifier of the commenter (e.g.:  "1")
- **commenter_full_name** - string - Full name of the commenter (e.g.:  "John Smith")
- **datetime** - string - Datetime when the feedback was provided (e.g.:  "2018-05-08 12:00")
- **comment** - string - A free text comment about this result (e.g.:  "This is a great result because...")

## ResultFeedback
- **feedback_list** - array - List of feedback posts for this result (e.g.: )

## MessageFeedback
- **feedback_list** - array - List of feedback posts for this entire message (e.g.: )
