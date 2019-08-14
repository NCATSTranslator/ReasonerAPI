#!/bin/bash
STATS=$(
    diff API/TranslatorReasonersAPI.yaml API/TranslatorReasonersAPI_optional.yaml \
    | \
    diffstat
)
if grep -q "deletion" <<< "$STATS"; then
    exit 1
else
    exit 0
fi