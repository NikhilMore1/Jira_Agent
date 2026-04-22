# 🎯 MR Agent - Quick Reference Card

## One-Page Cheat Sheet for MR Agent

---

## ⚡ 30-Second Summary

**MR Agent** = GitHub Pull Request creation automation tool

✅ Create PRs with one command  
✅ Link to Jira issues  
✅ Validate everything automatically  
✅ Works on Windows  
✅ Production ready  

---

## 🚀 Getting Started (5 Minutes)

### 1. Get GitHub Token
- Visit: https://github.com/settings/tokens
- Create token with: `repo`, `read:org` scopes
- Copy token (starts with `ghp_`)

### 2. Configure .env
```env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_OWNER=NikhilSharadMore
GITHUB_REPO=demo
```

### 3. Validate
```bash
python test_mr_agent_setup.py
```

---

## 📋 Basic Commands

### Simple PR
```bash
python agents/mr_agent.py \
  --title "Feature: Name" \
  --head "feature/name" \
  --base "develop"
```

### PR with Jira Link
```bash
python agents/mr_agent.py \
  --title "Feature: Name" \
  --head "feature/name" \
  --base "develop" \
  --jira-issue "EPMICMPSTP-713"
```

### All Options
```bash
python agents/mr_agent.py \
  --title "Feature: Name" \
  --head "feature/name" \
  --base "develop" \
  --description "Description" \
  --labels "feature,bug" \
  --assignees "user1" \
  --reviewers "user1,user2" \
  --jira-issue "EPMICMPSTP-XXX" \
  --changes "Change 1,Change 2" \
  --draft
```

### PowerShell
```powershell
.\run_mr_agent.ps1 -Title "Feature: Name" `
                   -Head "feature/name" `
                   -Base "develop"
```

---

## 🎯 Common Scenarios

### Create PR for Jira Story
```bash
# 1. Get story from Jira
python agents/jira_agent.py

# 2. Create and push branch
git checkout -b feature/story-name
git add .
git commit -m "feat: implement story"
git push origin feature/story-name

# 3. Create PR with MR Agent
python agents/mr_agent.py \
  --title "Feature: Story Title" \
  --head "feature/story-name" \
  --base "develop" \
  --jira-issue "EPMICMPSTP-XXX"
```

### Create Draft PR
```bash
python agents/mr_agent.py \
  --title "[WIP] Feature: Name" \
  --head "feature/name" \
  --base "develop" \
  --draft
```

### Create PR with Code Review
```bash
python agents/mr_agent.py \
  --title "Feature: Name" \
  --head "feature/name" \
  --base "develop" \
  --reviewers "john,jane" \
  --labels "feature,important"
```

---

## ✅ Arguments Reference

| Argument | Type | Required | Example |
|----------|------|----------|---------|
| `--title` | string | ✅ Yes | `"Feature: Auth"` |
| `--head` | string | ✅ Yes | `"feature/auth"` |
| `--base` | string | ✅ Yes | `"develop"` |
| `--description` | string | ❌ No | `"Implements OAuth"` |
| `--labels` | string | ❌ No | `"feature,auth"` |
| `--assignees` | string | ❌ No | `"john,jane"` |
| `--reviewers` | string | ❌ No | `"john,jane"` |
| `--jira-issue` | string | ❌ No | `"PROJ-123"` |
| `--changes` | string | ❌ No | `"Added X,Fixed Y"` |
| `--draft` | flag | ❌ No | (no value) |

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "GITHUB_TOKEN not set" | Add to .env: `GITHUB_TOKEN=ghp_xxx` |
| "Branch not found" | Push branch: `git push origin your-branch` |
| "PR already exists" | Close existing PR or use different branch |
| "Authentication failed" | Generate new token with correct scopes |
| Any issue | Run: `python test_mr_agent_setup.py` |

---

## 📚 Documentation

| When | Read This |
|------|-----------|
| 5 min overview | `MR_AGENT_QUICKSTART.md` |
| Step-by-step setup | `MR_AGENT_SETUP_CHECKLIST.md` |
| Complete guide | `MR_AGENT_IMPLEMENTATION_GUIDE.md` |
| API reference | `agents/MR_AGENT.md` |
| System overview | `AGENT_SYSTEM_SETUP.md` |
| Navigation | `MR_AGENT_INDEX.md` |

---

## 🔄 Full Workflow

```
1. Check Jira Stories
   python agents/jira_agent.py

2. Create Feature Branch
   git checkout -b feature/story-name

3. Implement & Commit
   git add . && git commit && git push

4. Create PR with MR Agent
   python agents/mr_agent.py --title "..." --head "..." --base "..." --jira-issue "..."

5. Code Review
   (Team reviews on GitHub)

6. Merge & Deploy
   (Merge when approved)
```

---

## ✨ Features

✅ Create GitHub PRs  
✅ Validate branches  
✅ Check duplicates  
✅ Link to Jira  
✅ Add labels  
✅ Assign reviewers  
✅ Auto-descriptions  
✅ Draft PR support  
✅ Error handling  
✅ Cross-platform  

---

## 📞 Quick Links

- Help: `python test_mr_agent_setup.py`
- Quick Start: `MR_AGENT_QUICKSTART.md`
- Setup: `MR_AGENT_SETUP_CHECKLIST.md`
- Full Docs: `agents/MR_AGENT.md`

---

## 🎯 Next Steps

1. Get GitHub token (2 min)
2. Add to .env (1 min)
3. Run validation (1 min)
4. Create first PR (1 min)

**Total: 5 minutes!**

---

## 💡 Pro Tips

- Always use `--jira-issue` for traceability
- Use `--draft` for work-in-progress
- Request reviewers with `--reviewers`
- Test with dummy branch first
- Run validation if stuck

---

## 🎉 Status

✅ **READY TO USE**

Everything is set up and ready!

Just add your GitHub token to .env and go!

---

**Print this page or bookmark it for quick reference!**

