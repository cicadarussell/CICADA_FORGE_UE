param(
    [string]$Name = "custom_box",
    [double]$Width = 80,
    [double]$Depth = 40,
    [double]$Height = 12,
    [string]$Material = "PLA",
    [int]$Infill = 15,
    [switch]$OpenReport
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Args = @(
    "-ExecutionPolicy", "Bypass", "-File", "$Repo\scripts\cicada_forge.ps1",
    "-Command", "custom-box",
    "-Name", $Name,
    "-Width", "$Width",
    "-Depth", "$Depth",
    "-Height", "$Height",
    "-Material", $Material,
    "-Infill", "$Infill"
)
if ($OpenReport) { $Args += "-OpenReport" }
& powershell @Args
exit $LASTEXITCODE
