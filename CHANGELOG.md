# Changelog

All notable changes to the Functional Specification Document skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.2.0] - 2026-03-10

### Added
- **Business Requirements Document (BRD) Support** — The skill can now generate BRDs in addition to FSDs.
- **references/brd-template.md** — New 7-section template for BRDs focusing on business goals, scope, stakeholders, and high-level requirements.
- **SKILL.md** — Updated instructions to detect when a user needs a BRD vs FSD and route them to the appropriate template.
- **README.md** — Updated documentation to reflect the new dual-document capability.

---

## [1.1.0] - 2026-03-05

### Changed — Content Rules Overhaul

This release enforces strict content rules that change how the FSD is generated and validated.

- **SKILL.md** — Added "Content Rules" section enforcing: no code samples, no code blocks (except Mermaid), "what/why" focus, Mermaid-only diagrams, and API/database exclusion
- **references/fsd-template.md** — Complete rewrite:
  - Reduced from 9 sections to 8 sections
  - Removed Section 4 "External Interface Requirements" (API, hardware, communication interfaces) — replaced with "User Interface Requirements" covering screens, navigation, and accessibility
  - Removed Section 5 "Data Requirements" (data model, data dictionary, migration) — these belong in a separate Database Design document
  - Removed Section 3.3 "Input/Output Specifications" with JSON code blocks
  - Replaced all plaintext/ASCII diagrams with Mermaid: system context (graph), sequence diagrams, state diagrams (stateDiagram-v2), flowcharts, navigation flows, feature interaction maps
  - All examples rewritten as textual descriptions rather than code
  - Added "Companion Documents" references for API Spec and DB Design
- **scripts/validate_fsd.py** — Added 3 new validation checks:
  - **Excluded section detection** — Flags API, database, data model, data dictionary, and related sections as errors
  - **Code block detection** — Flags non-Mermaid code blocks as errors; warns if no Mermaid diagrams found
  - **Mermaid diagram counting** — Reports total Mermaid diagrams in the validation summary
  - Updated required sections list: replaced "External Interface Requirements" and "Data Requirements" with "User Interface"
  - Updated requirement ID prefixes: added `UI-` prefix, removed `IO-` and `EI-` prefixes
- **README.md** — Updated to reflect 8-section structure, content rules table, new validation checks, companion documents section

### Removed

- All code samples and JSON examples from the template
- Section 4 "External Interface Requirements" (API/software/hardware/communication interfaces)
- Section 5 "Data Requirements" (data model, data dictionary, migration/seeding)
- Section 3.3 "Input/Output Specifications"
- ASCII/plaintext diagram notation
- `IO-` and `EI-` requirement ID prefixes from validator

---

## [1.0.0] - 2026-03-05

### Added

- **SKILL.md** — Main skill file with 4-phase workflow (Gather Context, Write FSD, Output & Validate, Review & Iterate)
- **references/fsd-template.md** — Complete 9-section FSD template with section-by-section guidance and concrete examples
  - Introduction (purpose, scope, definitions, references, conventions)
  - Product Overview (perspective, functions, user classes, environment, constraints, assumptions)
  - Functional Requirements (feature breakdown with FR-X.Y.Z IDs, MoSCoW priority, GIVEN/WHEN/THEN acceptance criteria, business rules, use cases, I/O specs)
  - External Interface Requirements (UI, API, hardware, communication)
  - Data Requirements (data model, data dictionary, migration/seeding)
  - Non-Functional Requirements (performance, security, reliability, scalability, maintainability, accessibility)
  - System Behavior & Error Handling (state diagrams, error matrix, edge cases)
  - Approval & Sign-Off (stakeholder table, revision history)
  - Appendices
- **scripts/validate_fsd.py** — Automated validation script with 9 check categories
- **README.md** — Installation guide, usage examples, output structure documentation
- **CHANGELOG.md** — This file
