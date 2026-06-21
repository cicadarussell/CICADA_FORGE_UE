# PHASE CLUSTER 002I - SESSION METADATA PANEL

## Build type

Mainline.

## Goal

Add a right-rail Session Metadata panel.

The Forge tab now has action buttons, selected-action state, Last Action, and an Event Log. Phase 002I adds a local session identity so future saved sessions have somewhere sensible to attach evidence, events, approvals, and project state.

Tiny passport for the baby cockpit. Bureaucracy, but useful.

## Scope

This phase adds:

- session ID generated when the Forge tab opens
- session start time
- safe UI event count
- last action
- right-rail `Session Metadata` panel
- memory-only state

## Out of scope

Do not add:

- persistent session save
- real project creation
- real graph opening
- real validation
- real export
- file writes
- CAD sidecar calls
- live camera calls
- machine commands

## Pass condition

Phase 002I passes when:

1. Unreal opens after rebuild.
2. UI shows:
   `Phase 002I: session metadata panel tracks the local Forge run`
3. Right rail shows:
   `Session Metadata`
4. Session Metadata includes:
   - `Session ID`
   - `Started`
   - `Safe UI events`
   - `Last action`
   - `Persistence: memory only`
5. Clicking buttons increments event count.
6. Clicking buttons updates last action.
7. Event Log still updates.
8. Output Log still writes:
   `CICADA Forge safe action stub clicked:`

## Next phase after pass

Phase 002J:
Add manual evidence note stub panel preparing for future screenshot/log receipt save.
