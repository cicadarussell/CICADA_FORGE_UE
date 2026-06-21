param([switch]$OpenReport)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

function Invoke-CicadaStep {
    param(
        [Parameter(Mandatory=$true)][string]$ScriptPath,
        [string[]]$ExtraArgs = @(),
        [switch]$WithOpenReport,
        [switch]$WithOpenDashboard
    )

    if (-not (Test-Path $ScriptPath)) {
        throw "Missing CICADA step script: $ScriptPath"
    }

    $CallArgs = @("-ExecutionPolicy", "Bypass", "-File", $ScriptPath)
    $CallArgs += $ExtraArgs

    if ($WithOpenReport) {
        $CallArgs += "-OpenReport"
    }

    if ($WithOpenDashboard) {
        $CallArgs += "-OpenDashboard"
    }

    Write-Host ""
    Write-Host "=== CICADA STEP ==="
    Write-Host $ScriptPath
    Write-Host ($CallArgs -join " ")
    Write-Host ""

    & powershell @CallArgs
    if ($LASTEXITCODE -ne 0) {
        Write-Host "CICADA STEP FAILED: $ScriptPath"
        exit $LASTEXITCODE
    }
}

Write-Host "=== CICADA PHASE 003O1 CLEAN FULL CHECK ==="
Write-Host "Nested switch forwarding fixed by passing switch names only when present."
Write-Host ""

Invoke-CicadaStep -ScriptPath "$Repo\scripts\diagnostics\cicada_health_report.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\launcher\cicada_generate_command_center.ps1" -WithOpenReport:$OpenReport

Invoke-CicadaStep -ScriptPath "$Repo\scripts\env\cicada_env_doctor.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\env\cicada_cad_engine_launcher_doctor.ps1" -WithOpenReport:$OpenReport

Invoke-CicadaStep -ScriptPath "$Repo\scripts\cad\cicada_cad_generate_part_engine.ps1" -ExtraArgs @("-Part", "examples\cad_parts\robot_sensor_plate_v02.part.json") -WithOpenReport:$OpenReport

Invoke-CicadaStep -ScriptPath "$Repo\scripts\slicer\cicada_slicer_readiness.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\slicer\cicada_slicer_dryrun_plan.ps1" -WithOpenReport:$OpenReport

Invoke-CicadaStep -ScriptPath "$Repo\scripts\diagnostics\cicada_health_report.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\ledger\cicada_ledger_record.ps1" -ExtraArgs @("-Phase", "003O1", "-Verdict", "PASS_OR_PARTIAL", "-Note", "Phase 003O1 cleanup full check executed; review release gate for exact status.", "-Source", "phase003O1-cleanup-full-check")
Invoke-CicadaStep -ScriptPath "$Repo\scripts\ledger\cicada_release_gate.ps1" -WithOpenReport:$OpenReport

# Dashboard supports -OpenDashboard, not -OpenReport. Use the master wrapper only for this safe non-nested command.
$DashboardArgs = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "dashboard")
if ($OpenReport) {
    $DashboardArgs += "-OpenDashboard"
}
& powershell @DashboardArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=== PHASE 003O1 CLEAN FULL CHECK COMPLETE ==="
Write-Host "Expected release-gate verdict: RC_READY or RC_PARTIAL. BLOCKED means real failure."
exit 0
