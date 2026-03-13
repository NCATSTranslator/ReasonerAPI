# Binding Structure Specification (TRAPI 2.0)

This guide specifies the TRAPI 2.0 binding structure requirements for:
- `Result.node_bindings`
- `Analysis.edge_bindings`
- `Analysis.path_bindings`
- `NodeBinding`, `EdgeBinding`, and `PathBinding`

It is based on:
- `TranslatorReasonerAPI.yaml` (TRAPI 2.0 schema)
- Migration guidance in `MigrationAndImplementationGuide2-0.md` section `3. Binding Structure Changes (Node/Edge/Path)`

The terms MUST, SHOULD, and MAY are used as defined in RFC 2119.

## Quick Format Reference

This compact pattern gives the 2.0 binding shape used by `node_bindings`, `edge_bindings`, and `path_bindings`:

```json
"<node/edge/path>_bindings": {
  "key1": {
    "ids": ["<CURIE/EdgeID/AuxGraphID>"]
  },
  "key2": {
    "ids": ["<CURIE/EdgeID/AuxGraphID>"]
  }
}
```

## 1. Result-Level Binding Structure

### 1.1 `Result.node_bindings`
- MUST be an object/map keyed by QNode ids.
- MUST have at least one property (`minProperties: 1`).
- Each value MUST be a `NodeBinding` object (not an array).
- The map keys MUST be identifiers from the input Query Graph `nodes`.
- This structure represents the mapping from input Query Graph nodes to bound Knowledge Graph nodes in the result.
- A single QNode key MAY map to multiple Knowledge Graph nodes via `NodeBinding.ids`.

### 1.2 `Result.analyses`
- SHOULD be present for complete result semantics.
- If present, MUST be an array with at least one item (`minItems: 1`).
- Each item MUST be an `Analysis` object.
- Each analysis captures how a particular reasoning service contributed to the result.
- Analysis entries are the home for service-specific bindings, scoring, and analysis-level provenance.

## 2. Analysis-Level Binding Structure

### 2.1 `Analysis.resource_id`
- MUST be present.
- MUST identify the resource generating the analysis.
- This identifier is the provenance anchor for the analysis output and any associated score/supporting artifacts.

### 2.2 `Analysis.edge_bindings` and `Analysis.path_bindings`
- At least one of these MUST be present in each analysis.
- If `edge_bindings` is present:
  - MUST be an object/map keyed by QEdge ids.
  - MUST have at least one property (`minProperties: 1`).
  - Each value MUST be an `EdgeBinding` object.
  - It defines Query Graph edge -> Knowledge Graph edge mappings for this analysis.
  - A single QEdge key MAY map to multiple Knowledge Graph edges via `EdgeBinding.ids`.
- If `path_bindings` is present:
  - MUST be an object/map keyed by QPath ids.
  - MUST have at least one property (`minProperties: 1`).
  - Each value MUST be a `PathBinding` object.
  - It defines Query Graph path -> Auxiliary Graph mappings, specifically for pathfinder-style analyses.

### 2.3 Other Analysis fields
- `score` MAY be included to represent relevance/confidence; higher MUST be better.
- `support_graphs` MAY be included as references to AuxiliaryGraph ids; if present it MUST be non-empty.
- `scoring_method` MAY be used to identify/explain the score generation method.
- `attributes` MAY carry additional analysis-specific metadata.

## 3. Binding Object Definitions

### 3.1 `NodeBinding`
- MUST include:
  - `ids`: array of CURIEs
- `ids` MUST contain at least one item (`minItems: 1`).
- `ids` are CURIE identifiers of one or more Knowledge Graph nodes bound to the QNode key.
- Binding semantics are direct: each NodeBinding must bind to nodes relevant to that original Query Graph node.
- `query_id` from older formats is obsolete and SHOULD NOT be emitted.
- Legacy per-binding `attributes` are obsolete and SHOULD NOT be emitted.

### 3.2 `EdgeBinding`
- MUST include:
  - `ids`: array of KnowledgeGraph edge ids
- `ids` MUST contain at least one item (`minItems: 1`).
- `ids` are Knowledge Graph edge keys bound to a given QEdge key.
- Edge bindings are analysis-scoped, allowing different analyses/services to bind different edge sets.
- Legacy per-binding `attributes` are obsolete and SHOULD NOT be emitted.

### 3.3 `PathBinding`
- MUST include:
  - `ids`: array of AuxiliaryGraph ids
- `ids` MUST contain at least one item (`minItems: 1`).
- `ids` are AuxiliaryGraph keys representing one or more supporting paths for the referenced QPath.
- AuxiliaryGraph edge order is not guaranteed; path interpretation comes from graph connectivity, not edge list ordering.

## 4. Conformance Examples

### 4.1 Valid 2.0 result with edge bindings
```json
{
  "node_bindings": {
    "n0": { "ids": ["NCBIGene:1234"] },
    "n1": { "ids": ["MONDO:1234"] }
  },
  "analyses": [
    {
      "resource_id": "infores:retriever",
      "edge_bindings": {
        "e0": { "ids": ["edge-1234-1234-1234-1234"] }
      }
    }
  ]
}
```

### 4.2 Valid 2.0 result with path bindings
```json
{
  "node_bindings": {
    "n0": { "ids": ["CHEBI:4567"] },
    "n1": { "ids": ["MONDO:4567"] }
  },
  "analyses": [
    {
      "resource_id": "infores:aragorn-shepherd",
      "path_bindings": {
        "p0": { "ids": ["auxGraph-4567-4567-4567-4567"] }
      }
    }
  ]
}
```

## 5. Validation Checklist

- `Result.node_bindings` is a non-empty map.
- Every `NodeBinding` has non-empty `ids`.
- `Result.analyses` is non-empty when present.
- Every `Analysis` has `resource_id`.
- Every `Analysis` has `edge_bindings` or `path_bindings` (or both).
- `edge_bindings`/`path_bindings` values are binding objects, not arrays.
- Every `EdgeBinding`/`PathBinding` has non-empty `ids`.
