#!/usr/bin/env python3
"""Validate the EXAM-CLEAN-013 manual review QA artifact."""

import json
import re
import sys
from collections import Counter
from pathlib import Path

ALLOWED_QA_STATUS = {"PASS", "WARN", "NEEDS_REVIEW"}


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


def parse_qa_blocks(text):
    pattern = re.compile(
        r"### Record \d+\n\n"
        r"- record_id: (?P<record_id>[^\n]+)\n"
        r"- question_type: (?P<question_type>[^\n]+)\n"
        r"- source_trace_status: (?P<source_trace_status>[^\n]+)\n"
        r"- prompt_or_passage_present: (?P<prompt_or_passage_present>[^\n]+)\n"
        r"- options_present_if_applicable: (?P<options_present_if_applicable>[^\n]+)\n"
        r"- answer_present: (?P<answer_present>[^\n]+)\n"
        r"- export_markdown_present: (?P<export_markdown_present>[^\n]+)\n"
        r"- export_word_present: (?P<export_word_present>[^\n]+)\n"
        r"- qa_status: (?P<qa_status>[^\n]+)\n"
        r"- qa_note: (?P<qa_note>[^\n]+)\n",
        re.MULTILINE,
    )
    return [match.groupdict() for match in pattern.finditer(text)]


def extract_count(text, label, findings):
    match = re.search(rf"^- {re.escape(label)}: (\d+)$", text, re.MULTILINE)
    if not match:
        findings.append(f"missing count line for {label}")
        return None
    return int(match.group(1))


def main(argv):
    if len(argv) != 3:
        print(
            "Usage: python3 workflow/validation/validate_manual_review_qa.py "
            "<structured_question_bank.jsonl> <manual_review_qa.md>",
            file=sys.stderr,
        )
        return 2

    jsonl_path = Path(argv[1])
    qa_path = Path(argv[2])

    try:
        records = load_jsonl(jsonl_path)
    except ValueError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    if len(records) != 8:
        print(f"FAIL expected 8 jsonl records, found {len(records)}", file=sys.stderr)
        return 1

    if not qa_path.is_file():
        print(f"FAIL QA markdown file does not exist: {qa_path}", file=sys.stderr)
        return 1

    text = qa_path.read_text(encoding="utf-8")
    findings = []

    qa_blocks = parse_qa_blocks(text)
    if len(qa_blocks) != 8:
        findings.append(f"expected 8 QA record blocks, found {len(qa_blocks)}")

    section_counts = Counter(record.get("section_type") for record in records)
    jsonl_by_id = {record["question_id"]: record for record in records}
    qa_ids = [block["record_id"] for block in qa_blocks]

    if len(set(qa_ids)) != len(qa_ids):
        findings.append("duplicate record_id entries found in QA markdown")

    qa_total = extract_count(text, "total_records", findings)
    qa_reading = extract_count(text, "reading_records", findings)
    qa_writing = extract_count(text, "writing_records", findings)

    if qa_total is not None and qa_total != len(records):
        findings.append(f"qa total_records={qa_total} does not match jsonl total_records={len(records)}")
    if qa_reading is not None and qa_reading != section_counts.get("reading", 0):
        findings.append(
            f"qa reading_records={qa_reading} does not match jsonl reading_records={section_counts.get('reading', 0)}"
        )
    if qa_writing is not None and qa_writing != section_counts.get("writing", 0):
        findings.append(
            f"qa writing_records={qa_writing} does not match jsonl writing_records={section_counts.get('writing', 0)}"
        )

    status_counts = Counter()

    for record in records:
        record_id = record["question_id"]
        if record_id not in qa_ids:
            findings.append(f"missing QA coverage for record_id={record_id}")

    for block in qa_blocks:
        record_id = block["record_id"]
        record = jsonl_by_id.get(record_id)
        if record is None:
            findings.append(f"QA markdown references unknown record_id={record_id}")
            continue

        if block["question_type"] != str(record.get("question_type")):
            findings.append(
                f"question_type mismatch for {record_id}: qa={block['question_type']} jsonl={record.get('question_type')}"
            )
        if block["source_trace_status"] != str(record.get("source_trace_status")):
            findings.append(
                f"source_trace_status mismatch for {record_id}: qa={block['source_trace_status']} jsonl={record.get('source_trace_status')}"
            )

        qa_status = block["qa_status"]
        if not qa_status:
            findings.append(f"missing qa_status for {record_id}")
        elif qa_status not in ALLOWED_QA_STATUS:
            findings.append(f"invalid qa_status for {record_id}: {qa_status}")
        else:
            status_counts[qa_status] += 1

    if section_counts.get("reading", 0) != 3:
        findings.append(f"expected reading=3 in JSONL, found {section_counts.get('reading', 0)}")
    if section_counts.get("writing", 0) != 5:
        findings.append(f"expected writing=5 in JSONL, found {section_counts.get('writing', 0)}")

    if findings:
        print("FAIL")
        for finding in findings:
            print(finding)
        return 1

    print(
        "PASS "
        f"manual_review_qa_records={len(qa_blocks)} "
        f"reading_records={section_counts.get('reading', 0)} "
        f"writing_records={section_counts.get('writing', 0)} "
        f"pass={status_counts.get('PASS', 0)} "
        f"warn={status_counts.get('WARN', 0)} "
        f"needs_review={status_counts.get('NEEDS_REVIEW', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
