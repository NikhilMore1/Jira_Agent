# 🚀 MR Agent Quick Start Guide

## What is the MR Agent?

The **MR Agent** creates GitHub Pull Requests automatically with:
- ✅ Proper formatting and descriptions
- ✅ Links to Jira issues
- ✅ Automatic labels and assignees
- ✅ Code review checklists
- ✅ Branch validation
- ✅ Support for draft PRs

---

## 5-Minute Setup

### Step 1: Get GitHub Personal Access Token (2 min)

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"**
3. Give it a name: `MR Agent Token`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read organization data)
5. Click **"Generate token"**
6. **COPY** the token (you won't see it again!)

### Step 2: Update .env File (1 min)

Edit `.env` and add/update:
```env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_OWNER=NikhilSharadMore
GITHUB_REPO=demo
```

### Step 3: Test Setup (1 min)

```bash
python agents/mr_agent.py --help
```

If you see the help menu, you're ready! ✅

### Step 4: Create Your First PR (1 min)

```bash
python agents/mr_agent.py \
  --title "Feature: Add Authentication" \
  --head "feature/auth" \
  --base "develop" \
  --description "Implements user login with JWT tokens"
```

---

## Common Usage Patterns

### 1. Simple Feature PR

```bash
python agents/mr_agent.py \
  --title "Feature: User Profile Page" \
  --head "feature/user-profile" \
  --base "develop" \
  --description "Adds user profile editing functionality"
```

### 2. PR with Jira Link

```bash
python agents/mr_agent.py \
  --title "Feature: Forgot Password with OTP" \
  --head "feature/otp-reset" \
  --base "develop" \
  --description "Implements OTP-based password reset" \
  --jira-issue "EPMICMPSTP-713"
```

### 3. PR with Multiple Labels and Reviewers

```bash
python agents/mr_agent.py \
  --title "Feature: JWT Authentication" \
  --head "feature/jwt-auth" \
  --base "develop" \
  --description "Implements JWT-based authentication" \
  --labels "feature,security,backend" \
  --assignees "john-dev,jane-reviewer" \
  --reviewers "john-dev,jane-reviewer" \
  --jira-issue "EPMICMPSTP-789"
```

### 4. Work in Progress PR (Draft)

```bash
python agents/mr_agent.py \
  --title "[WIP] Feature: New Dashboard" \
  --head "feature/dashboard" \
  --base "develop" \
  --description "Still working on this, not ready for review" \
  --draft
```

### 5. Bug Fix PR

```bash
python agents/mr_agent.py \
  --title "Fix: Login timeout issue" \
  --head "bugfix/login-timeout" \
  --base "develop" \
  --description "Fixed session timeout not working properly" \
  --labels "bug,critical" \
  --jira-issue "EPMICMPSTP-456"
```

---

## Using the PowerShell Script

```powershell
.\run_mr_agent.ps1 -Title "Feature: Auth" `
                   -Head "feature/auth" `
                   -Base "develop" `
                   -Description "OAuth2 authentication" `
                   -Labels "feature,auth" `
                   -JiraIssue "EPMICMPSTP-713"
```

---

## What Happens After PR Creation?

1. ✅ PR is created on GitHub
2. ✅ Links to Jira issue automatically
3. ✅ Labels are added
4. ✅ Assignees/Reviewers are notified
5. ✅ CI/CD pipeline runs automatically
6. ✅ Team reviews and approves
7. ✅ Merge when ready!

---

## Troubleshooting

### ❌ "GITHUB_TOKEN not set"
**Solution:** Add `GITHUB_TOKEN` to `.env` file

### ❌ "Branch not found"
**Solution:** Make sure you've pushed the branch:
```bash
git push origin feature/your-feature
```

### ❌ "PR already exists"
**Solution:** Close the existing PR or use a different branch name

### ❌ "Authentication failed"
**Solution:** Generate a new token with correct scopes

---

## Full Workflow Example

### From Jira Story to Deployed Code

```bash
# 1️⃣ Check your assigned stories
python agents/jira_agent.py

# 2️⃣ Create and checkout feature branch
git checkout -b feature/user-auth

# 3️⃣ Develop and test your code
# ... write code ...
git add .
git commit -m "feat: add JWT authentication"
git push origin feature/user-auth

# 4️⃣ Create PR linked to Jira
python agents/mr_agent.py \
  --title "Feature: JWT Authentication" \
  --head "feature/user-auth" \
  --base "develop" \
  --description "Implements JWT-based user authentication" \
  --labels "feature,security" \
  --jira-issue "EPMICMPSTP-789"

# 5️⃣ Wait for CI/CD and reviews
# ... GitHub Actions run tests ...
# ... Team reviews the code ...

# 6️⃣ Merge PR when approved
# https://github.com/YourRepo/pull/42/merge

# 7️⃣ Deploy to production
# ... deployment process ...
```

---

## Next Steps

### Learn More
- Read full documentation: `agents/MR_AGENT.md`
- Check GitHub API: https://docs.github.com/en/rest
- Learn Git workflow: https://guides.github.com/

### Integrate with Other Agents
- **Jira Agent** - Fetch stories
- **Code Agent** - Generate code
- **Test Agent** - Write tests
- **MR Agent** - Create PRs (you are here!)

---

## Quick Reference

| Task | Command |
|------|---------|
| Get help | `python agents/mr_agent.py --help` |
| Create simple PR | `python agents/mr_agent.py --title "..." --head "..." --base "..."` |
| Create PR with Jira link | Add `--jira-issue "PROJ-123"` |
| Create draft PR | Add `--draft` flag |
| Add reviewers | Add `--reviewers "user1,user2"` |
| Add labels | Add `--labels "feature,bug,..."` |

---

## Key Points to Remember

✅ Always push your branch before creating PR  
✅ Link to Jira issues for traceability  
✅ Use meaningful PR titles and descriptions  
✅ Request reviewers who understand the code  
✅ Draft PRs are great for WIP code  
✅ The agent validates everything automatically  

---

Good luck! 🚀

Questions? Check `agents/MR_AGENT.md` for detailed docs.

