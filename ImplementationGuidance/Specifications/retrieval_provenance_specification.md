# A TRAPI Attribute Specification for Source Retrieval Provenance

## Overview
"Source retrieval provenance" describes the set of Information Resources through which the knowledge expressed in an Edge was passed, through various retrieval and/or transform operations, on its way to its current serialized form. For example, the provenance of a Gene-Chemical Edge in a message sent to a Translator ARA (e.g. ARAGORN) might be traced through the Translator KP that provided it (e.g. MolePro), one or more intermediate aggregator resources (e.g. ChEMBL), and back to the resource that originally created/curated it (e.g. ClinicalTrials.org).

````
 ARAGORN  --retrieved_from-->   MolePro  --retrieved_from-->  ChEMBL  --retrieved_from-->  ClinicalTrials.gov
````
Note that source retrieval provenance concerns the **mechanical retrieval and transformation of data between web accessible information systems**. It does not trace the source of knowledge back to specific publications or data sets. And it is not concerned with the reasoning, inference or analysis activities that generate knowledge in the first place. These types of provenance are handled by a different set of properties in the EPC model (e.g. see the ‘Supporting Publications Specification’ [here]([url](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/ImplementationGuidance/Specifications/supporting_publications_specification.md))).

## The Model
While the TRAPI schema uses the generic Attribute class for representing nearly all metadata about Edges in knowledge graphs, metadata about **source retrieval provenance** is an exception - given the need to efficently find and parse this information for purposes of edge merging and debugging.  A complete specification will be provided here soon.  This early draft provies a brief overview of the model itself, guidance and conventions for implementing the model, and a few data examples to follow.

