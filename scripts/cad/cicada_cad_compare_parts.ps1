param(
    [Parameter(Mandatory=$true)][string]$PartA,
    [Parameter(Mandatory=$true)][string]$PartB
)

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Tool = Join-Path $Repo "tools\cicada_cad_sidecar\cicada_part_compare.py"
$A = Join-Path $Repo $PartA
$B = Join-Path $Repo $PartB

if (-not (Test-Path $A)) { throw "Missing PartA: $A" }
if (-not (Test-Path $B)) { throw "Missing PartB: $B" }

py -3 $Tool $A $B
