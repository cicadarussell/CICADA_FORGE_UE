Set-Location "C:\CICADA\CICADA_APPS\CICADA_FORGE_UE"

Write-Host "=== CICADA FORGE SAFE SYNC V0.2 ==="

Write-Host "Step 1: local status..."
git status --short

$changes = git status --porcelain

if (-not [string]::IsNullOrWhiteSpace($changes)) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    Write-Host "Local changes found. Saving checkpoint first..."
    git add .
    git commit -m "Checkpoint: CICADA FORGE safe sync $timestamp"
} else {
    Write-Host "No local changes to checkpoint."
}

Write-Host "Step 2: checking GitHub..."
git fetch origin

Write-Host "Step 3: downloading latest safely..."
git pull --rebase origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "Pull/rebase failed. Stopping before push."
    exit 1
}

Write-Host "Step 4: uploading to GitHub..."
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "Push failed. Check GitHub account permissions."
    exit 1
}

Write-Host "=== SYNC COMPLETE ==="
git status
