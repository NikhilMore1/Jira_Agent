# 🔀 MR Agent (GitHub Pull Request Agent)

## Overview

The **MR Agent** is an automated tool that creates GitHub Pull Requests (Merge Requests) with comprehensive formatting, descriptions, and metadata. It integrates seamlessly with Jira to link issues and helps maintain code quality through automated PR creation.

## Features

✅ **Create Pull Requests** - Automated PR creation with proper formatting  
✅ **Branch Validation** - Ensures branches exist before creating PR  
✅ **Jira Integration** - Link PRs to Jira issues automatically  
✅ **Label Management** - Add custom labels to PRs  
✅ **Assignee Assignment** - Assign reviewers and owners  
✅ **Draft PRs** - Support for draft/WIP pull requests  
✅ **Formatted Descriptions** - Auto-generates PR descriptions with checklist  
✅ **Error Handling** - Graceful error messages and validation  

---

## Setup

### 1. Get GitHub Personal Access Token

1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens
2. Click "Generate new token"
3. Select these scopes:
   - `repo` (full control of private repositories)
   - `read:org` (read organization data)
4. Copy the token

### 2. Update .env File

```env
# GitHub Configuration
GITHUB_API_URL=https://api.github.com
GITHUB_BASE_URL=https://github.com
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_OWNER=YourGitHubUsername
GITHUB_REPO=your-repository-name
```

### 3. Test Setup

```bash
python agents/mr_agent.py --help
```

---

## Usage

### Basic Usage

```bash
python agents/mr_agent.py \
  --title "Feature: Add User Authentication" \
  --head "feature/user-auth" \
  --base "develop" \
  --description "Implements OAuth2 authentication with JWT tokens"
```

### Advanced Usage with All Options

```bash
python agents/mr_agent.py \
  --title "Feature: Implement JWT Authentication" \
  --head "feature/jwt-auth" \
  --base "develop" \
  --description "Implements JWT-based authentication with refresh tokens" \
  --labels "feature,security,backend" \
  --assignees "john-reviewer,jane-reviewer" \
  --reviewers "john-reviewer,jane-reviewer" \
  --jira-issue "EPMICMPSTP-789" \
  --changes "Added JwtTokenProvider service,Implemented JWT filter,Created RefreshToken model" \
  --owner "YourOrg" \
  --repo "your-repo"
```

### Using Draft PRs (Work in Progress)

```bash
python agents/mr_agent.py \
  --title "[WIP] Feature: New Feature" \
  --head "feature/new-feature" \
  --base "develop" \
  --description "Work in progress, not ready for review yet" \
  --draft
```

---

## Command Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--title` | ✅ Yes | PR title |
| `--head` | ✅ Yes | Source branch (e.g., `feature/auth`) |
| `--base` | ✅ Yes | Target branch (e.g., `develop`) |
| `--description` | ❌ No | PR description (markdown) |
| `--labels` | ❌ No | Labels (comma-separated: `feature,auth,high-priority`) |
| `--assignees` | ❌ No | Assignees (comma-separated usernames) |
| `--reviewers` | ❌ No | Code reviewers (comma-separated usernames) |
| `--jira-issue` | ❌ No | Related Jira issue (e.g., `PROJ-123`) |
| `--changes` | ❌ No | Changes made (comma-separated) |
| `--draft` | ❌ No | Create as draft PR (no value needed) |
| `--owner` | ❌ No | GitHub owner/org (default from .env) |
| `--repo` | ❌ No | GitHub repository (default from .env) |

---

## Workflow Integration

### From Jira Story to GitHub PR

```
1. Read Jira Story (jira_agent.py)
   ↓
2. Develop on Feature Branch
   ↓
3. Create PR (mr_agent.py)
   ↓
4. Link to Jira Issue
   ↓
5. Code Review
   ↓
6. Merge & Deploy
```

### Example Workflow

```bash
# Step 1: Fetch Jira story details
python agents/jira_agent.py

# Step 2: Check out feature branch
git checkout -b feature/auth-otp

# Step 3: Develop and commit changes
git add .
git commit -m "feat: add OTP verification for password reset"
git push origin feature/auth-otp

# Step 4: Create PR linked to Jira
python agents/mr_agent.py \
  --title "Feature: Forgot Password with OTP Verification" \
  --head "feature/auth-otp" \
  --base "develop" \
  --description "Implements OTP-based password reset flow" \
  --labels "feature,authentication,backend" \
  --jira-issue "EPMICMPSTP-713"
```

---

## Auto-Generated PR Description

The agent automatically generates a PR description with:

```markdown
# Your custom description

## Related Issue
Closes #EPMICMPSTP-713

## Changes Made
- Added OTP validation service
- Implemented email sending
- Created password reset endpoint
- Added security tests

## Testing
- [ ] Tested locally
- [ ] Tests pass
- [ ] No console errors

## Checklist
- [ ] Code follows style guidelines
- [ ] No breaking changes
- [ ] Documentation updated
- [ ] Tests added/updated
```

