## Biolink 3.0 Qualifiers Examples

### Object qualifiers
_“Bisphenol A results in decreased degradation of ESR1 protein”_

![bisphenol](../images/bisphenolA.png)

* [object_qualifiers.json](object_qualifiers.json)

### Subject and object qualifiers
_“Methionine deficiency results in increased expression of ADRB2”_

![methionine](../images/methionine.png)

* [subject_and_object_qualifiers.json](subject_and_object_qualifiers.json)

### Complex GO-CAM statement
_"The protein ser/thr kinase activator activity of Ras85D in the plasma membrane directly positively regulates MAPKKK 
activity of Raf in the cytoplasm within the EGFR signaling pathway"_

![gocam](../images/gocam.png)

* [complex_gocam_qualifiers.json](complex_gocam_qualifiers.json)

### Qualifier Rules

These rules can not be enforced in the schema for TRAPI, but should be implemented in a validation layer.

1. __general rules__
   1. There may only be one of each type of qualifier in any edges.qualifier_constraints.qualifier_set
2. __qualifier_value__  
   1. is constrained by either: an enumeration in biolink, or an ontology term.  
      1. When an ontology term is used, the assumption is that annotations that use this term or any of its children should be returned.
   2. qualifier_value enumerations are hierarchical.  
      1. If a query asks for "biolink:object_aspect_qualifier" = "abundance", 
      then, aspects matching any child of abundance should also be returned. 
3. __qualified_predicate__ is required in any edges.qualifier_constraints.qualifier_set.  
   1. If the statement does not
   make use of a more or less specific value for the qualified_predicate, the value of qualified_predicate should
   be the predicate.