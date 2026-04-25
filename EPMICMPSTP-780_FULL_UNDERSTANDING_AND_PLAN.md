# EPMICMPSTP-780: Complete Plan & Understanding

## 📌 EXECUTIVE SUMMARY

**Story:** Ability Score Pre-calculation Engine - Pre-calculate ability scores on-demand using WeightedScoreCalculatorService

**What it does:** Creates a new REST API endpoint that allows users to trigger on-demand calculation of employee ability scores for a specific time period, with flexible filtering (by Practice or by Individual Employee).

**Why it matters:** This enables organizations to recalculate performance metrics on-demand rather than waiting for scheduled batch processes, providing real-time insights.

---

## 🎯 STORY DETAILS

| Field | Value |
|-------|-------|
| **Story Key** | EPMICMPSTP-780 |
| **Type** | Story |
| **Status** | Open |
| **Priority** | Major |
| **Assignee** | Nikhil Sharad More |
| **Project** | EPMICMPSTP (DEC2026-JAVA-TEAM10) |
| **Created** | 2026-04-24 |
| **Updated** | 2026-04-24 |

---

## 📋 WHAT IS THIS STORY ASKING FOR?

### The Requirement
Create a **REST API endpoint** that can:
1. Accept requests to recalculate ability scores
2. Support two modes of operation:
   - **Practice-Level**: Calculate scores for ALL employees in a specific practice
   - **User-Level**: Calculate scores for ONE specific employee
3. Execute within a specific time period (month/year)
4. Return status confirmation and details

### The API Endpoint

```
POST /api/v1/ability-scores/recalculate
```

---

## 📥 INPUT: REQUEST FORMAT

### Request Body (JSON)
```json
{
  "role": "P",
  "practicename": "java",
  "employeeUid": 456789,
  "period": "2026-03"
}
```

### Field Definitions

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| **role** | String | ✅ YES | Determines scope: "P" (Practice) or "U" (User) | "P" or "U" |
| **practicename** | String | 🔄 CONDITIONAL | Name of practice - Required if role="P" | "java", "python", "devops" |
| **employeeUid** | Long | 🔄 CONDITIONAL | Employee ID - Required if role="U" | 456789 |
| **period** | String | ✅ YES | Time period in YYYY-MM format | "2026-03", "2026-04" |

### Conditional Logic

```
IF role = "P" (Practice)
  THEN practicename is REQUIRED
  AND employeeUid is NOT needed
  
IF role = "U" (User/Employee)
  THEN employeeUid is REQUIRED
  AND practicename is NOT needed
```

### Validation Rules

| Field | Validation |
|-------|-----------|
| role | Must be exactly "P" or "U" (case-sensitive?) |
| practicename | Non-empty string, max 100 chars |
| employeeUid | Must be > 0 (positive integer) |
| period | Format: YYYY-MM, Valid months: 01-12 |

---

## 📤 OUTPUT: RESPONSE FORMAT

### Success Response (HTTP 202 Accepted)
```json
{
  "status": "ACCEPTED",
  "message": "Recalculation started",
  "period": "2026-03",
  "role": "P",
  "scope": "PRACTICE",
  "count": 3,
  "timestamp": 1703123456789
}
```

### Error Response (HTTP 400/500)
```json
{
  "status": "FAILED",
  "message": "Validation failed",
  "errorMessage": "Practice name is required when role is 'P'",
  "timestamp": 1703123456789
}
```

### Response Fields

| Field | Purpose |
|-------|---------|
| **status** | ACCEPTED, PROCESSING, COMPLETED, FAILED |
| **message** | Human-readable summary |
| **period** | The period processed |
| **role** | The role used (P or U) |
| **scope** | PRACTICE or USER |
| **count** | Number of employees processed |
| **errorMessage** | If status=FAILED, error details |
| **timestamp** | When response was generated |

---

## 🔄 HOW IT WORKS: PROCESSING FLOW

### Step 1: Receive Request
User sends POST request with role and period

### Step 2: Validate
- Check role is "P" or "U"
- Check period is YYYY-MM format
- Check conditional requirements based on role
- Return 400 if validation fails

### Step 3: Determine Scope
```
If role = "P":
  → Find ALL employees in that practice
  → Example: java practice → employees [456789, 456790, 456791]

If role = "U":
  → Use the single employeeUid provided
  → Example: [456789]
```

