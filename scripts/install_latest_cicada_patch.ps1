param(
    [Parameter(Mandatory=$true)]
    [string]$Repo,

    [Parameter(Mandatory=$true)]
    [string]$ZipFilter
)

$Downloads = Join-Path $env:USERPROFILE "Downloads"

$Zip = Get-ChildItem $Downloads -Filter $ZipFilter |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "Could not find patch ZIP in Downloads matching: $ZipFilter"
}

if (-not (Test-Path $Repo)) {
    throw "Repo path does not exist: $Repo"
}

$Temp = Join-Path $env:TEMP ("cicada_patch_" + [guid]::NewGuid().ToString())

Write-Host "=== CICADA PATCH INSTALLER ==="
Write-Host "ZIP:  $($Zip.FullName)"
Write-Host "Repo: $Repo"
Write-Host "Temp: $Temp"

New-Item -ItemType Directory -Path $Temp -Force | Out-Null
Expand-Archive -Path $Zip.FullName -DestinationPath $Temp -Force

robocopy $Temp $Repo /E /NFL /NDL /NJH /NJS /NP
$RoboCode = $LASTEXITCODE

if ($RoboCode -gt 7) {
    throw "Robocopy failed with code $RoboCode"
}

Remove-Item -LiteralPath $Temp -Recurse -Force

Write-Host "Patch installed into repo."
Write-Host "Review in GitHub Desktop, commit, then push."
