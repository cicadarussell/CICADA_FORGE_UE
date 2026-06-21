# PHASE 003D SMOKE TEST

## Repo checks

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_project_on_track_check.ps1"
```

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_validate_box_job_files.ps1"
```

## Generate one STL job

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\run_box_job.ps1" -Job "examples\box_jobs\test_block_20x20x10.json"
```

Expected:

- STL saved under `Saved/CICADAForge/STL`
- manifest saved under `Saved/CICADAForge/PrintHandoff`
- receipt saved under `Saved/CICADAForge/Receipts`
- direct printer send locked

## Generate all example jobs

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\run_all_box_jobs.ps1"
```

Expected:

- multiple STLs created
- multiple manifests created
- no G-code
- no serial/printer access

## Validate latest STL

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_validate_latest_stl.ps1"
```

Expected:

- 12 facets for simple box
- valid ASCII STL structure

## Unreal check

Expected text:

`Phase 003D: project tracker and box job runner are alive`

## Verdict

- [ ] PASS
- [ ] PARTIAL
- [ ] FAIL
