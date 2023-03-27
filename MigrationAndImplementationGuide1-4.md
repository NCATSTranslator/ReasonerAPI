# TRAPI 1.4 Migration and Implementation Guide

TRAPI 1.4 implements a few major breaking changes, and is therefore not backwards compatible with previous versions of TRAPI. This guide aims to provide instructions for how to transform a TRAPI 1.3 message into a TRAPI 1.4 message.

## TRAPI 1.3 Example Message

First we will start with an example TRAPI 1.3 message. For ease of reading, this message won't be exactly what a real message would look like. For instance, proper CURIE's will not be used in many cases, instead being replaced by more easily readable words and names. The example presented is a representation of a message sent by an ARA to the ARS, however this can be fairly easily generalized.

```
"message": {
    "query_graph": {
        "nodes": {
            "n0": {
                "id": "diabetes"
            },
            "n1": {
                "categories": ["drug"]
            }
        },
        "edges": {
            "e0": {
                "predicates":["treats],
                "subject": "n1",
                "object": "n0",
                "knowledge_type": "inferred"
            }
        }
    },
    "knowledge_graph": {
        "nodes": {
            "diabetes": {node_info},
            "metformin": {node_info},
            "hypoglycemia": {node_info}
            "extra_node": {node_info}
        },
        "edges": {
            "e01": {
                "subject": "metformin",
                "object": "diabetes",
                "predicate": "treats",
            },
            "e02": {
                "subject": "diabetes",
                "object": "hypoglycemia",
                "predicate": "similar_to"
            },
            "e12": {
                "subject": "metformin",
                "object": hypoglycemia,
                "predicate": "contraindicated for"
            },
            "creative_edge" {
                "subject": "metformin",
                "object": "diabetes",
                "predicate": "treats",
            },
            "extra_edge0": {
                "subject": "metformin",
                "object": "diabetes",
                "predicate": "co-occurs in literature with"
            },
            "extra_edge1": {
                "subject": "metformin",
                "object": "extra_node",
                "predicate": "related to"
            }
        }
    },
    "results": [
        {
            "node_bindings": {
                "n0": [
                    {
                        "id": "diabetes"
                    }
                ],
                "n1": [
                    {
                        "id": "metformin"
                    }
                ]
            },
            "edge_bindings": {
                "e0": [
                    {
                        "id": "e01"
                    }
                ]
            },
            "score": .4
        },
        {
            "node_bindings": {
                "n0": [
                    {
                        "id": "diabetes"
                    }
                ],
                "n1": [
                    {
                        "id": "metformin"
                    }
                ],
                "dummy_node": [
                    {
                        "id": "extra_node"
                    }
                ]
            },
            "edge_bindings": {
                "e0": [
                    {
                        "id": "e01"
                    }
                ],
                "dummy_edge0": [
                    {
                        "id": "extra_edge0"
                    }
                ],
                "dummy_edge1": [
                    {
                        "id": "extra_edge1"
                    }
                ]
            },
            "score": .6
        },
        {
            "node_bindings": {
                "n0": [
                    {
                        "id": "diabetes"
                    }
                ],
                "n1": [
                    {
                        "id": "metformin"
                    }
                ]
            },
            "edge_bindings": {
                "e0": [
                    {
                        "id": "creative_edge"
                    }
                ],
                "dummy_edge0": [
                    {
                        "id": "e02"
                    }
                ],
                "dummy_edge1": [
                    {
                        "id": "e12"
                    }
                ]
            },
            "score": .3
        }
    ]
}
```

This message is a creative mode query that asks which drug treats diabetes. Three results are returned in total. The first is a basic result that says metformin treats diabetes using a found edge. The second uses the same found edge, but also includes extra information in the form of literature co-occurrence edges and an estra node meant to help with scoring. The third uses a creative mode edge to determine that metformin treats diabetes.

## Migrating to TRAPI 1.4

Now we will go about transforming this message into a TRAPI 1.4 message, going step-by-step. Both the knowledge graph and the results will be modified, but first we creats the auxiliary graphs.

### Auxiliary Graphs

There is now a top level property of a message named "auxiliary_graphs". Auxiliary graphs are graphs that provide support or evidence for both results and knowledge graph edges. They are created by referencing edges from the knowledge graph. We will now create the auxiliary graphs neccessary for our TRAPI 1.4 message. These use the same edge identifiers used in the knowledge graph of our TRAPI 1.3 message.

```
"auxiliary_graphs": {
    "a0": {
        "edges": [
            "e02",
            "e12"
        ]
    },
    "a1": {
        "edges": [
            "extra_edge0"
        ]
    },
    "a2": {
        "edges": [
            "extra_edge1"
        ]
    }
}
```

These auxiliary graphs each represent something different. "a0" represents the explanation for the creative edge found in our original message. "a1" is the graph of literature co-occurrence. "a2" is used for the extra node. Some of this is up to an ARA's discretion. For instance, if both "a1" and "a2" were produced by the same ARA, then that ARA may decide to create only a single auxiliary graph for both. Therefore, this is also a valid representation:

```
"auxiliary_graphs": {
    "a0": {
        "edges": [
            "e02",
            "e12"
        ]
    },
    "a1": {
        "edges": [
            "extra_edge0",
            "extra_edge1"
        ]
    }
}
```

We will be using the first "auxiliary_graphs" list going forward.

### Knowledge Graph

Most of the knowledge graph will remain the same in this example. Only one of the edge would be significantly changed. For readibility, we will only go over that edge.

```
"creative_edge": {
    "subject": "metformin",
    "object": "diabetes",
    "predicate": "treats",
    "attributes": [
        {
            "attribute_type_id": "support graph",
            "values": [
                "a0"
            ]
        }
    ]
}
```

