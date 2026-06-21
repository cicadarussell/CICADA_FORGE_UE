param(
    [switch]$OpenReport,
    [switch]$OpenDashboard
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"


function Invoke-CicadaStep {
    param(
        [Parameter(Mandatory=$true)][string]$ScriptPath,
        [string[]]$ExtraArgs = @(),
        [switch]$WithOpenReport,
        [switch]$WithOpenDashboard,
        [switch]$WithOpenStl
    )

    if (-not (Test-Path $ScriptPath)) { throw "Missing CICADA step script: $ScriptPath" }

    $CallArgs = @("-ExecutionPolicy", "Bypass", "-File", $ScriptPath)
    $CallArgs += $ExtraArgs
    if ($WithOpenReport) { $CallArgs += "-OpenReport" }
    if ($WithOpenDashboard) { $CallArgs += "-OpenDashboard" }
    if ($WithOpenStl) { $CallArgs += "-OpenStl" }

    Write-Host ""
    Write-Host "=== CICADA STEP ==="
    Write-Host $ScriptPath
    Write-Host ($CallArgs -join " ")
    Write-Host ""

    & powershell @CallArgs
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}


Write-Host "=== CICADA PHASE 003P FULL INTEGRATION CHECK ==="

Invoke-CicadaStep -ScriptPath "$Repo\scripts\diagnostics\cicada_full_project_audit.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\launcher\cicada_generate_command_center.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\env\cicada_env_doctor.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\env\cicada_cad_engine_launcher_doctor.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\cad\cicada_cad_generate_part_engine.ps1" -ExtraArgs @("-Part", "examples\cad_parts\robot_sensor_plate_v02.part.json") -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\slicer\cicada_slicer_readiness.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\slicer\cicada_slicer_dryrun_plan.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\diagnostics\cicada_health_report.ps1" -WithOpenReport:$OpenReport

$DashArgs = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "dashboard")
if ($OpenDashboard) { $DashArgs += "-OpenDashboard" }
& powershell @DashArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Invoke-CicadaStep -ScriptPath "$Repo\scripts\ledger\cicada_ledger_record.ps1" -ExtraArgs @("-Phase", "003P", "-Verdict", "PASS_OR_PARTIAL", "-Note", "Phase 003P full integration check executed; review release gate for exact status.", "-Source", "phase003P-full-check")
Invoke-CicadaStep -ScriptPath "$Repo\scripts\ledger\cicada_release_gate.ps1" -WithOpenReport:$OpenReport

$DashArgs2 = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "dashboard")
if ($OpenDashboard) { $DashArgs2 += "-OpenDashboard" }
& powershell @DashArgs2
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=== PHASE 003P FULL INTEGRATION CHECK COMPLETE ==="
Write-Host "Expected release-gate verdict: RC_READY or RC_PARTIAL. BLOCKED means real failure."
exit 0
