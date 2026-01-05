#!/bin/bash
# Deployment script for GitHub and Vercel

echo "🚀 PDF Clearer - Deployment Script"
echo "===================================="
echo ""

# Check if git remote exists
if ! git remote get-url origin &> /dev/null; then
    echo "❌ No GitHub remote configured yet."
    echo ""
    echo "📝 Steps to deploy:"
    echo ""
    echo "1. Create a GitHub repository:"
    echo "   - Go to https://github.com/new"
    echo "   - Create a new repository"
    echo "   - Copy the repository URL"
    echo ""
    echo "2. Add the remote and push:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "3. Deploy to Vercel:"
    echo "   - Go to https://vercel.com"
    echo "   - Import your GitHub repository"
    echo "   - Click Deploy"
    echo ""
    exit 1
fi

echo "✅ Git remote configured"
echo ""

# Check current branch
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
echo ""

# Ask if user wants to push
read -p "Push to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin $BRANCH
    echo ""
    echo "✅ Pushed to GitHub!"
    echo ""
    echo "🌐 Next step: Deploy to Vercel"
    echo "   - Go to https://vercel.com"
    echo "   - Import your repository"
    echo "   - Or use: vercel --prod"
fi

