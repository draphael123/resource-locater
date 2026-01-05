# Deployment Instructions

## Deploy to GitHub

1. **Create a GitHub repository:**
   - Go to https://github.com/new
   - Create a new repository (e.g., "pdf-clearer" or "state-license-forms")
   - Don't initialize with README (we already have one)

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit: PDF Clearer and State License Forms Directory"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## Deploy to Vercel

### Option 1: Deploy from GitHub (Recommended)

1. **Connect GitHub to Vercel:**
   - Go to https://vercel.com
   - Sign in with your GitHub account
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the settings

2. **Deploy:**
   - Click "Deploy"
   - Vercel will automatically deploy your site
   - You'll get a URL like: `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```
   - Follow the prompts
   - Login if needed
   - Deploy to production with `vercel --prod`

## What Gets Deployed

- `index.html` - The main website with embedded form data
- All Python scripts (for reference, not executed on Vercel)
- README and documentation

## Notes

- The website is a static site, so no server configuration needed
- All form data is embedded in the HTML, so no external API calls
- PDF files are excluded from deployment (see .gitignore)

