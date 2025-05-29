# Pathfinder Implementation Guide

This guide explains how to construct Pathfinder queries, outlines general interpretation rules, and describes how to 
interpret the results they return.

### Summary

* Pathfinder Query Graphs do not contain edges, but instead contain Paths.
* Pathfinder Messages contain a Query Graph, a Knowledge Graph, Auxiliary Graphs, and Results.
* A Path can include constraints, but currently only `intermediate categories` constraints.
* Paths are represented within Auxiliary Graphs and are expected to be linear, with no way to skip any node in the path.
* Paths have a distinct set of Nodes.
* No branching Paths are allowed in Auxiliary Graphs.

## General Message Structure

Pathfinder queries utilize the same general message structure as other query types. This means that a Message still
has a Query Graph, a Knowledge Graph, Results, and Auxiliary Graphs.

## Query Graph

The Query Graph is not a traditional Query Graph, as it does not contain Edges. Instead, it contains Paths.

The Query Graph still has a field for Nodes, as a traditional Query Graph would, but instead of a field for Edges, it
has a field for Paths. This example shows a query that requests Paths connecting Crohn's
Disease with Parkinson's. All paths returned must connect these two nodes.

```
"query_graph": {
    "nodes": {
        "n0": {
            "ids": [
                "MONDO:0005011"
            ]
        },
        "n1": {
            "ids": [
                "MONDO:0005180"
            ]
        }
    },
    "paths": {
        "p0": {
            "subject": "n0",
            "object": "n1",
            "predicates": ["biolink:related_to"]
        }
    }
}
```

A Path can include constraints.  Currently, the only supported constraint type is `intermediate categories`, 
which requires that all returned paths contain at least one node matching the specified category.
In the example below, the intermediate category constraint listed requires that paths have at least one `Gene`
node between them.

```
"query_graph": {
    "nodes": {
        "n0": {
            "ids": [
                "MONDO:0005011"
            ]
        },
        "n1": {
            "ids": [
                "MONDO:0005180"
            ]
        }
    },
    "paths": {
        "p0": {
            "subject": "n0",
            "object": "n1",
            "constraints": [
                {
                    "intermediate_categories": ["biolink:Gene"]
                }
            ]
        }
    }
}
```

* Note: The query graph should not have any edges.

## Knowledge and Auxiliary Graphs

The Knowledge Graph in the message should have nodes and edges listed as usual. These correspond to whatever Nodes
and Edges are required to construct the paths between the subject and object nodes of the Query Graph Path. The Nodes
and Edges both follow the same rules as all other queries, although for the sake of brevity, the example below does not
contain all the required information typically found in a valid knowledge graph node and edge, such as knowledge
level or source.

```
"knowledge_graph": {
    "nodes": {
        "MONDO:0005011": {
            "categories": ["biolink:Disease"]
        },
        "MONDO:0005180": {
            "categories": ["biolink:Disease"]
        },
        "NCBIGene:120892": {
            "categories": ["biolink:Gene"]
        },
        "CL:0000540": {
            "categories": ["biolink:Cell"]
        }
    },
    "edges" {
        "e0": {
            "subject": "MONDO:0005011",
            "object": "NCBIGene:120892",
            "predicate": "biolink:condition_associated_with_gene"
        }
        "e1": {
            "subject": "NCBIGene:120892",
            "object": "MONDO:0005180",
            "predicate": "biolink:biomarker_for"
        },
        "e2": {
            "subject": "NCBIGene:120892",
            "object": "CL:0000540",
            "predicate": "biolink:located_in"
        },
        "e3": {
            "subject": "CL:0000540",
            "object": "MONDO:0005180",
            "predicate": "biolink:disrupted_by"
        },
        "e4": {
            "subject": "NCBIGene:120892",
            "object": "MONDO:0005180",
            "predicate": "biolink:gene_associated_with_condition"
        },
        "e5": {
            "subject": "MONDO:0005011",
            "object": "MONDO:0005180",
            "predicate": "biolink:associated_with"
        }
    }
}
```

Paths are represented within Auxiliary Graphs. Each Path references edges from the Knowledge Graph by key, stored in the
Auxiliary Graph's `edges` field. These Edges are unordered; their sequence does not convey Path structure. Instead, the
Path must be reconstructed from the graph itself.

Paths are expected to be linear—there should be no way to skip or bypass any node in the Path. However, parallel edges
between two nodes are allowed.

Using the Knowledge Graph above, we can construct the Auxiliary Graphs shown in the example below:

