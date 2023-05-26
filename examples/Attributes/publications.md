# A TRAPI Attribute Specification for Supporting Publications

## Overview

This specification describes how the `biolink:publications` attribute MUST be used by Translator Knowledge Providers (KPs) to report  
publications (broadly defined here to include any document made available for public consumption) that support
a declared Edge.

The Biolink Model describes the `biolink:publications` attribute as follows:
```yaml
publications:
  aliases: ["supporting publications", "supporting documents"]
  is_a: association slot
  description: >-
    A list of one or more publications that report the statement expressed in an Association, 
    or provide information used as evidence supporting this statement. 
    The notion of a ‘Publication’ is considered broadly to include any document made   
    available for public consumption. It covers scientific journal issues, individual articles, and
    books - as well as things like pre-prints, white papers, patents, drug
    labels, web pages, protocol documents, and even a part of a publication if
    of significant knowledge scope (e.g. a figure, figure legend, or section
    highlighted by NLP).
  range: publication
```

### Implementation Guidance

**1.** When a knowledge source reports one or more publication supporting an Edge, KPs MUST use the `biolink:publications` edge property as the `Attribute.attribute_type_id` field, and capture publications as a list in the `Attribute.value` field. e.g.:

````
"attribute_type_id": "biolink:publications",
"value": ["PMID:31737390", "PMID:29076384"]
````

