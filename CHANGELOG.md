# Changelog

All notable changes to the Functional Specification Document skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
- **scripts/validate_fsd.py** — Automated validation script with 9 check categories:
  - Required section detection
  - Recommended subsection detection
  - Empty section detection (hierarchy-aware)
  - Placeholder text detection (TBD, TODO, TBC, Lorem ipsum)
  - Requirement ID format validation (FR/NFR/UC/BR/IO/EI-X.Y.Z)
  - MoSCoW priority label validation
  - Acceptance criteria presence check
  - Cross-reference integrity verification
  - Non-functional requirement measurability check (flags vague adjectives)
  - Supports `--strict` mode (warnings become errors) and `--json` output
- **README.md** — Installation guide, usage examples, output structure documentation
- **CHANGELOG.md** — This file