The diagram below shows the classes and properties defined in the [TRAPI schema]([url](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml#L1107)) to support representation of source retrieval provenance metadata.

![image](https://github.com/NCATSTranslator/ReasonerAPI/assets/5184212/840b8061-2fe4-4e15-968f-97cd87de22ab)

The `Edge.sources` property contains one or more `RetrievalSource` objects - which capture information about how a particular InformationResource served as a source from which knowledge expressed in an Edge, or data used to generate this knowledge, was retrieved. 

| Property | Description |
| ------------- | ------------- |
| resource_id | (required) The CURIE for an InformationResource that served as a source of knowledge expressed in an Edge, or a source of data used to generate this knowledge.  |
| resource_role  | (required) The role played by the InformationResource in serving as a source for an Edge (primary_knowledge_source, aggregator_knowledge_source, supporting_data_source).  |
| upstream_resource_ids| (optional) An upstream InformationResource from which the resource being described directly retrieved a record of the knowledge expressed in the Edge, or data used to generate this knowledge. |
| source_record_urls | (optional) A URL linking to a specific web page or document provided by the source that contains a record of the knowledge expressed in the Edge. |


## Implementation Guidance
A quick guide for implementers. Using the model describd above:

1. All Edges MUST report **one and only one** Retrieval Source serving as the `primary knowledge source`. 

2. All Edges MUST provide a list of any Retrieval Sources that served as `aggregator knowledge sources` by retrieving the knowledge expressed in the Edge from the priamry source of another aggregator.  

3. All Edges representing knowledge generated through analysis of data by a Translator Knoledge Provider (KP) SHOULD report any Retrieval Sources providing the data that they operated on as a `supporting data source`. 
4. Values of the `RetrievalSource.resource_id` MUST be an CURIE from the InfoRes Catalog [here]([url](https://github.com/biolink/biolink-model/blob/master/infores_catalog.yaml)) (e.g. “infores:dgidb”, “infores:molepro”)


## Data Examples

Below we provide JSON data examples illustrating two retrieval scenarios.

**Scenario 1**: Knowledge retrieval from a single external knowledge source 
A single Edge originates in primary source KS1, and is retrieved through multiple aggregators ending with the UI. Along the way, ARA1 merges the two edges retrieved from KP1 and KP1.  

![image](https://github.com/NCATSTranslator/ReasonerAPI/assets/5184212/39f08657-f4a5-4410-b2c4-244a9558ef4b)
*KS = an external Knowledge Source. KP = a Translator Knowledge Provider.  ARA = a Translator Automated Reasoning Agent, UI  = the Translator User Interface.
Each arrow in the diagram below (R1-R5) represents the distinct retrieval of one edge.*

  ````
  {
  "edges": {
    "subject": "RXCUI:1544384",
    "predicate": "biolink:treats",
    "object": "MONDO:0008383",
    "sources": [
      "type": biolink:RetrievalSource,
      "resource_id": "infores:KS_1",
      "resource_role": "primary knowledge source",
      },
      {                                        # R1
      "type": biolink:RetrievalSource
      "resource_id": "infores:KP_1",
      "resource_role": "aggregator knowledge source",
      "usptream_resource_ids": ["infores:KS_1"]      
      },
      {                                        # R2
      "type": biolink:RetrievalSource,
      "resource_id": "infores:KP_2",
      "resource_role": "aggregator knowledge source",
      "usptream_resource_ids": ["infores:KS_1"]
      },
      {                                        # R3, R4
      "type": biolink:RetrievalSource,
      "resource_id": "infores:ARA1",
      "resource_role": "aggregator knowledge source",
      "usptream_resource_ids": ["infores:KP_1", "infores:KP_2"]
      },
      {                                        # R5
      "type": biolink:RetrievalSource,
      "resource_id": "infores:UI",
      "resource_role": "aggregator knowledge source",
      "usptream_resource_ids": ["infores:ARA_1"]
      },
   ]
 }
````

**Scenario 2:** Retrieveal of knowledge generated by a KP from data 
In this scenario, the knoweldge expressed in the Edge being retrieved was originally generated by a KP based on on analysis of data it retrieved from upstream data sources. This is often the case for KPs like ICEES, COHD, and Multiomics KP that generate Edges reporting statistical corelations between variables in clinical, environmntal, or multiomics datasets. 

In the scenario diagrammed below, data from two soruces (DB1, DB2) is retrieved by KP1, where the data is analyzed to generate an Edge. This makes KP1 the "primary source" of the knowledge, and DB1 and DB2 "supporting data sources". ARA1 then retrieves this edges from KP1 and then passes it along to the UI. 

![image](https://github.com/NCATSTranslator/ReasonerAPI/assets/5184212/40cce738-1235-4ab3-8628-fca92e348761)
*DB = an external data source. KP = a Translator Knowledge Provider.  ARA = a Translator Automated Reasoning Agent, UI  = the Translator User Interface.
Each arrow (R1-R5) represents a distinct retrieval event (grey arrows/text indicates the retrieval of *data* rather than knowledge).*

````
    {
    "edges": { 
    "id": "e21aa4542"                         
    "subject": "RXCUI:1544384",
    "predicate": "biolink:correlated_with",
    "object": "MONDO:0008383",
    "sources": [
      {                                        
      "type": biolink:RetrievalSource,
      "resource_id": "infores:DB_1",
      "resource_role": "supporting data source",
      },
      {                                               
      "type": biolink:RetrievalSource,
      "resource_id": "infores:DB_2",
      "resource_role": "supporting data source",
      },
      {                                                
      "type": biolink:Source,                      # R1, R2
      "resource_id": "infores:KP_1",
      "resource_role": "primary knowledge source",
      "upstreams_resource_ids": ["infores:DB_1", "infores:DB_2"]
      },
      {                                            # R3    
      "type": biolink:RetrievalSource,
      "resource_id": "infores:ARA_1",
      "resource_role": "aggregator data source",
      "upstreams_resource_ids": ["infores:KP_1"] 
      },
      {                                            # R4         
      "type": biolink:RetrievalSource,
      "resource_id": "infores:UI",
      "resource_role": "aggregator data source",
      "upstreams_resource_ids": ["infores:ARA_1"] 
      },
    ]
  }
````




