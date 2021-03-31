# Translator Reasoner API Policies

This document described development and release policies for the Translator Reasoner API.

## Stable branches
- The repository has two "stable" branches, `master` and `extended`
- The `master` branch contains the latest stable version of the core API schema
- The `extended` branch contains the latest stable extended API schema, a definition of additional properties that are used and promoted by at least one team

## In-development branches
- The repository may contain a number of branches for pre-release versions, e.g. `v1.1.x`

## Version numbering
- Each merge into master must include a version bump
- The `extended` branch shall maintain the same version number as `master`
