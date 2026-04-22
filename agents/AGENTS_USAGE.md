# 📖 How to Use the 3 Agents with GitHub Copilot

## Overview

You now have **3 markdown-based agents** that work directly with GitHub Copilot Chat in your IDE.

No Python. No installation. Just open the files and chat with Copilot.

---

## 🎯 Complete Workflow

### **Phase 1: Read Jira Stories (JIRA Agent)**

**Step 1:** Open `agents/JIRA_AGENT.md` in your IDE

**Step 2:** In GitHub Copilot Chat, write:
```
@copilot You are the Jira Agent as defined in agents/JIRA_AGENT.md.

Board URL: https://epam.atlassian.net/jira/software/projects/DEMO/boards/1
Assignee: Nikhil Sharadmore

Fetch all stories assigned to me and list them clearly.
```

**Step 3:** Copilot will:
- ✅ Use your Jira credentials
- ✅ Query the DEMO board
- ✅ Filter by "Nikhil Sharadmore"
- ✅ Return structured story list

**Example Output:**
```
✅ Found 2 stories for 'Nikhil Sharadmore' in project 'DEMO':

──────────────────────────────────────────
KEY: DEMO-101
SUMMARY: Create Patient Management API
STATUS: To Do
PRIORITY: High
POINTS: 5

DESCRIPTION:
Build a Patient entity and REST API with:
- Entity: Patient (id, name, email, phone, age)
- Endpoints: POST, GET (list), GET (by id), DELETE
- Use pagination for list endpoint

ACCEPTANCE CRITERIA:
✓ POST /api/v1/patients → 201
✓ GET /api/v1/patients → 200 with pagination
✓ GET /api/v1/patients/{id} → 200
✓ DELETE /api/v1/patients/{id} → 204

──────────────────────────────────────────
KEY: DEMO-102
SUMMARY: Add Appointment Scheduling
...
```

---

### **Phase 2: Generate Code (CODE Agent)**

**Step 1:** Open `agents/CODE_AGENT.md` in your IDE

**Step 2:** Copy the story from Phase 1 and ask Copilot:
```
@copilot You are the Code Agent as defined in agents/CODE_AGENT.md.

From the story above (DEMO-101 - Patient API):

Generate all 5 Java files:
1. Patient.java (entity)
2. PatientRepository.java (repository)
3. PatientService.java (interface)
4. PatientServiceImpl.java (implementation)
5. PatientController.java (controller)

Use the project structure: com.springsequrity.demo.*
```

**Step 3:** Copilot will generate complete, production-ready code

**Step 4:** Copy each generated class and save to the project:
```
src/main/java/com/springsequrity/demo/entity/Patient.java
src/main/java/com/springsequrity/demo/repository/PatientRepository.java
src/main/java/com/springsequrity/demo/service/PatientService.java
src/main/java/com/springsequrity/demo/service/PatientServiceImpl.java
src/main/java/com/springsequrity/demo/controllers/PatientController.java
```

**Example Generated Code:**
```java
// Patient.java
@Entity
public class Patient {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    
    @Column(length = 100, nullable = false)
    private String name;
    
    @Column(unique = true)
    private String email;
    
    private int age;
    private long phone;
    
    // getters/setters...
}

// PatientController.java
@RestController
@RequestMapping("/api/v1/patients")
public class PatientController {
    @Autowired
    private PatientService patientService;
    
    @PostMapping
    public ResponseEntity<Patient> createPatient(@RequestBody Patient patient) { ... }
    
    @GetMapping
    public ResponseEntity<Page<Patient>> getAllPatients(...) { ... }
    
    // ...
}
```

---

### **Phase 3: Write Tests (TEST Agent)**

**Step 1:** Open `agents/TEST_AGENT.md` in your IDE

**Step 2:** Ask Copilot:
```
@copilot You are the Test Agent as defined in agents/TEST_AGENT.md.

Write JUnit 5 tests for the Patient code generated in Phase 2.

Entity: Patient
Service: PatientServiceImpl
Controller: PatientController

Tests must cover all acceptance criteria from DEMO-101:
✓ POST creates patient (201)
✓ GET lists with pagination (200)
✓ GET by id returns patient (200)
✓ GET by id returns 404 if not found
✓ DELETE removes patient (204)

Generate both test classes:
- PatientServiceImplTest.java
- PatientControllerTest.java
```

**Step 3:** Copilot will generate comprehensive JUnit 5 tests

**Step 4:** Save test files to:
```
src/test/java/com/springsequrity/demo/service/PatientServiceImplTest.java
src/test/java/com/springsequrity/demo/controllers/PatientControllerTest.java
```

**Step 5:** Run tests:
```powershell
cd "C:\Users\NikhilSharadMore\Downloads\demo (1)\demo"
mvn test
```

