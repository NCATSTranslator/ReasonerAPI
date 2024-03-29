This guide is split into two major sections. The first section focuses on ARAs. The second section focuses on KPs.

# TRAPI 1.4 Migration and Implementation Guide - ARA

TRAPI 1.4 implements a few major breaking changes, and is therefore not backwards compatible with previous versions of TRAPI. This guide aims to provide instructions for how to transform a TRAPI 1.3 message into a TRAPI 1.4 message.

## TRAPI 1.3 Example Message

First we will start with an example TRAPI 1.3 message. For ease of reading, this message won't be exactly what a real message would look like. For instance, proper CURIEs will not be used in the example in many cases (like edge predicates) where they normally would be, instead being replaced by more easily readable words and names. CURIEs will be used in some instances where using the CURIE is pertinent to the change. The example presented is a representation of a message sent by an ARA to the ARS, however this can be fairly easily generalized.

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
                "predicates":["treats"],
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

This message is a creative mode query that asks which drug treats diabetes. Three results are returned in total. The first is a basic result that says metformin treats diabetes using a found edge. The second uses the same found edge, but also includes extra information in the form of literature co-occurrence edges and an extra node meant to help with scoring. The third uses a creative mode edge to determine that metformin treats diabetes.

The results are shown broken up for illustrative purposes to make this guide clearer, however that is not the true expected behavior. Instead, under the current universal binding scheme, the message would more likely look like this.

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
                    },
                    {
                        "id": "creative_edge"
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
            "score": .7
        }
    ]
}
```

## Migrating to TRAPI 1.4

Now we will go about transforming this message into a TRAPI 1.4 message, going step-by-step. Both the knowledge graph and the results will be modified, but first we create the auxiliary graphs.

### Auxiliary Graphs

There is now a top level property of a message named "auxiliary_graphs". Auxiliary graphs are graphs that provide support or evidence for both results and knowledge graph edges. They are composed of references to Edges in the knowledge graph.

- Auxiliary graphs SHOULD be referenced as support graphs on edges to provide the support for that edge, e.g. why that edge is inferred to be true
- Auxiliary graphs SHOULD be referenced as support graphs in Analyses to provide support for the analysis score. e.g. literature co-occurrence edges that do not really support the existence of other edges, but rather used to support scoring of a result, SHOULD be placed in an analysis support graph

We will now create the auxiliary graphs neccessary for our TRAPI 1.4 message. These use the same edge identifiers used in the knowledge graph of our TRAPI 1.3 message.

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

Most of the knowledge graph will remain the same in this example. Only one of the edges would be significantly changed. For readibility, we will only go over that edge.

```
"creative_edge": {
    "subject": "metformin",
    "object": "diabetes",
    "predicate": "treats",
    "attributes": [
        {
            "attribute_type_id": "biolink:support_graphs",
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
        "analyses":[analysis objects]
    }
]
```

Notice that a result now has only two top-level properties: node bindings and analyses. Edge bindings and scores will now be included in the analyses, which is a list of analysis objects. We will go through creating an analysis object from each of the previous results.

Also notice that the node bindings lack any extra nodes. Only nodes that are present in the original query graph can be used in node bindings. The query graph may not be modified.

The first result has the most straighforward anaylsis block:

```
{
    "resource_id": "infores:ara0"
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
    "resource_id": "infores:ara0"
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
    "resource_id": "infores:ara0"
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
        "resource_id": "infores:ara0"
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
        "resource_id": "infores:ara0"
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
        "resource_id": "infores:ara0"
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
        "analyses":[
            {
                "resource_id": "infores:ara0"
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
                        "attribute_type_id": "biolink:support_graphs",
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
                "extra_edge0"
            ]
        },
        "a2": {
            "edges" [
                "extra_edge1"
            ]
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
            "analyses":[
                {
                    "resource_id": "infores:ara0"
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

# TRAPI 1.4 Migration and Implementation Guide - KP

The process for KP's is much simpler. However, in this section we will also go over the changes to source retrieval provenance as well. Although this change does affect ARA's as well, the effect is much greater for KP's.

## TRAPI 1.3 Example Message

We will use a much simpler example message for the KP guide.

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
                "object": "n0"
            }
        }
    },
    "knowledge_graph": {
        "nodes": {
            "diabetes": {node_info},
            "metformin": {node_info}
        },
        "edges": {
            "e01": {
                "subject": "metformin",
                "object": "diabetes",
                "predicate": "treats",
                "attributes": [
                    {
                        "attribute_type_id": "biolink:primary_knowledge_source",
                        "value": ["infores:ks0"],
                        "value_type_id": "biolink:InformationResource",
                        "attribute_source": "infores:kp0"
                    },
                    {
                        "attribute_type_id": "biolink:aggregator_knowledge_source",
                        "value": ["infores:ks1"],
                        "value_type_id": "biolink:InformationResource",
                        "attribute_source": "infores:kp0"
                    },
                    {
                        "attribute_type_id": "biolink:aggregator_knowledge_source",
                        "value": ["infores:kp0"],
                        "value_type_id": "biolink:InformationResource",
                        "attribute_source": "infores:kp0"
                    },
                ]
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
            }
        }
    ]
}
```

This KP response contains one edge. As illustrated, kp0 was able to obtain this edge from two seperate sources: ks0 and ks1. However, kp0 was able to determine that ks1 obtained this assertion from ks0, and this ks0 is the primary knowledge source.

## Migrating to TRAPI 1.4

Like the ARA guide, we will need to modify both the results and the knowledge graph for this example. However, we do not need to create any auxiliary graphs for this example, so that portion of the message may be excluded.

### Knowledge Graph

The main change here will be restructring the provenance information on the edge. This is done using the new "sources" field of an edge.

```
"e01": {
    "subject": "metformin",
    "object": "diabetes",
    "predicate": "treats",
    "attributes": []
    "sources":[
        {
            "resource_id": "infores:ks0",
            "resource_role": "primary_knowledge_source"
        },
        {
            "resource_id": "infores:ks1",
            "resource_role": "aggregator_knowledge_source",
            "upstream_resource_ids": [
                "infores:ks0"
            ]
        }
        {
            "resource_id": "infores:kp0",
            "resource_role": "aggregator_knowledge_source",
            "upstream_resource_ids": [
                "infores:ks0",
                "infores:ks1"
            ]
        }
    ]
}
```

Note that kp0 has two upstream resources listed, ks1 has one upstream resource listed, and ks0 has none.

### Results

Result generation for KP's is also relatively simple. In this case, we just migrate the edge bindings into the analysis section of the result.

```
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
    "analyses": [
        {
            "resource_id": "infores:kp0",
            "edge_bindings": {
                "e0": [
                    {
                        "id": "e01"
                    }
                ]
            }
        }
    ]
}
```

## TRAPI 1.4 Example Message

Now we can put these two sections back together to get the final message. The various JSON properties are given some credible final values not all present in the above text (but this allows this sample to validate properly using the reasoner-validator):

```
"message": {
    "query_graph": {
        "nodes": {
            "n0": {
                "ids": ["diabetes"]
            },
            "n1": {
                "categories": ["biolink:Drug"]
            }
        },
        "edges": {
            "e0": {
                "predicates":["biolink:treats"],
                "subject": "n1",
                "object": "n0"
            }
        }
    },
    "knowledge_graph": {
        "nodes": {
            "MONDO:0005148": {"name": "diabetes", "categories": ["biolink:Disease"]},
            "ncats.drug:9100L32L2N":  {"name": "metformin", "categories": ["biolink:Drug"]}
        },
        "edges": {
            "e01": {
                "subject": "ncats.drug:9100L32L2N",
                "object": "MONDO:0005148",
                "predicate": "biolink:treats",
                "attributes": [],
                "sources":[
                    {
                        "resource_id": "infores:ks0",
                        "resource_role": "primary_knowledge_source"
                    },
                    {
                        "resource_id": "infores:ks1",
                        "resource_role": "aggregator_knowledge_source",
                        "upstream_resource_ids": [
                            "infores:ks0"
                        ]
                    },
                    {
                        "resource_id": "infores:kp0",
                        "resource_role": "aggregator_knowledge_source",
                        "upstream_resource_ids": [
                            "infores:ks0",
                            "infores:ks1"
                        ]
                    }
                ]
            }
        }
    },
    "results": [
        {
            "node_bindings": {
                "n0": [
                    {
                        "id": "MONDO:0005148"
                    }
                ],
                "n1": [
                    {
                        "id": "ncats.drug:9100L32L2N"
                    }
                ]
            },
            "analyses": [
                {
                    "resource_id": "infores:kp0",
                    "edge_bindings": {
                        "e0": [
                            {
                                "id": "e01"
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```
