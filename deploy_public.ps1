$source = "Dev/Recon"
$dest = "Public/recon"

Write-Host "🚀 Deploying Recon to Public Staging..." -ForegroundColor Cyan

# Ensure dest exists
if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    Write-Host "Created $dest" -ForegroundColor Green
}

# Robocopy Mirror (Excluding .git, dist, build, private stuff)
robocopy $source $dest /MIR /XD .git __pycache__ dist build venv node_modules .next /XF .env .env.template *.spec

Write-Host "`n✅ Deployment Complete." -ForegroundColor Green
Write-Host "You can now go to '$dest' and push to your public GitHub."
