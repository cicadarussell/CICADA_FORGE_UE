# PHASE 003C SMOKE TEST

## Unreal test

- [ ] Forge tab opens.
- [ ] UI shows:
      `Phase 003C: print-ready STL handoff workflow is alive`
- [ ] Centre workspace shows:
      `Print-Ready Sketch Box Workflow`
- [ ] Click:
      `[preset] 20 x 20 x 10 mm test block`
- [ ] Click:
      `[check] Validate sketch + printer fit`
- [ ] Click:
      `[export] Generate STL`
- [ ] Click:
      `[printer] Save manual print handoff manifest`
- [ ] Click:
      `[slicer] Open latest STL in default app`
- [ ] STL opens in associated slicer/viewer if Windows has one.
- [ ] STL appears under:
      `Saved/CICADAForge/STL`
- [ ] Manifest appears under:
      `Saved/CICADAForge/PrintHandoff`
- [ ] No G-code streaming occurs.
- [ ] No serial command occurs.
- [ ] No direct printer send occurs.

## Script tests

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_find_slicers.ps1"
```

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\open_latest_stl_in_default_app.ps1"
```

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_validate_latest_stl.ps1"
```

## Verdict

- [ ] PASS - print-ready STL handoff works.
- [ ] PARTIAL - STL exports but default app or manifest fails.
- [ ] FAIL - project fails to open or compile.
