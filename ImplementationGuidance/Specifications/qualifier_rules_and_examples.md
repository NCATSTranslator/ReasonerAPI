## Qualifier Rules

These rules can not be enforced in the schema for TRAPI, but should be implemented in a validation layer.

1. __general rules for constraints__
   1. There MUST be only one instance of each qualifier type in a single `QEdge.constraints.qualifiers` object (qualifier-set)
      1. `qualified_predicate` is an optional qualifier (see [localization_or_transport.json](../DataExamples/localization_or_transport.json)). Both the `qualified_predicate` and the `predicates` constraint SHOULD be met when both are present on the same QEdge (see [causes_predicate_vs_qualifier.json](../DataExamples/causes_predicate_vs_qualifier.json)).
   2. If a KP receives a query with `constraints.qualifiers` on a QEdge, the edges it returns for that QEdge MUST satisfy at least 1 of `constraints.qualifiers` objects (qualifier-set) - meaning all constraints within that object.
      1. If an Edge satisfies a `constraints.qualifiers` object and contains other qualifiers not specified in that object, it MAY also be returned.
2. __for the constraint qualifier values__  
   1. They may be from a Biolink enum for the qualifier type or from an ontology.  
      1. When an ontology term is used, the assumption is that edges that use this term or any of its descendants 
      should be returned.
      2. When an Biolink enum value is used, the assumption is that edges that use this value or any 
      of its descendants should be returned. 
         1. For example, if a query asks for "biolink:object_aspect_qualifier" = "abundance", then edges with object_aspect_qualifier matching any descendant of "abundance" should also be returned.


## Biolink Qualifiers Examples

### Object qualifiers
_“Bisphenol A results in decreased degradation of ESR1 protein”_

```
subject: CHEBI:33216 # Bisphenol A
predicate: biolink:affects 
qualified_predicate: biolink:causes
object: NCBIGene:2099  # ESR1
object_aspect_qualifier: degradation
object_direction_qualifier: decreased
```
* [object_qualifiers.json](../DataExamples/object_qualifiers.json)

Note: the predicate chosen should reflect the relationship between the subject and the object, and is not required
to be "affects".  For example, below we see a statement where the relationship between Bisphenol A and ESR1 is
not causal. 

_"Bisphenol A is associated with decreased degradation of ESR1 protein"_

```
subject: CHEBI:33216 # Bisphenol A
predicate: biolink:associated_with
object: NCBIGene:2099  # ESR1
object_aspect_qualifier: degradation
object_direction_qualifier: decreased
```


### Subject and object qualifiers
_“Methionine deficiency results in increased expression of ADRB2”_

```
subject: "CHEBI:16811", # methionine
subject_aspect_qualifier: abundance
subject_direction_qualifier: decreased
predicate: biolink:affects 
qualified_predicate: biolink:causes
object: "NCBIGene:154" # ADRB2
object_aspect_qualifier: expression
object_direction_qualifier: increased
```

* [subject_and_object_qualifiers.json](../DataExamples/subject_and_object_qualifiers.json)

_"Fenofibrate is an agonist of PPARA protein"_

```
subject: "CHEBI:5001"  # Fenofibrate
predicate: biolink:affects             
qualified_predicate: biolink:causes
object: "NCBIGene:5465"  # PPARA
object_aspect_qualifier: activity
object_direction_qualifier: increased
causal_mechanism_qualifier: agonism
```

### Complex statement

_"The protein ser/thr kinase activator activity of Ras85D in the plasma membrane directly positively regulates MAPKKK 
activity of Raf in the cytoplasm within the EGFR signaling pathway"_

```
subject: FB:FBgn0003205 # Dmel Ras85D
subject_aspect_qualifier: GO:0043539 # protein ser/thr kinase activator activity
subject_context_qualifier: GO:0005886 # plasma membrane
predicate: biolink:regulates   
qualified_predicate: biolink:causes
object: FB:FBgn0003079 # Dmel Raf
object_aspect_qualifier: GO:0004708 # MAPKKK activity
object_context_qualifier: GO:0005737 #cytoplasm
object_direction_qualifier: increased
pathway_context_qualifier: GO:0038134 # ERBB2-EGFR signaling pathway
```
Please note, pathway_context_qualifier is still under discussion in the Biolink Model. If you are trying to 
represent GO-CAMs, please contact the Biolink Model team for more information.

* [complex_gocam_qualifiers.json](../DataExamples/complex_gocam_qualifiers.json)


### Querying for "_affects transport of_ *OR* _affects localization of_" with qualifiers instead of predicates.

_"What chemicals affect either the localization or the transport of ADRB2"_

* [localization_or_transport.json](../DataExamples/localization_or_transport.json)

Note: in this example we also specify set_interpretation to have results collated.


### When to use predicate=causes vs. qualified_predicate=causes

_"What chemicals cause increased activity of PPARA protein"_

* [causes_predicate_vs_qualifier.json](../DataExamples/causes_predicate_vs_qualifier.json)

Note: in this example we need to convert the user's request for "causes" (predicate) to an "affects" predicate 
with a "causes" qualified_predicate.
