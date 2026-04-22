# ✅ MR Agent - Setup Checklist

## 🚀 Getting Started with MR Agent

Follow this checklist to get the MR Agent up and running in just a few minutes.

---

## Phase 1: Setup (5 minutes)

### 1.1 Get GitHub Personal Access Token
- [ ] Open browser and go to: https://github.com/settings/tokens
- [ ] Click "Generate new token" → "Generate new token (classic)"
- [ ] Set token name to: "MR Agent Token"
- [ ] Select required scopes:
  - [ ] ☑ `repo` (Full control of private repositories)
  - [ ] ☑ `read:org` (Read organization data)
- [ ] Click "Generate token"
- [ ] **IMPORTANT:** Copy the token immediately (you won't see it again!)
- [ ] Store token safely (you'll need it in next step)

### 1.2 Update .env File
- [ ] Open file: `C:\Users\NikhilSharadMore\Downloads\demo (1)\.env`
- [ ] Find the GitHub Configuration section
- [ ] Add/update these values:
  ```env
  GITHUB_TOKEN=ghp_paste_your_token_here
  GITHUB_OWNER=NikhilSharadMore
  GITHUB_REPO=demo
  ```
- [ ] Save the file (Ctrl+S)

### 1.3 Validate Setup
- [ ] Open terminal/PowerShell in project directory
- [ ] Run this command:
  ```bash
  python test_mr_agent_setup.py
  ```
- [ ] Verify output shows all ✅ checks:
  - [ ] ✅ Token is valid
  - [ ] ✅ Repository accessible
  - [ ] ✅ Found X branches
  - [ ] ✅ Token has correct scopes
  - [ ] ✅ Configuration is complete

**If all checks pass → Move to Phase 2!** ✅

---

## Phase 2: First PR Creation (5 minutes)

### 2.1 Prepare Your Feature Branch

Option A: Use existing branch
- [ ] Have your feature branch ready and pushed to GitHub
- [ ] Example: `feature/auth`, `feature/otp`, etc.

Option B: Create test branch
```bash
git checkout -b feature/test-mr
git push origin feature/test-mr
```

### 2.2 Create Your First PR

**Command:**
```bash
python agents/mr_agent.py \
  --title "Test: MR Agent Functionality" \
  --head "feature/test-mr" \
  --base "develop" \
  --description "Testing the MR Agent for the first time"
```

**Alternative using PowerShell:**
```powershell
.\run_mr_agent.ps1 -Title "Test: MR Agent" `
                   -Head "feature/test-mr" `
                   -Base "develop" `
                   -Description "Testing MR Agent"
```

### 2.3 Verify PR Creation

- [ ] Command completes successfully
- [ ] You see ✅ PULL REQUEST CREATED SUCCESSFULLY! message
- [ ] PR number is displayed (e.g., PR #42)
- [ ] URL is shown
- [ ] Open the URL in your browser to view the PR
- [ ] PR appears on GitHub: https://github.com/NikhilSharadMore/demo/pulls

**Congratulations!** Your first PR was created with MR Agent! 🎉

---

## Phase 3: Real PR with Jira Link (10 minutes)

### 3.1 Check Your Jira Stories

- [ ] Run Jira Agent to see your assigned stories:
  ```bash
  python agents/jira_agent.py
  ```
- [ ] Note down a story key (e.g., EPMICMPSTP-713)

### 3.2 Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# ... implement the feature ...
git add .
git commit -m "feat: implement your feature"
git push origin feature/your-feature-name
```

### 3.3 Create PR with Jira Link

```bash
python agents/mr_agent.py \
  --title "Feature: Your Feature Title" \
  --head "feature/your-feature-name" \
  --base "develop" \
  --description "Implements the feature as per requirements" \
  --labels "feature,backend" \
  --jira-issue "EPMICMPSTP-713"
```

### 3.4 Verify and Review

- [ ] PR is created successfully
- [ ] PR title is correct
- [ ] PR description includes your changes
- [ ] Jira issue is linked
- [ ] Labels are applied
- [ ] PR number is displayed
- [ ] All information is accurate

**Perfect!** Your Jira-linked PR is ready for review! ✅

---

## Phase 4: Advanced Usage (Optional)

### 4.1 Add Reviewers

```bash
python agents/mr_agent.py \
  --title "Feature: Your Feature" \
  --head "feature/your-feature" \
  --base "develop" \
  --description "Your description" \
  --reviewers "john-reviewer,jane-reviewer"
```

### 4.2 Add Multiple Labels

```bash
python agents/mr_agent.py \
  --title "Feature: Your Feature" \
  --head "feature/your-feature" \
  --base "develop" \
  --labels "feature,security,backend,high-priority"
```

### 4.3 Create Draft PR

```bash
python agents/mr_agent.py \
  --title "[WIP] Feature: Work in Progress" \
  --head "feature/wip-feature" \
  --base "develop" \
  --description "Still working on this feature" \
  --draft
```

### 4.4 Include Changes List

```bash
python agents/mr_agent.py \
  --title "Feature: JWT Authentication" \
  --head "feature/jwt" \
  --base "develop" \
  --description "Implements JWT-based authentication" \
  --changes "Added JWT provider,Implemented auth filter,Created token model,Added refresh logic"
```

---

## Phase 5: Troubleshooting

If you encounter any issues, work through this checklist:

### Issue: "GITHUB_TOKEN not set"

**Checklist:**
- [ ] .env file exists in project root
- [ ] GITHUB_TOKEN line is present
- [ ] Token starts with `ghp_`
- [ ] No extra spaces or quotes around token
- [ ] .env file was saved

**Fix:**
```env
GITHUB_TOKEN=ghp_your_token_here
```

### Issue: "Branch not found"

**Checklist:**
- [ ] Branch exists locally: `git branch`
- [ ] Branch is pushed to GitHub: `git push origin branch-name`
- [ ] Branch name is spelled correctly
- [ ] Branch name doesn't have typos

**Fix:**
```bash
git push origin your-branch-name
# Wait a moment, then try again
```

### Issue: "PR already exists"

**Checklist:**
- [ ] Check if PR is already open: GitHub → Pulls
- [ ] Close existing PR, OR
- [ ] Use a different branch name

### Issue: "Authentication failed"

**Checklist:**
- [ ] Token is valid: Check GitHub settings
- [ ] Token hasn't expired: Generate new if needed
- [ ] Token has correct scopes: `repo`, `read:org`
- [ ] Token is correctly copied (no extra characters)

**Fix:**
```bash
# Visit: https://github.com/settings/tokens
# Generate new token with correct scopes
# Update .env with new token
```

### Run Diagnostics

If stuck, run the validation script:
```bash
python test_mr_agent_setup.py
```

This will show detailed diagnostics for each component.

---

## Phase 6: Daily Usage

### Create PR from Jira Story

```bash
# 1. Fetch your stories
python agents/jira_agent.py

# 2. Create feature branch
git checkout -b feature/story-name

# 3. Implement and commit
git add .
git commit -m "feat: implement story"
git push origin feature/story-name

# 4. Create PR linked to Jira
python agents/mr_agent.py \
  --title "Feature: Story Title" \
  --head "feature/story-name" \
  --base "develop" \
  --jira-issue "EPMICMPSTP-XXX"
```

### Create PR with Multiple Details

```bash
python agents/mr_agent.py \
  --title "Feature: Complete Feature" \
  --head "feature/complete" \
  --base "develop" \
  --description "Full feature implementation" \
  --labels "feature,important" \
  --assignees "you" \
  --reviewers "reviewer1,reviewer2" \
  --jira-issue "EPMICMPSTP-789"
```

---

## 📚 Documentation Quick Links

| When | What to Read |
|------|--------------|
| Stuck? | Read `MR_AGENT_QUICKSTART.md` |
| Want to learn everything? | Read `MR_AGENT_IMPLEMENTATION_GUIDE.md` |
| Need API reference? | Read `agents/MR_AGENT.md` |
| Understand full system? | Read `AGENT_SYSTEM_SETUP.md` |
| Don't know where to start? | Read `MR_AGENT_INDEX.md` |

---

## ✅ Final Verification Checklist

- [ ] .env file updated with GitHub token
- [ ] Token starts with `ghp_`
- [ ] GITHUB_OWNER set to NikhilSharadMore
- [ ] GITHUB_REPO set to demo
- [ ] `python test_mr_agent_setup.py` passes all checks
- [ ] First test PR created successfully
- [ ] PR appears on GitHub
- [ ] You can view PR on GitHub web interface
- [ ] Ready to create real PRs!

---

## 🎯 Next Milestones

### This Week
- [ ] Create PR for first Jira story
- [ ] Link PR to Jira issue
- [ ] Get approval from reviewer
- [ ] Merge PR successfully

### This Month
- [ ] Create multiple PRs
- [ ] Integrate with Code Agent
- [ ] Automate full workflow
- [ ] Deploy to production

### This Quarter
- [ ] Full agent system working (Jira → Code → MR)
- [ ] Automated testing integrated
- [ ] Deployment pipeline automated
- [ ] Team using system daily

---

## 💡 Pro Tips

1. **Test First:** Always test with a dummy PR first
2. **Name Branches Well:** Use `feature/`, `bugfix/`, `hotfix/` prefixes
3. **Link Jira:** Always include `--jira-issue` for traceability
4. **Request Reviewers:** Use `--reviewers` to notify reviewers
5. **Use Labels:** Categorize PRs with appropriate labels
6. **Write Descriptions:** Clear descriptions help reviewers
7. **Draft PRs:** Use `--draft` for work-in-progress
8. **Validate Setup:** Run `test_mr_agent_setup.py` if issues arise

---

## 🆘 Getting Help

1. **Setup Issues:** Run `python test_mr_agent_setup.py`
2. **How to Use:** Read `MR_AGENT_QUICKSTART.md`
3. **Complete Docs:** Read `agents/MR_AGENT.md`
4. **System Overview:** Read `AGENT_SYSTEM_SETUP.md`
5. **Examples:** See `MR_AGENT_IMPLEMENTATION_GUIDE.md`

---

## 🎉 Success Indicators

You know MR Agent is working when:

✅ `test_mr_agent_setup.py` passes all checks  
✅ You can create a PR with just one command  
✅ PR appears on GitHub within seconds  
✅ PR is linked to Jira issue automatically  
✅ Labels and reviewers are assigned  
✅ Description is formatted nicely  
✅ You can repeat this for multiple PRs  

---

## 📋 Important Files

| File | Purpose |
|------|---------|
| `.env` | Configuration (UPDATE THIS) |
| `agents/mr_agent.py` | Main implementation |
| `test_mr_agent_setup.py` | Validation tool |
| `MR_AGENT_QUICKSTART.md` | Quick start guide |
| `agents/MR_AGENT.md` | Full documentation |

---

**Start with Phase 1 above and follow the steps. You'll have MR Agent working in less than 15 minutes!**

Good luck! 🚀

