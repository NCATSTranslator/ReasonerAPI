# NCATS Translator Reasoners API
This API specification represents a version 0.8.0 draft of the NCATS Translator Reasoners API.
It is intended that the various reasoner tools will support this API so that remote calls to
any of the reasoners may be made using the same API with the same result format, which will
facilitate comparison among reasoners and chaining of queries to different reasoners to
achieve an aggregated result.

## Previous versions
- Previous versions of the draft standard may be found at https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI/tree/master/API
- Early Google-doc based discussion may be found at https://drive.google.com/drive/folders/1kTIW6W7sLdSAhH9qBBeSAEZ4ouAViI4x
- Emerging KG Standard: https://docs.google.com/document/d/1TrvqJPe_HwmRJ5HCwZ7fsi9_mwGcwLOZ53Fnjo8Sh4E/edit#

## Notes
- The target output is intended to be JSON-LD

# Specification

## Top level (Response)

- context - URI - URL of the JSON-LD context file of this document. An actual context file remains yet been developed.
- id - URI - URI of this Reasoning Tools response if it is persisted somewhere.
- type - text - Type definition of this response object.
- schema_version - text - The API standard will likely evolve over time. This encodes the schema version used in this response.
