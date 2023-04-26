# The "biolink:publications" Attribute Specification

## Overview

Translator KPs represent knowledge in the form of Associations, which hold a core Statement expressed using subject, 
predicate, object, and qualifier slots, along with optional evidence and provenance metadata. In particular, the 
‘biolink:publications’ edge property is used to capture any published documents that report or support the Edge
(e.g. white papers, pre-prints, patents, drug labels, web pages). 

In Biolink Model, the `biolink:publications` edge property is defined as:

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

Note, the range for `publications` is `publication` which is actually a [Biolink Model class](https://biolink.github.io/biolink-model/docs/Publication.html#class-publication).  
However, using a collection of CURIEs as shorthand syntax for representing a full list of `biolink:Publication` objects 
is expected in a TRAPI message.


### Implementation Guidance

1. The `biolink:publications` edge property MUST be used in a TRAPI Attribute object in every Edge.

```
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
     "wikidata:Q177094",
     "http://info.gov.hk/gia/general/201011/02/P201011020204.htm"
    ],
    "value_type_id": "biolink:Uriorcurie",
    "attribute_source": "infores:molepro"
   }
  ]
```

2. The `biolink:publications` attribute MAY be either be a list of CURIEs or URIs or a list of strings, but MUST not
a mixture of both.  If there is a source that has both textual `biolink:publications` and CURIE/URI identifiers, 
a KP MUST report the CURIE/URI identifiers in one attribute stanza with the `value_type_id` of `biolink:uriorcurie` and
a KP MUST report the textual `biolink:publications` in a separate attribute stanza with the `value_type_id` 
of `EDAM-DATA:0970`.

```json
[
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
    "value_type_id": "string",
    "attribute_source": "infores:hmdb"
  }
]
```

3. If a source provides a CURIE-form identifier for a supporting publication, Knowledge Providers MUST ensure the 
prefix spelling and casing match that in the Biolink Model [prefix map](https://github.com/biolink/biolink-model/blob/master/prefix-map/biolink-model-prefix-map.json). 
(e.g "PMID:1593752", "doi:10.1177/00928615010300134").

4. If a source provides a URL for a supporting publication, Knowledge Providers SHOULD report this full URL directly, 
EXCEPT where a Pubmed, Pubmed Central, or DOI identifier is provided as part of a full URL. In such cases, KPs 
MUST report the CURIE form of this identifier, e.g.:
- http://www.ncbi.nlm.nih.gov/pubmed/ 29076384 → PMID: 29076384
- http://europepmc.org/articles/PMC6246007 → PMC:6246007
- https://doi.org/10.1080/17512433.2018.1398644 → DOI:0.1080/17512433.2018.1398644

5. Where multiple types of publication identifiers or URLs exist for a single Publication (e.g. a PMID, PMCID, 
and DOI for the same journal article):
- Knowledge Providers MUST provide only one identifier/URL per publication.
- PMID CURIEs MUST be used when available.

6. Where multiple distinct CURIES/URIs support a single Edge, these MUST be reported in a single Attribute object 
as a list in the value field, as below:
"value": ["PMID:31737390", "PMID:6815562", "wikidata:Q177094","http://info.gov.hk/gia/general/201011/02/P201011020204.htm"] 

Knowledge Providers can expect consumers to obtain metadata about a supporting journal articles that 
are index by Pubmed (e.g. title, journal, abstract, dates), from the Text Mining Knowledge Provider’s 
Publication Metadata API. However, the Knowledge Providers MAY use the Attribute description and 
value_url fields to provide additional metadata in the TRAPI message itself.
