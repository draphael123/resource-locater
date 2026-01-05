# PowerShell deployment script for GitHub and Vercel

Write-Host "🚀 PDF Clearer - Deployment Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if git remote exists
try {
    $remote = git remote get-url origin 2>$null
    Write-Host "✅ Git remote configured: $remote" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "❌ No GitHub remote configured yet." -ForegroundColor Red
    Write-Host ""
    Write-Host "📝 Steps to deploy:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Create a GitHub repository:" -ForegroundColor White
    Write-Host "   - Go to https://github.com/new" -ForegroundColor Gray
    Write-Host "   - Create a new repository" -ForegroundColor Gray
    Write-Host "   - Copy the repository URL" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Add the remote and push:" -ForegroundColor White
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Gray
    Write-Host "   git branch -M main" -ForegroundColor Gray
    Write-Host "   git push -u origin main" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Deploy to Vercel:" -ForegroundColor White
    Write-Host "   - Go to https://vercel.com" -ForegroundColor Gray
    Write-Host "   - Import your GitHub repository" -ForegroundColor Gray
    Write-Host "   - Click Deploy" -ForegroundColor Gray
    Write-Host ""
    exit
}

# Check current branch
$branch = git branch --show-current
Write-Host "Current branch: $branch" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to push
$response = Read-Host "Push to GitHub? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    git push origin $branch
    Write-Host ""
    Write-Host "✅ Pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Next step: Deploy to Vercel" -ForegroundColor Yellow
    Write-Host "   - Go to https://vercel.com" -ForegroundColor Gray
    Write-Host "   - Import your repository" -ForegroundColor Gray
    Write-Host "   - Or use: vercel --prod" -ForegroundColor Gray
}

