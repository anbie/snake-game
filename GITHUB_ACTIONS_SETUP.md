# GitHub Actions Setup Guide

This guide explains how to set up GitHub Actions workflows for automated testing in your Snake Game repository.

## What is GitHub Actions?

GitHub Actions is a CI/CD (Continuous Integration/Continuous Deployment) platform that allows you to automate your build, test, and deployment pipeline. It runs workflows automatically when certain events occur in your repository (like pushing code or creating pull requests).

## How GitHub Actions Works

1. **Workflow Files**: YAML files in `.github/workflows/` directory define your automation
2. **Triggers**: Workflows run on specific events (push, pull request, schedule, etc.)
3. **Jobs**: Each workflow contains one or more jobs that run in parallel or sequentially
4. **Steps**: Jobs contain steps that execute commands or actions
5. **Runners**: GitHub provides virtual machines (Ubuntu, Windows, macOS) to run your workflows

## Setup Steps

### Step 1: Create the Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `snake-game`
3. Choose visibility (Public or Private)
4. **Important**: Do NOT initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### Step 2: Push Your Code to GitHub

The workflow file is already in your repository at `.github/workflows/tests.yml`. Push your code:

```bash
git push -u origin main
```

If you get an error about the repository not existing, make sure you created it in Step 1.

### Step 3: GitHub Actions Activates Automatically

Once you push code containing a `.github/workflows/` directory:

1. GitHub automatically detects the workflow file
2. The workflow will run on the next push or pull request
3. No additional configuration needed!

### Step 4: View Workflow Results

1. Go to your repository on GitHub: `https://github.com/anbie/snake-game`
2. Click on the "Actions" tab at the top
3. You'll see a list of workflow runs
4. Click on any run to see detailed logs and results

## Understanding the Workflow File

Our workflow file (`.github/workflows/tests.yml`) does the following:

```yaml
name: Run Tests                    # Workflow name shown in GitHub UI

on:                                # Triggers
  push:
    branches: [ main, master ]     # Run on push to main/master
  pull_request:
    branches: [ main, master ]     # Run on PRs to main/master

jobs:
  test:                            # Job name
    runs-on: ubuntu-latest         # Use Ubuntu runner
    
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']  # Test on multiple Python versions
    
    steps:                         # Steps to execute
    - name: Checkout code          # Get your code
      uses: actions/checkout@v3
    
    - name: Set up Python          # Install Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies   # Install system packages
      run: |
        sudo apt-get update
        sudo apt-get install -y python3-pygame xvfb
    
    - name: Install Python deps    # Install Python packages
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests              # Execute tests
      run: |
        xvfb-run -a python -m pytest test_snake_game.py -v --cov=snake_game
```

## Key Components Explained

### 1. xvfb (X Virtual Framebuffer)

```bash
xvfb-run -a python -m pytest test_snake_game.py
```

- **Why needed**: Pygame requires a display to initialize, but GitHub Actions runners don't have a display
- **What it does**: Creates a virtual display so Pygame can run in headless mode
- **The `-a` flag**: Automatically selects a display number

### 2. Matrix Strategy

```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11']
```

- Runs tests on multiple Python versions simultaneously
- Ensures compatibility across different Python versions
- Each version runs as a separate job

### 3. Workflow Triggers

```yaml
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
```

- **push**: Runs when you push commits to main/master
- **pull_request**: Runs when someone creates a PR to main/master

## Viewing Test Results

### In GitHub UI

1. Navigate to the "Actions" tab
2. Click on a workflow run
3. Click on a job (e.g., "test (3.11)")
4. Expand steps to see detailed output
5. Green checkmark ✅ = tests passed
6. Red X ❌ = tests failed

### Status Badges

Add this to your README to show test status:

```markdown
![Tests](https://github.com/anbie/snake-game/workflows/Run%20Tests/badge.svg)
```

This badge shows:
- ✅ Green "passing" if all tests pass
- ❌ Red "failing" if any test fails

## Troubleshooting

### Workflow Not Running

**Problem**: Workflow doesn't appear in Actions tab

**Solutions**:
1. Ensure `.github/workflows/tests.yml` is in the repository
2. Check YAML syntax (use a YAML validator)
3. Make sure you pushed the `.github` directory
4. Verify the workflow file is on the main/master branch

### Tests Failing on GitHub but Pass Locally

**Problem**: Tests pass on your machine but fail in GitHub Actions

**Common causes**:
1. **Display issues**: Make sure you're using `xvfb-run`
2. **Dependencies**: Ensure all dependencies are in `requirements.txt`
3. **Python version**: Test locally with the same Python version
4. **File paths**: Use relative paths, not absolute paths

### Permission Errors

**Problem**: Workflow can't access repository

**Solution**: 
- GitHub Actions has default permissions
- For this project, no special permissions needed
- If needed, add to workflow:
  ```yaml
  permissions:
    contents: read
  ```

## Running Tests Locally (Same as GitHub)

To replicate the GitHub Actions environment locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Run tests with coverage (like GitHub Actions)
pytest test_snake_game.py -v --cov=snake_game --cov-report=term-missing

# On Linux/Mac with xvfb
xvfb-run -a pytest test_snake_game.py -v --cov=snake_game
```

## Customizing the Workflow

### Run on Different Events

```yaml
on:
  push:                    # On every push
  pull_request:           # On every PR
  schedule:               # On a schedule
    - cron: '0 0 * * 0'  # Every Sunday at midnight
  workflow_dispatch:      # Manual trigger
```

### Add More Jobs

```yaml
jobs:
  test:
    # ... existing test job ...
  
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run linter
        run: |
          pip install flake8
          flake8 snake_game.py
```

### Deploy on Success

```yaml
jobs:
  test:
    # ... test job ...
  
  deploy:
    needs: test              # Only run if tests pass
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: echo "Deploying..."
```

## Best Practices

1. **Keep workflows fast**: Optimize test execution time
2. **Use caching**: Cache dependencies to speed up runs
3. **Fail fast**: Stop on first failure in matrix builds
4. **Clear naming**: Use descriptive names for jobs and steps
5. **Secrets management**: Use GitHub Secrets for sensitive data
6. **Status checks**: Require passing tests before merging PRs

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Python Testing with GitHub Actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)

## Summary

Your GitHub Actions workflow is already set up! Once you:

1. ✅ Create the repository on GitHub
2. ✅ Push your code with `git push -u origin main`
3. ✅ GitHub Actions will automatically run tests on every commit

The workflow will:
- Run 50+ unit tests
- Test on Python 3.8, 3.9, 3.10, and 3.11
- Generate coverage reports
- Show results in the Actions tab
- Display status badge in README

No additional setup required! 🎉