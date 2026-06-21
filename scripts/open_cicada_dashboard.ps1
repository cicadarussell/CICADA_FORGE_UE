param(
    [switch]$Regenerate
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

if ($Regenerate) {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard
    exit $LASTEXITCODE
}

$Dashboard = Join-Path $Repo "Saved\CICADAForge\Dashboard\index.html"

if (-not (Test-Path $Dashboard)) {
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\cicada_forge.ps1" -Command dashboard -OpenDashboard
    exit $LASTEXITCODE
}

Start-Process $Dashboard
