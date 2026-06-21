$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"
$Saved = Join-Path $Repo "Saved\CICADAForge"

Write-Host "=== CICADA SAVED ARTIFACT INVENTORY ==="
Write-Host "Repo: $Repo"
Write-Host ""

$paths = @(
    "BoxJobs",
    "STL",
    "Reports",
    "RunReports",
    "PrintHandoff",
    "Receipts",
    "FeatureGraphs"
)

foreach ($folder in $paths) {
    $full = Join-Path $Saved $folder
    Write-Host "[$folder]"
    if (Test-Path $full) {
        Get-ChildItem $full -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 10 |
            ForEach-Object {
                Write-Host ("  {0}  {1} bytes  {2}" -f $_.LastWriteTime, $_.Length, $_.FullName)
            }
    } else {
        Write-Host "  Not created yet."
    }
    Write-Host ""
}
