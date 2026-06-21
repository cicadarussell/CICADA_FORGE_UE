$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_stl_sidecar\cicada_box_stl_sidecar.py"

if (-not (Test-Path $Tool)) {
    throw "Missing STL sidecar: $Tool"
}

py -3 $Tool --width 80 --depth 40 --height 12
