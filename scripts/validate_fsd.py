#!/usr/bin/env python3
"""
Validate a Functional Specification Document for structural completeness,
requirement formatting, content rules, and cross-reference integrity.

Usage:
    python validate_fsd.py <path-to-fsd.md>
    python validate_fsd.py <path-to-fsd.md> --strict
    python validate_fsd.py <path-to-fsd.md> --json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    severity: Severity
    section: str
    message: str
    line: int | None = None

    def to_dict(self):
        d = {"severity": self.severity.value, "section": self.section, "message": self.message}
        if self.line is not None:
            d["line"] = self.line
        return d


@dataclass
class ValidationResult:
    issues: list[Issue] = field(default_factory=list)
    sections_found: list[str] = field(default_factory=list)
    requirement_ids: list[str] = field(default_factory=list)
    cross_references: list[str] = field(default_factory=list)
    mermaid_count: int = 0
    code_block_count: int = 0

    @property
    def error_count(self):
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self):
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    @property
    def passed(self):
        return self.error_count == 0

    def to_dict(self):
        return {
            "passed": self.passed,
            "errors": self.error_count,
            "warnings": self.warning_count,
            "sections_found": self.sections_found,
            "requirement_ids_found": len(self.requirement_ids),
            "mermaid_diagrams": self.mermaid_count,
            "code_blocks_found": self.code_block_count,
            "issues": [i.to_dict() for i in self.issues],
        }


REQUIRED_SECTIONS = [
    "Introduction",
    "Product Overview",
    "Functional Requirements",
    "User Interface",
    "Non-Functional Requirements",
    "System Behavior",
    "Approval",
]

RECOMMENDED_SUBSECTIONS = {
    "Introduction": ["Purpose", "Scope", "Definitions", "References", "Conventions"],
    "Product Overview": ["Product Perspective", "Product Functions", "User Classes", "Operating Environment", "Constraints", "Assumptions"],
    "Functional Requirements": ["Feature", "Use Case"],
    "Non-Functional Requirements": ["Performance", "Security", "Reliability", "Scalability"],
}

EXCLUDED_SECTIONS = [
    "api",
    "database",
    "data requirements",
    "data model",
    "data dictionary",
    "api specification",
    "api endpoint",
    "software interface",
    "hardware interface",
    "communication interface",
]

MOSCOW_VALUES = {"must", "should", "could", "won't", "wont", "will not"}

REQ_ID_PATTERN = re.compile(r"\b(FR|NFR|UC|BR|UI)-[\d]+(?:\.[\d]+)*\b")


def read_document(path: Path) -> tuple[str, list[str]]:
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    return content, lines


def _heading_level(line: str) -> int:
    match = re.match(r"^(#{1,6})\s+", line.strip())
    return len(match.group(1)) if match else 0


def extract_sections(lines: list[str]) -> dict[str, tuple[int, int]]:
    sections: dict[str, tuple[int, int]] = {}
    heading_positions: list[tuple[str, int]] = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"^#{1,6}\s+", stripped):
            title = stripped.lstrip("#").strip()
            heading_positions.append((title, i))

    for idx, (title, start) in enumerate(heading_positions):
        end = heading_positions[idx + 1][1] if idx + 1 < len(heading_positions) else len(lines)
        sections[title] = (start, end)

    return sections


def extract_sections_hierarchical(lines: list[str]) -> dict[str, tuple[int, int]]:
    sections: dict[str, tuple[int, int]] = {}
    heading_positions: list[tuple[str, int, int]] = []

    for i, line in enumerate(lines):
        level = _heading_level(line)
        if level > 0:
            title = line.strip().lstrip("#").strip()
            heading_positions.append((title, i, level))

    for idx, (title, start, level) in enumerate(heading_positions):
        end = len(lines)
        for jdx in range(idx + 1, len(heading_positions)):
            if heading_positions[jdx][2] <= level:
                end = heading_positions[jdx][1]
                break
        sections[title] = (start, end)

    return sections


def check_required_sections(sections: dict[str, tuple[int, int]], result: ValidationResult):
    section_titles = list(sections.keys())
    result.sections_found = section_titles

    for required in REQUIRED_SECTIONS:
        found = any(required.lower() in title.lower() for title in section_titles)
        if not found:
            result.issues.append(Issue(
                severity=Severity.ERROR,
                section="Document Structure",
                message=f'Required section "{required}" is missing',
            ))

    for parent, subsections in RECOMMENDED_SUBSECTIONS.items():
        parent_exists = any(parent.lower() in t.lower() for t in section_titles)
        if not parent_exists:
            continue
        for sub in subsections:
            found = any(sub.lower() in t.lower() for t in section_titles)
            if not found:
                result.issues.append(Issue(
                    severity=Severity.WARNING,
                    section=parent,
                    message=f'Recommended subsection "{sub}" not found under "{parent}"',
                ))


def check_excluded_sections(sections: dict[str, tuple[int, int]], result: ValidationResult):
    section_titles = list(sections.keys())
    for title in section_titles:
        title_lower = title.lower()
        for excluded in EXCLUDED_SECTIONS:
            if excluded in title_lower and "reference" not in title_lower:
                result.issues.append(Issue(
                    severity=Severity.ERROR,
                    section=title,
                    message=f'Section "{title}" should not be in the FSD — API and database specifications belong in separate documents',
                ))
                break


def check_empty_sections(lines: list[str], result: ValidationResult):
    hier_sections = extract_sections_hierarchical(lines)
    for title, (start, end) in hier_sections.items():
        body_lines = [l.strip() for l in lines[start + 1 : end] if l.strip()]
        content_lines = [
            l for l in body_lines
            if not re.match(r"^#{1,6}\s+", l) and l not in ("---", "")
        ]
        if not content_lines:
            result.issues.append(Issue(
                severity=Severity.ERROR,
                section=title,
                message=f'Section "{title}" is empty or contains only sub-headings — add content',
                line=start + 1,
            ))

        placeholder_patterns = ["tbd", "todo", "tbc", "[placeholder]", "[to be determined]", "lorem ipsum"]
        for i, line in enumerate(lines[start + 1 : end], start=start + 2):
            if any(p in line.lower() for p in placeholder_patterns):
                result.issues.append(Issue(
                    severity=Severity.WARNING,
                    section=title,
                    message=f"Placeholder text detected: \"{line.strip()[:80]}\"",
                    line=i,
                ))


def check_code_blocks(content: str, lines: list[str], result: ValidationResult):
    mermaid_count = 0
    code_block_count = 0
    in_block = False
    block_start = 0
    is_mermaid = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```") and not in_block:
            in_block = True
            block_start = i
            lang = stripped[3:].strip().lower()
            is_mermaid = lang == "mermaid"
            if is_mermaid:
                mermaid_count += 1
            else:
                code_block_count += 1
        elif stripped == "```" and in_block:
            if not is_mermaid:
                result.issues.append(Issue(
                    severity=Severity.ERROR,
                    section="Content Rules",
                    message=f"Non-Mermaid code block found — the FSD must not contain code samples or code blocks",
                    line=block_start + 1,
                ))
            in_block = False

    result.mermaid_count = mermaid_count
    result.code_block_count = code_block_count

    if mermaid_count == 0:
        result.issues.append(Issue(
            severity=Severity.WARNING,
            section="Diagrams",
            message="No Mermaid diagrams found — the FSD should use Mermaid for state diagrams, flowcharts, and sequence diagrams",
        ))


def check_requirement_ids(content: str, lines: list[str], result: ValidationResult):
    full_ids = re.findall(r"\b(?:FR|NFR|UC|BR|UI)-[\d]+(?:\.[\d]+)*\b", content)
    result.requirement_ids = sorted(set(full_ids))

    if not full_ids:
        result.issues.append(Issue(
            severity=Severity.ERROR,
            section="Functional Requirements",
            message="No requirement IDs found. Requirements should use the format FR-X.Y.Z, NFR-X.Y.Z, etc.",
        ))
        return

    fr_ids = [rid for rid in full_ids if rid.startswith("FR-")]
    if not fr_ids:
        result.issues.append(Issue(
            severity=Severity.WARNING,
            section="Functional Requirements",
            message="No functional requirement IDs (FR-X.Y.Z) found",
        ))


def check_moscow_priorities(content: str, lines: list[str], result: ValidationResult):
    priority_pattern = re.compile(r"\*\*Priority\*\*\s*[:\|]\s*(\w[\w\s']*)", re.IGNORECASE)
    matches = priority_pattern.findall(content)

    if not matches:
        has_requirements = bool(REQ_ID_PATTERN.search(content))
        if has_requirements:
            result.issues.append(Issue(
                severity=Severity.WARNING,
                section="Functional Requirements",
                message="No MoSCoW priority labels found. Each requirement should have a priority (Must/Should/Could/Won't).",
            ))
        return

    for match in matches:
        value = match.strip().lower()
        if value not in MOSCOW_VALUES:
            result.issues.append(Issue(
                severity=Severity.ERROR,
                section="Requirements",
                message=f'Invalid priority value: "{match.strip()}". Must be one of: Must, Should, Could, Won\'t',
            ))


def check_acceptance_criteria(content: str, lines: list[str], result: ValidationResult):
    req_blocks = re.findall(
        r"(#{2,5}\s+(?:FR|NFR)-[\d.]+.*?)(?=#{2,5}\s|$)",
        content,
        re.DOTALL,
    )

    criteria_patterns = [
        re.compile(r"acceptance\s+criteria", re.IGNORECASE),
        re.compile(r"\bGIVEN\b.*\bWHEN\b.*\bTHEN\b", re.IGNORECASE),
        re.compile(r"\b(GIVEN|WHEN|THEN)\b", re.IGNORECASE),
    ]

    fr_blocks = [b for b in req_blocks if re.search(r"FR-[\d.]+", b)]
    if not fr_blocks:
        return

    blocks_without_criteria = 0
    for block in fr_blocks:
        has_criteria = any(p.search(block) for p in criteria_patterns)
        if not has_criteria:
            title_match = re.search(r"#{2,5}\s+(FR-[\d.]+[^\n]*)", block)
            title = title_match.group(1) if title_match else "Unknown FR"
            result.issues.append(Issue(
                severity=Severity.WARNING,
                section="Functional Requirements",
                message=f'Requirement "{title}" is missing acceptance criteria (GIVEN/WHEN/THEN)',
            ))
            blocks_without_criteria += 1

    if fr_blocks and blocks_without_criteria == len(fr_blocks):
        result.issues.append(Issue(
            severity=Severity.ERROR,
            section="Functional Requirements",
            message="None of the functional requirements have acceptance criteria",
        ))


def check_cross_references(content: str, result: ValidationResult):
    all_ids = set(re.findall(r"\b(?:FR|NFR|UC|BR|UI)-[\d]+(?:\.[\d]+)*\b", content))
    result.cross_references = sorted(all_ids)

    defined_pattern = re.compile(
        r"(?:\*\*ID\*\*\s*[:\|]\s*|#{2,5}\s+)((?:FR|NFR|UC|BR|UI)-[\d]+(?:\.[\d]+)*)"
    )
    defined_ids = set(defined_pattern.findall(content))

    referenced_but_undefined = all_ids - defined_ids
    loose_refs = set()
    for ref_id in referenced_but_undefined:
        occurrences = [
            m.start() for m in re.finditer(re.escape(ref_id), content)
        ]
        if len(occurrences) >= 1:
            context_has_definition = False
            for pos in occurrences:
                surrounding = content[max(0, pos - 100) : pos + len(ref_id) + 100]
                if re.search(r"(?:\*\*ID\*\*|#{2,5})\s*[:\|]?\s*" + re.escape(ref_id), surrounding):
                    context_has_definition = True
                    break
            if not context_has_definition:
                loose_refs.add(ref_id)

    for ref_id in sorted(loose_refs):
        result.issues.append(Issue(
            severity=Severity.WARNING,
            section="Cross-References",
            message=f'ID "{ref_id}" is referenced but not formally defined (no heading or ID field)',
        ))


def check_error_handling(content: str, result: ValidationResult):
    error_keywords = ["error handling", "error matrix", "error code", "exception"]
    has_error_section = any(kw in content.lower() for kw in error_keywords)

    if not has_error_section:
        result.issues.append(Issue(
            severity=Severity.WARNING,
            section="System Behavior & Error Handling",
            message="No error handling section or error matrix found",
        ))


def check_nfr_measurability(content: str, lines: list[str], result: ValidationResult):
    nfr_section_start = None
    nfr_section_end = None

    for i, line in enumerate(lines):
        if re.match(r"^#{1,2}\s+.*non-functional", line, re.IGNORECASE):
            nfr_section_start = i
        elif nfr_section_start and re.match(r"^#{1,2}\s+", line) and not re.search(r"non-functional", line, re.IGNORECASE):
            if i > nfr_section_start + 1:
                nfr_section_end = i
                break

    if nfr_section_start is None:
        return

    if nfr_section_end is None:
        nfr_section_end = len(lines)

    nfr_content = "\n".join(lines[nfr_section_start:nfr_section_end])

    vague_adjectives = ["fast", "quick", "responsive", "secure enough", "highly available", "robust", "good performance"]
    for adj in vague_adjectives:
        if adj in nfr_content.lower():
            result.issues.append(Issue(
                severity=Severity.WARNING,
                section="Non-Functional Requirements",
                message=f'Vague term "{adj}" found — NFRs should have measurable targets (e.g., "< 200ms" instead of "fast")',
            ))


def validate(path: Path, strict: bool = False) -> ValidationResult:
    result = ValidationResult()

    if not path.exists():
        result.issues.append(Issue(Severity.ERROR, "File", f"File not found: {path}"))
        return result

    if not path.suffix.lower() == ".md":
        result.issues.append(Issue(Severity.WARNING, "File", "Expected a .md file"))

    content, lines = read_document(path)

    if len(content.strip()) < 500:
        result.issues.append(Issue(
            severity=Severity.ERROR,
            section="Document",
            message=f"Document is very short ({len(content)} chars). A valid FSD should be substantially longer.",
        ))

    sections = extract_sections(lines)
    check_required_sections(sections, result)
    check_excluded_sections(sections, result)
    check_empty_sections(lines, result)
    check_code_blocks(content, lines, result)
    check_requirement_ids(content, lines, result)
    check_moscow_priorities(content, lines, result)
    check_acceptance_criteria(content, lines, result)
    check_cross_references(content, result)
    check_error_handling(content, result)
    check_nfr_measurability(content, lines, result)

    if strict:
        for issue in result.issues:
            if issue.severity == Severity.WARNING:
                issue.severity = Severity.ERROR

    return result


def print_report(result: ValidationResult, use_json: bool = False):
    if use_json:
        print(json.dumps(result.to_dict(), indent=2))
        return

    print("=" * 60)
    print("  FSD Validation Report")
    print("=" * 60)
    print()

    status = "PASSED" if result.passed else "FAILED"
    status_icon = "✓" if result.passed else "✗"
    print(f"  Status: {status_icon} {status}")
    print(f"  Errors: {result.error_count}")
    print(f"  Warnings: {result.warning_count}")
    print(f"  Sections found: {len(result.sections_found)}")
    print(f"  Requirement IDs found: {len(result.requirement_ids)}")
    print(f"  Mermaid diagrams: {result.mermaid_count}")
    if result.code_block_count > 0:
        print(f"  ⚠ Non-Mermaid code blocks: {result.code_block_count}")
    print()

    if result.issues:
        print("-" * 60)
        print("  Issues")
        print("-" * 60)
        print()

        for sev in [Severity.ERROR, Severity.WARNING, Severity.INFO]:
            sev_issues = [i for i in result.issues if i.severity == sev]
            if not sev_issues:
                continue

            label = sev.value.upper()
            for issue in sev_issues:
                line_info = f" (line {issue.line})" if issue.line else ""
                print(f"  [{label}] {issue.section}{line_info}")
                print(f"          {issue.message}")
                print()

    if result.requirement_ids:
        print("-" * 60)
        print("  Requirement IDs")
        print("-" * 60)
        print()
        for rid in result.requirement_ids[:30]:
            print(f"    {rid}")
        if len(result.requirement_ids) > 30:
            print(f"    ... and {len(result.requirement_ids) - 30} more")
        print()

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Functional Specification Document for structural completeness."
    )
    parser.add_argument("file", type=Path, help="Path to the FSD markdown file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()
    result = validate(args.file, strict=args.strict)
    print_report(result, use_json=args.json)
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
