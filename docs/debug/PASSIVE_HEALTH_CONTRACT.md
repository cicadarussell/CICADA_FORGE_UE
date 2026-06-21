# PASSIVE HEALTH CONTRACT

## Purpose

Avoid false failures when artifacts were not generated.

## Status meanings

| Status | Meaning |
|---|---|
| PASS | file/check exists and looks OK |
| NOT_RUN | artifact missing because user has not generated it yet |
| CHECK | ambiguous state |
| FAIL | required code/config missing or safety violation |

## Passive mode

Default mode. Missing generated artifacts are NOT_RUN.

## Strict mode

Generated artifacts can be treated as failures when required.


## Patch-folder testing note

When running against a patch folder instead of the full repo, missing base Unreal files may show as CHECK in passive mode rather than FAIL.

Use strict mode only when testing the real full repository.
