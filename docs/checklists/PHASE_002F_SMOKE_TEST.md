# PHASE 002F SMOKE TEST

## Files expected

- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeProjectState.cpp`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_002F_VISIBLE_SELECTED_ACTION_STATE.md`
- [ ] `docs/checklists/PHASE_002F_SMOKE_TEST.md`

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 002F: selected action state updates on screen`
- [ ] Left rail shows:
      `Selected action: none`
- [ ] Clicking `New design` changes visible text to include:
      `Selected action: New design - safe stub only`
- [ ] Clicking `Open feature graph` changes visible text to include:
      `Selected action: Open feature graph - safe stub only`
- [ ] Clicking `Run validation` changes visible text to include:
      `Selected action: Run validation - safe stub only`
- [ ] Clicking `Export proof receipt` changes visible text to include:
      `Selected action: Export proof receipt - safe stub only`
- [ ] Output Log still logs:
      `CICADA Forge safe action stub clicked:`
- [ ] No file export occurs.
- [ ] No CAD sidecar call occurs.
- [ ] No machine bridge action occurs.
- [ ] Non-normalized config path warning is gone or reduced.

## Verdict

- [ ] PASS - visible selected action updates safely.
- [ ] PARTIAL - UI opens but selected-action display/logging fails.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`
