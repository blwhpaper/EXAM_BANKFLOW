#!/usr/bin/env python3
"""Validate the EXAM-CLEAN-010 structured question-bank JSONL."""

import json
import sys
from collections import Counter
from pathlib import Path


INPUT_SLICE_PATHS = (
    Path("workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl"),
    Path("workflow/records/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.jsonl"),
)
READY_STATUSES = {"READY", "confirmed"}
REQUIRED_FIELDS = (
    "question_id",
    "exam_id",
    "source_file",
    "source_page_or_section",
    "source_question_number",
    "section_type",
    "question_text",
    "answer",
    "answer_source",
    "source_trace_status",
    "manual_review_note",
)


def is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def is_non_empty_value(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


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
            records.append((line_number, record))
    return records


def expected_input_count():
    count = 0
    for path in INPUT_SLICE_PATHS:
        records = load_jsonl(path)
        count += len(records)
    return count


def validate_record(path, line_number, record, seen_ids):
    findings = []
    question_id = record.get("question_id", "<missing>")
    prefix = f"{path}:{line_number} question_id={question_id}"

    for field in REQUIRED_FIELDS:
        if not is_non_empty_value(record.get(field)):
            findings.append(f"{prefix}: missing required field {field}")

    if question_id in seen_ids:
        findings.append(f"{prefix}: duplicate question_id")
    else:
        seen_ids.add(question_id)

    section_type = record.get("section_type")
    question_type = record.get("question_type")
    options = record.get("options")
    answer = record.get("answer")
    answer_source = record.get("answer_source")

    if not is_non_empty_value(answer):
        findings.append(f"{prefix}: answer must be non-empty")

    if not isinstance(answer_source, dict):
        findings.append(f"{prefix}: answer_source must be an object")
    else:
        if not is_non_empty_string(answer_source.get("answer_source_file")):
            findings.append(f"{prefix}: answer_source missing answer_source_file")
        span = answer_source.get("answer_source_span")
        if not isinstance(span, dict):
            findings.append(f"{prefix}: answer_source missing answer_source_span")
        else:
            if not is_non_empty_string(span.get("locator_type")):
                findings.append(f"{prefix}: answer_source_span missing locator_type")
            if not (
                is_non_empty_value(span.get("paragraph"))
                or is_non_empty_value(span.get("page"))
                or is_non_empty_value(span.get("line_start"))
            ):
                findings.append(f"{prefix}: answer_source_span missing concrete locator")

    if section_type == "reading":
        if question_type != "reading_subquestion":
            findings.append(f"{prefix}: reading section_type must use question_type=reading_subquestion")
        if not is_non_empty_string(record.get("passage_id")):
            findings.append(f"{prefix}: reading record missing passage_id")
        if not is_non_empty_string(record.get("block_id")):
            findings.append(f"{prefix}: reading record missing block_id")
        if not is_non_empty_string(record.get("passage_ref")):
            findings.append(f"{prefix}: reading record missing passage_ref")
        if not isinstance(options, list) or not options:
            findings.append(f"{prefix}: reading record missing options array")
    elif section_type == "writing":
        if question_type != "writing":
            findings.append(f"{prefix}: writing section_type must use question_type=writing")
        if options is not None:
            findings.append(f"{prefix}: writing record must keep options=null")
    else:
        findings.append(f"{prefix}: unsupported section_type {section_type}")

    status = record.get("source_trace_status")
    if status in READY_STATUSES and not is_non_empty_value(answer):
        findings.append(f"{prefix}: READY/confirmed record cannot have empty answer")

    if record.get("manual_review_status") == "required" and not is_non_empty_string(record.get("manual_review_note")):
        findings.append(f"{prefix}: manual_review_status=required missing manual_review_note")

    return findings


def main(argv):
    if len(argv) != 2:
        print(
            "Usage: python3 workflow/validation/validate_structured_question_bank.py <structured_question_bank.jsonl>",
            file=sys.stderr,
        )
        return 2

    path = Path(argv[1])
    try:
        records = load_jsonl(path)
    except ValueError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    findings = []
    seen_ids = set()
    section_counts = Counter()
    manual_review = 0

    for line_number, record in records:
        findings.extend(validate_record(path, line_number, record, seen_ids))
        section_counts[str(record.get("section_type"))] += 1
        if record.get("manual_review_status") == "required":
            manual_review += 1

    try:
        input_count = expected_input_count()
    except ValueError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    output_count = len(records)
    if output_count != input_count:
        findings.append(
            f"{path}: output record count {output_count} does not match input slice count {input_count}"
        )

    if findings:
        print("FAIL")
        for finding in findings:
            print(finding)
        return 1

    print(
        "PASS "
        f"structured_records={output_count} "
        f"input_records={input_count} "
        f"reading_records={section_counts.get('reading', 0)} "
        f"writing_records={section_counts.get('writing', 0)} "
        f"manual_review={manual_review}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
