# Translator Reasoner API

[![ReasonerAPI build status on Travis CI](https://travis-ci.org/NCATSTranslator/ReasonerAPI.svg?branch=master)](https://travis-ci.org/NCATSTranslator/ReasonerAPI)

The Translator Reasoner API (TRAPI) defines a standard HTTP API for communicating biomedical questions and answers. It leverages the [Biolink model](https://github.com/biolink/biolink-model/) to precisely describe the semantics of biological entities and relationships. TRAPI's graph-based query-knowledge-binding structure enables expressive yet concise description of biomedical questions and answers.

TRAPI is described primarily by an [OpenAPI](https://github.com/OAI/OpenAPI-Specification) document [here](TranslatorReasonerAPI.yaml). The request/response structure is also documented in a more human-readable form [here](docs/reference.md).

## Example

A simple but meaningful question asks "What drugs treat type-2 diabetes?". Answers could include for example "metformin" and "glyburide". Let's walk through how such a question could be asked and answering using TRAPI.

### Query graph

Each question is framed as a [directed graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)#Directed_graph) where biomedical entities are represented by nodes and relationships between them are represented by (directed) edges.

This question includes two nodes, "type-2 diabetes" and a "drug", and one edge, "treats". The basic "query graph" therefore looks like this:

```json
{
    "nodes": {
        "type-2 diabetes": {"ids": ["MONDO:0005148"]},
        "drug": {"categories": ["biolink:Drug"]}
    },
    "edges": {
        "treats": {"subject": "drug", "predicates": ["biolink:treats"], "object": "type-2 diabetes"}
    }
}
```

TRAPI requires the values for `ids`, `categories`, and `predicates` to be [CURIEs](https://en.wikipedia.org/wiki/CURIE) in order to unambiguously identify the specific entities, entity categories, and relationship predicates. The node and edge keys have no bearing on the query graph semantics, so you can choose simple placeholders (e.g. "n01"/"e02") or human-readable names, as above. Note that the node "drug" has no `ids`; that's what we want to find out! The query graph can thus be thought of as a template for an answer to the question.

### Knowledge graph

A collection of biomedical knowledge can be represented in a similar format, but where each node must be fully specified.

```json
{
    "nodes": {
        "MONDO:0005148": {"name": "type-2 diabetes"},
        "CHEBI:6801": {"name": "metformin", "categories": ["biolink:Drug"]}
    },
    "edges": {
        "df87ff82": {"subject": "CHEBI:6801", "predicate": "biolink:treats", "object": "MONDO:0005148"}
    }
}
```

In a "knowledge graph", the node keys _are_ semantically meaningful; they must be CURIEs identifying biomedical entities, equivalent to the `ids` from the query graph.

In TRAPI lingo, a knowledge graph is not an answer, it is just knowledge. Answering a question involves mapping knowledge onto a question.

### Results

Each "result", or answer to the question, is a set of "bindings" between the knowledge graph and query graph. In our simple example, the knowledge-graph node "MONDO:0005148" will be bound to the query-graph node "type-2 diabetes" and the knowledge-graph node "CHEBI:6801" will be bound to the query-graph node "drug". The knowledge-graph edge "df87ff82" will be bound to the query-graph edge "treats".

```json
{
    "node_bindings": {
        "type-2 diabetes": [{"id": "MONDO:0005148"}],
        "drug": [{"id": "CHEBI:6801"}]
    },
    "edge_bindings": {
        "treats": [{"id": "df87ff82"}]
    }
}
```

This format allows concise communication of the knowledge relevant to a question and precisely how it is used to formulate answers.

### Message

The query graph, knowledge graph, and results together form a "message":

```json
{
    "query_graph": {
        "nodes": {
            "type-2 diabetes": {"ids": ["MONDO:0005148"]},
            "drug": {"categories": ["biolink:Drug"]}
        },
        "edges": {
            "treats": {"subject": "drug", "predicates": ["biolink:treats"], "object": "type-2 diabetes"}
        }
    },
    "knowledge_graph": {
        "nodes": {
            "MONDO:0005148": {"name": "type-2 diabetes"},
            "CHEBI:6801": {"name": "metformin", "categories": ["biolink:Drug"]}
        },
        "edges": {
            "df87ff82": {"subject": "CHEBI:6801", "predicate": "biolink:treats", "object": "MONDO:0005148"}
        }
    },
    "results": [
        {
            "node_bindings": {
                "type-2 diabetes": [{"id": "MONDO:0005148"}],
                "drug": [{"id": "CHEBI:6801"}]
            },
            "edge_bindings": {
                "treats": [{"id": "df87ff82"}]
            }
        }
    ]
}
```

The client receiving this message in response to the initial query graph has only to look at what is bound to "drug" to find the answer to their question.

These messages form the backbone of TRAPI. They are transmitted between clients and servers implementing TRAPI by including them in the body of a POST request/response, along with any other meta-information:

```json
{
    "message": {
        "query_graph": ...,
        "knowledge_graph": ...,
        "results": ...
    },
    "other information": ...
}
```

## Contributing

TRAPI is developed by The [Biomedical Data Translator](https://ncats.nih.gov/translator) Consortium. Consortium members and external contributors are encouraged to submit issues and pull requests. See the [development policies](Policies.md) for guidelines on branches and versioning.
