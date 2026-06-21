# PHASE 003F SMOKE TEST

## Repo audit

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\phase003F_repo_audit.ps1"
```

## One-shot generate/analyze/report

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\new_run_analyze_box_job.ps1" -Name "demo_box" -Width 80 -Depth 40 -Height 12 -OpenReport
```

Expected:

- job JSON saved
- STL saved
- print manifest saved
- receipt saved
- STL quality gate passes
- report JSON saved
- report HTML saved/opened
- direct printer send locked

## Analyze existing latest STL

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_analyze_latest_stl.ps1"
```

## Generate report only

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_generate_latest_stl_report.ps1" -Open
```

## Quality gate only

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\diagnostics\cicada_stl_quality_gate.ps1"
```

## Expected stats for simple box

- triangle count: 12
- boundary edges: 0
- non-manifold edges: 0
- quality pass: true

## Verdict

- [ ] PASS
- [ ] PARTIAL
- [ ] FAIL
