## Biolink Qualifiers Examples

### Object qualifiers
_“Bisphenol A results in decreased degradation of ESR1 protein”_

```
subject: Bisphenol A
predicate: affects 
qualified_predicate: causes
object: ESR1
object_aspect_qualifier: degradation
object_direction_qualifier: decreased
```
* [object_qualifiers.json](object_qualifiers.json)

Note: the predicate chosen should reflect the relationship between the subject and the object, and is not required
to be "affects".  For example, below we see a statement where the relationship between Bisphenol A and ESR1 is
not causal. 

_"Bisphenol A is associated with decreased degradation of ESR1 protein"_

```
subject: Bisphenol A
predicate: associated_with
object: ESR1
object_aspect_qualifier: degradation
object_direction_qualifier: decreased
```


### Subject and object qualifiers
_“Methionine deficiency results in increased expression of ADRB2”_

```
subject: Methionine
subject_aspect_qualifier: abundance
subject_direction_qualifier: decreased
predicate: affects 
qualified_predicate: causes
object: ADRB2 
object_aspect_qualifier: expression
object_direction_qualifier: increased
```

* [subject_and_object_qualifiers.json](subject_and_object_qualifiers.json)

_"Fenofibrate is an agonist of PPARA protein"_

```
subject: Fenofibrate
predicate: affects             
qualified_predicate: causes
object: PPARA protein
object_aspect_qualifier: activity
object_direction_qualifier: increased
mechanism_qualifier: agonism
```

### Complex statement

_"The protein ser/thr kinase activator activity of Ras85D in the plasma membrane directly positively regulates MAPKKK 
activity of Raf in the cytoplasm within the EGFR signaling pathway"_

```
subject: Dmel Ras85D
subject_aspect_qualifier: protein ser/thr kinase activator activity
subject_context_qualifier: plasma membrane
predicate: regulates   
qualified_predicate: causes
object: Dmel Raf
object_aspect_qualifier: MAPKKK activity
object_context_qualifier: cytoplasm
object_direction_qualifier: increased
pathway_context_qualifier: EGFR pathway
```

* [complex_gocam_qualifiers.json](complex_gocam_qualifiers.json)


### Localization or Transport Query

_"What chemicals affect either the localization or the transport of ADRB2"_

* [localization_or_transport.json](localization_or_transport.json)


### Qualifier Rules

These rules can not be enforced in the schema for TRAPI, but should be implemented in a validation layer.

1. __general rules__
   1. There MUST be only one of each type of qualifier in any edges.qualifier_constraints.qualifier_set
      1. There MUST be only one qualified_predicate for each set of qualifiers in a QualifierConstraint. 
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