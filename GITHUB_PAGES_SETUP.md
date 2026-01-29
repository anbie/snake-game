# GitHub Pages Setup Guide

This guide will help you set up GitHub Pages for your Snake Game project to host the documentation website.

## 🚀 Quick Setup

### Step 1: Push the New Files to GitHub

First, commit and push the new files to your repository:

```bash
git add index.html .github/workflows/deploy.yml GITHUB_PAGES_SETUP.md
git commit -m "Add GitHub Pages website and automated deployment"
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/anbie/snake-game
2. Click on **Settings** (top menu)
3. In the left sidebar, click on **Pages** (under "Code and automation")
4. Under **Source**, select:
   - Source: **GitHub Actions** (recommended for automated deployment)
   - OR if you prefer manual deployment: **Deploy from a branch** → **main** → **/ (root)**

### Step 3: Wait for Deployment

- If you selected **GitHub Actions**: The deployment will start automatically. Check the **Actions** tab to see the progress.
- The first deployment usually takes 1-2 minutes
- Once complete, your site will be available at: **https://anbie.github.io/snake-game/**

## 📋 What Was Created

### 1. `index.html`
A beautiful, responsive website featuring:
- Game description and features
- Interactive game mode explanations
- Installation instructions
- Controls guide
- Project statistics
- Links to GitHub repository
- Responsive design for mobile and desktop

### 2. `.github/workflows/deploy.yml`
GitHub Actions workflow that:
- Automatically deploys to GitHub Pages on every push to main
- Can be manually triggered from the Actions tab
- Uses the latest GitHub Pages actions for reliable deployment

### 3. This Setup Guide
Instructions for enabling and managing GitHub Pages

## 🎨 Customization

### Update the Website Content

Edit `index.html` to customize:
- Colors (search for color codes like `#667eea`)
- Text content
- Features and descriptions
- Add screenshots or videos

After editing, commit and push:
```bash
git add index.html
git commit -m "Update website content"
git push origin main
```

The site will automatically redeploy within 1-2 minutes.

### Add Screenshots

To add game screenshots:
1. Take screenshots of your game
2. Add them to a `docs/images/` folder
3. Update `index.html` to include the images:
```html
<img src="docs/images/screenshot.png" alt="Game Screenshot">
```

## 🔧 Troubleshooting

### Site Not Deploying

1. Check the **Actions** tab for any errors
2. Ensure GitHub Pages is enabled in Settings → Pages
3. Verify the workflow file is in `.github/workflows/deploy.yml`
4. Make sure you have the correct permissions set

### 404 Error

1. Wait a few minutes after the first deployment
2. Clear your browser cache
3. Check that the repository is public (or you have GitHub Pro for private repos)

### Workflow Permissions Error

If you see a permissions error:
1. Go to Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Check "Allow GitHub Actions to create and approve pull requests"
5. Click Save

## 📱 Viewing Your Site

Once deployed, your site will be available at:
- **Production URL**: https://anbie.github.io/snake-game/
- **Repository**: https://github.com/anbie/snake-game

You can share this URL with anyone to showcase your project!

## 🔄 Automatic Updates

Every time you push changes to the `main` branch:
- The GitHub Actions workflow automatically runs
- Your website is rebuilt and redeployed
- Changes appear within 1-2 minutes

## 📊 Monitoring Deployments

To check deployment status:
1. Go to the **Actions** tab in your repository
2. Look for "Deploy to GitHub Pages" workflows
3. Click on any workflow run to see detailed logs
4. Green checkmark = successful deployment
5. Red X = deployment failed (check logs for details)

## 🎉 Next Steps

After setup:
1. ✅ Verify your site is live at https://anbie.github.io/snake-game/
2. 📸 Consider adding screenshots or a demo video
3. 🔗 Update your README.md to link to the live site
4. 📱 Share the URL on social media or with friends
5. ⭐ Ask people to star your repository!

## 💡 Tips

- The website is purely informational since the game is a Python desktop application
- Consider creating a web version using JavaScript if you want a playable browser version
- You can use custom domains with GitHub Pages (see GitHub documentation)
- The site is automatically HTTPS enabled

## 📚 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Custom Domains for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

---

Made with ❤️ for the Snake Game project
