# A TRAPI Attribute Specification for Supporting Publications

## Overview

Translator Knowledge Graphs represent knowledge in the form of Associations, which hold a core Statement expressed using subject, 
predicate, object, and qualifier slots, along with optional evidence, provenance, and confidence (EPC) metadata. In a TRAPI message, 
this EPC information is captured in key-value based Attribute objects.  

Consistent and computable representation of a particular type of EPC information requires a normative specification for how the key and value fields are populated in an Attribute, including:

  1. a standard Biolink edge property or properties that can populate the key `attribute_type_id` field; and  
  2. a standard datatype, syntax, and/or enumeration for populating the `value` field.  

One critical type of EPC  information that Translator users want to see are publications (considered broadly to include white papers, 
pre-prints, patents, drug labels, web pages, etc.) that report the knowledge expressed in an Edge, or describe evidence supporting it.

The specification below describes how information about supporting publications should be captured in an Edge Attribute object, using 
the `biolink:publications` property as the key attribute_type_id, as defined below:

```yaml
publications:
  aliases: ["supporting publications", "supporting documents"]
  is_a: association slot
  description: >-
    One or more publications that report the statement expressed in an Association, 
    or provide information used as evidence supporting this statement. 
    The notion of a ‘Publication’ is considered broadly to include any document made   
    available for public consumption. It covers scientific journal issues, individual articles, and
    books - as well as things like pre-prints, white papers, patents, drug
    labels, web pages, protocol documents, and even a part of a publication if
    of significant knowledge scope (e.g. a figure, figure legend, or section
    highlighted by NLP).
  range: publication
```

Note, the range for `biolink:publications` is `biolink:publication` which is actually a [Biolink Model class](https://biolink.github.io/biolink-model/docs/Publication.html#class-publication).  However, using a collection of CURIEs as shorthand syntax for representing a full list of `biolink:Publication` objects 
is expected in a TRAPI message (see below).


### Implementation Guidance

1. The `biolink:publications` edge property MUST be used as the `attribute_type_id` in Attributes reporting publications that support an Edge.

```json
"attribute_type_id": "biolink:publications"
```

2. Where multiple distinct publications support a single Edge, these MAY be reported together in a single Attribute object 
as a list in the `value` field, as below:

```json
"value": ["PMID:31737390", "PMID:6815562","http://info.gov.hk/gia/general/201011/02/P201011020204.htm"] 
```

3. Supporting publications are most typically referenced using a CURIE or URI/URL (as above), but may also be captured as free-text strings that describe the publication.  

4. If a source provides an Edge where some publications are referenced as CURIE/URIs, and other reported as free-text descriptions for others - the publications referenced by CURIE or URI MUST be captured in a separate Attribute object from those referenced as free-text.  
     a. The `value_type_id` in the Attribute holding CURIEs and/or URIs MUST be `biolink:uriorcurie`  
     b. The `value_type_id` in the Attribute holding free text descriptions MUST be **[T.B.D.]**   

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
        },
        {
          "attribute_type_id": "biolink:publications",
          "value": [
            "Thematic Review Series: Glycerolipids. Phosphatidylserine and phosphatidylethanolamine in mammalian cells: two metabolically related aminophospholipids",
            "Toranosuke Saito, Takashi Ishibashi, Tomoharu Shiozaki, Tetsuo Shiraishi, 'Developer for pressure-sensitive recording sheets, aqueous dispersion of the developer and method for preparing the developer.' U.S. Patent US5118443, issued September, 1986.: http://www.google.ca/patents/US5118443"
          ],
          "value_type_id": "   [t.b.d.]    ",
          "attribute_source": "infores:hmdb"
        }
      ]
    }
  ]
}
```

5. If a source provides a CURIE identifier for a supporting publication, Knowledge Providers MUST ensure the 
prefix spelling and casing match that in the Biolink Model [prefix map](https://github.com/biolink/biolink-model/blob/master/prefix-map/biolink-model-prefix-map.json). (e.g "PMID:1593752", "doi:10.1177/00928615010300134").

6. If a source provides a URL for a supporting publication, Knowledge Providers MUST report this full URL directly, 
EXCEPT where a Pubmed, Pubmed Central, or DOI identifier is provided as part of a full URL. In such cases, KPs 
MUST report the CURIE form of this identifier, e.g.:  
    a. http://www.ncbi.nlm.nih.gov/pubmed/29076384 → PMID: 29076384  
    b. http://europepmc.org/articles/PMC6246007 → PMC:6246007  
    c. https://doi.org/10.1080/17512433.2018.1398644 → DOI:0.1080/17512433.2018.1398644  

7. Where multiple types of publication identifiers or URLs exist for a single Publication (e.g. a PMID, PMCID, 
and DOI for the same journal article):  
    a. Knowledge Providers MUST provide only one identifier/URL per publication.  
    b. PMID CURIEs MUST be used when available. 

8. Knowledge Providers can expect consumers to obtain metadata about a supporting journal articles that 
are index by Pubmed (e.g. title, journal, abstract, dates), from the Text Mining Knowledge Provider’s 
Publication Metadata API. However, the Knowledge Providers MAY use the Attribute description and 
value_url fields to provide additional metadata in the TRAPI message itself.
