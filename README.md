# Functional Specification Document (FSD)

A Cursor agent skill that generates comprehensive, implementation-ready Functional Specification Documents. It defines system functionality, business rules, user interactions, acceptance criteria, data models, and error handling — focusing on **what** the system must do, not how to build it.

Every generated FSD follows a structured 9-section template, uses MoSCoW prioritization, GIVEN/WHEN/THEN acceptance criteria, and hierarchical requirement IDs (FR-X.Y.Z) for full traceability from spec to test to implementation.

---

## Installation

```bash
npx skills add https://github.com/rahmat1929/skill-functional-specification-document --skill functional-specification-document
```

### Verify installation

After installing, the skill should appear in Cursor's skill list. Test it by asking the agent:

> "Create a functional spec for the authentication module"

If it responds by asking clarifying questions or generating an FSD, the skill is active.

---

## Skill Contents

```
functional-specification-document/
├── SKILL.md                        # Main skill instructions & workflow
├── README.md                       # This file
├── CHANGELOG.md                    # Version history
├── references/
│   └── fsd-template.md             # Complete FSD template (9 sections) with examples
└── scripts/
    └── validate_fsd.py             # Automated FSD structural validator
```

---

## How It Works

The skill follows a 4-phase workflow:

| Phase | What happens |
|-------|-------------|
| **1. Gather Context** | Reads your PRD/brief or runs an interactive interview to understand the system |
| **2. Write the FSD** | Generates a full document following the 9-section template with requirement IDs, acceptance criteria, and priority labels |
| **3. Output & Validate** | Saves as `FSD-[Project-Name].md` and runs the validation script to check structural completeness |
| **4. Review & Iterate** | Presents the draft with flagged assumptions, incorporates feedback, re-validates |

---

## Usage Examples

### Example 1: Interactive — Spec a new system from scratch

Just describe what you want. The skill triggers automatically.

**Prompt:**

> I need a functional spec for a food delivery app. It should support customer ordering, restaurant management, and a driver tracking system.

**What happens:**

The agent starts an interview to gather context:

> *"Got it — a food delivery platform with three user types. Let me understand the scope:*
> 1. *Who are the user roles? (e.g., Customer, Restaurant Owner, Driver, Admin)*
> 2. *What are the core workflows each role performs?"*

You answer, it asks targeted follow-ups, and once it has enough context it generates the full FSD and saves it as `FSD-Food-Delivery-App.md`.

**What you get:**

- `FSD-Food-Delivery-App.md` with all 9 sections populated
- Requirement IDs: FR-3.1.1 (Customer Registration), FR-3.2.1 (Place Order), FR-3.3.1 (Driver Assignment), etc.
- Use cases with main flow, alternative flows, and exception flows
- Data model for Users, Restaurants, Orders, OrderItems, Drivers, DeliveryTracking
- Error handling matrix for payment failures, GPS unavailability, restaurant rejection
- NFRs with measurable targets (e.g., "order placement API responds within 300ms at p95")
- Validation report confirming structural completeness

---

### Example 2: From an existing PRD or brief

Point the agent to a document you already have.

**Prompt:**

> Here's our PRD for the new inventory management system — `docs/PRD-Inventory-v2.md`. Can you turn this into a functional specification?

**What happens:**

The agent reads your PRD, extracts requirements, identifies gaps and ambiguities, and asks clarifying questions before generating the FSD:

> *"I've read the PRD. A few things I need clarity on before writing the spec:*
> 1. *Section 3.2 mentions 'role-based access' but doesn't list the roles — who are the user types?*
> 2. *The PRD says 'real-time stock updates' — what's the acceptable latency? Sub-second? Under 5 seconds?*
> 3. *Is the CSV export in Section 4.1 a one-time download or a scheduled recurring export?"*

After you clarify, it generates a complete FSD grounded in your PRD's requirements.

---

### Example 3: Spec a single feature

You don't need a whole product — the skill works for individual features too.

**Prompt:**

> Spec out how password reset should work for our platform. We use email-based auth with Auth0.

**What you get:**

A focused FSD covering:
- FR-3.1.1: Password reset request (email input, rate limiting)
- FR-3.1.2: Reset token generation (expiry, single-use)
- FR-3.1.3: Reset link delivery (email template, deep link for mobile)
- FR-3.1.4: New password submission (complexity validation, session invalidation)
- Use case with main flow + exception flows (invalid token, expired link, account lockout)
- Error handling matrix for each failure scenario
- Acceptance criteria in GIVEN/WHEN/THEN format for every requirement

---

### Example 4: Casual phrasing (still triggers)

You don't need to say "functional specification" — natural language works.

**Prompt:**

> Write up how the checkout flow should behave, step by step, with all the edge cases. I need something I can hand to the dev team.

