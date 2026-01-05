# GitHub Setup Instructions

## Create GitHub Repository

1. **Go to GitHub:**
   - Visit https://github.com/new
   - Sign in to your account

2. **Create Repository:**
   - Repository name: `pdf-clearer` (or your preferred name)
   - Description: "PDF form clearing tools and state license application forms directory"
   - Visibility: Public or Private (your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

3. **Copy the repository URL:**
   - It will look like: `https://github.com/YOUR_USERNAME/pdf-clearer.git`

## Push to GitHub

Run these commands in your terminal (replace with your actual repository URL):

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Verify

- Go to your GitHub repository page
- You should see all your files
- The `index.html` file should be visible

## Next: Deploy to Vercel

See `QUICK_DEPLOY.md` or `DEPLOYMENT.md` for Vercel deployment instructions.