```
"auxiliary_graphs": {
    "a0": {
        "edges": [
            "e0",
            "e1",
            "e4"
        ]
    },
    "a1": {
        "edges": [
            "e0",
            "e2",
            "e3"
        ]
    },
    "a2": {
        "edges": [
            "e5"
        ]
    },
}
```

Each generated Path has a distinct set of Nodes, and no Auxiliary Graph contains branching Paths. For example, while `a0`
and `a1` share an intermediate node, they differ by at least one Node, so they are treated as separate Paths. Path `a0`
includes two parallel (but not branching) edges between a pair of nodes.

Path `a2` represents a direct lookup edge between Crohn’s and Parkinson’s. If such a direct edge exists between the two
input nodes, it should be included as a valid path.

The Paths shown correspond to the unconstrained version of the initial query. Applying `intermediate category` 
constraints would yield a slightly different set of paths. As show below in the constrained version of the 
Auxiliary Graphs, `a2` is  removed because it does not contain any `Gene` nodes. Therefore, it is not a valid Path 
for the constrained version of the query.

```
"auxiliary_graphs": {
    "a0": {
        "edges": [
            "e0",
            "e1",
            "e4"
        ]
    },
    "a1": {
        "edges": [
            "e0",
            "e2",
            "e3"
        ]
    }
}
```


## Results

Each individual Result is structured similarly, with Node Bindings and Analyses. Both input
nodes must be pinned, and therefor no unpinned nodes will exist in the Query Graph.  This means there is only one result
for each query, contained within the Results field of the Message. This Result can have many Analyses, each one
corresponding to a different Path. This follows the same Result-merging rules used in other query types, where results
that contain the same nodes but different analyses are combined into a single result, with their analyses concatenated.

Each analysis no longer contains Edge Bindings, with no Query Graph edges to bind to. Instead, the Analysis utilizes
Path Bindings to bind to Query Graph Paths. Each Path Binding binds an Auxiliary Graph by `id` to a Query Graph Path.
This is similar to how Edge Bindings bind a Knowledge Graph Edge, by id, to a Query Graph Edge.

```
"results": [
    {
        "node_bindings": {
            "n0": [
                {
                    "id": "MONDO:0005011",
                    "attributes": []
                }
            ],
            "n1": [
                {
                    "id": "MONDO:0005180",
                    "attributes": []
                }
            ]
        },
        "analyses": [
            {
                "path_bindings": {
                    "p0": [
                        {
                            "id": "a0"
                        }
                    ],
                },
                "score": .85
            },
            {
                "path_bindings": {
                    "p0": [
                        {
                            "id": "a1"
                        }
                    ],
                },
                "score": .7
            },
            {
                "path_bindings": {
                    "p0": [
                        {
                            "id": "a2"
                        }
                    ],
                },
                "score": .9
            }
        ]
    }
]
```

This is only valid for the unconstrained version of the query. The `intermediate category` constraint version
would look like this.

```
"results": [
    {
        "node_bindings": {
            "n0": [
                {
                    "id": "MONDO:0005011",
                    "attributes": []
                }
            ],
            "n1": [
                {
                    "id": "MONDO:0005180",
                    "attributes": []
                }
            ]
        },
        "analyses": [
            {
                "path_bindings": {
                    "p0": [
                        {
                            "id": "a0"
                        }
                    ],
                },
                "score": .85
            },
            {
                "path_bindings": {
                    "p0": [
                        {
                            "id": "a1"
                        }
                    ],
                },
                "score": .7
            }
        ]
    }
]
```

The Analysis containing the Path generated by the lookup Query is removed.

## Complete Message

The complete Message for the unconstrained query is shown below, with the Query Graph, Knowledge Graph, Auxiliary Graphs
and Results all included. The constrained version is shown after that.

### Unconstrained

