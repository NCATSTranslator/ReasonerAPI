## Biolink 3.0 Qualifiers Examples

### Object qualifiers
“Bisphenol A results in decreased degradation of ESR1 protein”

![bisphenol](../images/bisphenolA.png)

* [object_qualifiers.json](object_qualifiers.json)

### Subject and object qualifiers
“Methionine deficiency results in increased expression of ADRB2”

![methionine](../images/methionine.png)

* [subject_and_object_qualifiers.json](subject_and_object_qualifiers.json)

### Complex GO-CAM statement
"The protein ser/thr kinase activator activity of Ras85D in the plasma membrane directly positively regulates MAPKKK 
activity of Raf in the cytoplasm within the EGFR signaling pathway"

![gocam](../images/gocam.png)

* [complex_gocam_qualifiers.json](complex_gocam_qualifiers.json)

### Rules

* There may only be one of each type of qualifier in any edges.qualifier_constraints.qualifier_set
* qualifier_value is defined by either: an enumerated value in biolink, or an ontology term. 
* qualifier_value enumerations are hierarchical.  If a query asks for "biolink:object_aspect_qualifier" = "abundance", 
then, aspects matching any child of abundance should also be returned. 
* qualified_predicate is required in any edges.qualifier_constraints.qualifier_set.  If the statement does not
make use of a more or less specific value for the qualified_predicate, the value of qualified_predicate should
be the predicate. 
* 