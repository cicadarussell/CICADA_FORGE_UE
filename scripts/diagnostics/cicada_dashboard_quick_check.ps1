$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Dashboard = Join-Path $Repo "Saved\CICADAForge\Dashboard\index.html"
$Snapshot = Join-Path $Repo "Saved\CICADAForge\Dashboard\cicada_dashboard_snapshot.json"

Write-Host "=== CICADA DASHBOARD QUICK CHECK ==="

if (-not (Test-Path $Dashboard)) {
    Write-Host "Dashboard missing: $Dashboard"
    exit 1
}

if (-not (Test-Path $Snapshot)) {
    Write-Host "Dashboard snapshot missing: $Snapshot"
    exit 1
}

$Html = Get-Content $Dashboard -Raw
$Json = Get-Content $Snapshot -Raw | ConvertFrom-Json

if ($Html -notmatch "CICADA FORGE CONTROL ROOM") {
    Write-Host "FAIL: dashboard title marker missing."
    exit 1
}

if ($Html -notmatch "Machine bridge") {
    Write-Host "FAIL: machine bridge marker missing."
    exit 1
}

if ($Json.machine_bridge -ne "LOCKED") {
    Write-Host "FAIL: snapshot machine_bridge was not LOCKED."
    exit 1
}

Write-Host "PASS: dashboard exists and safety marker is present."
Write-Host "Dashboard: $Dashboard"
Write-Host "Snapshot: $Snapshot"