### Step 4: Process Recalculation
For EACH employee in scope:
1. Call WeightedScoreCalculatorService
2. Get calculated ability score
3. Store result in database (create or update)
4. Track success/failure

### Step 5: Return Response
- Return 202 ACCEPTED (not 200 OK, because it's accepted for processing)
- Include count of employees processed
- Can be async (recommended) or synchronous

---

## 💡 SCOPE EXPLANATION

### Practice-Level Recalculation (role = "P")

**Request:**
```json
{
  "role": "P",
  "practicename": "java",
  "period": "2026-03"
}
```

**What happens:**
1. System finds all employees in Java practice
2. Suppose Java has: [Emp1: 456789, Emp2: 456790, Emp3: 456791]
3. For each employee, calculate ability score for 2026-03
4. Save 3 records to database
5. Return count=3

**Use case:** "Recalculate everyone's ability score for the Java team this month"

---

### User-Level Recalculation (role = "U")

**Request:**
```json
{
  "role": "U",
  "employeeUid": 456789,
  "period": "2026-03"
}
```

**What happens:**
1. System takes the specific employee (456789)
2. Calculate ability score for 2026-03
3. Save 1 record to database
4. Return count=1

**Use case:** "Recalculate John Doe's ability score for March 2026"

---

## 🗄️ DATABASE & DATA MODEL

### What needs to be stored?

```
AbilityScore Table
├── id (PK)
├── employeeUid (indexed)
├── period (indexed, e.g., "2026-03")
├── weightedScore (calculated value, 0-100)
├── practiceName (for reference)
├── status (COMPLETED, FAILED)
├── errorMessage (if failed)
├── createdAt (timestamp)
└── updatedAt (timestamp)
```

### Why these fields?
- **employeeUid + period**: Unique combination (one score per employee per month)
- **weightedScore**: The actual calculated score
- **status**: Track if calculation succeeded or failed
- **errorMessage**: Helps debug failures
- **timestamps**: Audit trail

---

## 🏗️ ARCHITECTURE: COMPONENTS NEEDED

### 1. **Entity/Model Layer**
```
AbilityScore.java
├── Database representation
├── JPA annotations
├── Getters/Setters (Lombok)
└── Business logic if any
```

### 2. **Data Transfer Objects (DTOs)**
```
RecalculateAbilityScoreRequest.java
├── Input validation
├── Field descriptions
└── Conditional validation logic

RecalculationResponse.java
├── Output format
├── Factory methods for responses
└── JSON serialization
```

### 3. **Repository Layer**
```
AbilityScoreRepository.java
└── Database queries:
    ├── Save/Update records
    ├── Find by employeeUid + period
    ├── Find by practice + period
    └── Query failed records
```

### 4. **Service Layer**
```
AbilityScoreRecalculationService.java
├── recalculateAbilityScores(request)
├── validateRequest()
├── determineScope()
├── getEmployeesInScope()
├── processRecalculation()
├── calculateWeightedScore()
└── error handling & logging
```

### 5. **Controller/API Layer**
```
AbilityScoreController.java
├── @PostMapping("/recalculate")
├── Request mapping
├── Input validation
├── Error handling
└── HTTP response status codes
```

### 6. **Exception Handling**
```
InvalidAbilityScoreRequestException.java
└── Custom exception for validation errors
```

---

## 🔗 INTEGRATION POINTS

### External Service: WeightedScoreCalculatorService

```
WHAT WE NEED TO KNOW:
├── Does it already exist in the codebase?
├── What parameters does it accept?
│   └── Probably: employeeUid, period
├── What does it return?
│   └── The calculated weighted score (Double, 0-100)
├── Does it have error handling?
└── Is it synchronous or asynchronous?

HOW TO USE IT:
Double score = weightedScoreCalculatorService.calculate(employeeUid, period);
```

### Employee Database/Service

```
WHAT WE NEED TO KNOW:
├── How do we get all employees in a practice?
├── Does an employee service exist?
├── Is there an employee-practice mapping table?
└── How to query employees by practice name?

MOCK IMPLEMENTATION:
java practice → [456789, 456790, 456791]
python practice → [456792, 456793]
devops practice → [456794, 456795, 456796]
```

---

## ⚠️ EDGE CASES & CONSIDERATIONS

### Question 1: What if no employees found?
**Case:** Request for practice that has no employees
```json
{
  "role": "P",
  "practicename": "nonexistent-practice",
  "period": "2026-03"
}
```
**Decision Needed:** 
- Return COMPLETED with count=0? OR
- Return error 404? OR
- Return ACCEPTED anyway?
**Best Practice:** Return COMPLETED with count=0 and message "No employees found in practice"

### Question 2: What if calculation fails for some employees?
**Case:** Out of 3 employees, 2 succeed, 1 fails
**Decision Needed:**
- Fail entire request? OR
- Partial success (return which ones failed)? OR
- Retry only failures?
**Best Practice:** Log failures, continue with others, track status per employee

### Question 3: Duplicate records handling?
**Case:** Same period recalculated twice
**Decision Needed:**
- Create new record (duplicate)? OR
- Update existing record? OR
- Reject duplicate?
**Best Practice:** Update existing record (idempotent operation)

### Question 4: Future dates allowed?
**Case:** Request for period "2026-12" in April 2026
**Decision Needed:**
- Allow? OR
- Reject?
**Best Practice:** Allow (might want future projections)

### Question 5: Past dates allowed?
**Case:** Request for period "2024-01" 
**Decision Needed:**
- Allow?
**Best Practice:** Allow (recalculate historical data)

### Question 6: Same month recalculation multiple times?
**Decision:** Idempotent - should return same result, update previous record

---

## ✅ TESTING STRATEGY

### Unit Tests Needed

```
1. Practice-Level Happy Path
   Input: role=P, practicename=java, period=2026-03
   Expected: status=ACCEPTED, count>0

2. User-Level Happy Path
   Input: role=U, employeeUid=456789, period=2026-03
   Expected: status=ACCEPTED, count=1

3. Invalid Role
   Input: role=X
   Expected: status=FAILED, error message

4. Missing Period
   Input: (no period field)
   Expected: status=FAILED, error

5. Invalid Period Format
   Input: period=2026-13 (invalid month)
   Expected: status=FAILED

6. Missing Practice Name (when role=P)
   Expected: status=FAILED

7. Invalid Employee UID (when role=U)
   Input: employeeUid=-1 or 0
   Expected: status=FAILED

8. Update Existing Record
   Run recalculation twice for same period
   Expected: Second run updates first record

9. Different Practice Scopes
   Test with java, python, devops practices
   Expected: Different counts

10. Empty Practice (no employees)
    Expected: count=0, status=COMPLETED
```

### Integration Tests

```
1. End-to-end POST request
2. Database persistence
3. Integration with WeightedScoreCalculatorService
4. Error scenarios
```

### Manual Testing with cURL

```bash
# Practice-level
curl -X POST http://localhost:8080/api/v1/ability-scores/recalculate \
  -H "Content-Type: application/json" \
  -d '{
    "role": "P",
    "practicename": "java",
    "period": "2026-03"
  }'

# User-level
curl -X POST http://localhost:8080/api/v1/ability-scores/recalculate \
  -H "Content-Type: application/json" \
  -d '{
    "role": "U",
    "employeeUid": 456789,
    "period": "2026-03"
  }'

# Invalid - missing period
curl -X POST http://localhost:8080/api/v1/ability-scores/recalculate \
  -H "Content-Type: application/json" \
  -d '{
    "role": "P",
    "practicename": "java"
  }'
```

---

## 📈 IMPLEMENTATION PHASES

### Phase 1: Database Setup
- Create `ability_scores` table
- Add indexes on (employee_uid, period)
- Add constraints

### Phase 2: Core Models & DTOs
- Create `AbilityScore` entity
- Create `RecalculateAbilityScoreRequest` DTO
- Create `RecalculationResponse` DTO

### Phase 3: Repository & Validation
- Create `AbilityScoreRepository`
- Add validation logic
- Create exception classes

### Phase 4: Service Logic
- Create `AbilityScoreRecalculationService`
- Implement scope determination
- Implement recalculation logic
- Add error handling

### Phase 5: Controller/API
- Create `AbilityScoreController`
- Implement POST endpoint
- Add route handling
- HTTP response codes

### Phase 6: Testing
- Unit tests for each component
- Integration tests
- Manual testing

### Phase 7: Documentation
- Swagger/OpenAPI docs
- README updates
- Code comments

---

## 🚀 SUCCESS CRITERIA

### Functional Requirements ✅
- [ ] Endpoint accepts POST requests
- [ ] Validates role ("P" or "U")
- [ ] Enforces conditional field requirements
- [ ] Calculates scores for requested scope
- [ ] Stores results in database
- [ ] Returns proper response format

### Non-Functional Requirements ✅
- [ ] Handles large practice groups (100+ employees)
- [ ] Proper error messages
- [ ] Logging at appropriate levels
- [ ] Database indexes for performance
- [ ] Transaction management

### Code Quality ✅
- [ ] Comprehensive unit tests (>80% coverage)
- [ ] No null pointer exceptions
- [ ] Proper exception handling
- [ ] Clear code comments
- [ ] Follows Spring best practices

---

## 📊 DECISION POINTS BEFORE IMPLEMENTATION

### 1. Synchronous vs Asynchronous Processing?
- **Sync:** Process immediately, return when done
- **Async:** Queue job, return immediately with job ID
- **Recommendation:** Async (for large practices)

### 2. Case-Sensitive Role?
- **Currently:** Assuming case-sensitive ("P" or "U", not "p" or "u")
- **Verify:** Confirm requirement

### 3. WeightedScoreCalculatorService Integration?
- **Need to:** Find existing service in codebase
- **Or:** Create mock if doesn't exist

### 4. Employee-Practice Mapping?
- **Need to:** Understand how employees link to practices
- **Is there:** An employee master table?

### 5. Authorization/Security?
- **Should:** Role-based access control (RBAC)?
- **Admin only:** Or any user can trigger?

### 6. Audit Trail?
- **Track:** Who triggered recalculation?
- **Log:** In separate audit table?

---

## 📝 QUESTIONS FOR PRODUCT/TEAM

1. ❓ Should recalculation be async or sync?
2. ❓ Where is the employee master data stored?
3. ❓ What's the maximum employees in a practice?
4. ❓ Should we validate that practice/employee exists?
5. ❓ Need authorization checks?
6. ❓ Historical data allowed?
7. ❓ Retry failed calculations?
8. ❓ Notification when complete (for async)?

---

## 🎓 KEY CONCEPTS

### REST Status Codes
- **202 ACCEPTED**: Request accepted for processing (async recommended)
- **200 OK**: Immediate success
- **400 Bad Request**: Validation failed
- **401 Unauthorized**: Auth required
- **403 Forbidden**: Permission denied
- **500 Internal Server Error**: Server error

### Request Validation Layers
1. **HTTP Layer**: Content-Type, method
2. **DTO Layer**: NotNull, Pattern, Size
3. **Business Layer**: Conditional logic
4. **Database Layer**: Constraints

### Scope vs Scale
- **Scope**: What data to process (practice or user)
- **Scale**: How much data (1 employee vs 1000)

---

## 🔍 UNDERSTANDING VERIFICATION

### If you understand this story, you should be able to answer:

1. ✅ What does role="P" mean?
   → Process all employees in a practice

2. ✅ What happens with role="U"?
   → Process one specific employee

3. ✅ Why is period required?
   → Ability scores are per time period (YYYY-MM)

4. ✅ What's the difference between POST /ability-scores and POST /ability-scores/recalculate?
   → Recalculate triggers computation; POST might just retrieve

5. ✅ Can the same employee-period be processed twice?
   → Yes, but should update existing record

6. ✅ What if WeightedScoreCalculatorService fails?
   → Log failure, continue with others, mark as FAILED

7. ✅ What determines if request is valid?
   → Role check, conditional field checks, period format

---

## 📋 DEPENDENCY CHECKLIST

### Required Dependencies
- [ ] Spring Boot Web
- [ ] Spring Data JPA
- [ ] Validation (jakarta.validation)
- [ ] Lombok (optional but recommended)
- [ ] Database driver (H2/PostgreSQL)

### Existing Services to Integrate
- [ ] WeightedScoreCalculatorService
- [ ] Employee Service (to get employees by practice)
- [ ] Database schema exists?

### Documentation
- [ ] Swagger/OpenAPI
- [ ] API endpoint documentation
- [ ] Code comments

---

*Generated: 2026-04-25 for Nikhil Sharad More*
*Story: EPMICMPSTP-780*

