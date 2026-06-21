# PHASE CLUSTER 002J - EVIDENCE RECEIPT COCKPIT

## Build type

Mainline.

## Goal

Bundle a larger UI-state cluster: memory-only evidence controls plus a receipt preview.

The Forge now has action buttons, selected-action state, session metadata, Last Action, and Event Log. Phase 002J adds the first memory-only evidence receipt cockpit, so proof/results have a visible place before we build persistence.

Because apparently even buttons need paperwork now. Annoying. Correct.

## Scope

This phase adds:

- `Evidence Receipt Controls` in the centre workspace
- `Evidence Receipt Preview` in the right status rail
- evidence buttons:
  - Screenshot observed
  - Output log checked
  - UI pass candidate
- system button:
  - Clear visible event log
- shared mutable UI state:
  - total safe event count
  - last action
  - last evidence marker
  - receipt readiness
- action buttons, evidence buttons, session metadata, last action, event log, and receipt preview all update from the same memory-only state

## Out of scope

Do not add:

- persistent receipt save
- real screenshot capture
- real project creation
- real graph opening
- real validation
- real export
- file writes
- CAD sidecar calls
- live camera calls
- machine commands

## Pass condition

Phase 002J passes when:

1. Unreal opens after rebuild.
2. UI shows:
   `Phase 002J: evidence receipt cockpit is alive`
3. Centre workspace shows:
   `Evidence Receipt Controls`
4. Right rail shows:
   `Evidence Receipt Preview`
5. Clicking evidence buttons updates:
   - Event Log
   - Session Metadata event count
   - Receipt Preview last evidence
   - Receipt Preview status
6. Clicking action buttons still updates:
   - selected action
   - Last Action
   - Event Log
   - Session Metadata
7. Clear visible event log clears visible history and records a system event.
8. Output Log still writes safe stub lines.
9. No file export, CAD call, sidecar call, or machine command occurs.

## Next phase after pass

Phase 002K:
Add the first local receipt save dry-run path, but still no machine/CAD sidecar. It should write only a small text/JSON receipt under `Saved/CICADAForge/Receipts` after explicit button click.
