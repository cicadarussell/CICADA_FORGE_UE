# PHASE 003A SMOKE TEST

## Files expected

- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_003A_FEATURE_GRAPH_V0.md`
- [ ] `docs/checklists/PHASE_003A_SMOKE_TEST.md`

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 003A: feature graph V0 and backend inspector are alive`
- [ ] Centre workspace shows:
      `Feature Graph V0 Controls`
- [ ] Right rail shows:
      `Feature Graph Status`
- [ ] Click:
      `[graph] Add Box primitive`
- [ ] Click:
      `[graph] Add Cylinder primitive`
- [ ] Click:
      `[graph] Add Hole placeholder`
- [ ] Feature Graph V0 panel shows 3 operations.
- [ ] Click:
      `[graph] Run feature validation dry-run`
- [ ] Validation shows PASS.
- [ ] Click:
      `[graph] Save feature graph dry-run JSON`
- [ ] JSON appears under:
      `Saved/CICADAForge/FeatureGraphs`
- [ ] Click:
      `[graph] Reset feature graph`
- [ ] Feature Graph V0 panel clears operations.
- [ ] No CAD export occurs.
- [ ] No sidecar call occurs.
- [ ] No machine bridge action occurs.

## Verdict

- [ ] PASS - Feature Graph V0 works.
- [ ] PARTIAL - UI opens but one feature graph action fails.
- [ ] FAIL - project fails to open or compile.
