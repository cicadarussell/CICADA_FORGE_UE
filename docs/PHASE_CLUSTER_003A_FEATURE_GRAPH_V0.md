# PHASE CLUSTER 003A - FEATURE GRAPH V0 DATA MODEL

## Build type

Mainline cumulative patch.

## Why this phase matters

The cockpit now shows evidence, receipts, diagnostics, and backend status. The next useful system is not a prettier UI.

The next useful system is a real internal design-intent model.

Phase 003A creates Feature Graph V0: a memory-only list of operations with validation and dry-run JSON save.

## Scope

This phase adds:

- `Feature Graph V0 Controls`
- `Feature Graph V0` status panel
- `Feature Graph Status` in right rail
- Add Box primitive
- Add Cylinder primitive
- Add Hole placeholder
- Run feature validation dry-run
- Save feature graph dry-run JSON
- Reset feature graph
- Feature op count in Backend Health
- Feature graph validity state
- Feature graph dry-run JSON under:
  `Saved/CICADAForge/FeatureGraphs`

## Strict boundaries

Allowed:

- UI updates
- memory state
- Output Log lines
- local dry-run JSON under project Saved folder

Not allowed:

- generated mesh preview
- STEP/STL export
- CAD sidecar calls
- machine commands
- automatic manufacturing actions

## Pass condition

Phase 003A passes when:

1. Unreal opens after rebuild.
2. UI shows:
   `Phase 003A: feature graph V0 and backend inspector are alive`
3. Feature Graph V0 Controls appear.
4. Add Box/Cylinder/Hole buttons add visible operations.
5. Validation passes when graph has one or more operations.
6. Reset clears operations.
7. Save feature graph dry-run JSON writes under:
   `Saved/CICADAForge/FeatureGraphs`
8. Backend Health updates op count and validation status.
9. No CAD export, sidecar call, or machine command occurs.

## Next phase after pass

Phase 003B:
Add a safer internal feature schema and basic operation IDs/types/parameters as a more formal model, preparing for visual nodes and CAD sidecar serialization.
