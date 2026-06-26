#!/usr/bin/env python3
"""Validate the EXAM-CLEAN-015 review package artifact."""

import json
import re
import sys
from collections import Counter
from pathlib import Path


REQUIRED_SECTIONS = (
    "## Package Purpose",
    "## Input Artifact List",
    "## Output Artifact List",
    "## Record Coverage Summary",
    "## Source Trace Coverage Summary",
    "## Answer Alignment Summary",
    "## Manual Review QA Summary",
    "## Export Coverage Summary",
    "## Reviewer Checklist",
    "## Known Limitations / Not Covered Scope",
    "## Final Handoff Statement",
)
REQUIRED_ARTIFACT_REFERENCES = (
    "workflow/exports/EXAM-CLEAN-011_QUESTION_BANK_SUMMARY.md",
    "workflow/exports/EXAM-CLEAN-012_QUESTION_BANK_SUMMARY.docx",
    "workflow/exports/EXAM-CLEAN-014_QUESTION_BANK_INDEX.xlsx",
    "workflow/cleaning/EXAM-CLEAN-013_MANUAL_REVIEW_QA.md",
)


def load_jsonl(path):
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: record is not an object")
            records.append(record)
    return records


def extract_count(text, label, findings):
    match = re.search(rf"^- {re.escape(label)}: (\d+)$", text, re.MULTILINE)
    if not match:
        findings.append(f"missing count line for {label}")
        return None
    return int(match.group(1))


def main(argv):
    if len(argv) != 3:
        print(
            "Usage: python3 workflow/validation/validate_review_package.py "
            "<structured_question_bank.jsonl> <review_package.md>",
            file=sys.stderr,
        )
        return 2

    jsonl_path = Path(argv[1])
    review_package_path = Path(argv[2])

    try:
        records = load_jsonl(jsonl_path)
    except ValueError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    if not review_package_path.is_file():
        print(f"FAIL review package file does not exist: {review_package_path}", file=sys.stderr)
        return 1

    text = review_package_path.read_text(encoding="utf-8")
    findings = []
    section_counts = Counter(record.get("section_type") for record in records)

    for heading in REQUIRED_SECTIONS:
        if heading not in text:
            findings.append(f"missing required section heading: {heading}")

    for artifact_ref in REQUIRED_ARTIFACT_REFERENCES:
        if artifact_ref not in text:
            findings.append(f"missing required artifact reference: {artifact_ref}")

    total_records = len(records)
    reading_records = section_counts.get("reading", 0)
    writing_records = section_counts.get("writing", 0)

    pkg_total = extract_count(text, "total_records", findings)
    pkg_reading = extract_count(text, "reading_records", findings)
    pkg_writing = extract_count(text, "writing_records", findings)

    if pkg_total is not None and pkg_total != total_records:
        findings.append(f"review package total_records={pkg_total} does not match jsonl total_records={total_records}")
    if pkg_reading is not None and pkg_reading != reading_records:
        findings.append(
            f"review package reading_records={pkg_reading} does not match jsonl reading_records={reading_records}"
        )
    if pkg_writing is not None and pkg_writing != writing_records:
        findings.append(
            f"review package writing_records={pkg_writing} does not match jsonl writing_records={writing_records}"
        )

    if "workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl" not in text:
        findings.append("missing structured question-bank source reference")
    if "qa_pass_records: 8" not in text:
        findings.append("missing manual review QA pass summary line")
    if "answer_status distribution:" not in text:
        findings.append("missing answer alignment distribution summary")
    if "source_trace_status distribution:" not in text:
        findings.append("missing source trace distribution summary")

    if findings:
        print("FAIL")
        for finding in findings:
            print(finding)
        return 1

    print(
        "PASS "
        f"review_package_records={total_records} "
        f"reading_records={reading_records} "
        f"writing_records={writing_records} "
        f"required_sections={len(REQUIRED_SECTIONS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
