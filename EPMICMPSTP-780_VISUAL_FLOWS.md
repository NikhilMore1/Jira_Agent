# EPMICMPSTP-780: Visual Flow Diagrams

## Request Flow Diagram

```
┌─────────────────────┐
│   CLIENT REQUEST    │
│  POST /api/v1/...   │
│  ability-scores/    │
│  recalculate        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  AbilityScoreController             │
│  @PostMapping("/recalculate")       │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  STEP 1: Basic Validation           │
│  ✓ Role is "P" or "U"?             │
│  ✓ Period format YYYY-MM?          │
│  ✓ Not null?                        │
└──────────┬──────────────────────────┘
           │
           ├─── IF INVALID ──────────────┐
           │                             │
           ▼                             ▼
    ✅ VALID                      ❌ 400 Bad Request
           │                             │
           ▼                             ▼
┌─────────────────────────────────────┐ │
│  STEP 2: Conditional Validation     │ │
│  If role="P":                       │ │
│    ✓ practicename not empty?        │ │
│  If role="U":                       │ │
│    ✓ employeeUid > 0?               │ │
└──────────┬──────────────────────────┘ │
           │                             │
           ├─── IF INVALID ────────────┐ │
           │                           │ │
           ▼                           ▼ ▼
    ✅ VALID                   ❌ 400 Bad Request
           │                           │
           ▼                           ▼
┌─────────────────────────────────────┐─────────────────┐
│  AbilityScoreRecalculationService   │  Return Error   │
│  recalculateAbilityScores()         │  Response       │
└──────────┬──────────────────────────┘─────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  STEP 3: Determine Scope            │
├─────────────────────────────────────┤
│  IF role="P":                       │
│    scope = PRACTICE                 │
│    practicename = "java"            │
│                                     │
│  IF role="U":                       │
│    scope = USER                     │
│    employeeUid = 456789             │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  STEP 4: Get Employees in Scope     │
├─────────────────────────────────────┤
│  IF scope=PRACTICE:                 │
│    Query employees where             │
│    practice="java"                  │
│    Result: [emp1, emp2, emp3]       │
│                                     │
│  IF scope=USER:                     │
│    Result: [emp]                    │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  STEP 5: Process Each Employee      │
│  FOR each employee IN scope:        │
│    ┌──────────────────────────┐     │
│    │ Calculate weighted score │     │
│    │ (using external service) │     │
│    └────────────┬─────────────┘     │
│                 ▼                    │
│    ┌──────────────────────────┐     │
│    │ Check if record exists   │     │
│    │ for (employee, period)   │     │
│    └──────────┬───────────────┘     │
│              / \                    │
│             /   \                   │
│        YES /     \ NO               │
│          /         \                │
│         ▼           ▼               │
│    UPDATE       CREATE              │
│    RECORD       NEW RECORD          │
│      + save ability score           │
│      + set status="COMPLETED"       │
│      ✓ Increment count             │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  STEP 6: Return Response            │
│  ✓ status: "ACCEPTED"              │
│  ✓ message: "Recalculation..."     │
│  ✓ count: number_processed         │
│  ✓ period: "2026-03"               │
│  ✓ HTTP 202 ACCEPTED               │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│  CLIENT RECEIVES RESPONSE}           │
│  {                                  │
│    "status": "ACCEPTED",            │
│    "count": 3,                      │
│    "period": "2026-03"              │
│  }                                  │
└─────────────────────────────────────┘
```

---

## Practice-Level Scope Processing

```
REQUEST:
{
  "role": "P",
  "practicename": "java",
  "period": "2026-03"
}

         ▼

SCOPE DETERMINATION:
  Role = "P" (Practice)
  Practice = "java"

         ▼

FETCH EMPLOYEES:
  Query: "Get all employees in 'java' practice"
  
  ┌──────────────────────────────────┐
  │  EmployeeService or DB Query     │
  │  WHERE practice = 'java'         │
  └──────────────────────────────────┘
  
         ▼
  
  RESULTS: 3 employees
  [
    { id: 456789, name: "John", practice: "java" },
    { id: 456790, name: "Jane", practice: "java" },
    { id: 456791, name: "Bob", practice: "java" }
  ]

         ▼

PROCESS EACH:

  ┌─────────────────────────────────────────────────┐
  │ Employee 1 (ID: 456789)                         │
  ├─────────────────────────────────────────────────┤
  │ Calculate Score → WeightedScoreCalculatorService│
  │ Score: 78.5                                     │
  │ Save: AbilityScore(emp=456789, period=2026-03)  │
  └─────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────┐
  │ Employee 2 (ID: 456790)                         │
  ├─────────────────────────────────────────────────┤
  │ Calculate Score → WeightedScoreCalculatorService│
  │ Score: 82.3                                     │
  │ Save: AbilityScore(emp=456790, period=2026-03)  │
  └─────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────┐
  │ Employee 3 (ID: 456791)                         │
  ├─────────────────────────────────────────────────┤
  │ Calculate Score → WeightedScoreCalculatorService│
  │ Score: 85.0                                     │
  │ Save: AbilityScore(emp=456791, period=2026-03)  │
  └─────────────────────────────────────────────────┘

         ▼

RESPONSE:
{
  "status": "ACCEPTED",
  "message": "Recalculation started",
  "period": "2026-03",
  "role": "P",
  "scope": "PRACTICE",
  "count": 3  ◄─── 3 employees processed
}
```

