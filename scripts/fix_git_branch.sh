#!/bin/bash

echo "🔧 Fixing Git Branch Issues"
echo "============================"

# Check current state
echo "1. Checking current Git state..."
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "NO_BRANCH")
echo "   Current branch: $CURRENT_BRANCH"

# Check if we're in a git repository
if [ "$CURRENT_BRANCH" = "NO_BRANCH" ]; then
    echo "❌ Not in a Git repository or no commits yet"
    echo "   Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: AI Test Automation Framework"
fi

# Check available branches
echo ""
echo "2. Available branches:"
git branch -a

# Create feature branch if it doesn't exist
echo ""
echo "3. Creating feature branch..."
if git show-ref --quiet refs/heads/feature/ai_testAutomation; then
    echo "✅ Branch feature/ai_testAutomation already exists"
    git checkout feature/ai_testAutomation
else
    echo "📝 Creating new branch: feature/ai_testAutomation"
    git checkout -b feature/ai_testAutomation
fi

# Check for changes to commit
echo ""
echo "4. Checking for uncommitted changes..."
if [ -n "$(git status --porcelain)" ]; then
    echo "📦 Found uncommitted changes:"
    git status --porcelain
    
    echo ""
    echo "5. Committing changes..."
    git add .
    git commit -m "feat: add AI test automation framework
    
- Add UI automation tests with Selenium and Playwright
- Add API testing for REST and GraphQL endpoints  
- Add AI model testing capabilities
- Add test configuration and utility functions
- Add comprehensive test examples"
else
    echo "✅ No uncommitted changes"
fi

# Push to remote
echo ""
echo "6. Pushing to remote repository..."
git push --set-upstream origin feature/ai_testAutomation

echo ""
echo "✅ Done! Your branch is now pushed to GitHub."
echo "🔗 You can now create a Pull Request"
