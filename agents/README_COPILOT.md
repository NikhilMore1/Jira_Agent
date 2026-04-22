# 🤖 Agent Configuration Guide

This folder contains **3 autonomous agents** configured as Markdown files for use with **GitHub Copilot**.

Each agent is a standalone Copilot configuration that can be loaded into your IDE and used directly.

---

## 📋 Agents Overview

| Agent | File | Purpose |
|-------|------|---------|
| **Jira Agent** | `JIRA_AGENT.md` | Reads Jira board, extracts stories assigned to you |
| **Code Agent** | `CODE_AGENT.md` | Generates Spring Boot Java code from stories |
| **Test Agent** | `TEST_AGENT.md` | Writes JUnit 5 tests for the generated code |

---

## 🚀 How to Use with GitHub Copilot

### Step 1: Open any agent MD file
```
Open: agents/JIRA_AGENT.md (or CODE_AGENT.md or TEST_AGENT.md)
```

### Step 2: Ask Copilot to follow the agent role
```
@copilot You are the Jira Agent. Follow the role and instructions in this file.
I want to fetch stories for "Nikhil Sharadmore" from board: https://epam.atlassian.net/jira/software/projects/DEMO/boards/1
```

### Step 3: Copilot executes as the agent
The agent will:
- Read the Jira API requirements
- Use your Jira credentials from environment
- Return structured story data

---

## 📝 Configuration Files

Each agent MD file contains:

1. **ROLE** – What the agent does
2. **CONTEXT** – Background and constraints
3. **INPUTS** – What you give it
4. **OUTPUTS** – What it produces
5. **INSTRUCTIONS** – Step-by-step tasks
6. **EXAMPLES** – Sample usage

---

## 🔧 Environment Setup

Before using agents, ensure these are set in your shell:

```powershell
# Jira credentials
$env:JIRA_BASE_URL = "https://epam.atlassian.net"
$env:JIRA_EMAIL = "nikhil_sharadmore@epam.com"
$env:JIRA_API_TOKEN = "HhgjXYsKuC8Uc0kHYiYeuI0sW7T8Pp7JbiopDB"

# Project path
$env:PROJECT_ROOT = "C:\Users\NikhilSharadMore\Downloads\demo (1)\demo"
```

---

## 📌 Quick Example

**1. Fetch Jira stories:**
```
@copilot Use JIRA_AGENT.md. Fetch stories for Nikhil Sharadmore from DEMO board.
```

**2. Generate code:**
```
@copilot Use CODE_AGENT.md. From the stories above, generate Patient entity, repository, service, and controller.
```

**3. Write tests:**
```
@copilot Use TEST_AGENT.md. Write JUnit 5 tests for the Patient code generated above.
```

---

## ✅ No Python. No Framework. Pure Copilot Chat.

All three agents work directly in GitHub Copilot Chat within your IDE — no installation, no dependencies, no runtime required.

