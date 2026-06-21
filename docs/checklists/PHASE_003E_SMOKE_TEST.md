# PHASE 003E SMOKE TEST

## Repo audit

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003E_repo_audit.ps1"
```

## Open local editor

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\open_box_job_editor.ps1"
```

Expected:

- browser opens local editor
- changing width/depth/height updates JSON preview
- download job JSON works
- copied command references the job runner

## Create editable job from PowerShell

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\new_box_job.ps1" -Name "custom_test" -Width 60 -Depth 30 -Height 8 -Material PETG -Infill 25
```

Expected:

- job JSON appears under:
  `Saved/CICADAForge/BoxJobs`

## Create and run job

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\new_and_run_box_job.ps1" -Name "custom_test_run" -Width 60 -Depth 30 -Height 8 -Material PETG -Infill 25
```

Expected:

- STL appears under:
  `Saved/CICADAForge/STL`
- manifest appears under:
  `Saved/CICADAForge/PrintHandoff`
- receipt appears under:
  `Saved/CICADAForge/Receipts`
- direct printer send remains locked

## Summary

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_box_job_summary.ps1" -Job "Saved\CICADAForge\BoxJobs\custom_test_run.json"
```

## Verdict

- [ ] PASS
- [ ] PARTIAL
- [ ] FAIL
