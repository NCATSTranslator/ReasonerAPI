# A TRAPI Specification for Knowledge Level and Agent Type Edge Annotations

## Overview
‘At-a-Glance’ (AAG) provenance information allow users to make a first-pass assessment of the strength, relevance, and utility of a given Edge or Result. They are supported by five specific edge properties defined in the Biolink Model:
- agent_type
- knowledge_level
- evidence_types (name t.b.d)
- method_types (name t.b.d)
- score

These properties are complemented by a larger and more complex provenance model that is being developed to support a more detailed representation of evidence and provenance metadata, and will be documented elsewhere.
   
The scope of this initial AAG specification covers two properties: 
1. `agent_type`: describes the high-level category of agent that originally generated a statement of knowledge or other type of information. 
     - Permissible values are defined in the **biolink:AgentTypeEnum** enumeration:

           manual_agent
           automated_agent
            — data_analysis_pipeline
            — computational_model
            — text_mining_agent
            — image_processing_agent
           manual_validation_of_ automated_agent
           not_provided
        
     - This property indicates the type of agent who *produced a final statement of knowledge*, which is often different from the agent or agents who produced *information used as evidence* to support the generation of this knowledge. For example, if a human curator concludes that a particular gene variant causes a medical condition - based on their interpretation of information produced by computational modeling tools, automated data analysis pipelines, and robotic laboratory assay systems - the agent type for this statement is "manual_agent" despite all of the evidence being created by automated agents. But if any of these systems is programmed to generate knowledge statements directly and without human assistance, the statement would be attributed to an "automated_agent".

2. `knowledge_level`: describes the level of knowledge expressed in a statement, based on the reasoning or analysis methods used to generate the statement, or the scope or specificity of what the statement expresses to be true. 
     - Permissible values are defined in the **biolink:KnowledgeLevelEnum** enumeration:

           knowledge_assertion
           logical_entailment
           prediction
           statistical_association
           observation
           not_provided

     - The notion of a 'level' of knowledge can in one sense relate to the strength of a statement - i.e. how confident we are that it says something true about our domain of discourse. Here, we can generally consider Assertions to be stronger than Entailments to be stronger than Predictions. But in another sense, 'level' of knowledge can refer to the scope or specificity of what a statement expresses -  on a spectrum from context-specific results of a data analysis, to generalized assertions of knowledge or fact. Here, Statistical Associations and Observations represent more foundational statements that are only slightly removed from the data on which they are based (the former reporting the direct results of an analysis in terms of correlations between variables in the data, and the latter describing phenomena that were observed/reported to have occurred).



## Implementation Guidance

1. Knowledge Providers MUST report one and only one agent type on each Edge they return in a TRAPI message, using an Attribute object keyed on the `agent_type` property. The value of this property MUST come from the biolink:AgentTypeEnum.

       {
          "attribute_type_id": "biolink:agent_type",
          "value": "manual_agent",
          "attribute_source": "infores:molepro"
       }

2. Knowledge Providers MUST report one and only one knowledge level for each Edge returned in a TRAPI message, using an Attribute object keyed on the  `knowledge_level` property. The value MUST come from the biolink:KnowledgeLevelEnum.

       {   
       "attribute_type_id": "biolink:knowledge_level",
       "value": "knowledge_assertion",
       "attribute_source": "infores:molepro"
       }

3. The main challenge in applying this standard concerns selecting appropriate agent type and knowledge level terms for a given Edge.  Here we offer three forms of guidance:  
  
   a. Detailed descriptions of each knowledge level and agent type permissible value (see [Biolink Model definitions](https://github.com/biolink/biolink-model/blob/knowledge_level_agent_type/biolink-model.yaml) - but descriptions will soon be imported as Appendix I in this document).  
     
   b. Specific guidance for assigning agent type and knowledge level to Edges in the context of Translator knowledge graphs - including mappings between Knowledge Provider resources and the types of agent type and knowledge level values relevant to each  (see [here](https://docs.google.com/document/d/1_Iol_nQhONsRyQp6ibDUBbtiY0zp7Txbs7mg6xSMXSU/edit#heading=h.1ptdqc6t27xt) - soon to be imported as Appendix II in this document).  
     
   c. A catalog of examples illustrating how agent type and knowledge level terms are applied to annotate the diverse kinds of Edges provided in Translator KGs (see [here](https://docs.google.com/document/d/1_Iol_nQhONsRyQp6ibDUBbtiY0zp7Txbs7mg6xSMXSU/edit#heading=h.g44g32y7i8lo) - soon to be imported as Appendix III in this document).  


----------


## Appendices

### Appendix I: KL and AT Term Definitions 
- *See definitions in [Biolink Model](https://github.com/biolink/biolink-model/blob/master/biolink-model.yaml), which will be imported here Appendix I.*
  
  
### Appendix II: Specific Guidance for Agent Type and Knowledge Level Annotation on Translator Edges
- *See [here](https://docs.google.com/document/d/1_Iol_nQhONsRyQp6ibDUBbtiY0zp7Txbs7mg6xSMXSU/edit#heading=h.1ptdqc6t27xt) - soon to be imported here as Appendix II.*
  
  
### Appendix III: Examples of Agent Type and Knowledge Level Annotations on Translator Edges
- *See [here](https://docs.google.com/document/d/1_Iol_nQhONsRyQp6ibDUBbtiY0zp7Txbs7mg6xSMXSU/edit#heading=h.g44g32y7i8lo) - soon to be imported here as Appendix III.*