**Prompt:**

> Can you document the requirements for our notification service? It needs to support email, SMS via Twilio, and push notifications via Firebase.

**Prompt:**

> Spec out the admin dashboard — user management, analytics, and content moderation.

All of these trigger the skill and produce a structured FSD.

---

### Example 5: Validate an existing FSD

If you already have an FSD, you can validate it for structural completeness.

**Prompt:**

> Validate the FSD at `docs/FSD-Payment.md`

**Or run the script directly:**

```bash
# Standard validation
python .agents/skills/functional-specification-document/scripts/validate_fsd.py docs/FSD-Payment.md

# Strict mode — warnings become errors
python .agents/skills/functional-specification-document/scripts/validate_fsd.py docs/FSD-Payment.md --strict

# JSON output — for CI/CD pipelines
python .agents/skills/functional-specification-document/scripts/validate_fsd.py docs/FSD-Payment.md --json
```

**Sample output:**

```
============================================================
  FSD Validation Report
============================================================

  Status: ✓ PASSED
  Errors: 0
  Warnings: 2
  Sections found: 32
  Requirement IDs found: 45

------------------------------------------------------------
  Issues
------------------------------------------------------------

  [WARNING] Cross-References
            ID "FR-3.4.2" is referenced but not formally defined

  [WARNING] Non-Functional Requirements
            Vague term "fast" found — use measurable targets (e.g., "< 200ms")

------------------------------------------------------------
  Requirement IDs
------------------------------------------------------------

    FR-3.1.1, FR-3.1.2, FR-3.2.1, FR-3.2.2, FR-3.3.1 ... (45 total)

============================================================
```

---

## Output Document Structure

Every generated FSD follows this 9-section structure:

| # | Section | Contents |
|---|---------|----------|
| 1 | **Introduction** | Purpose, scope, definitions & acronyms, references, document conventions (SHALL/SHOULD/MAY) |
| 2 | **Product Overview** | Product perspective, high-level functions, user classes, operating environment, constraints, assumptions & dependencies |
| 3 | **Functional Requirements** | Feature breakdown with IDs (FR-X.Y.Z), descriptions, MoSCoW priority, acceptance criteria (GIVEN/WHEN/THEN), business rules; use cases with main/alternative/exception flows; input/output specifications |
| 4 | **External Interface Requirements** | User interfaces, API/software interfaces, hardware interfaces, communication protocols |
| 5 | **Data Requirements** | Data model/ERD, data dictionary (field-level definitions), data migration & seeding |
| 6 | **Non-Functional Requirements** | Performance (with measurable targets), security, reliability & availability (RTO/RPO), scalability, maintainability, accessibility (WCAG) |
| 7 | **System Behavior & Error Handling** | State diagrams, error handling matrix (code, condition, user message, system action, severity), edge cases & boundary conditions |
| 8 | **Approval & Sign-Off** | Stakeholder sign-off table, revision history |
| 9 | **Appendices** | Architecture diagrams, wireframes, API catalog, ERD, glossary |

---

## Validation Checks

The `validate_fsd.py` script checks 9 categories:

| Check | Severity | What it catches |
|-------|----------|----------------|
| Required sections | Error | Missing top-level sections (Introduction, Functional Requirements, etc.) |
| Recommended subsections | Warning | Missing subsections (e.g., no "Security" under Non-Functional Requirements) |
| Empty sections | Error | Sections with no content (only sub-headings or blank) |
| Placeholder detection | Warning | TBD, TODO, TBC, [placeholder], Lorem ipsum |
| Requirement ID format | Error | No requirement IDs, or IDs not following FR-X.Y.Z / NFR-X.Y.Z convention |
| MoSCoW priorities | Error/Warning | Invalid priority labels or missing priorities entirely |
| Acceptance criteria | Warning/Error | Functional requirements without GIVEN/WHEN/THEN criteria |
| Cross-reference integrity | Warning | IDs referenced but never formally defined |
| NFR measurability | Warning | Vague adjectives ("fast", "secure enough") instead of measurable targets |

---

## Governance Rules

- **Requirement IDs:** Hierarchical format — `FR-3.1.1`, `NFR-6.2.1`, `UC-3.2.1`, `BR-3.1.1a`
- **Priority:** Every requirement gets a MoSCoW label (Must / Should / Could / Won't)
- **Acceptance Criteria:** Every Must/Should requirement has GIVEN/WHEN/THEN criteria
- **Traceability:** Use cases reference FR IDs; error matrix references flows; data model covers all entities in requirements
- **No scope creep:** Features outside stated scope are explicitly marked as Won't
- **Assumptions flagged:** Unclear business logic marked with `[ASSUMPTION]` for stakeholder review

---

## License

MIT

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m "Add improvement"`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request
