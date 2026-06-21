param(
    [switch]$Open
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_stl_sidecar\cicada_stl_analyzer.py"

if (-not (Test-Path $Tool)) {
    throw "Missing STL analyzer: $Tool"
}

$args = @($Tool, "--report")
if ($Open) {
    $args += "--open-report"
}

py -3 @args
