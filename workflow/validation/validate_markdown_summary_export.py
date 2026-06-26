#!/usr/bin/env python3
"""Validate the EXAM-CLEAN-011 markdown summary export."""

import json
import re
import sys
from collections import Counter
from pathlib import Path


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


def require(text, needle, findings, label):
    if needle not in text:
        findings.append(f"missing markdown content for {label}: {needle}")


def extract_count(text, label, findings):
    match = re.search(rf"^- {re.escape(label)}: (\d+)$", text, re.MULTILINE)
    if not match:
        findings.append(f"missing count line for {label}")
        return None
    return int(match.group(1))


def main(argv):
    if len(argv) != 3:
        print(
            "Usage: python3 workflow/validation/validate_markdown_summary_export.py <structured_question_bank.jsonl> <summary.md>",
            file=sys.stderr,
        )
        return 2

    jsonl_path = Path(argv[1])
    markdown_path = Path(argv[2])

    try:
        records = load_jsonl(jsonl_path)
    except ValueError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    if not markdown_path.is_file():
        print(f"FAIL markdown file does not exist: {markdown_path}", file=sys.stderr)
        return 1

    text = markdown_path.read_text(encoding="utf-8")
    findings = []

    total_count = len(records)
    section_counts = Counter(record.get("section_type") for record in records)
    manual_review_count = sum(1 for record in records if record.get("manual_review_status") == "required")

    md_total = extract_count(text, "total_records", findings)
    md_reading = extract_count(text, "reading_records", findings)
    md_writing = extract_count(text, "writing_records", findings)
    md_manual = extract_count(text, "manual_review_required_records", findings)

    if md_total is not None and md_total != total_count:
        findings.append(f"markdown total_records={md_total} does not match jsonl total_records={total_count}")
    if md_reading is not None and md_reading != section_counts.get("reading", 0):
        findings.append(
            f"markdown reading_records={md_reading} does not match jsonl reading_records={section_counts.get('reading', 0)}"
        )
    if md_writing is not None and md_writing != section_counts.get("writing", 0):
        findings.append(
            f"markdown writing_records={md_writing} does not match jsonl writing_records={section_counts.get('writing', 0)}"
        )
    if md_manual is not None and md_manual != manual_review_count:
        findings.append(
            f"markdown manual_review_required_records={md_manual} does not match jsonl manual_review_required_records={manual_review_count}"
        )

    require(text, "| question_id | exam_id | section | question_type | source_file | source_question_number | answer | manual_review |", findings, "summary table header")
    require(text, "- manual_review=0", findings, "manual_review zero note")

    for record in records:
        question_id = record["question_id"]
        require(text, f"### {question_id}", findings, f"record heading {question_id}")
        require(text, f"- question_id: {question_id}", findings, f"question_id line {question_id}")
        require(text, f"- exam_id: {record['exam_id']}", findings, f"exam_id line {question_id}")
        require(text, f"- section: {record['section_type']}", findings, f"section line {question_id}")
        require(text, f"- question_type: {record['question_type']}", findings, f"question_type line {question_id}")
        require(text, f"- source_question_number: {record['source_question_number']}", findings, f"source question number {question_id}")
        require(text, f"- source_file: `{record['source_file']}`", findings, f"source_file line {question_id}")
        require(text, f"- source_page_or_section: `{record['source_page_or_section']}`", findings, f"source_page_or_section line {question_id}")
        require(text, f"- manual_review: {record['manual_review_status']}", findings, f"manual_review line {question_id}")
        require(text, f"- manual_review_note: {record['manual_review_note']}", findings, f"manual_review_note line {question_id}")
        require(text, f"  - source_trace_status: {record['source_trace_status']}", findings, f"source_trace_status line {question_id}")
        require(text, f"  - validation_state: {record['validation_status']['state']}", findings, f"validation_state line {question_id}")
        require(text, f"  - answer_status: {record['validation_status']['answer_status']}", findings, f"answer_status line {question_id}")
        require(text, f"  - explanation_status: {record['validation_status']['explanation_status']}", findings, f"explanation_status line {question_id}")
        require(text, f"  - answer_source_file: `{record['answer_source']['answer_source_file']}`", findings, f"answer_source_file line {question_id}")
        require(text, f"  - source_ref: `{record['source_span']['source_ref']}`", findings, f"source_ref line {question_id}")
        require(text, f"  - locator_type: {record['source_span']['locator_type']}", findings, f"source locator line {question_id}")

        paragraph = record["source_span"].get("paragraph")
        if paragraph is not None:
            require(text, f"  - paragraph: {paragraph}", findings, f"source paragraph line {question_id}")

        if record["section_type"] == "reading":
            require(text, f"- answer: {record['answer']}", findings, f"reading answer line {question_id}")
            require(text, f"  - passage_id: {record['passage_id']}", findings, f"passage_id line {question_id}")
            require(text, f"  - block_id: {record['block_id']}", findings, f"block_id line {question_id}")
            require(text, f"  - passage_ref: `{record['passage_ref']}`", findings, f"passage_ref line {question_id}")
            require(text, f"- question_text: {record['question_text']}", findings, f"question_text line {question_id}")
            for option in record.get("options") or []:
                require(text, f"  - {option['label']}. {option['text']}", findings, f"option {question_id} {option['label']}")
        elif record["section_type"] == "writing":
            answer = record.get("answer")
            if isinstance(answer, dict):
                require(text, "- answer_reference_status: confirmed sample_answer object preserved from JSONL", findings, f"writing answer status {question_id}")
                require(text, answer.get("text", ""), findings, f"writing answer text {question_id}")
            require(text, f"- writing_task: {record['question_text']}", findings, f"writing task line {question_id}")
        else:
            findings.append(f"unsupported section_type in JSONL: {record['section_type']}")

    if findings:
        print("FAIL")
        for finding in findings:
            print(finding)
        return 1

    print(
        "PASS "
        f"jsonl_records={total_count} "
        f"markdown_records={total_count} "
        f"reading_records={section_counts.get('reading', 0)} "
        f"writing_records={section_counts.get('writing', 0)} "
        f"manual_review={manual_review_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
