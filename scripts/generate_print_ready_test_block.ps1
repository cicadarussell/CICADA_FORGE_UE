$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_stl_sidecar\cicada_parametric_box_stl.py"

if (-not (Test-Path $Tool)) {
    throw "Missing STL sidecar: $Tool"
}

py -3 $Tool --width 20 --depth 20 --height 10
