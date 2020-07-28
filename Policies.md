# NCATS Translator API Policies

This document described development and release policies for the NCATS Translator API

## Repository branches
- The repository has two primary branches, `master` and `extended`
- The `master` branch contains the current core API schema, both in-development changes and tagged releases
- The `extended` branch contains the current extended API schema, a definition of additional properties that are used and promoted by at least one team

## Version Numbering
- After a tagged release, the very next commit to the `master` branch will receive an increment to the next minor version number with '-dev' appended
  (e.g. 0.9.3-dev)
- In the process of tagging a release, the version number shall be incremented again to the next minor version number or major version numbers as appropriate,
  with no suffix (e.g. 0.9.4 or 1.0.0)
- The `extended` branch shall maintain the same version number as the core


