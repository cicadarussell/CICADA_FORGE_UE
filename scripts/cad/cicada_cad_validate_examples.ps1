$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_cad_sidecar.py"

if (-not (Test-Path $Tool)) {
    throw "Missing CAD sidecar: $Tool"
}

py -3 $Tool validate-examples
