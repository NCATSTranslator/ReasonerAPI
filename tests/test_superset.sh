#!/bin/bash
DIFF=$(diff API/TranslatorReasonersAPI.yaml API/TranslatorReasonersAPI_optional.yaml)
STATS=$(diffstat <<< "$DIFF")
if echo "$STATS" | grep -q "deletion"; then
    >&2 echo 'Some lines from API/TranslatorReasonersAPI.yaml do not exist in API/TranslatorReasonersAPI_optional.yaml:'
    DELS=$(echo "$DIFF" | grep -E '^<' | sed -E 's/^<//')
    >&2 echo "$DELS"
    exit 1
else
    exit 0
fi