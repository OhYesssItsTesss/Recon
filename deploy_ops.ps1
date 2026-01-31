# Deploy Ops - The "Easy Button" for Recon
# 1. Syncs Dev/Recon -> Public/recon
# 2. Pushes Public/recon to GitHub

$ErrorActionPreference = "Stop"
$originalDir = Get-Location
$repoRoot = "C:\Users\jparr\Documents\The_Ecosystem"

Write-Host "Starting Recon Deployment Sequence..." -ForegroundColor Cyan

# 1. Run the Sync Script
Write-Host "Syncing Files..." -ForegroundColor Yellow
& "$repoRoot\deploy_public.ps1"

# 2. Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Set-Location "$repoRoot\Public\recon"

if ((git status --porcelain) -eq $null) {
    Write-Host "  - No changes to commit." -ForegroundColor Gray
} else {
    git add .
    git commit -m "chore: Auto-deploy from Ops Script"
    git push
    Write-Host "  - Changes pushed successfully." -ForegroundColor Green
}

# 3. Return
Set-Location $originalDir
Write-Host "Deployment Complete." -ForegroundColor Green