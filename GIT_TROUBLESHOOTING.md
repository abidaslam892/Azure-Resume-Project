# Git Repository Troubleshooting Guide 🔧

## Common Git Issues and Solutions

### 1. **Authentication Issues**

#### Problem: "Permission denied (publickey)" or "Authentication failed"

**Solutions:**
```bash
# Check your GitHub authentication
gh auth status

# Login to GitHub CLI (recommended)
gh auth login

# Or configure Git with your credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# For HTTPS authentication, use personal access token
git remote set-url origin https://your-username:your-token@github.com/username/repo.git
```

### 2. **Remote Repository Issues**

#### Problem: "fatal: remote origin already exists"

**Solution:**
```bash
# Remove existing remote and add new one
git remote remove origin
git remote add origin https://github.com/username/Azure-Resume-Challenge.git
```

#### Problem: "fatal: repository not found"

**Solution:**
```bash
# Make sure repository exists on GitHub and URL is correct
git remote -v  # Check current remote URL
git remote set-url origin https://github.com/correct-username/correct-repo.git
```

### 3. **Push/Pull Issues**

#### Problem: "Updates were rejected because the remote contains work that you do not have locally"

**Solution:**
```bash
# Pull changes first, then push
git pull origin main --rebase
git push origin main

# Or force push (CAUTION: only if you're sure)
git push origin main --force
```

#### Problem: "Your branch is ahead of 'origin/main' by X commits"

**Solution:**
```bash
# Simply push your commits
git push origin main
```

### 4. **Merge Conflicts**

#### Problem: Merge conflicts during pull/merge

**Solution:**
```bash
# View conflicted files
git status

# Edit files to resolve conflicts (remove <<<<<<, ======, >>>>>> markers)
# Then mark as resolved
git add .
git commit -m "Resolve merge conflicts"
```

### 5. **Large File Issues**

#### Problem: "file is X MB; this exceeds GitHub's file size limit"

**Solution:**
```bash
# Remove large files from Git history
git filter-branch --tree-filter 'rm -f path/to/large/file' HEAD

# Or use .gitignore to prevent committing large files
echo "*.zip" >> .gitignore
echo "*.tar.gz" >> .gitignore
git add .gitignore
git commit -m "Add gitignore for large files"
```

### 6. **Branch Issues**

#### Problem: "fatal: The current branch main has no upstream branch"

**Solution:**
```bash
# Set upstream branch
git push -u origin main
```

#### Problem: Working on wrong branch

**Solution:**
```bash
# Create and switch to correct branch
git checkout -b feature-branch
# Or switch to existing branch
git checkout main
```

### 7. **Commit Issues**

#### Problem: "Please tell me who you are" error

**Solution:**
```bash
# Configure Git identity
git config --global user.name "Your Full Name"
git config --global user.email "your.email@gmail.com"

# For this repository only
git config user.name "Your Full Name"
git config user.email "your.email@gmail.com"
```

#### Problem: Want to undo last commit

**Solution:**
```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and changes (DANGEROUS)
git reset --hard HEAD~1
```

### 8. **File Tracking Issues**

#### Problem: Files not being tracked/ignored incorrectly

**Solution:**
```bash
# Force add ignored files
git add -f filename

# Stop tracking file but keep it
git rm --cached filename

# Check what's being ignored
git check-ignore -v path/to/file
```

## 🚀 **Recommended Workflow for Azure Resume Project**

### Initial Setup (One Time)
```bash
# 1. Navigate to project
cd /home/abid/Project/Azure-Resume-Project

# 2. Run the setup script
./setup-git-repository.sh

# 3. Create GitHub repository on GitHub.com

# 4. Connect local to GitHub
git remote add origin https://github.com/yourusername/Azure-Resume-Challenge.git

# 5. Push to GitHub
git push -u origin main
```

### Regular Workflow
```bash
# 1. Check status
git status

# 2. Add changes
git add .

# 3. Commit with meaningful message  
git commit -m "feat: add new feature or fix: fix issue"

# 4. Push to GitHub
git push origin main
```

### Before Making Changes
```bash
# Always pull latest changes first
git pull origin main

# Create feature branch for new work
git checkout -b feature/new-feature

# Make changes, commit, then merge back
git checkout main
git merge feature/new-feature
git branch -d feature/new-feature
```

## 🛠️ **Emergency Recovery Commands**

### If Everything Goes Wrong
```bash
# 1. Backup current work
cp -r . ../project-backup-$(date +%Y%m%d-%H%M%S)

# 2. Reset to last known good state
git reset --hard HEAD

# 3. Or start fresh (LAST RESORT)
rm -rf .git
git init
git add .
git commit -m "Fresh start"
```

### Check Repository Health
```bash
# Verify repository integrity
git fsck

# Clean up repository
git gc --prune=now

# Show repository information
git remote -v
git branch -a
git log --oneline -10
```

## 📞 **Getting Help**

If you're still having issues:

1. **Check Git status**: `git status`
2. **Check remote configuration**: `git remote -v`
3. **Check current branch**: `git branch`
4. **View recent commits**: `git log --oneline -5`
5. **Use the provided scripts**:
   - `./setup-git-repository.sh` - Complete setup
   - `./push-to-github.sh` - Safe push to GitHub

## ✅ **Success Checklist**

- [ ] Git repository initialized
- [ ] .gitignore file created
- [ ] All files committed
- [ ] Remote origin configured
- [ ] Successfully pushed to GitHub
- [ ] Repository visible on GitHub.com
- [ ] Can pull and push without errors

Remember: Git is forgiving - most "disasters" can be recovered from! The key is to commit often and push regularly.