```
{
    "message" {
        "query_graph": {
            "nodes": {
                "n0": {
                    "ids": [
                        "MONDO:0005011"
                    ]
                },
                "n1": {
                    "ids": [
                        "MONDO:0005180"
                    ]
                }
            },
            "paths": {
                "p0": {
                    "subject": "n0",
                    "object": "n1",
                    "predicates": ["biolink:related_to"]
                }
            }
        },
        "knowledge_graph": {
            "nodes": {
                "MONDO:0005011": {
                    "categories": ["biolink:Disease"]
                },
                "MONDO:0005180": {
                    "categories": ["biolink:Disease"]
                },
                "NCBIGene:120892": {
                    "categories": ["biolink:Gene"]
                },
                "CL:0000540": {
                    "categories": ["biolink:Cell"]
                }
            },
            "edges" {
                "e0": {
                    "subject": "MONDO:0005011",
                    "object": "NCBIGene:120892",
                    "predicate": "biolink:condition_associated_with_gene"
                }
                "e1": {
                    "subject": "NCBIGene:120892",
                    "object": "MONDO:0005180",
                    "predicate": "biolink:biomarker_for"
                },
                "e2": {
                    "subject": "NCBIGene:120892",
                    "object": "CL:0000540",
                    "predicate": "biolink:located_in"
                },
                "e3": {
                    "subject": "CL:0000540",
                    "object": "MONDO:0005180",
                    "predicate": "biolink:disrupted_by"
                },
                "e4": {
                    "subject": "NCBIGene:120892",
                    "object": "MONDO:0005180",
                    "predicate": "biolink:gene_associated_with_condition"
                },
                "e5": {
                    "subject": "MONDO:0005011",
                    "object": "MONDO:0005180",
                    "predicate": "biolink:associated_with"
                }
            }
        },
        "auxiliary_graphs": {
            "a0": {
                "edges": [
                    "e0",
                    "e1",
                    "e4"
                ]
            },
            "a1": {
                "edges": [
                    "e0",
                    "e2",
                    "e3"
                ]
            },
            "a2": {
                "edges": [
                    "e5"
                ]
            },
        },
        "results": [
            {
                "node_bindings": {
                    "n0": [
                        {
                            "id": "MONDO:0005011",
                            "attributes": []
                        }
                    ],
                    "n1": [
                        {
                            "id": "MONDO:0005180",
                            "attributes": []
                        }
                    ]
                },
                "analyses": [
                    {
                        "path_bindings": {
                            "p0": [
                                {
                                    "id": "a0"
                                }
                            ],
                        },
                        "score": .85
                    },
                    {
                        "path_bindings": {
                            "p0": [
                                {
                                    "id": "a1"
                                }
                            ],
                        },
                        "score": .7
                    },
                    {
                        "path_bindings": {
                            "p0": [
                                {
                                    "id": "a2"
                                }
                            ],
                        },
                        "score": .9
                    }
                ]
            }
        ]
    }
}
```

### Constrained

```
{
    "message" {
        "query_graph": {
            "nodes": {
                "n0": {
                    "ids": [
                        "MONDO:0005011"
                    ]
                },
                "n1": {
                    "ids": [
                        "MONDO:0005180"
                    ]
                }
            },
            "paths": {
                "p0": {
                    "subject": "n0",
                    "object": "n1",
                    "constraints": [
                        {
                            "intermediate_categories": ["biolink:Gene"]
                        }
                    ]
                }
            }
        },
        "knowledge_graph": {
            "nodes": {
                "MONDO:0005011": {
                    "categories": ["biolink:Disease"]
                },
                "MONDO:0005180": {
                    "categories": ["biolink:Disease"]
                },
                "NCBIGene:120892": {
                    "categories": ["biolink:Gene"]
                },
                "CL:0000540": {
                    "categories": ["biolink:Cell"]
                }
            },
            "edges" {
                "e0": {
                    "subject": "MONDO:0005011",
                    "object": "NCBIGene:120892",
                    "predicate": "biolink:condition_associated_with_gene"
                }
                "e1": {
                    "subject": "NCBIGene:120892",
                    "object": "MONDO:0005180",
                    "predicate": "biolink:biomarker_for"
                },
                "e2": {
                    "subject": "NCBIGene:120892",
                    "object": "CL:0000540",
                    "predicate": "biolink:located_in"
                },
                "e3": {
                    "subject": "CL:0000540",
                    "object": "MONDO:0005180",
                    "predicate": "biolink:disrupted_by"
                },
                "e4": {
                    "subject": "NCBIGene:120892",
                    "object": "MONDO:0005180",
                    "predicate": "biolink:gene_associated_with_condition"
                }
            }
        },
        "auxiliary_graphs": {
            "a0": {
                "edges": [
                    "e0",
                    "e1",
                    "e4"
                ]
            },
            "a1": {
                "edges": [
                    "e0",
                    "e2",
                    "e3"
                ]
            }
        },
        "results": [
            {
                "node_bindings": {
                    "n0": [
                        {
                            "id": "MONDO:0005011",
                            "attributes": []
                        }
                    ],
                    "n1": [
                        {
                            "id": "MONDO:0005180",
                            "attributes": []
                        }
                    ]
                },
                "analyses": [
                    {
                        "path_bindings": {
                            "p0": [
                                {
                                    "id": "a0"
                                }
                            ],
                        },
                        "score": .85
                    },
                    {
                        "path_bindings": {
                            "p0": [
                                {
                                    "id": "a1"
                                }
                            ],
                        },
                        "score": .7
                    }
                ]
            }
        ]
    }
}
```