#!/bin/bash

# GitHub Repository Setup and Push Script
# This script helps you push to GitHub without common errors

set -e

echo "🔗 GitHub Repository Push Setup"
echo "================================"

# Check if we're in a Git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a Git repository"
    echo "Please run this script from your project directory"
    exit 1
fi

echo ""
echo "📋 Current Git Status:"
git status --porcelain

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "📝 Found uncommitted changes. Committing them first..."
    git add .
    git commit -m "chore: Final updates before GitHub push

- Completed Git repository setup
- Added comprehensive documentation
- Fixed all deployment configurations
- Project ready for GitHub publication"
    echo "✅ Changes committed"
fi

echo ""
echo "🔍 Checking remote repository configuration..."

# Check if remote origin exists
if git remote get-url origin >/dev/null 2>&1; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ Remote origin already configured: $REMOTE_URL"
    
    echo ""
    echo "🚀 Pushing to GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub!"
        echo ""
        echo "🌐 Your repository is now updated on GitHub"
        echo "Repository URL: $REMOTE_URL"
    else
        echo "❌ Push failed. Please check:"
        echo "1. GitHub repository exists"
        echo "2. You have push permissions"
        echo "3. Your GitHub authentication is working"
    fi
else
    echo "⚠️  No remote origin configured"
    echo ""
    echo "📋 To connect to GitHub:"
    echo "1. Create a new repository on GitHub"
    echo "2. Copy the repository URL"
    echo "3. Run: git remote add origin <repository-url>"
    echo "4. Run: git push -u origin main"
    echo ""
    echo "Example:"
    echo "git remote add origin https://github.com/yourusername/Azure-Resume-Challenge.git"
    echo "git push -u origin main"
fi

echo ""
echo "📊 Repository Information:"
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --oneline)"
echo "Total commits: $(git rev-list --count HEAD)"

exit 0