---

## User-Level Scope Processing

```
REQUEST:
{
  "role": "U",
  "employeeUid": 456789,
  "period": "2026-03"
}

         ▼

SCOPE DETERMINATION:
  Role = "U" (User/Employee)
  EmployeeUid = 456789

         ▼

FETCH EMPLOYEES:
  Scope is single employee
  
  List = [456789]  ◄─── Just one employee

         ▼

PROCESS:

  ┌──────────────────────────────────────────────┐
  │ Employee (ID: 456789)                        │
  ├──────────────────────────────────────────────┤
  │ Calculate Score → WeightedScoreCalculatorService
  │ Score: 78.5                                  │
  │ Save: AbilityScore(emp=456789, period=2026-03)
  └──────────────────────────────────────────────┘

         ▼

RESPONSE:
{
  "status": "ACCEPTED",
  "message": "Recalculation started",
  "period": "2026-03",
  "role": "U",
  "scope": "USER",
  "count": 1  ◄─── Only 1 employee processed
}
```

---

## Validation Decision Tree

```
                    ┌──── START ────┐
                    │   New Request │
                    └────────┬──────┘
                             │
                    ┌────────▼────────┐
                    │ role provided?  │
                    └─┬──────────┬────┘
                      │          │
                     NO         YES
                      │          │
                      ▼          ▼
                    ❌          ┌──────────────┐
                    FAIL        │role="P"|"U"?│
                                └─┬──────┬────┘
                                  │      │
                                 NO    YES
                                  │      │
                                  ▼      ▼
                                ❌      ┌────────────────┐
                                FAIL    │period provided?│
                                        └─┬────────┬─────┘
                                          │        │
                                         NO       YES
                                          │        │
                                          ▼        ▼
                                        ❌        ┌──────────────────┐
                                        FAIL      │period=YYYY-MM?   │
                                                  └─┬──────────┬─────┘
                                                    │          │
                                                   NO         YES
                                                    │          │
                                                    ▼          ▼
                                                  ❌          ┌─────────┐
                                                  FAIL        │role="P"?│
                                                              └─┬───┬───┘
                                                                │   │
                                                               YES  NO
                                                                │   │
                                ┌───────────────────┐         ▼   │
                                │ role="U"        │ ┌─────────────┐
                                │ employeeUid?    │ │practicename?│
                                └─┬───┬───┬───────┘ └─┬──────┬────┘
                                  │   │   │          │      │
                          EMPTY NO │   │ YES        NO     YES
                            or ≤0  │   │            │      │
                                   │   │            ▼      ▼
                                   ▼   ▼           ❌      ✅
                                  ❌ ✅          FAIL    VALID
                                 FAIL VALID
```

---

## API Contract Summary

### Request Schema
```
{
  "type": "object",
  "required": ["role", "period"],
  "properties": {
    "role": {
      "type": "string",
      "enum": ["P", "U"],
      "description": "Processing scope: P=Practice, U=User"
    },
    "practicename": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "description": "Required if role=P"
    },
    "employeeUid": {
      "type": "integer",
      "format": "int64",
      "minimum": 1,
      "description": "Required if role=U"
    },
    "period": {
      "type": "string",
      "pattern": "^\\d{4}-(0[1-9]|1[0-2])$",
      "example": "2026-03",
      "description": "YYYY-MM format, months 01-12"
    }
  }
}
```

