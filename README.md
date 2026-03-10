# Requirements & Functional Specification Document Generator

An agent skill that generates structured Business Requirements Documents (BRDs) and implementation-ready Functional Specification Documents (FSDs). It defines business goals, functional requirements, user interactions, acceptance criteria, and error handling — focusing on **what** the system must do and **why**, not how to build it.

Every generated FSD follows a structured 8-section template with MoSCoW prioritization, GIVEN/WHEN/THEN acceptance criteria, hierarchical requirement IDs (FR-X.Y.Z), and Mermaid diagrams for all visual representations. BRDs follow a 7-section template focusing on business goals, stakeholders, scope, and high-level business rules.

---

## Installation

```bash
npx skills add https://github.com/rahmat1929/skill-functional-specification-document --skill functional-specification-document
```

### Manual install

Clone and copy to your preferred scope:

| Scope | Path |
|-------|------|
| Project (shared) | `.agents/skills/functional-specification-document/` |
| Personal (local) | `~/.cursor/skills/functional-specification-document/` |

```bash
git clone https://github.com/rahmat1929/skill-functional-specification-document.git
cp -r skill-functional-specification-document/ .agents/skills/functional-specification-document/
```

### Verify installation

Ask the agent:

> "Create a functional spec for the authentication module" or "Write a BRD for the new onboarding flow"

If it responds by asking clarifying questions or generating an FSD with Mermaid diagrams, the skill is active.

---

## Skill Contents

```text
functional-specification-document/
├── SKILL.md                        # Main skill instructions & workflow
├── README.md                       # This file
├── CHANGELOG.md                    # Version history
├── references/
│   ├── brd-template.md             # Complete BRD template
│   └── fsd-template.md             # Complete FSD template (8 sections) with Mermaid examples
└── scripts/
    └── validate_fsd.py             # Automated FSD structural validator
```

---

## How It Works

| Phase | What happens |
|-------|-------------|
| **1. Gather Context** | Reads your PRD/brief or runs an interactive interview to understand the system |
| **2. Write the Document** | Generates a full document following the respective template (BRD or FSD) with requirement IDs, priority labels, and diagrams if applicable |
| **3. Output & Validate** | Saves as `BRD-[Project-Name].md` or `FSD-[Project-Name].md` and runs validation (for FSDs) to check structure and rules |
| **4. Review & Iterate** | Presents the draft with flagged assumptions, incorporates feedback, re-validates |

---

## Usage Examples

### Example 1: Interactive — Spec a new system from scratch

**Prompt:**

> I need a functional spec for a food delivery app. It should support customer ordering, restaurant management, and a driver tracking system.

**What you get:**

- `FSD-Food-Delivery-App.md` with all 8 sections populated
- Mermaid sequence diagrams for key user flows (ordering, driver assignment, delivery tracking)
- Mermaid state diagram for the order lifecycle
- Mermaid flowchart for navigation and feature interactions
- Requirement IDs: FR-3.1.1 (Customer Registration), FR-3.2.1 (Place Order), FR-3.3.1 (Driver Assignment), etc.
- Use cases with main flow, alternative flows, and exception flows
- Error handling matrix for payment failures, GPS unavailability, restaurant rejection
- NFRs with measurable targets
- No code blocks, no API specs, no database schemas — pure behavioral specification

---

### Example 2: From an existing PRD or brief

**Prompt:**

> Here's our PRD for the new inventory management system — `docs/PRD-Inventory-v2.md`. Can you turn this into a functional specification?

The agent reads your PRD, extracts requirements, identifies gaps, asks clarifying questions, then generates a complete FSD with Mermaid diagrams throughout.

---

### Example 3: Spec a single feature

**Prompt:**

> Spec out how password reset should work for our platform. We use email-based auth with Auth0.

**What you get:**

A focused FSD with Mermaid sequence diagram for the reset flow, state diagram for token lifecycle, requirement IDs, acceptance criteria, and error handling — all without a single line of code.

---

### Example 4: Casual phrasing (still triggers)

**Prompt:**

> "Write up how the checkout flow should behave, step by step, with all the edge cases."

> "Document the requirements for our notification service."

> "Spec out the admin dashboard — user management, analytics, and content moderation."

---

## Output Document Structure

### Business Requirements Document (BRD)

| # | Section | Contents |
|---|---------|----------|
| 1 | **Executive Summary** | Purpose, background, and problem statement |
| 2 | **Business Goals & Objectives** | Project goals and success metrics (KPIs) |
| 3 | **Project Scope** | In scope and out of scope |
| 4 | **Stakeholders** | Roles, influence, and responsibilities |
| 5 | **Business Requirements** | High-level requirements mapped to MoSCoW priorities and business rules |
| 6 | **Assumptions, Constraints & Dependencies** | Factors believed to be true, limitations, and external reliance |
| 7 | **Glossary of Terms** | Definitions of business-specific jargon and acronyms |

### Functional Specification Document (FSD)

