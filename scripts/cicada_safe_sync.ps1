Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE SAFE SYNC ==="

Write-Host "Step 1: checking GitHub..."
git fetch origin

Write-Host "Step 2: downloading latest..."
git pull --rebase origin main

$changes = git status --porcelain

if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "No local changes. Repo is clean."
    git status
    exit 0
}

Write-Host "Step 3: local changes found:"
git status --short

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "Step 4: saving checkpoint..."
git add .
git commit -m "Checkpoint: CICADA FORGE safe sync $timestamp"

Write-Host "Step 5: uploading to GitHub..."
git push origin main

Write-Host "=== SYNC COMPLETE ==="
git status