---

## Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `GITHUB_TOKEN not set` | Token missing in .env | Add your GitHub Personal Access Token |
| `Branch not found` | Head or base branch doesn't exist | Create the branch first with `git push` |
| `PR already exists` | PR from same branch already open | Close existing PR or use different branch |
| `Authentication failed` | Invalid token | Generate new token with proper scopes |
| `No push access` | Token doesn't have `repo` scope | Regenerate token with correct permissions |

---

## Output Example

```
🔀 GitHub MR Agent: Creating Pull Request...

📦 Repository: NikhilSharadMore/demo
🎯 Title: Feature: Add User Authentication
🌿 Branch: feature/user-auth → develop

🔍 Validating branches...
✅ Both branches exist

🔍 Checking for existing PRs...
✅ No existing PR

📤 Creating PR...

⚙️  Adding metadata...

======================================================================
✅ PULL REQUEST CREATED SUCCESSFULLY!
======================================================================

📋 PR #42: Feature: Add User Authentication
──────────────────────────────────────────────────────────────────────
🔗 URL: https://github.com/NikhilSharadMore/demo/pull/42
📊 Status: OPEN
🌿 Branch: feature/user-auth → develop
⏰ Created: 2024-01-15T10:30:00Z
🏷️  Labels: feature, security, backend
👤 Assignees: john-reviewer, jane-reviewer
👥 Reviewers: john-reviewer, jane-reviewer

📝 Description:
──────────────────────────────────────────────────────────────────────
   Implements OAuth2 authentication with JWT tokens for secure user login.
   
   ## Related Issue
   Closes #EPMICMPSTP-789
   
   ## Changes Made
   - Added JWT token provider service
   - Implemented authentication filter
   - Created token refresh logic
   ... (5 lines total)

======================================================================
💡 Next Steps:
   1. Add description and acceptance criteria
   2. Link to related Jira issue
   3. Wait for CI/CD to pass
   4. Request reviewers for code review
   5. Merge once approved
======================================================================
```

---

## Best Practices

### Branch Naming Conventions

```
feature/feature-name           - New feature
bugfix/bug-description         - Bug fix
hotfix/urgent-fix              - Urgent production fix
refactor/refactoring-name      - Code refactoring
docs/documentation-update      - Documentation
chore/dependency-update        - Dependencies or build
```

### PR Title Format

Use conventional commits:
```
feat: Add user authentication
fix: Resolve login timeout issue
docs: Update API documentation
refactor: Simplify auth module
```

### Description Guidelines

1. **Clear Summary** - What does this PR do?
2. **Why** - Why is this change needed?
3. **How** - How does it work?
4. **Testing** - How to test it?
5. **Checklist** - Before merging checklist

---

## Troubleshooting

### Test Connection
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('GITHUB_TOKEN:', 'SET' if os.getenv('GITHUB_TOKEN') else 'NOT SET')
print('GITHUB_OWNER:', os.getenv('GITHUB_OWNER'))
print('GITHUB_REPO:', os.getenv('GITHUB_REPO'))
"
```

### Validate Token
```bash
python -c "
import requests
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}
r = requests.get('https://api.github.com/user', headers=headers)
print(f'Status: {r.status_code}')
print(f'User: {r.json().get(\"login\")}' if r.status_code == 200 else f'Error: {r.text}')
"
```

---

## Integration with Code Agent

The MR Agent works with the **Code Agent** in this workflow:

1. **Code Agent** - Implements Jira story requirements
2. **MR Agent** - Creates PR for code review
3. **CI/CD** - Automated tests run on PR
4. **Code Review** - Team reviews PR
5. **Merge** - Merge when approved

---

## Notes

- **Draft PRs**: Use for work-in-progress. Convert to ready when done.
- **Auto-linking**: GitHub auto-links PRs mentioning `#ISSUE_NUMBER`
- **Templates**: Some repos have PR templates in `.github/PULL_REQUEST_TEMPLATE.md`
- **Permissions**: Ensure token has `repo` and `read:org` scopes
- **Rate Limiting**: GitHub allows 5,000 requests/hour with token
- **Protected Branches**: Some branches require approvals before merge

---

## Related Agents

- **Jira Agent** (`agents/jira_agent.py`) - Fetch user stories
- **Code Agent** (`agents/code_agent.py`) - Implement features
- **Test Agent** (`agents/test_agent.py`) - Write and run tests
- **MR Agent** (`agents/mr_agent.py`) - Create pull requests

---

## Support

For issues or questions:
1. Check the `.env` file configuration
2. Verify GitHub token has proper scopes
3. Ensure branches exist and are pushed
4. Review error messages for specific issues

Last Updated: 2024-01-15

