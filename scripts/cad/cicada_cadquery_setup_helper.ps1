param(
    [switch]$InstallUser
)

Write-Host "=== CICADA CADQUERY SETUP HELPER ==="
Write-Host "This does not run automatically. It only installs if -InstallUser is explicitly supplied."
Write-Host ""

$Probe = Join-Path $env:TEMP "cicada_cadquery_probe.py"
@"
import importlib.util
import sys
print("Python:", sys.version)
print("CadQuery available:", importlib.util.find_spec("cadquery") is not None)
print("FreeCAD module available:", importlib.util.find_spec("FreeCAD") is not None)
"@ | Set-Content -Encoding UTF8 $Probe

py -3 $Probe

if (-not $InstallUser) {
    Write-Host ""
    Write-Host "No install requested."
    Write-Host "To attempt user-level CadQuery install:"
    Write-Host '  powershell -ExecutionPolicy Bypass -File "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE\scripts\cad\cicada_cadquery_setup_helper.ps1" -InstallUser'
    exit 0
}

Write-Host ""
Write-Host "Attempting user-level CadQuery install with pip. This needs internet and may take a while, because CAD kernels are not tiny houseplants."
py -3 -m pip install --user --upgrade pip
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

py -3 -m pip install --user cadquery
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "Rechecking..."
py -3 $Probe
