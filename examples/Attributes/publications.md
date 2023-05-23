# A TRAPI Attribute Specification for Supporting Publications

## Overview

This specification describes how the `biolink:publications` attribute MUST be used by Knowledge Providers (KPs) to report  
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

**1.** When an external knowledge source reports one or more publication supporting an Edge, KPs MUST use the `biolink:publications` edge property as the `Attribute.attribute_type_id` field, and capturing the publication designator(s) in the  `Attribute.value` field.

````
"attribute_type_id": "biolink:publications",
"value": ["PMID:31737390"]
````

**2.** Knowledge sources typically designate supporting publications using a [CURIE](https://www.w3.org/TR/2010/NOTE-curie-20101216/) or full
[URI/URL](https://www.w3.org/Addressing/) -  but may in some cases provide only a free-text string title or description. Specific instructions for reporting publications using each of these designator types in the `Attribute.value` field are provided below: 

**2a.** When an external source provides a **CURIE identifier** for a supporting publication, the ingesting KP MUST ensure that the
prefix spelling and casing match that in the Biolink Model [prefix map](https://github.com/biolink/biolink-model/blob/master/prefix-map/biolink-model-prefix-map.json). (e.g "PMID:1593752", "doi:10.1177/00928615010300134").

**2b.** When an external source provides a **full URL** for a publication, the ingesting KP may report the full URL EXCEPT in cases where it contains a Pubmed, Pubmed Central, or DOI identifier. Here, the ingesting KP MUST convert full URLs into CURIE form, using prefixes in the Biolink Model [prefix map](https://github.com/biolink/biolink-model/blob/master/prefix-map/biolink-model-prefix-map.json). e.g.:
    
```
    http://www.ncbi.nlm.nih.gov/pubmed/29076384   →  PMID: 29076384  
    http://europepmc.org/articles/PMC6246007      →  PMC:6246007
    https://doi.org/10.1080/17512433.2018.1398644 →  DOI:0.1080/17512433.2018.1398644
``` 
  
**2c.** When an external source provides a **free-text description** of a supporting publication (e.g. its title, or a formatted reference), the ingesting KP MAY capture this text they see fit.
    
**3.** If an external source provides **multiple ids for a single supporting publication** (e.g. a PMID, PMCID, and DOI for the same journal article), KPs MUST report only one id per publication, in the following order of preference: PMID > PMCID > DOI.  

**4.** When a knowledge source reports **multiple distinct supporting publications for a single Edge**, the ingesting KP MUST capture them as a list in the `Attribute.value` field according to the specific instructions below:

**4a.** When all publications supporting the Edge are reported **in CURIE or URI/URL format**, the KP MUST capture them as a list in a single Attribute object where the `Attribute.value_type_id` is "linkml:Uriorcurie":

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
  
**4b.** When all publications supporting the Edge are reported **as free-text descriptions**, the KP MUST capture them as a list in a single Attribute object where the `Attribute.value_type_id` is "T.B.D.":

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
          "value_type_id": "**[T.B.D.]**",
          "attribute_source": "infores:hmdb"
        }
      ]
    }
  ]
}
```

**4c.** When some of the publications supporting the Edge are in **CURIE/URI format** and others are **free-text**, the ingesting KP MUST **create two 'publications' Attributes**: one to hold those reported in CURIE and URI format, and a second to hold those described as free-text: 


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
          "value_type_id": "**[T.B.D.]**",
          "attribute_source": "infores:hmdb"
        }
      ]
    }
  ]
}
```
    
**5.** Knowledge Providers can expect consumers to obtain metadata about supporting journal articles that 
are index by Pubmed (e.g. title, journal, abstract, dates, equivalent identifiers), from the Text Mining Knowledge Provider’s 
Publication Metadata API. However, the Knowledge Providers MAY use the `Attribute.description` and 
`Attribute.value_url` fields to provide additional metadata in the TRAPI message itself.
