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
* [object_qualifiers.json](object_qualifiers.json)

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
object: "NCBIGene:154", # ADRB2
object_aspect_qualifier: expression
object_direction_qualifier: increased
```

* [subject_and_object_qualifiers.json](subject_and_object_qualifiers.json)

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

* [complex_gocam_qualifiers.json](complex_gocam_qualifiers.json)


### Querying for "_affects transport of_ *OR* _affects localization of_" with qualifiers instead of predicates.

_"What chemicals affect either the localization or the transport of ADRB2"_

* [localization_or_transport.json](localization_or_transport.json)


### When to use predicate=causes vs. qualified_predicate=causes

_"What chemicals cause increased activity of PPARA protein"_

* [causes_predicate_vs_qualifier.json](causes_predicate_vs_qualifier.json)

Note: in this example we need to convert the user's request for "causes" (predicate) to an "affects" predicate 
with a "causes" qualified_predicate.

### Qualifier Rules

These rules can not be enforced in the schema for TRAPI, but should be implemented in a validation layer.

1. __general rules__
   1. There MUST be only one of each type of qualifier in any edges.qualifier_constraints.qualifier_set
      1. There MUST be only one qualified_predicate for each set of qualifiers in a QualifierConstraint. 
      2. qualified_predicate is an optional qualifier. (see [localization_or_transport.json](localization_or_transport.json))
         1. Both the qualified_predicate and the predicate edge properties SHOULD be queried when a predicate is provided. 
         see [causes_predicate_vs_qualifier.json](causes_predicate_vs_qualifier.json)
   2. If a KP receives non-empty QEdge.qualifier_constraints, it MUST only return edges that satisfy the entire set of 
   qualifier_constraints. If a KP does not yet support QEdge.qualifier_constraints, it MUST return an empty response 
   because no matches are found.
      1. If a knowledge statement contains more qualifiers or differently typed qualifiers than those specified in
      edges.qualifier_constraints.qualifier_set in addition to the entire set of qualifier_constraints, the knowledge 
      statement MAY also be returned.
   3. Qualifier constraints should be treated as "or" constraints.
2. __qualifier_value__  
   1. is constrained by either: an enumeration in biolink, or an ontology term.  
      1. When an ontology term is used, the assumption is that annotations that use this term or any of its children 
      should be returned.
      2. When an enumerated value is used, the assumption is that annotations that use this enumerated value or any 
      of its children should be returned. 
         1. For example, if a query asks for "biolink:object_aspect_qualifier" = "abundance", 
         then, aspects matching any child of "abundance" should also be returned (if the other qualifiers used in this
         query are also satisfied).