### Response Schema (202 ACCEPTED)
```
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": ["ACCEPTED", "FAILED"],
      "description": "Processing status"
    },
    "message": {
      "type": "string",
      "description": "Human-readable message"
    },
    "period": {
      "type": "string",
      "example": "2026-03"
    },
    "role": {
      "type": "string",
      "enum": ["P", "U"]
    },
    "scope": {
      "type": "string",
      "enum": ["PRACTICE", "USER"]
    },
    "count": {
      "type": "integer",
      "description": "Number of employees processed"
    },
    "errorMessage": {
      "type": "string",
      "description": "Error details if status=FAILED"
    },
    "timestamp": {
      "type": "integer",
      "format": "int64",
      "description": "Response timestamp in millis"
    }
  }
}
```

---

## Database Schema

```sql
CREATE TABLE ability_scores (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    employee_uid BIGINT NOT NULL,
    period VARCHAR(7) NOT NULL,                    -- YYYY-MM format
    weighted_score DOUBLE,
    practice_name VARCHAR(100),
    status VARCHAR(50) NOT NULL DEFAULT 'COMPLETED',
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    KEY idx_employee_period (employee_uid, period),
    KEY idx_period (period),
    UNIQUE KEY unique_employee_period (employee_uid, period)
);
```

---

## Class Structure Overview

```
com.springsequrity.demo
│
├── controller/
│   └── AbilityScoreController
│       └── @PostMapping("/api/v1/ability-scores/recalculate")
│
├── service/
│   └── AbilityScoreRecalculationService
│       ├── recalculateAbilityScores()
│       ├── validateRequest()
│       ├── determineScope()
│       ├── getEmployeesInScope()
│       └── processRecalculation()
│
├── repository/
│   └── AbilityScoreRepository
│       ├── findByEmployeeUidAndPeriod()
│       ├── save()
│       └── [query methods...]
│
├── model/
│   └── AbilityScore
│       ├── id
│       ├── employeeUid
│       ├── period
│       ├── weightedScore
│       ├── practiceName
│       ├── status
│       └── timestamps
│
├── dto/
│   ├── RecalculateAbilityScoreRequest
│   │   ├── role
│   │   ├── practicename
│   │   ├── employeeUid
│   │   └── period
│   │
│   └── RecalculationResponse
│       ├── status
│       ├── message
│       ├── period
│       ├── count
│       └── metadata
│
└── exception/
    └── InvalidAbilityScoreRequestException
```

---

## Data Flow Example: Practice-Level

```
CLIENT REQUEST:
POST /api/v1/ability-scores/recalculate
Content-Type: application/json

{
  "role": "P",
  "practicename": "java",
  "period": "2026-03"
}

         ▼ (Validation passes)

IN MEMORY PROCESSING:
      Practice = "java"
      Period = "2026-03"
      EmployeeIds = [456789, 456790, 456791]

         ▼ (Loop through employees)

DATABASE OPERATIONS:
      INSERT/UPDATE ability_scores
      SET weighted_score = 78.5
      WHERE employee_uid = 456789 AND period = "2026-03"
      
      INSERT/UPDATE ability_scores
      SET weighted_score = 82.3
      WHERE employee_uid = 456790 AND period = "2026-03"
      
      INSERT/UPDATE ability_scores
      SET weighted_score = 85.0
      WHERE employee_uid = 456791 AND period = "2026-03"

         ▼ (Response prepared)

HTTP RESPONSE (202):
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

---

## Error Handling Flow

```
                    CLIENT REQUEST
                           │
                           ▼
                ┌───────────────────────┐
                │  Parse JSON Body     │
                └──────────┬────────────┘
                           │
                      ┌────▼─────┐
                      │ Success? │
                      └─┬──────┬─┘
                        │      │
                       YES    NO
                        │      │
                        ▼      ▼
                       ✅    400 Bad Request
                       │    (JSON parse error)
                       │
                       ▼
           ┌──────────────────────────┐
           │ Validate DTO fields      │
           │ (NotBlank, Pattern, etc) │
           └───┬────────────────────┬─┘
               │                    │
             Pass                 Fail
              │                     │
              ▼                     ▼
             ✅                  400 Bad Request
             │                   (Field validation)
             │
             ▼
  ┌──────────────────────────────┐
  │ Business Logic Validation    │
  │ (Conditional checks)         │
  └──┬──────────────────────────┬┘
     │                          │
   Pass                       Fail
    │                          │
    ▼                          ▼
   ✅                     400 Bad Request
   │                    (Business rule)
   │
   ▼
┌──────────────────────────────┐
│ Service Processing           │
│ (Calculate scores, save DB)  │
└───┬────────────────────────┬─┘
    │                        │
  Success                  Failure
    │                        │
    ▼                        ▼
   ✅                    500 Server Error
   202 ACCEPTED         (with error details)
```

---

*Visual diagrams for EPMICMPSTP-780*

