# Examples of Attribute Types

This document provides a set of Attribute types proposed for common agreement.

name | type | example values | comments
| --- | --- | --- |--- |
is_defined_by | ?? | "ARAX", "ARAX/KG2" | Not sure what type to use for this one...
defined_datetime | ?? | "2020-04-19 12:42:36" | Should this be a metadata type or "biolink:TimeType"?
provided_by | biolink:provided_by | "umls_source:NCI" | 'umls_source:ATC' on nodes or ['SEMMEDDB:', 'umls_source:MTH'] on edges
confidence | biolink:ConfidenceLevel | 1, 0.5 | 
weight | ?? | 1, 0.5 | Not sure what to put here as I didn't find any specifically mentioning edge weights...
all_names |  | ['Sodium equilin sulfate', 'Estratab'] | Not sure what to put for this...
deprecated | | False | Not sure what to put here...| 
equivalent_curies | biolink:synonym | ['UMLS:C0242700', 'MESH:D018489', 'SNOMED:21162009'] | Thought this might also be a synonym type
full_name | biolink:full_name | |
negated | biolink:negated | False |
probability | biolink:p_value | 0.00019258212 | Thoughts on p-value for probability?
publications | biolink:publications | ["PMID:16798005", "PMID:24139633", "PMID:6208804"] |
relation | biolink:relation | 'rdfs:subClassOf' |
symbol | biolink:symbol | 'BRCA1' |
synonym| biolink:synonym | ['Imidazole derivatives', 'intestinal antiinfectives'] |
update_date| ?? | 'Mon Jan 4 19:28:17 2021' |
uri | metatype:Uri | |


