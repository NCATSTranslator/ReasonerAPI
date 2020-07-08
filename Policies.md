NCATS Translator API Policies

[![NCATS-ReasonerStdAPI build status on Travis CI](https://travis-ci.com/NCATS-Tangerine/NCATS-ReasonerStdAPI.svg?branch=master)](https://travis-ci.com/NCATS-Tangerine/NCATS-ReasonerStdAPI)

This document described development and release policies for the NCATS Translator API

## Version Numbering
- The `master` branch contains the current release version, with an embedded version number that is an even final number (e.g. 0.9.2)
- The `development` branch contains changes in progress, with an embedded version number that is the next odd number over release with 'dev' appended
  (e.g. 0.9.3dev) (unless it is synchronized with `master`)
- The `extended` branch contains additional properties that are used and promoted by at least one team, with an embedded version number that is the 
  next odd number over release with 'ext' appended. (e.g. 0.9.3ext), unless `development` is synchronized with `master`, 
  in which case it is the release version with 'ext' appended. (e.g. 0.9.2ext).




