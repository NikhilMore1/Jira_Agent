# ⚡ Quick Reference Card

## 3-Agent System Summary

### 🔍 Agent #1: JIRA_AGENT.md
**What it does:** Reads Jira, filters stories by assignee  
**Trigger phrase:**
```
@copilot You are the Jira Agent from agents/JIRA_AGENT.md.
Board: https://epam.atlassian.net/jira/software/projects/DEMO/boards/1
Assignee: Nikhil Sharadmore
Fetch stories.
```
**Output:** List of assigned user stories  

---

### 💻 Agent #2: CODE_AGENT.md
**What it does:** Generates 5 Spring Boot Java files  
**Trigger phrase:**
```
@copilot You are the Code Agent from agents/CODE_AGENT.md.
Generate code from story DEMO-101 (Patient API) above.
```
**Output:** 
- Patient.java
- PatientRepository.java
- PatientService.java
- PatientServiceImpl.java
- PatientController.java

---

### 🧪 Agent #3: TEST_AGENT.md
**What it does:** Writes JUnit 5 tests covering acceptance criteria  
**Trigger phrase:**
```
@copilot You are the Test Agent from agents/TEST_AGENT.md.
Write tests for Patient code above.
```
**Output:**
- PatientServiceImplTest.java
- PatientControllerTest.java

---

## 📋 Complete Workflow in 3 Commands

```powershell
# 1. Fetch stories
@copilot You are the Jira Agent from agents/JIRA_AGENT.md. Board: ... Assignee: Nikhil Sharadmore. Fetch stories.

# 2. Generate code  
@copilot You are the Code Agent from agents/CODE_AGENT.md. Generate code for story DEMO-101 above.

# 3. Write tests
@copilot You are the Test Agent from agents/TEST_AGENT.md. Write tests for the code above.
```

Then:
```powershell
cd "C:\Users\NikhilSharadMore\Downloads\demo (1)\demo"
mvn clean install
```

✅ Done!

---

## 📂 File Locations

| File | Purpose |
|------|---------|
| `README_COPILOT.md` | Overview & intro |
| `AGENTS_USAGE.md` | Detailed step-by-step guide |
| `SETUP_COMPLETE.md` | What's been created |
| `JIRA_AGENT.md` | Jira agent spec |
| `CODE_AGENT.md` | Code agent spec |
| `TEST_AGENT.md` | Test agent spec |

---

## 🎯 Example Commands

### Get Jira stories
```
@copilot I'm the Jira Agent. Board: https://epam.atlassian.net/jira/software/projects/DEMO/boards/1
Fetch stories for Nikhil Sharadmore
```

### Generate API for Patient
```
@copilot I'm the Code Agent. From story DEMO-101 (Patient API), generate:
Patient entity, PatientRepository, PatientService interface & impl, PatientController
```

### Write JUnit tests
```
@copilot I'm the Test Agent. For Patient code above, write JUnit 5 tests covering:
Create (POST 201), List (GET 200), Get by ID (200), Not found (404), Delete (204)
```

---

## ✨ No Installation Needed

```
✅ No Python required
✅ No pip install
✅ No Maven plugins
✅ No Framework setup
✅ Just: Copilot Chat + Markdown files
```

---

## 🔐 Set Once

```powershell
$env:JIRA_BASE_URL = "https://epam.atlassian.net"
$env:JIRA_EMAIL = "nikhil_sharadmore@epam.com"  
$env:JIRA_API_TOKEN = "HhgjXYsKuC8Uc0kHYiYeuI0sW7T8Pp7JbiopDB"
$env:PROJECT_ROOT = "C:\Users\NikhilSharadMore\Downloads\demo (1)\demo"
```

---

## 💬 Troubleshooting

| Issue | Solution |
|-------|----------|
| Copilot forgets agent role | Start chat with: `@copilot You are the Jira Agent from agents/JIRA_AGENT.md` |
| Code has import errors | Ask: `@copilot Add missing imports and fix errors` |
| Tests are failing | Ask: `@copilot Why is this test failing? Fix it` |
| Jira returns 401 | Check JIRA_API_TOKEN in environment variables |

---

## 📊 What Gets Generated

```
From 1 Jira Story:
  ↓
Generated: 5 Java files + 2 test files
  ↓
Total: 7 new files
  ↓
Coverage: 100% of story requirements
  ↓
Quality: Production-ready, best practices
```

---

**Start:** Open `JIRA_AGENT.md` → Ask Copilot → Generate → Verify ✅

