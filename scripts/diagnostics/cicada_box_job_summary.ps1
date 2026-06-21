param(
    [string]$Job = "examples\box_jobs\test_block_20x20x10.json"
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_stl_sidecar\cicada_box_job_runner.py"
$JobPath = Join-Path $Repo $Job

if (-not (Test-Path $Tool)) {
    throw "Missing job runner: $Tool"
}

if (-not (Test-Path $JobPath)) {
    throw "Missing job: $JobPath"
}

py -3 $Tool summary $JobPath
