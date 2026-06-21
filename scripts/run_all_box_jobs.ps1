$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_stl_sidecar\cicada_box_job_runner.py"
$Jobs = Join-Path $Repo "examples\box_jobs"

if (-not (Test-Path $Tool)) {
    throw "Missing job runner: $Tool"
}

if (-not (Test-Path $Jobs)) {
    throw "Missing jobs folder: $Jobs"
}

Get-ChildItem $Jobs -Filter "*.json" | Sort-Object Name | ForEach-Object {
    Write-Host ""
    Write-Host "=== Running box job: $($_.Name) ==="
    py -3 $Tool run $_.FullName
}
