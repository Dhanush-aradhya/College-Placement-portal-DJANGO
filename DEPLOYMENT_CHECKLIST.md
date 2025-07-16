# Pre-Push Security Checklist ✅

## Before pushing to GitHub, ensure:

### ✅ Completed Items:
- [x] `.gitignore` file created and configured
- [x] `requirements.txt` exists
- [x] `README.md` created with setup instructions
- [x] `.env.example` created for environment variables

### 🚨 CRITICAL - Complete Before Push:

#### 1. **Environment Variables Setup**
- [ ] Create `.env` file (DO NOT commit this)
- [ ] Move sensitive data from `settings.py` to `.env`:
  - [ ] Generate new SECRET_KEY
  - [ ] Move database credentials
- [ ] Update `settings.py` to use environment variables
- [ ] Test that the application still works

#### 2. **Remove Sensitive Files** 
- [ ] Remove or move `student_usns.csv` to a secure location
- [ ] Ensure `db.sqlite3` is not being tracked
- [ ] Verify `mediafiles/` directory is ignored

#### 3. **Clean Repository**
```bash
# Remove cached files if they were previously tracked
git rm -r --cached __pycache__/
git rm --cached db.sqlite3
git rm --cached student_usns.csv
git rm -r --cached mediafiles/
```

#### 4. **Settings Update**
Replace current `settings.py` with `settings_secure.py` or update manually:
- [ ] Use environment variables for SECRET_KEY
- [ ] Use environment variables for database config
- [ ] Set DEBUG=False for production

#### 5. **Final Verification**
- [ ] Test app runs with new settings
- [ ] Verify no sensitive data in git status
- [ ] Check `.gitignore` is working

## Quick Setup Commands:

```bash
# 1. Initialize git (if not done)
git init

# 2. Add gitignore and safe files first
git add .gitignore README.md requirements.txt .env.example
git commit -m "Initial setup with security files"

# 3. Remove sensitive files from tracking
git rm --cached db.sqlite3 student_usns.csv
git rm -r --cached mediafiles/ __pycache__/

# 4. Add remaining safe files
git add .
git commit -m "Add project files (excluding sensitive data)"

# 5. Push to GitHub
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Files that should NEVER be in Git:
- `db.sqlite3` (database)
- `mediafiles/` (user uploads)
- `.env` (environment variables)
- `student_usns.csv` (sensitive data)
- `__pycache__/` (Python cache)
- Any files with passwords or API keys
