#!/usr/bin/env python3
"""Validate the EXAM-CLEAN-006 minimal question-record JSONL slice."""

import json
import sys
from pathlib import Path


OPTION_LABELS = {"A", "B", "C", "D"}
TRACE_FIELDS = (
    "source_file",
    "source_page_or_section",
    "source_question_number",
    "source_trace_status",
)


def is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def option_labels(options):
    labels = set()
    if not isinstance(options, list):
        return labels
    for option in options:
        if not isinstance(option, dict):
            continue
        label = option.get("label")
        text = option.get("text")
        if is_non_empty_string(label) and is_non_empty_string(text):
            labels.add(label.strip().upper())
    return labels


def needs_manual_review(record):
    status = record.get("source_trace_status")
    note = record.get("manual_review_note")
    validation_status = record.get("validation_status")
    if status == "NEEDS_MANUAL_REVIEW":
        return True
    if isinstance(note, str) and "NEEDS_MANUAL_REVIEW" in note:
        return True
    if isinstance(validation_status, dict) and validation_status.get("state") in {"warn", "fail"}:
        return True
    return False


def validate_record(record, line_number):
    errors = []
    question_id = record.get("question_id") or f"line {line_number}"

    if not is_non_empty_string(record.get("question_id")):
        errors.append(f"line {line_number}: missing question_id")

    question_text = record.get("question_text") or record.get("stem")
    if not is_non_empty_string(question_text):
        errors.append(f"{question_id}: missing question_text/stem")

    if record.get("question_type") == "reading_subquestion":
        if not is_non_empty_string(record.get("passage_id")):
            errors.append(f"{question_id}: missing passage_id")
        if not is_non_empty_string(record.get("block_id")):
            errors.append(f"{question_id}: missing block_id")
        if not (
            is_non_empty_string(record.get("passage_text"))
            or is_non_empty_string(record.get("passage_ref"))
        ):
            errors.append(f"{question_id}: missing passage_text or passage_ref")

    labels = option_labels(record.get("options"))
    missing_labels = sorted(OPTION_LABELS - labels)
    extra_labels = sorted(labels - OPTION_LABELS)
    if missing_labels:
        errors.append(f"{question_id}: missing option labels {','.join(missing_labels)}")
    if extra_labels:
        errors.append(f"{question_id}: unexpected option labels {','.join(extra_labels)}")

    answer = record.get("answer")
    if is_non_empty_string(answer):
        normalized_answer = answer.strip().upper()
        if normalized_answer not in OPTION_LABELS:
            errors.append(f"{question_id}: answer not in A-D ({answer})")
    elif not needs_manual_review(record):
        errors.append(f"{question_id}: missing answer without manual review status")

    for field in TRACE_FIELDS:
        if not is_non_empty_string(record.get(field)):
            errors.append(f"{question_id}: missing source trace field {field}")

    if "manual_review_note" not in record:
        errors.append(f"{question_id}: missing manual_review_note field")

    return errors


def main(argv):
    if len(argv) != 2:
        print(
            "FAIL usage: python3 workflow/validation/validate_question_records_slice.py "
            "<question-records.jsonl>",
            file=sys.stderr,
        )
        return 2

    input_path = Path(argv[1])
    if not input_path.is_file():
        print(f"FAIL input file not found: {input_path}", file=sys.stderr)
        return 2

    errors = []
    record_count = 0
    manual_review_count = 0

    with input_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(record, dict):
                errors.append(f"line {line_number}: record entry is not an object")
                continue
            record_count += 1
            if needs_manual_review(record):
                manual_review_count += 1
            errors.extend(validate_record(record, line_number))

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"PASS question_records={record_count} manual_review={manual_review_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
