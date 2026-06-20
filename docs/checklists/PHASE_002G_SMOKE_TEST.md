# PHASE 002G SMOKE TEST

## Files expected

- [ ] `Config/DefaultGame.ini`
- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_002G_LAST_ACTION_STATUS_CARD.md`
- [ ] `docs/checklists/PHASE_002G_SMOKE_TEST.md`

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 002G: last action status card mirrors button clicks`
- [ ] Left rail shows:
      `Selected action: none`
- [ ] Right rail shows:
      `Last Action`
      `Last Action: none`
- [ ] Clicking each button updates the left selected-action text.
- [ ] Clicking each button updates the right Last Action text.
- [ ] Output Log still logs:
      `CICADA Forge safe action stub clicked:`
- [ ] No file export occurs.
- [ ] No CAD sidecar call occurs.
- [ ] No machine bridge action occurs.
- [ ] `ProjectID import failed` warning is gone.

## Verdict

- [ ] PASS - Last Action card mirrors clicks safely.
- [ ] PARTIAL - UI opens but Last Action mirror/logging fails.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`
