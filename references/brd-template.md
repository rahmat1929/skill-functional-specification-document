# Business Requirements Document — Template Reference

This file contains the full document template with section-by-section guidance for a Business Requirements Document (BRD). When generating a BRD, follow this structure and adapt to the project's needs.

**Content rules reminder:** The BRD focuses on the *business needs*, *goals*, and *what* the system must do from a business perspective, not the technical or functional *how*. Avoid technical implementation details, architectural diagrams, or system-level workflows (which belong in the FSD).

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Goals & Objectives](#2-business-goals--objectives)
3. [Project Scope](#3-project-scope)
4. [Stakeholders](#4-stakeholders)
5. [Business Requirements](#5-business-requirements)
6. [Assumptions, Constraints & Dependencies](#6-assumptions-constraints--dependencies)
7. [Glossary of Terms](#7-glossary-of-terms)

---

## 1. Executive Summary

### 1.1 Document Purpose
State the purpose of this BRD and who the intended audience is (usually business stakeholders, project managers, and lead technical staff).

### 1.2 Background and Problem Statement
Describe the current state, the business problem, or the opportunity that this project addresses. Why is this project being undertaken?

---

## 2. Business Goals & Objectives

### 2.1 Project Goals
What is the overarching goal of this initiative?

**Example:**
> To reduce customer onboarding time from 3 days to under 10 minutes.

### 2.2 Success Metrics (KPIs)
How will the business measure the success of this project? Provide quantifiable metrics.

| Metric | Baseline | Target |
|--------|----------|--------|
| Onboarding Time | 3 days | < 10 mins |
| Support Tickets | 50/week | < 10/week |

---

## 3. Project Scope

### 3.1 In Scope
List the specific business capabilities, departments, or geographic regions that are included in this project.

### 3.2 Out of Scope
List the capabilities, departments, or regions explicitly excluded from this project to prevent scope creep.

---

## 4. Stakeholders

Identify the key people or departments involved in or affected by the project.

| Role | Name/Department | Influence/Interest | Key Responsibilities |
|------|-----------------|--------------------|----------------------|
| Sponsor | Jane Doe / Exec | High/High | Final approval and funding |
| SME | John Smith / Ops | Medium/High | Provides operational requirements |

---

## 5. Business Requirements

Break down the high-level business requirements (BRs). These should describe *what* the business needs the system to do, not *how* it will be implemented. UseMoSCoW priority (Must, Should, Could, Won't).

### 5.1 [Requirement Category Name]

| ID | Title | Description | Priority |
|----|-------|-------------|----------|
| BR-1.1 | Automated KYC | The system must verify customer identity automatically without manual intervention. | Must |
| BR-1.2 | Multi-currency | The platform must support transactions in USD, EUR, and GBP. | Should |

*(Repeat for different categories as needed)*

### 5.2 Business Rules
List the rules that govern the business processes (e.g., policies, legal regulations, industry standards).

* **BRule-1:** Customers must be 18 years or older.
* **BRule-2:** Transactions over $10,000 require secondary manager approval.

---

## 6. Assumptions, Constraints & Dependencies

### 6.1 Assumptions
Factors believed to be true for the project to succeed (e.g., "The marketing budget will remain unchanged").

### 6.2 Constraints
Limitations on the project (e.g., budget limits, hard deadlines, regulatory compliance like GDPR).

### 6.3 Dependencies
External factors the project relies on (e.g., "Relies on the completion of the new Data Warehouse project by Q3").

---

## 7. Glossary of Terms

Define any business-specific jargon, acronyms, or standard terms used in the document to ensure all stakeholders have a shared understanding.

| Term | Definition |
|------|------------|
| KYC | Know Your Customer - the process of verifying user identity |
| SME | Subject Matter Expert |
