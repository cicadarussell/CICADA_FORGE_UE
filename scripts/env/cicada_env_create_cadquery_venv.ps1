$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Venv = Join-Path $Repo ".cicada_envs\cadquery"

Write-Host "=== CICADA CADQUERY VENV CREATE ==="
Write-Host "Venv: $Venv"

if (Test-Path $Venv) {
    Write-Host "Venv already exists."
    exit 0
}

py -3 -m venv $Venv
exit $LASTEXITCODE