The auxiliary graph that is being used as evidence for the creative edge is now attached to the attribute of the creative edge.

### Results

Results experience the largest refactor in TRAPI 1.4. From the three results presented before, we now make a single result.

```
"results": [
    {
        "node_bindings": {
            "n0": [
                "id": "diabetes"
            ],
            "n1": [
                "id": "metformin"
            ]
        },
        "analyses":[analysis objects]
    }
]
```

Notice that a result now has only two top-level properties: node bindings and analyses. Edge bindings and scores will now be included in the analyses, which is a list of analysis objects. We will go through creating an analysis object from each of the previous results.

Also notice that the node bindings lack any extra nodes. Only nodes that are present in the original query graph can be used in node bindings. The query graph may not be modified.

The first result has the most straighforward anaylsis block:

```
{
    "reasoner_id": "ara0"
    "edge_bindings": {
        "e0": [
            {
                "id": "e01"
            }
        ]
    },
    "score": .4
}
```

From the second result, we construct this analysis:

```
{
    "reasoner_id": "ara0"
    "edge_bindings": {
        "e0": [
            {
                "id": "e01"
            }
        ]
    }
    "support_graphs": [
        "a1",
        "a2"
    ],
    "score": .6
}
```

The auxiliary graphs that we constructed earlier are now being used as support for this analysis block, so therefore go into the "support_graphs" field of the analysis block.

Lastly, the third result generates this analysis:

```
{
    "reasoner_id": "ara0"
    "edge_bindings": {
        "e0": [
            {
                "id": "creative_edge"
            }
        ]
    }
    "score": .3
}
```

Notice that the other components of the creative edge, the edges used to support it, are not included in the edge bindings. Instead, they have been included as evidence for the edge itself.

Those are all of the generated analysis blocks. As you can see, like node bindings, edge bindings can also only include edges found in the original query graph.

So the completed "analyses" list with these analysis blocks will look like this

```
"analyses": [
    {
        "reasoner_id": "ara0"
        "edge_bindings": {
            "e0": [
                {
                    "id": "e01"
                }
            ]
        },
        "score": .4
    },
    {
        "reasoner_id": "ara0"
        "edge_bindings": {
            "e0": [
                {
                    "id": "e01"
                }
            ]
        }
        "support_graphs": [
            "a1",
            "a2"
        ],
        "score": .6
    },
    {
        "reasoner_id": "ara0"
        "edge_bindings": {
            "e0": [
                {
                    "id": "creative_edge"
                }
            ]
        }
        "score": .3
    }
]
```

However, an ARA also has discretion in the construction of the analysis blocks as well. All three of those analysis blocks can be combined into a single analysis instead. If that decision is made, then the results would look like this instead.

```
"results": [
    {
        "node_bindings": {
            "n0": [
                "id": "diabetes"
            ],
            "n1": [
                "id": "metformin"
            ]
        },
        "analyses":[
            {
                "reasoner_id": "ara0"
                "edge_bindings": {
                    "e0": [
                        {
                            "id": "e01"
                        },
                        {
                            "id": "creative_edge"
                        }
                    ]
                },
                "support_graphs": [
                    "a1",
                    "a2"
                ]
                "score": .7
            },
        ]
    }
]
```

## TRAPI 1.4 Example Message

Finally, we can put all of it back together, to show the full message.

```
"message": {
    "query_graph": {
        "nodes": {
            "n0": {
                "id": "diabetes"
            },
            "n1": {
                "categories": ["drug"]
            }
        },
        "edges": {
            "e0": {
                "predicates":["treats],
                "subject": "n1",
                "object": "n0",
                "knowledge_type": "inferred"
            }
        }
    },
    "knowledge_graph": {
        "nodes": {
            "diabetes": {node_info},
            "metformin": {node_info},
            "hypoglycemia": {node_info}
            "extra_node": {node_info}
        },
        "edges": {
            "e01": {
                "subject": "metformin",
                "object": "diabetes",
                "predicate": "treats",
            },
            "e02": {
                "subject": "diabetes",
                "object": "hypoglycemia",
                "predicate": "similar_to"
            },
            "e12": {
                "subject": "metformin",
                "object": hypoglycemia,
                "predicate": "contraindicated for"
            },
            "creative_edge": {
                "subject": "metformin",
                "object": "diabetes",
                "predicate": "treats",
                "attributes": [
                    {
                        "attribute_type_id": "support graph",
                        "values": [
                            "a0"
                        ]
                    }
                ]
            },
            "extra_edge0": {
                "subject": "metformin",
                "object": "diabetes",
                "predicate": "co-occurs in literature with"
            },
            "extra_edge1": {
                "subject": "metformin",
                "object": "extra_node",
                "predicate": "related to"
            }
        }
    },
    "auxiliary_graphs": {
        "a0": {
            "edges": [
                "e02",
                "e12"
            ]
        },
        "a1": {
            "edges": [
                "extra_edge0",
                "extra_edge1"
            ]
        }
    },
    "results": [
        {
            "node_bindings": {
                "n0": [
                    "id": "diabetes"
                ],
                "n1": [
                    "id": "metformin"
                ]
            },
            "analyses":[
                {
                    "reasoner_id": "ara0"
                    "edge_bindings": {
                        "e0": [
                            {
                                "id": "e01"
                            },
                            {
                                "id": "creative_edge"
                            }
                        ]
                    },
                    "support_graphs": [
                        "a1",
                        "a2"
                    ]
                    "score": .7
                },
            ]
        }
    ]
}
```