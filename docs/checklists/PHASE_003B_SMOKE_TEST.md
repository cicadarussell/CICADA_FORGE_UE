# PHASE 003B SMOKE TEST

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 003B: sketch box to STL export pipeline is alive`
- [ ] Centre workspace shows:
      `Sketch Box -> STL Controls`
- [ ] Click:
      `[sketch] Create rectangle 80 x 40 mm`
- [ ] Click:
      `[feature] Extrude sketch 12 mm`
- [ ] Click:
      `[check] Validate sketch box`
- [ ] Click:
      `[export] Generate box STL`
- [ ] STL appears under:
      `Saved/CICADAForge/STL`
- [ ] Click:
      `[printer] Prepare locked print handoff manifest`
- [ ] Manifest appears under:
      `Saved/CICADAForge/PrintHandoff`
- [ ] Click:
      `[folder] Open STL output folder`
- [ ] Folder opens.
- [ ] No direct printer command occurs.
- [ ] No G-code streaming occurs.
- [ ] No serial command occurs.

## Script tests

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_saved_artifact_inventory.ps1"
```

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_validate_latest_stl.ps1"
```

## Verdict

- [ ] PASS - STL export and locked print handoff work.
- [ ] PARTIAL - UI opens but STL or manifest fails.
- [ ] FAIL - project fails to open or compile.
