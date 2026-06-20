# PHASE CLUSTER 002G - LAST ACTION STATUS CARD

## Build type

Mainline.

## Goal

Mirror button-click state into the right status rail.

Phase 002F made the left rail admit button clicks happened. Phase 002G makes the status rail admit it too. Truly, software inches toward honesty.

## Scope

This phase adds:

- right-rail `Last Action` status display
- button click updates both left and right text
- Output Log safe stub logging remains
- ProjectID config warning fix

## Out of scope

Do not add:

- persistent selected-action save
- real project creation
- real graph opening
- real validation
- real export
- file writes
- CAD sidecar calls
- live camera calls
- machine commands

## Pass condition

Phase 002G passes when:

1. Unreal opens after rebuild.
2. UI shows:
   `Phase 002G: last action status card mirrors button clicks`
3. Right rail shows:
   `Last Action`
4. Clicking each button updates:
   - left selected-action text
   - right Last Action text
5. Output Log still writes:
   `CICADA Forge safe action stub clicked:`
6. ProjectID import warning is gone.

## Next phase after pass

Phase 002H:
Add an in-memory Forge event log panel listing the last few safe UI events.
