param([switch]$Regenerate)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Center = Join-Path $Repo "Saved\CICADAForge\CommandCenter\index.html"

if ($Regenerate -or -not (Test-Path $Center)) {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\launcher\cicada_generate_command_center.ps1" -OpenReport
    exit $LASTEXITCODE
}

Start-Process $Center
