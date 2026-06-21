$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Venv = Join-Path $Repo ".cicada_envs\cadquery"
$Py = Join-Path $Venv "Scripts\python.exe"

Write-Host "=== CICADA CADQUERY INSTALL INTO VENV ==="
Write-Host "This is explicit and may use internet. Nothing machine-related will run."

if (-not (Test-Path $Py)) {
    Write-Host "Venv Python missing. Creating venv first..."
    powershell -ExecutionPolicy Bypass -File "$Repo\scripts\env\cicada_env_create_cadquery_venv.ps1"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

& $Py -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $Py -m pip install cadquery
exit $LASTEXITCODE
