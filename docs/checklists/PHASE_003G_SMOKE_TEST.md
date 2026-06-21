# PHASE 003G SMOKE TEST

## Repo audit

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003G_repo_audit.ps1"
```

## No-Unreal doctor

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command doctor
```

Expected:

- required files show exists true
- Python version is printed
- slicer discovery runs
- latest artifacts listed

## No-Unreal full check

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command full-check -OpenReport
```

Expected:

- job created
- STL created
- quality gate pass
- report created
- manifest check pass
- run report created/opened
- direct printer send false
- machine bridge locked

## Custom box

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command custom-box -Name "custom_plate" -Width 120 -Depth 50 -Height 6 -Material PETG -Infill 20 -OpenReport
```

Expected:

- custom STL
- custom manifest
- custom report
- safety locks remain

## Verdict

- [ ] PASS
- [ ] PARTIAL
- [ ] FAIL
