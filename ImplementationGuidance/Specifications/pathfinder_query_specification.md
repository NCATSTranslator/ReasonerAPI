# Pathfinder Implementation Guide

The following guide is intended to provide information on how to generate pathfinder queries, as well as general rules on how pathfinder queries should be interpreted. This guide also will provide information on how to interpret the results returned by those queries.

## General Message Structure

Pathfinder queries utilize the same general message structure as other query types. This means that a Message still has a Query Graph, a Knowledge Graph, Results, and Auxiliary Graphs.

## Query Graph

The Query Graph still has a field for nodes, as a traditional query graph would, but instead of a field for edges, it has a field for paths instead, as shown bellow. This example shows a query that requests paths connecting Crohn's Disease with Parkinson's. All paths returned must connect these two nodes.

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

A path can also have constraints listed on them. This constraint is intended to provide additional information to the pathfinder tool on how to process the query, allowing for smarter pruning. Presently, only intermediate categories are acceptable path constraints, and these intermediate category constraints are meant to allow the tool to understand that it should only return paths with at least one node that fits that category. All paths returned in the results are required to have at least one node of the category listed.

In the example below, utilizing the same query looking for paths between Crohn's and Parkinson's, the constraint listed requires that paths have at least one Gene node between them.

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

The query graph should not have any edges.

## Knowledge and Auxiliary Graphs

The Knowledge Graph in the message should have nodes and edges listed as usual. These would correspond to whatever nodes and edges are required to construct the paths between the subject and object nodes of the query graph path. The nodes and edges both follow the same rules as all other queries, although for the sake of brevity, the example below does not contain all of the required information typically found in a valid knowledge graph node and edge, such as knowledge level or source.

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

Paths themselves are encoded within the Auxiliary Graphs. Edges from the knowledge graph are referenced based on key in an auxiliary graph, within the aux graph's 'edges' field. These edges are not listed in any particular order, and the order they are listed in does not provide any additional information on the path. The path is implicitly defined by the auxiliary graph, and must be constructed. Additionally, the path is expected to be linear, meaning there should be no way to circumvent any node included in the path, although parallel edges between a pair of nodes is allowed.

Using the knowledge graph above, we can construct the auxiliary graphs shown in the example below

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

As shown, each path that is generated has a distinct list of nodes. Additionally, no auxiliary graph has any branching paths included. Even though a0 and a1 share an intermediate node, since a1 contains a node that a0 does not, they are kept separate. Additionally, a0 also contains two parallel, but not branching, edges between two of its nodes. Also, note that a2 represents the direct lookup edge between Crohn's and Parkinson's. If a lookup edge between the two input nodes exists, this edge should be returned as a path as well. 

These paths are the ones that would be returned by the unconstrained version of the intial query shown aboce, but running the constrained version as well would return slightly different paths.

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

Note that a2 is now removed because it did not contain any Gene nodes. Therefore, it is not a valid path for the constrained version of the query.

## Results

Each individual result is structured similarly as well, with node bindings and and analyses. However, as both input nodes are pinned, and there exist no unpinned nodes in the query graph, that means there is only one single result for each query, contained within the "Results" field of the Message.  This result would have many analyses, each one corresponding to a different path. This follows the same result merging rules used in other query types, where results that contain the same nodes but different analyses are combined into a single result, with their analyses concatenated.

Each analysis no longer contains edge bindings, with no query graph edges to bind to. Instead, this analysis utilizes path bindings to bind to query graph paths. Each path binding binds an auxiliary graph, by id, to a query graph path, similar to how edge bindings bind a knowledge graph edge, by id, to a query graph edge. 

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

Once again, just as it was for auxiliary graphs, this is only valid for the unconstrained version of the query. The constrained version would instead look like this.

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

Once again, the analysis containing the path generated by the lookup query is removed.

## Complete Message

Finally, we can put all of these parts of the message together, to create one final message.

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