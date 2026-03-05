---
name: functional-specification-document
description: Generate a comprehensive Functional Specification Document (FSD) from project requirements, PRDs, briefs, or interactive interviews. Use this skill whenever the user mentions functional specs, FSD, software specification, feature specification, system specification, functional requirements document, or wants to document how a system should behave before implementation. Also trigger when users ask to "spec out" a feature, write up requirements, or create a detailed plan for developers to build from — even if they don't use the term "functional specification" explicitly.
---

# Functional Specification Document Generator

This skill produces structured, implementation-ready Functional Specification Documents. An FSD bridges the gap between what stakeholders want (captured in a PRD or brief) and what engineers need to build. It answers "what does the system do and how should it behave?" without dictating internal architecture.

## When to use this skill

- A user wants to create a functional specification for a new product, feature, or system
- A user has a PRD, project brief, or set of requirements and needs them turned into a detailed spec
- A user asks to "spec out" or "write up" how something should work
- A user needs to document functional requirements, use cases, or acceptance criteria

## Workflow

### Phase 1: Gather Context

Before writing anything, understand what you're specifying. There are two paths depending on what the user provides:

**Path A — User provides a source document (PRD, brief, requirements list, etc.):**
Read the document thoroughly. Extract the core requirements, identify gaps, and list clarifying questions. Present the questions to the user before proceeding. Don't guess at ambiguous requirements — ask.

**Path B — No source document (interactive interview):**
Walk through these questions to build a mental model of the system:

1. What is the product/feature? (one-sentence elevator pitch)
2. Who are the users? (roles, personas, access levels)
3. What are the core workflows? (the 3-5 things users will actually do)
4. What systems does this interact with? (APIs, databases, third-party services)
5. Are there constraints? (regulatory, platform, timeline, tech stack)
6. What does success look like? (KPIs, acceptance criteria)

Don't ask all questions at once — use the first couple of answers to tailor follow-ups. The goal is to get enough information to write a solid first draft, not to exhaustively document everything upfront.

### Phase 2: Write the FSD

Read `references/fsd-template.md` for the full document template and section-by-section guidance. Follow that template structure, but adapt it to the project — skip sections that genuinely don't apply (e.g., "Hardware Interfaces" for a pure web app) and expand sections that need more depth.

**Key principles while writing:**

- **Be specific.** "The system should be fast" is not a requirement. "Search results return within 200ms for up to 10,000 records" is.
- **Use consistent language.** "SHALL" = mandatory, "SHOULD" = recommended, "MAY" = optional. Define this in the Document Conventions section and stick to it.
- **Every feature gets acceptance criteria.** If you can't write a test for it, the requirement isn't clear enough.
- **Separate what from how.** Describe observable behavior, not implementation details. "The system SHALL authenticate users via OAuth 2.0" is fine (it's an interface contract). "The system SHALL use a HashMap to store session tokens" is not (that's an architecture decision).
- **Assign priority to each requirement.** Use MoSCoW: Must / Should / Could / Won't. This prevents scope creep and helps teams negotiate tradeoffs.
- **Number every requirement.** Use a hierarchical ID scheme (e.g., FR-3.2.1) so requirements are traceable from spec to test to implementation.

### Phase 3: Output

Save the FSD as a Markdown file. Use the naming convention: `FSD-[Project-Name].md`

After generating the document, run the validation script to check structural completeness:

```bash
python <skill-path>/scripts/validate_fsd.py <path-to-generated-fsd>
```

The validation script checks for:
- Presence of all required sections
- Requirement IDs follow the numbering convention
- Every feature has acceptance criteria
- Priority labels are valid MoSCoW values
- No empty sections (placeholder-only content)
- Cross-reference integrity (referenced IDs exist)

If validation reports issues, fix them before presenting the final document to the user. Show the user the validation summary alongside the finished document so they know it's been checked.

### Phase 4: Review & Iterate

Present the draft to the user. Highlight:
- Sections where you made assumptions (flag these explicitly)
- Areas that need more detail from stakeholders
- Requirements you marked as "Could" or "Won't" that the user might want to reconsider

Incorporate feedback and regenerate. Each revision should re-run validation.

## Document Structure Summary

The full FSD follows this top-level structure (see `references/fsd-template.md` for details):

1. **Introduction** — Purpose, scope, definitions, references, conventions
2. **Product Overview** — Context, high-level functions, users, environment, constraints, assumptions
3. **Functional Requirements** — Feature breakdown with IDs, descriptions, acceptance criteria, priority, business rules; use cases with flows; input/output specs
4. **External Interface Requirements** — UI, API/software, hardware, communication interfaces
5. **Data Requirements** — Data model, data dictionary, migration/seeding
6. **Non-Functional Requirements** — Performance, security, reliability, scalability, maintainability, accessibility
7. **System Behavior & Error Handling** — State transitions, error matrix, edge cases
8. **Approval & Sign-Off** — Stakeholder table, revision history
9. **Appendices** — Diagrams, mockups, supplementary material

## Output Quality Checklist

Before delivering the final FSD, mentally verify:

- [ ] Every requirement has a unique ID
- [ ] Every requirement has a priority (Must/Should/Could/Won't)
- [ ] Every feature has testable acceptance criteria
- [ ] Use cases cover main flow + at least one alternative/error flow
- [ ] Data model covers all entities mentioned in the requirements
- [ ] Error handling is specified for user-facing operations
- [ ] Non-functional requirements have measurable targets (not vague adjectives)
- [ ] No section is left as a placeholder or TODO
- [ ] Cross-references between sections are consistent
- [ ] The document can be handed to a developer who has never seen the project and they could start building
