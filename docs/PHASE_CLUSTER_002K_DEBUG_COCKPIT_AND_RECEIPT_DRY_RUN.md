# PHASE CLUSTER 002K - DEBUG COCKPIT AND RECEIPT DRY-RUN

## Build type

Mainline cumulative patch.

## Why this phase is larger

The user asked for larger, more focused phase clusters and more debugging tools.

This phase is therefore bigger than the earlier tiny increments, but still stays inside strict safety bounds.

## Goal

Turn the Phase 002 UI shell into a real debug/evidence cockpit:

- safe action stubs
- evidence markers
- diagnostics
- event log
- session metadata
- receipt preview
- explicit local dry-run receipt save

This starts moving from "UI exists" to "UI produces proof."

## Scope

This phase adds:

- right-rail `Diagnostics` panel
- debug buttons:
  - Run UI state self-check
  - Classify known log noise
- explicit local dry-run receipt save:
  - writes JSON text under `Saved/CICADAForge/Receipts`
  - updates receipt preview with path
  - increments receipt count
- receipt preview:
  - session ID
  - event count
  - last action
  - last evidence
  - last receipt path
- event log keeps latest eight entries
- PowerShell log quickscan tool

## Strict boundaries

Allowed:

- UI updates
- Output Log lines
- local JSON receipt under project `Saved`
- PowerShell log scan script

Not allowed:

- CAD export
- sidecar calls
- machine commands
- automated screenshot capture
- arbitrary file writing outside project `Saved/CICADAForge/Receipts`
- destructive actions

## Pass condition

Phase 002K passes when:

1. Unreal opens after rebuild.
2. UI shows:
   `Phase 002K: debug cockpit and receipt dry-run are alive`
3. Centre workspace shows:
   `Evidence + Debug Controls`
4. Right rail shows:
   - Session Metadata
   - Last Action
   - Event Log
   - Evidence Receipt Preview
   - Diagnostics
5. Action buttons update selected action / Last Action / Event Log.
6. Evidence buttons update receipt preview.
7. Debug buttons update Diagnostics.
8. Save local dry-run receipt writes one JSON file under:
   `Saved/CICADAForge/Receipts`
9. Output Log shows CICADA safe stub lines.
10. No CAD export, sidecar call, or machine command occurs.

## Next phase after pass

Phase 003A:
Begin the Feature Graph V0 data model, likely not yet visual nodes. Add a small internal feature graph state with safe primitive operation cards and validation status.
