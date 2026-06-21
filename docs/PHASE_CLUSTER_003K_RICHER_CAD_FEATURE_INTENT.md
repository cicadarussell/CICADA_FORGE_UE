# PHASE CLUSTER 003K - RICHER CAD FEATURE INTENT

## Build type

Mainline cumulative patch.

## Why this phase exists

Phase 003I/003J created the CAD sidecar and builder path. Phase 003K makes the CAD intent more useful for robot parts.

## Added

- V0.2 CAD feature intent:
  - holes
  - slots
  - standoffs
- V0.2 schema:
  `tools/cicada_cad_sidecar/schemas/cicada_part_schema_v0_2.json`
- sidecar validation/reporting for:
  - slot extents
  - standoff dimensions
  - pilot hole constraints
  - estimated removed/added volume
- richer SVG previews for:
  - holes
  - slots
  - standoffs
- new builders:
  - sensor plate
  - slotted motor mount
- sample pack:
  - mounting plate
  - robot plate
  - sensor plate
  - slotted motor mount
- part comparison tool:
  `tools/cicada_cad_sidecar/cicada_part_compare.py`
- dashboard command cards
- installer now preserves `Saved` by default

## Truth boundary

CadQuery is still optional.

If CadQuery is missing, STEP remains blocked honestly.

That is correct.
