# Quick Deployment Guide

## Step 1: Push to GitHub

```bash
# If you haven't set up the remote yet:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**First, create the repository on GitHub:**
1. Go to https://github.com/new
2. Name it (e.g., "pdf-clearer" or "state-license-forms")
3. Don't initialize with README
4. Copy the repository URL

## Step 2: Deploy to Vercel

### Easy Method (GitHub Integration):

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New Project"
4. Select your repository
5. Click "Deploy"
6. Done! Your site will be live at `https://your-project.vercel.app`

### CLI Method:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# For production
vercel --prod
```

## What's Included

✅ `index.html` - Complete website with all form links
✅ All Python scripts for PDF processing
✅ Documentation and deployment configs
❌ PDF files excluded (too large, not needed for website)

## Your Live Site

Once deployed, your website will be accessible at:
- `https://your-project.vercel.app`
- Or a custom domain if you configure one

The website includes:
- 31 state license application forms
- Search and filter functionality
- Direct links to state board websites
- Search results with form download links

