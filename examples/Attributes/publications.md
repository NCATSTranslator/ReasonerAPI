# A TRAPI Attribute Specification for Supporting Publications

## Overview

This specification describes how the `biolink:publications` attribute MUST be used to report the collection of 
publications (broadly defined here to include any document made available for public consumption) that support
a declared Edge.

Biolink Model describes the `biolink:publications` attribute as follows:
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

1. The `biolink:publications` edge property MUST be used as the `attribute_type_id` to report 
publications that support an Edge.

2. `biolink:publications` are typically referenced using a [CURIE](https://www.w3.org/TR/2010/NOTE-curie-20101216/) or 
[URI/URL](https://www.w3.org/Addressing/) but may also be captured as free-text strings. 
If a source provides an Edge where some publications are referenced as CURIE/URIs, and others reported as free-text 
descriptions, the publications referenced by CURIE or URI MUST be captured in a separate Attribute from those referenced as free-text.  For example:

A source providing only URIs and CURIEs:
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
          "value_type_id": "biolink:Uriorcurie",
          "attribute_source": "infores:hmdb"
        }
      ]
    }
  ]
}
```

A source providing only free-text descriptions (note the change in value_type_id):
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

A source providing CURIEs, URIs, and free-text descriptions.  Note the existance of two attribute objects to 
disambiguate the `uriorcurie` typed `biolink:publications` list from the `**[T.B.D]**` typed `biolink:publications` 
list:

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
        },
        {
          "attribute_type_id": "biolink:publications",
          "value": [
            "PMID:31737390",
            "PMID:6815562",
            "http://info.gov.hk/gia/general/201011/02/P201011020204.htm"
          ],
          "value_type_id": "biolink:Uriorcurie",
          "attribute_source": "infores:hmdb"
        }
      ]
    }
  ]
}
```

3. If a source provides a CURIE identifier for a supporting publication, it MUST follow the
prefix spelling and casing match that in the Biolink Model [prefix map](https://github.com/biolink/biolink-model/blob/master/prefix-map/biolink-model-prefix-map.json). (e.g "PMID:1593752", "doi:10.1177/00928615010300134").


4. A source MAY provide a URL as one of the values of the `biolink:publications` attribute, EXCEPT in cases where  
a Pubmed, Pubmed Central, or DOI identifier is part of the full URL. In such cases, the identifier MUST be reported 
in its CURIE form, listed below in order of preference for use in Translator (most preferred to least preferred):
If a source provides more than one of the above identifiers for a single publication, the source MUST only report one 
identifier. The preferred order of reporting is: PMID, PMCID, DOI. 


```
    http://www.ncbi.nlm.nih.gov/pubmed/29076384   →  **PMID: 29076384**  
    http://europepmc.org/articles/PMC6246007      →  **PMC:6246007**  
    https://doi.org/10.1080/17512433.2018.1398644 →  **DOI:0.1080/17512433.2018.1398644**  
```

5. Knowledge Providers can expect consumers to obtain metadata about a supporting journal articles that 
are index by Pubmed (e.g. title, journal, abstract, dates), from the Text Mining Knowledge Provider’s 
Publication Metadata API. However, the Knowledge Providers MAY use the Attribute description and 
value_url fields to provide additional metadata in the TRAPI message itself.
