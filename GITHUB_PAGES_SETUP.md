# GitHub Pages Setup Guide

This guide will help you complete the GitHub Pages setup for your Snake Game project.

## ✅ Files Already Committed

The following files have been added to your repository:
- `index.html` - Beautiful responsive website
- `.github/workflows/deploy.yml` - Automated deployment workflow
- `GITHUB_PAGES_SETUP.md` - This setup guide

## 🚀 Final Setup Steps

### Step 1: Enable GitHub Pages

1. Go to your repository settings: https://github.com/anbie/snake-game/settings/pages
2. Under **"Build and deployment"** section:
   - **Source**: Select **"GitHub Actions"**
3. That's it! The deployment will start automatically.

### Step 2: Monitor Deployment

1. Go to the **Actions** tab: https://github.com/anbie/snake-game/actions
2. You should see a "Deploy to GitHub Pages" workflow running
3. Wait 1-2 minutes for the first deployment to complete
4. Once complete (green checkmark ✓), your site is live!

### Step 3: Access Your Website

Your website will be available at:
**https://anbie.github.io/snake-game/**

## 🔄 Automatic Updates

The website now automatically updates whenever you:
- Push changes to the `main` branch
- Modify `index.html`
- Update any file in the repository

The GitHub Actions workflow will:
1. Detect the push to main
2. Automatically rebuild the site
3. Deploy the updated version
4. Complete in 1-2 minutes

## 📋 What Was Created

### 1. `index.html`
A beautiful, responsive website featuring:
- Game description and features
- Interactive game mode explanations (Classic & Fun)
- Installation instructions with code blocks
- Controls guide with visual keyboard layout
- Project statistics (100+ tests, 2 modes, 4 food colors, 7 Python versions)
- Links to GitHub repository
- Fully responsive design for mobile and desktop
- Modern gradient design with smooth animations

### 2. `.github/workflows/deploy.yml`
GitHub Actions workflow that:
- Triggers automatically on every push to main
- Can be manually triggered from the Actions tab
- Uses the latest GitHub Pages actions (v4)
- Handles permissions automatically
- Prevents concurrent deployments

### 3. This Setup Guide
Complete instructions for setup and customization

## 🎨 Customization

### Update Website Content

Edit `index.html` to customize:
- Colors (search for `#667eea` and `#764ba2` for the main gradient)
- Text content and descriptions
- Features and game modes
- Add screenshots or videos
- Update statistics

After editing:
```bash
git add index.html
git commit -m "Update website content"
git push origin main
```

The site will automatically redeploy within 1-2 minutes.

### Add Screenshots

To add game screenshots:
1. Create a `docs/images/` folder:
```bash
mkdir -p docs/images
```

2. Add your screenshots to this folder

3. Update `index.html` to include images:
```html
<div class="section">
    <h2>📸 Screenshots</h2>
    <img src="docs/images/gameplay.png" alt="Gameplay Screenshot" style="max-width: 100%; border-radius: 10px;">
</div>
```

4. Commit and push:
```bash
git add docs/images/ index.html
git commit -m "Add game screenshots"
git push origin main
```

### Add a Demo Video

If you have a demo video:
```html
<div class="section">
    <h2>🎥 Demo Video</h2>
    <video controls style="max-width: 100%; border-radius: 10px;">
        <source src="docs/videos/demo.mp4" type="video/mp4">
    </video>
</div>
```

## 🔧 Troubleshooting

### Site Not Deploying

1. **Check Actions tab** for any errors: https://github.com/anbie/snake-game/actions
2. **Verify GitHub Pages is enabled**: Settings → Pages → Source should be "GitHub Actions"
3. **Check workflow file exists**: `.github/workflows/deploy.yml` should be in your repo
4. **Wait a few minutes**: First deployment can take 2-3 minutes

### Workflow Permissions Error

If you see a permissions error in Actions:
1. Go to Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select **"Read and write permissions"**
4. Check **"Allow GitHub Actions to create and approve pull requests"**
5. Click **Save**
6. Re-run the failed workflow

### 404 Error When Visiting Site

1. **Wait 5 minutes** after first deployment
2. **Clear browser cache** (Ctrl+Shift+R or Cmd+Shift+R)
3. **Check repository visibility**: Must be public (or GitHub Pro for private)
4. **Verify deployment succeeded**: Check Actions tab for green checkmark

### Changes Not Appearing

1. **Wait 1-2 minutes** after pushing
2. **Hard refresh** your browser (Ctrl+Shift+R)
3. **Check Actions tab** to ensure deployment completed
4. **Clear browser cache** completely

## 📱 Viewing Your Site

Once deployed, your site will be available at:
- **Live Site**: https://anbie.github.io/snake-game/
- **Repository**: https://github.com/anbie/snake-game
- **Actions**: https://github.com/anbie/snake-game/actions

Share this URL to showcase your project!

## 📊 Monitoring Deployments

To check deployment status:
1. Go to **Actions** tab: https://github.com/anbie/snake-game/actions
2. Look for "Deploy to GitHub Pages" workflows
3. Click on any workflow run to see detailed logs
4. **Green checkmark ✓** = successful deployment
5. **Red X ✗** = deployment failed (check logs for details)

Each deployment shows:
- Commit message that triggered it
- Duration (usually 30-60 seconds)
- Deployment URL
- Detailed step-by-step logs

## 🎉 Next Steps

After setup:
1. ✅ Verify your site is live at https://anbie.github.io/snake-game/
2. 📸 Consider adding screenshots of the game in action
3. 🎥 Add a demo video showing both game modes
4. 🔗 Update your main README.md to link to the live site:
   ```markdown
   ## 🌐 Live Website
   Visit the project website: https://anbie.github.io/snake-game/
   ```
5. 📱 Share the URL on social media or with friends
6. ⭐ Ask people to star your repository!

## 💡 Pro Tips

- **The website is informational** since the game is a Python desktop application
- **Consider a web version**: Use JavaScript/HTML5 Canvas for a browser-playable version
- **Custom domains**: You can use your own domain with GitHub Pages (see GitHub docs)
- **HTTPS enabled**: Your site is automatically served over HTTPS
- **SEO friendly**: The HTML includes proper meta tags for search engines
- **Mobile responsive**: The site works great on phones and tablets

## 🔗 Useful Links

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Custom Domains for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Your Repository](https://github.com/anbie/snake-game)
- [Your Actions](https://github.com/anbie/snake-game/actions)

## 📈 Analytics (Optional)

To track visitors, you can add Google Analytics or GitHub's built-in traffic stats:
- **GitHub Traffic**: Settings → Insights → Traffic (shows views and clones)
- **Google Analytics**: Add tracking code to `index.html`

## 🆘 Need Help?

If you encounter issues:
1. Check the [GitHub Pages documentation](https://docs.github.com/en/pages)
2. Review the [Actions logs](https://github.com/anbie/snake-game/actions)
3. Open an issue in your repository
4. Check GitHub Status: https://www.githubstatus.com/

---

Made with ❤️ for the Snake Game project