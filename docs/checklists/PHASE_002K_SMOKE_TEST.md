# PHASE 002K SMOKE TEST

## Files expected

- [ ] `Config/CICADAForgeState.ini`
- [ ] `Plugins/CICADAForge/Source/CICADAForgeEditor/Private/CICADAForgeEditorModule.cpp`
- [ ] `docs/PHASE_CLUSTER_002K_DEBUG_COCKPIT_AND_RECEIPT_DRY_RUN.md`
- [ ] `docs/checklists/PHASE_002K_SMOKE_TEST.md`
- [ ] `scripts/diagnostics/cicada_unreal_log_quickscan.ps1`

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 002K: debug cockpit and receipt dry-run are alive`
- [ ] Centre workspace shows:
      `Evidence + Debug Controls`
- [ ] Right rail shows:
      `Diagnostics`
      `Evidence Receipt Preview`
- [ ] Clicking action buttons updates selected action and Last Action.
- [ ] Clicking evidence buttons updates Receipt Preview.
- [ ] Clicking `Run UI state self-check` updates Diagnostics.
- [ ] Clicking `Classify known log noise` updates Diagnostics.
- [ ] Clicking `Save local dry-run receipt` writes a JSON receipt under:
      `Saved/CICADAForge/Receipts`
- [ ] Receipt Preview shows the receipt path.
- [ ] Output Log still logs safe action/evidence/debug/receipt lines.
- [ ] No CAD export occurs.
- [ ] No sidecar call occurs.
- [ ] No machine bridge action occurs.

## PowerShell log quickscan

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_unreal_log_quickscan.ps1"
```

Expected useful output:

- build success/fail count
- CICADA Forge lines
- errors
- warnings
- known non-blocking noise count

## Verdict

- [ ] PASS - Debug cockpit and dry-run receipt work.
- [ ] PARTIAL - UI opens but receipt/diagnostics fail.
- [ ] FAIL - project fails to open or compile.

## Evidence

Record result in:

`docs/evidence/EVIDENCE_LOG.md`
