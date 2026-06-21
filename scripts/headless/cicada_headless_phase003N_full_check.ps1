param([switch]$OpenReport)

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


Invoke-CicadaStep -ScriptPath "$Repo\scripts\diagnostics\cicada_health_report.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\launcher\cicada_generate_command_center.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\headless\cicada_headless_phase003M_full_check.ps1" -WithOpenReport:$OpenReport
Invoke-CicadaStep -ScriptPath "$Repo\scripts\diagnostics\cicada_health_report.ps1" -WithOpenReport:$OpenReport

$DashArgs = @("-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1", "-Command", "dashboard")
if ($OpenReport) { $DashArgs += "-OpenDashboard" }
& powershell @DashArgs
exit $LASTEXITCODE
