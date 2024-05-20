# A TRAPI Specification for Knowledge Level and Agent Type Edge Annotations

## Overview
‘At-a-Glance’ (AAG) provenance information allow users to make a first-pass assessment of the strength, relevance, and utility of a given Edge or Result. They are supported by five specific edge properties defined in the Biolink Model:
- agent_type
- knowledge_level
- evidence_types (name t.b.d)
- method_types (name t.b.d)
- score

These properties are complemented by a larger and more complex provenance model that is being developed to support a more detailed representation of evidence and provenance metadata, and will be documented elsewhere.
   
The scope of this initial specification covers only **Agent Type** and **Knowledge Level** metadata - which describes the type of knowledge expressed in an edge based on type of agent that originally generated a statement of knowledge encoded in an Edge, and the level of knowledge expressed in an Edge.  

In the **short term** we have created a single property that conflates these dimensions and uses a small set of terms that cover aspects of agent type and knowledge level. 

In the **long term** we will capture metadata about these two dimensions using separate edge properties, each supported by an enumeration of terms. Both solutions are described below.

## Short Term Specification 
A short term implementation, uses a single `knowledge_type` property to capture a single term from an enumeration of 5 high level categories that hit on most important distinctions users will care about, and two ‘escape terms' will be used for cases where one of these five terms is not appropriate.  

### Enumeration of Permissible Values:
- `curated`: knowledge generated through manual curation  or interpretation of data or published study results
- `predicted`: statements generated computationally through inference over less direct forms of evidence (without human intervention or review)
- `text_mined`: statements extracted from published text by NLP agents (without human intervention or review)
- `correlation`: statistical associations calculated between variables in a clinical or omics dataset, by an automated analysis pipeline
- `observed`: edge reports a phenomenon that was reported/observed to have occurred (and possibly some quantification. e.g. how many times, at what frequency)
- `not provided`: knowledge level may not fit into the categories above, or is not provided/able to be determined.
- `mixed`: used for sources that might provide edges with different knowledge levels, e.g. correlations in addition to curated Edges - set tag to Curated, unless predicate rules override

### Implementation Guidance: 
The short term plan does not require any effort on the part of KPs/ARAs. Rather than annotate individual edges in KP knowledge graphs with these terms directly, the SRI team has used them to annotate each entry in the Infores Catalog. The UI team will lookup knowledge type information here and assign infores-level tags to any edges where the infores is indicated as the primary source.  

While this will not always be accurate (e.g. in cases where a given infores provides edges with different knowledge levels) - it is a practical first step toward providing knowledge level/agent type metadata in the UI, and getting feedback from stakeholders. 

