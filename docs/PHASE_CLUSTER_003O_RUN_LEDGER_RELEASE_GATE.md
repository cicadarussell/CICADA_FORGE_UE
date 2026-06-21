# PHASE CLUSTER 003O - RUN LEDGER AND RELEASE CANDIDATE GATE

## Build type
Mainline cumulative patch.

## Why this phase exists
The project now has checks, reports, command pages, and generated artifacts. Phase 003O adds the operating spine:

- record what actually ran
- snapshot latest useful state
- gate whether the repo is RC_READY, RC_PARTIAL, or BLOCKED
- separate "not generated yet" from "actually broken"

## Added
- `tools/cicada_ledger/cicada_run_ledger.py`
- `scripts/ledger/cicada_ledger_record.ps1`
- `scripts/ledger/cicada_ledger_latest.ps1`
- `scripts/ledger/cicada_release_gate.ps1`
- `scripts/headless/cicada_headless_phase003O_full_check.ps1`
- wrapper commands: `ledger-record`, `ledger-latest`, `release-gate`, `phase003O-full-check`

## Verdict meanings
- RC_READY: all required checks/artifacts passed
- RC_PARTIAL: code checks passed, some artifacts not generated yet
- BLOCKED: actual failure or safety issue