**Example Test Output:**
```
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.springsequrity.demo.service.PatientServiceImplTest
[INFO] PatientService Tests
[INFO]   ✓ Should save patient successfully
[INFO]   ✓ Should get all patients with pagination
[INFO]   ✓ Should get patient by ID
[INFO]   ✓ Should return null when patient not found
[INFO]   ✓ Should delete patient
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0

[INFO] Running com.springsequrity.demo.controllers.PatientControllerTest
[INFO] PatientController Tests
[INFO]   ✓ POST should create patient with 201 status
[INFO]   ✓ GET should return all patients with pagination
[INFO]   ✓ GET by ID should return patient
[INFO]   ✓ GET by ID should return 404 when not found
[INFO]   ✓ DELETE should remove patient with 204 status
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0

[INFO] -------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] -------------------------------------------------------
```

---

## 🔧 Environment Setup (One-time)

Before using the agents, set these environment variables in PowerShell:

```powershell
# Jira Configuration
$env:JIRA_BASE_URL = "https://epam.atlassian.net"
$env:JIRA_EMAIL = "nikhil_sharadmore@epam.com"
$env:JIRA_API_TOKEN = "HhgjXYsKuC8Uc0kHYiYeuI0sW7T8Pp7JbiopDB"

# Project Path
$env:PROJECT_ROOT = "C:\Users\NikhilSharadMore\Downloads\demo (1)\demo"
```

Or add to your PowerShell profile to make permanent:
```powershell
code $PROFILE  # Opens your profile file
```

Then paste the environment variables above.

---

## 📋 File Reference

| Agent | File | Use When |
|-------|------|----------|
| **Jira Agent** | `JIRA_AGENT.md` | You need to fetch and read Jira stories |
| **Code Agent** | `CODE_AGENT.md` | You need to generate Spring Boot Java code |
| **Test Agent** | `TEST_AGENT.md` | You need to write JUnit 5 tests |

---

## 💬 Chat Examples

### Example 1: Full Workflow (Story → Code → Tests)

```
@copilot You are the Jira Agent from agents/JIRA_AGENT.md.
Board: https://epam.atlassian.net/jira/software/projects/DEMO/boards/1
Assignee: Nikhil Sharadmore
Fetch my stories.
```

*Then copy the first story and ask:*

```
@copilot You are the Code Agent from agents/CODE_AGENT.md.
Generate code for the story above (the Patient API story).
```

*Then copy the generated code and ask:*

```
@copilot You are the Test Agent from agents/TEST_AGENT.md.
Write tests for the Patient code above.
```

---

### Example 2: Quick Code Generation

```
@copilot You are the Code Agent from agents/CODE_AGENT.md.

Generate code for an Appointment entity with:
- id (auto)
- patientId (int)
- doctorId (int)
- appointmentDate (LocalDateTime)
- status (String)

Full CRUD API with pagination.
Endpoints: POST, GET (list), GET (by id), DELETE
```

---

### Example 3: Test-Driven Development

```
@copilot You are the Test Agent from agents/TEST_AGENT.md.

Write tests for UserService with these requirements:
- Create user (name, email, phone)
- List users with pagination
- Get user by ID
- Delete user
- Handle not-found errors (return null)

Generate: UserServiceImplTest.java and UserControllerTest.java
```

---

## ✅ Verification Checklist

After completing the workflow:

- [ ] Phase 1: Jira stories fetched and understood
- [ ] Phase 2: 5 Java files generated and placed in correct directories
- [ ] Phase 3: 2 test classes generated and placed in correct directories
- [ ] `mvn test` runs successfully with all tests passing
- [ ] `mvn clean install` succeeds with BUILD SUCCESS

---

## 🐛 Troubleshooting

### Issue: Copilot doesn't understand the agent role
**Solution**: Start with: `@copilot You are the Jira Agent as defined in agents/JIRA_AGENT.md`

### Issue: Generated code has import errors
**Solution**: Ask Copilot: "Add missing imports and fix compilation errors"

### Issue: Tests are failing
**Solution**: Ask Copilot: "Why is this test failing? Fix the assertion"

### Issue: Jira API returns 401 Unauthorized
**Solution**: Check your JIRA_API_TOKEN in .env is correct and not expired

---

## 🎓 Pro Tips

1. **Be specific**: The more details you provide, the better code Copilot generates
2. **Reference files**: Use `@copilot agents/JIRA_AGENT.md` to ensure Copilot reads the full spec
3. **Iterate**: If output isn't perfect, ask Copilot to refine it
4. **Copy-paste**: When Copilot generates code, copy it directly into your IDE
5. **Compile early**: After each phase, verify with `mvn clean compile`

---

## 🚀 Summary

```
📖 Open JIRA_AGENT.md → Ask Copilot → Get Stories
   ↓
💻 Open CODE_AGENT.md → Ask Copilot → Get Code
   ↓
🧪 Open TEST_AGENT.md → Ask Copilot → Get Tests
   ↓
✅ Run: mvn test → All tests pass → Done!
```

---

**Questions?** Review the individual agent files (JIRA_AGENT.md, CODE_AGENT.md, TEST_AGENT.md) for detailed specifications and examples.