**2.** Knowledge sources typically designate supporting publications using a **[CURIE](https://www.w3.org/TR/2010/NOTE-curie-20101216/)** or full
**[URI/URL](https://www.w3.org/Addressing/)**, but may in some cases provide only a **free-text string** title or description. Specific syntax and reporting requirements apply to each designator type:

**---2a.** When a knowledge source provides a **CURIE** for a publication, the ingesting KP MUST ensure that its prefix matches the **spelling and casing** defined in the Biolink Model [prefix map](https://github.com/biolink/biolink-model/blob/master/prefix-map/biolink-model-prefix-map.json) - and make adjustments as necessary. (e.g "PMID" not "pmid", "doi" not "DOI").

**---2b.** When a knowledge source provides a **URL** for a publication, the ingesting KP MUST report the full URL **EXCEPT** in cases where it contains a Pubmed, Pubmed Central (Europe or NLM), or DOI identifier. Here, the KP MUST convert the URL into CURIE form, e.g.:
    
```
    http://www.ncbi.nlm.nih.gov/pubmed/29076384    →  PMID:29076384  
    https://www.ncbi.nlm.nih.gov/pmc/PMC6246007    →  PMCID:6246007
    http://europepmc.org/articles/PMC6246007       →  PMC:6246007
    https://doi.org/10.1080/17512433.2018.1398644  →  doi:0.1080/17512433.2018.1398644
``` 
  
**---2c.** When a knowledge source provides a **free-text description** of a supporting publication (e.g. its title, or a bibliographic reference), the ingesting KP MAY capture this text they see fit.
  
    
**3.** If a knowledge source reports **multiple publications supporting a single Edge**, the ingesting KP SHOULD organize them into Attribute objects according to the specific instructions below.    
  
**---3a.** When all publications supporting the Edge are reported **in CURIE or URI/URL format**, the KP SHOULD capture them as a list in a single Attribute object where the `value_type_id` is "linkml:Uriorcurie":

```json
{
  "edges": [
    {
      "id": "Association001",
      "subject": "CHEBI:3215",
      "predicate": "biolink:interacts_with",
      "object": "NCBIGene:51176",
      "attributes": [
        {
          "attribute_type_id": "biolink:publications",
          "value": [
            "PMID:31737390",
            "PMID:6815562",
            "http://info.gov.hk/gia/general/201011/02/P201011020204.htm"
          ],
          "value_type_id": "linkml:Uriorcurie",
          "attribute_source": "infores:hmdb"
        }
      ]
    }
  ]
}
```
  
**---3b.** When all publications supporting the Edge are reported **as free-text descriptions**, the KP SHOULD capture them as a list in a single Attribute object where the `value_type_id` is "linkml:String":

```json
{
  "edges": [
    {
      "id": "Association001",
      "subject": "CHEBI:3215",
      "predicate": "biolink:interacts_with",
      "object": "NCBIGene:51176",
      "attributes": [
        {
          "attribute_type_id": "biolink:publications",
          "value": [
            "Thematic Review Series: Glycerolipids. Phosphatidylserine and phosphatidylethanolamine in mammalian cells: two metabolically related aminophospholipids",
            "Toranosuke Saito, Takashi Ishibashi, Tomoharu Shiozaki, Tetsuo Shiraishi, 'Developer for pressure-sensitive recording sheets, aqueous dispersion of the developer and method for preparing the developer.' U.S. Patent US5118443, issued September, 1986.: http://www.google.ca/patents/US5118443"
          ],
          "value_type_id": "linkml:String",
          "attribute_source": "infores:hmdb"
        }
      ]
    }
  ]
}
```

**---3c.** When some of the publications supporting the Edge are in **CURIE/URI format** and others are **free-text**, the ingesting KP MUST **create separate 'publications' Attributes** to hold those reported in CURIE and URI format separately from those described as free-text: 


```json
{
  "edges": [
    {
      "id": "Association001",
      "subject": "CHEBI:3215",
      "predicate": "biolink:interacts_with",
      "object": "NCBIGene:51176",
      "attributes": [
        {
          "attribute_type_id": "biolink:publications",
          "value": [
            "PMID:31737390",
            "PMID:6815562",
            "http://info.gov.hk/gia/general/201011/02/P201011020204.htm"
          ],
          "value_type_id": "linkml:Uriorcurie",
          "attribute_source": "infores:hmdb"
        },
        {
          "attribute_type_id": "biolink:publications",
          "value": [
            "Thematic Review Series: Glycerolipids. Phosphatidylserine and phosphatidylethanolamine in mammalian cells: two metabolically related aminophospholipids",
            "Toranosuke Saito, Takashi Ishibashi, Tomoharu Shiozaki, Tetsuo Shiraishi, 'Developer for pressure-sensitive recording sheets, aqueous dispersion of the developer and method for preparing the developer.' U.S. Patent US5118443, issued September, 1986.: http://www.google.ca/patents/US5118443"
          ],
          "value_type_id": "linkml:String",
          "attribute_source": "infores:hmdb"
        }
      ]
    }
  ]
}
```

**NOTE** that the requirement level 'SHOULD' is used above because KPs MAY choose at any time to **separate an individual publication into its own Attribute**, if they wish to provide specific information about it using Attribute fields (e.g. `description`), or using a nested Attribute object. 

**4.** If a knowledge source provides **multiple identifiers for a single publication supporting an Edge** (e.g. a PMID, PMCID, and DOI for the same journal article), KPs MUST report only one identifier per publication, in the following order of preference: PMID > PMCID > PMC > DOI.  

**5.** KPs can expect consumers to obtain **metadata about supporting journal articles** that are index by Pubmed (e.g. title, journal, abstract, dates, equivalent identifiers), from the Text Mining Knowledge Provider’s Publication Metadata API. However, the Knowledge Providers MAY use the `Attribute.description` and `Attribute.value_url` fields to provide additional metadata in the TRAPI message itself.

**6.** Finally, in the short term KPs can continue the current practice of including references to **supporting clinical trial records** alongside references to publications in Attribute objects using the `biolink:publications` edge property. Trial identifiers from clinicaltrials.gov MUST be reported in CURIE format using the prefix "clinicaltrials" (e.g. "clinicaltrials:NCT00222573").

```json
{
  "attribute_type_id": "biolink:publications",            
  "value": [
           "PMID:31737390",  
           "PMID:6815562",  
           "clinicaltrials:NCT00222573",
           "clinicaltrials:NCT00503152",
           "clinicaltrials:NCT00634963"
           ]                                      
  "value_type_id": "biolink:Uriorcurie",    
  "value_urls":  "https://clinicaltrials.gov/search?id=%22NCT02658760%22OR%22NCT02679560%22OR%22NCT05084573%22",
  "attribute_source": "infores:chembl"
}, 
````
**NOTE** however that we will soon be moving to **use of a new `supporting_studies` Edge property** to capture supporting clincial trials and other types of studies in a seperate Attribute from publications. A specification for this is forthcoming. 
