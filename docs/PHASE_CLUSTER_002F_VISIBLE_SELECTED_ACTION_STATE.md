# PHASE CLUSTER 002F - VISIBLE SELECTED ACTION STATE

## Build type

Mainline.

## Goal

Make button clicks visibly update the Forge UI, not just Output Log.

Phase 002E proved the buttons were alive. Phase 002F makes them talk back on screen. Revolutionary technology: a button that admits it was pressed.

## Scope

This phase adds:

- visible selected-action text below the left-rail buttons
- button click updates:
  `Selected action: <name> - safe stub only`
- Output Log safe stub logging remains
- config path normalization for `CICADAForgeState.ini`

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

Phase 002F passes when:

1. Unreal opens after rebuild.
2. `Window -> CICADA Forge` opens the Forge tab.
3. UI shows:
   `Phase 002F: selected action state updates on screen`
4. Left rail initially shows:
   `Selected action: none`
5. Clicking each button visibly changes selected-action text.
6. Output Log still writes:
   `CICADA Forge safe action stub clicked:`
7. Non-normalized config path warning is gone or reduced.

## Next phase after pass

Phase 002G:
Add a small right-rail `Last Action` card fed from the same selected-action state, preparing for a future event bus / UI state model.
