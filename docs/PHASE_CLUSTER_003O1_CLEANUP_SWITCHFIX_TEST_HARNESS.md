# PHASE CLUSTER 003O1 - CLEANUP SWITCH FIX AND TEST HARNESS

## Build type

Cleanup patch over Phase 003O.

## Why this exists

The Phase 003O install audit passed and release-gate worked, but `phase003O-full-check -OpenReport` failed because nested PowerShell scripts passed switch values as strings.

Bad pattern:

```powershell
-OpenReport:$OpenReport
```

Safe pattern:

```powershell
$args = @("-ExecutionPolicy", "Bypass", "-File", $ScriptPath)
if ($OpenReport) { $args += "-OpenReport" }
powershell @args
```

Phase 003O1 replaces the 003O full-check orchestration with safe array-based switch forwarding.

## Also added

- `.gitignore` entries for local/generated outputs:
  - `.cicada_envs/`
  - `Saved/CICADAForge/`
  - Unreal `Binaries/Intermediate`
- cleanup audit script:
  `scripts/phase003O1_cleanup_audit.ps1`

## Main command

```powershell
powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cicada_forge.ps1" -Command phase003O-full-check -OpenReport
```

## Expected verdict

- `RC_READY` if all useful artifacts exist.
- `RC_PARTIAL` if code is fine but dashboard/STL/manifest/etc. have not been generated.
- `BLOCKED` only for real failure or safety issue.