More details about the short term implementation can be found in the [document here](https://docs.google.com/document/d/1TQtQCtHWvGRsSbyQSVMwkJF0WcRt4-qZWXbUKnyTI8Q/edit#).  

## Long Term Specification
Longer term we will define distinct properties and enumerations that classify agent type and knowledge level at a more granular level, and are used to annotate individual edges directly.

### Agent Type
**Biolink Edge Property**:
   - `agent_type`: describes the high-level category of agent that originally generated a statement of knowledge or other type of information. Permissible values are provided by the **biolink:AgentTypeEnum** enumeration, as defined below:

**Permissible Values**:

   - `manual_agent`: a human agent is responsible for generating the knowledge expressed in the Edge.  The human may utilize computationally generated information as evidence for the resulting knowledge, but the human is the one who ultimately generates this knowledge.
    - `automated_agent`: an automated agent, typically a software program or tool, is responsible for generating the knowledge expressed in the Edge. Human contribution to the knowledge creation process  ends with the definition and coding of algorithms or analysis pipelines that get  executed by the automated agent.
        - `data_analysis_pipeline`:  an automated agent that executes an analysis workflow over data and reports results in an Edge. These typically  report statistical associations/correlations between variables in the input data.
        - `computational_model`: an automated agent that generates knowledge (typically predictions) based on rules/logic explicitly encoded in an algorithm (e.g. heuristic models, supervised classifiers), or  learned from patterns observed in data (e.g. ML models, unsupervised classifiers).
        - `text_mining_agent`:  an automated agent that uses Natural Language Processing to recognize concepts and/or relationships in text, and generates Edges relating these concepts with formally encoded semantics.
        - `image_processing_agent`: an automated agent that processes images to generate Edges reporting knowledge  derived from the image and/or expressed in text the image depicts (e.g. via OCR).
   - ` manual_validation_of_ automated_agent`: a human agent reviews and validates/approves the veracity of knowledge that is initially generated by an automated agent.
   - `not_provided`:  the agent type is not provided, typically because it cannot be determined from available information if the agent that generated the knowledge is manual or automated.

Note that this property indicates the type of agent who *produced a final statement of knowledge*, which is often different from the agent or agents who produced *information used as evidence* to support the generation of this knowledge. For example, if a human curator concludes that a particular gene variant causes a medical condition - based on their interpretation of information produced by computational modeling tools, automated data analysis pipelines, and robotic laboratory assay systems - the agent type for this statement is "manual_agent" despite all of the evidence being created by automated agents. But if any of these systems is programmed to generate knowledge statements directly and without human assistance, the statement would be attributed to an "automated_agent".

### Knowledge Level
**Biolink Edge Property**: 
- `knowledge_level`: describes the level of knowledge expressed in a statement, based on the reasoning or analysis methods used to generate the statement, or the scope or specificity of what the statement expresses to be true. Permissible values are defined in the **biolink:KnowledgeLevelEnum** enumeration:

**Permissible Values**:
   - `knowledge_assertion`: a statement of purported fact that is put forth by an agent as true, based on assessment of direct evidence. Assertions generally have a high confidence of being true based on the strength of evidence supporting them.
   - `logical_entailment`: a statement reporting a conclusion that follows logically from premises, which are typically well-established facts or knowledge assertions. (e.g. fingernail part of finger, finger part of hand → fingernail part of hand)). Logical entailments are based on dedictive inference, and generally have a high degree of confidence when based on sound premises and inference logic. 
   - `prediction`: a statement of a possible fact based on more probabilistic (non-deductive) forms of reasoning over indirect forms of evidence, that lead to more speculative conclusions. Predictions often have a lower degree of confidence based on the indirect nature of their evidence and reasoning supporting them.
   - `statistical_association`: a statement that reports concepts representing variables in a dataset to be statistically associated in the context of a particular cohort or dataset (e.g. “Metformin Treatment (variable 1) is correlated with Diabetes Diagnosis (variable 2) in EHR dataset X”). These associations are inherently true in that they simple report the results of some statistical analysis, but do not interpret these data to draw broader conclusions about general types in the domain of discourse.
   - `observation`: a statement reporting (and possibly quantifying) a phenomenon that was observed to occur - absent any analysis or interpretation that generates a statistical association or supports a broader conclusion or inference. Observation statements are also inherently true in that they simple report what an agent observed - without any interpretation or inference. 
   - `not_provided`: the knowledge level/type fora  statement is not provided, typically because it cannot be determined from available information.

NOTE that the notion of a 'level' of knowledge can in one sense relate to the strength of a statement - i.e. how confident we are that it says something true about our domain of discourse. Here, we can generally consider Knowledge Assertions to be stronger than Entailments to be stronger than Predictions. But in another sense, 'level' of knowledge can refer to the scope or specificity of what a statement expresses -  on a spectrum from context-specific results of a data analysis, to generalized assertions of knowledge or fact. Here, Statistical Associations and Observations represent more foundational statements that are only slightly removed from the data on which they are based (the former reporting the direct results of an analysis in terms of correlations between variables in the data, and the latter describing phenomena that were observed/reported to have occurred).

## Implementation Guidance

1. Knowledge Providers MUST report one and only one `agent type` on each Edge they return in a TRAPI message, using an Attribute object keyed on the `agent_type` property. The value of this property MUST come from the biolink:AgentTypeEnum.

       {
          "attribute_type_id": "biolink:agent_type",
          "value": "manual_agent",
          "attribute_source": "infores:molepro"
       }

2. Knowledge Providers MUST report one and only one `knowledge level` for each Edge returned in a TRAPI message, using an Attribute object keyed on the  `knowledge_level` property. The value MUST come from the biolink:KnowledgeLevelEnum.

       {   
       "attribute_type_id": "biolink:knowledge_level",
       "value": "knowledge_assertion",
       "attribute_source": "infores:molepro"
       }

3. The main challenge in applying this standard concerns selecting appropriate agent type and knowledge level terms for a given Edge. To assist KPs in this task, a [Supplemental Guidance document](https://docs.google.com/document/d/140dtM5CjWM97JiBRdAmDT-9IKqHoOj-xbE_5TWkdYqg/edit) provides additional implementation support beyond the base specification above. This includes clarification of key distinctions, tips for proper term selection, and a corpus of examples illustrating how agent type and knowledge level terms are applied to the diverse kinds of Edges provided in Translator knowledge graphs.