| # | Section | Contents |
|---|---------|----------|
| 1 | **Introduction** | Purpose, scope, definitions & acronyms, references, document conventions (SHALL/SHOULD/MAY) |
| 2 | **Product Overview** | Product perspective (with Mermaid context diagram), high-level functions, user classes, operating environment, constraints, assumptions & dependencies |
| 3 | **Functional Requirements** | Feature breakdown with IDs (FR-X.Y.Z), descriptions, MoSCoW priority, acceptance criteria (GIVEN/WHEN/THEN), business rules; use cases with Mermaid sequence diagrams; feature interaction maps |
| 4 | **User Interface Requirements** | Screen inventory, navigation flow (Mermaid flowchart), screen descriptions, accessibility requirements |
| 5 | **Non-Functional Requirements** | Performance (measurable targets), security, reliability & availability (RTO/RPO), scalability, maintainability |
| 6 | **System Behavior & Error Handling** | State diagrams (Mermaid stateDiagram), error handling matrix, edge cases, critical flow diagrams (Mermaid flowchart) |
| 7 | **Approval & Sign-Off** | Stakeholder sign-off table, revision history |
| 8 | **Appendices** | Supplementary Mermaid diagrams, wireframe references, glossary |

**Excluded by design:** API endpoint catalogs, database schemas, data dictionaries — these belong in companion API Specification and Database Design documents.

---

## Validation Checks & Scripts

```bash
python .agents/skills/functional-specification-document/scripts/validate_fsd.py docs/FSD-Payment.md
```

**Sample output:**

```text
============================================================
  FSD Validation Report
============================================================

  Status: ✓ PASSED
  Errors: 0
  Warnings: 2
  Sections found: 32
  Requirement IDs found: 45
  Mermaid diagrams: 8

  [WARNING] Cross-References
            ID "FR-3.4.2" is referenced but not formally defined

  [WARNING] Non-Functional Requirements
            Vague term "fast" found — use measurable targets

============================================================
```

Use `--strict` to treat warnings as errors, or `--json` for CI/CD integration.

| Check | Severity | What it catches |
|-------|----------|----------------|
| Required sections | Error | Missing top-level sections from the 8-section structure |
| Excluded sections | Error | API or database sections that shouldn't be in the FSD |
| Recommended subsections | Warning | Missing subsections (e.g., no "Security" under NFRs) |
| Empty sections | Error | Sections with no content |
| Code block detection | Error | Non-Mermaid code blocks (violates content rules) |
| Mermaid diagram presence | Warning | No Mermaid diagrams found |
| Placeholder detection | Warning | TBD, TODO, TBC, [placeholder], Lorem ipsum |
| Requirement ID format | Error | Missing IDs or wrong format |
| MoSCoW priorities | Error/Warning | Invalid or missing priority labels |
| Acceptance criteria | Warning/Error | Requirements without GIVEN/WHEN/THEN |
| Cross-reference integrity | Warning | Referenced IDs never formally defined |
| NFR measurability | Warning | Vague adjectives instead of measurable targets |

---

## Content Rules

All generated FSDs follow these strict content rules:

| Rule | Description |
|------|-------------|
| **No code samples** | Only explanations, conceptual descriptions, and structured information |
| **No code blocks** | The only permitted fenced blocks are Mermaid diagrams |
| **"What" and "why" focus** | Developer-friendly language focused on system behavior and business rationale |
| **Architecture first** | Prioritize system relationships and module interactions over implementation details |
| **Mermaid exclusively** | All diagrams (flowcharts, sequences, state machines) use Mermaid format |
| **Exclude API & Database** | API endpoints and database schemas belong in separate companion documents |

---

## Governance Rules

- **Requirement IDs:** Hierarchical format — `FR-3.1.1`, `NFR-5.2.1`, `UC-3.2.1`, `BR-3.1.1a`, `UI-4.4.1`
- **Priority:** Every requirement gets a MoSCoW label (Must / Should / Could / Won't)
- **Acceptance Criteria:** Every Must/Should requirement has GIVEN/WHEN/THEN criteria
- **Diagrams:** All visual representations use Mermaid — no exceptions
- **No code:** Zero code samples, zero code blocks (except Mermaid)
- **Separation of concerns:** API specs and database schemas are referenced but never included
- **Assumptions flagged:** Unclear business logic marked with `[ASSUMPTION]` for stakeholder review

---

## Companion Documents

The FSD is one part of a complete specification pipeline. It references but does not include:

| Document | What it covers | Relationship to FSD |
|----------|---------------|-------------------|
| **API Specification** | Endpoint contracts, request/response schemas, auth, versioning | Implements FSD's functional requirements as API contracts |
| **Database Design** | Schema, migrations, indexing, ERD | Implements FSD's entity descriptions as database structures |

---

## Supported Platforms

| Platform | Status |
|---|---|
| Claude | ✅ |
| ChatGPT | ✅ |
| Gemini | ✅ |

---

## Requirements

- Python 3.10+ (for validator script, no pip dependencies required)

---

## License

MIT
