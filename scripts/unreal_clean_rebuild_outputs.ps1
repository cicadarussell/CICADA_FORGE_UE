Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

$Repo = "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE UNREAL STALE-BINARY CLEAN ==="

Remove-Item "$Repo\Binaries" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$Repo\Intermediate" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$Repo\Saved" -Recurse -Force -ErrorAction SilentlyContinue

Remove-Item "$Repo\Plugins\CICADAForge\Binaries" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$Repo\Plugins\CICADAForge\Intermediate" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Cleaned root/plugin Binaries, Intermediate, and Saved."
Write-Host "Reopen CICADA_FORGE_UE.uproject and allow one rebuild."
