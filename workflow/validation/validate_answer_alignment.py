#!/usr/bin/env python3
"""Validate answer-alignment expectations for question-record slices.

This validator is intentionally narrow. It checks that answer fields exist in a
schema-compatible shape for the record type, that answer support remains
traceable to visible source ranges, and that unresolved items are explicitly
marked for manual review instead of being guessed.
"""

import json
import sys
from pathlib import Path


READY_STATUSES = {"READY", "confirmed"}
REVIEW_STATUSES = {"NEEDS_MANUAL_REVIEW", "UNKNOWN", "EXCLUDED"}
OBJECTIVE_TYPES = {"single_choice", "multiple_choice", "reading_subquestion"}
SUBJECTIVE_TYPES = {"writing", "short_answer", "grammar_fill"}


def is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def is_non_empty_value(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def load_records(path):
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


def validate_record(path, line_number, record):
    findings = []
    question_id = record.get("question_id", "<missing>")
    question_type = str(record.get("question_type") or "").strip()
    answer = record.get("answer")
    source_trace_status = record.get("source_trace_status")
    validation_status = record.get("validation_status")
    source_trace = record.get("source_trace")
    manual_review_status = record.get("manual_review_status")
    manual_review_note = record.get("manual_review_note")

    prefix = f"{path}:{line_number} question_id={question_id}"

    if question_type in OBJECTIVE_TYPES:
        if not is_non_empty_string(answer):
            findings.append(f"{prefix}: objective question must use non-empty string answer")
        if not isinstance(record.get("options"), list):
            findings.append(f"{prefix}: objective question missing options array")

    elif question_type in SUBJECTIVE_TYPES:
        if not isinstance(answer, dict):
            findings.append(f"{prefix}: subjective question must use object answer payload")
        else:
            if not is_non_empty_string(answer.get("answer_type")):
                findings.append(f"{prefix}: subjective answer missing answer_type")
            if not is_non_empty_string(answer.get("text")):
                findings.append(f"{prefix}: subjective answer missing text")
            if not is_non_empty_string(answer.get("source")):
                findings.append(f"{prefix}: subjective answer missing source")

    elif not is_non_empty_value(answer):
        findings.append(f"{prefix}: answer missing for unclassified question type {question_type}")

    if source_trace_status in READY_STATUSES:
        if not isinstance(source_trace, dict):
            findings.append(f"{prefix}: READY/confirmed record missing source_trace object")
        else:
            if not is_non_empty_string(source_trace.get("answer_source_file")):
                findings.append(f"{prefix}: source_trace missing answer_source_file")
            answer_source_span = source_trace.get("answer_source_span")
            if not isinstance(answer_source_span, dict):
                findings.append(f"{prefix}: source_trace missing answer_source_span")
            else:
                if not is_non_empty_string(answer_source_span.get("locator_type")):
                    findings.append(f"{prefix}: answer_source_span missing locator_type")
                if not (
                    is_non_empty_value(answer_source_span.get("paragraph"))
                    or is_non_empty_value(answer_source_span.get("page"))
                    or is_non_empty_value(answer_source_span.get("line_start"))
                ):
                    findings.append(f"{prefix}: answer_source_span missing concrete locator")
                if not is_non_empty_string(answer_source_span.get("excerpt")):
                    findings.append(f"{prefix}: answer_source_span missing excerpt")

    if not isinstance(validation_status, dict):
        findings.append(f"{prefix}: validation_status missing")
    else:
        answer_status = validation_status.get("answer_status")
        if answer_status == "confirmed" and not is_non_empty_value(answer):
            findings.append(f"{prefix}: answer_status=confirmed but answer is empty")
        if answer_status != "confirmed" and source_trace_status in READY_STATUSES:
            findings.append(
                f"{prefix}: source_trace_status={source_trace_status} conflicts with answer_status={answer_status}"
            )

    if source_trace_status in REVIEW_STATUSES or (
        isinstance(validation_status, dict)
        and validation_status.get("answer_status") in {"missing_in_source", "uncertain"}
    ):
        if manual_review_status != "required":
            findings.append(f"{prefix}: unresolved answer must set manual_review_status=required")
        if not is_non_empty_string(manual_review_note):
            findings.append(f"{prefix}: unresolved answer missing manual_review_note")

    return findings


def main(argv):
    if len(argv) < 2:
        print(
            "Usage: python3 workflow/validation/validate_answer_alignment.py <slice.jsonl> [<slice.jsonl> ...]",
            file=sys.stderr,
        )
        return 2

    total_records = 0
    confirmed_answers = 0
    manual_review = 0
    missing_answers = 0
    findings = []

    for raw_path in argv[1:]:
        path = Path(raw_path)
        try:
            records = load_records(path)
        except ValueError as exc:
            print(f"FAIL {exc}", file=sys.stderr)
            return 1

        for line_number, record in records:
            total_records += 1
            findings.extend(validate_record(path, line_number, record))

            validation_status = record.get("validation_status")
            answer = record.get("answer")
            if isinstance(validation_status, dict) and validation_status.get("answer_status") == "confirmed":
                confirmed_answers += 1
            if record.get("manual_review_status") == "required":
                manual_review += 1
            if not is_non_empty_value(answer):
                missing_answers += 1

    if findings:
        print("FAIL")
        for finding in findings:
            print(finding)
        return 1

    print(
        f"PASS answer_alignment_records={total_records} "
        f"confirmed_answers={confirmed_answers} manual_review={manual_review} missing_answers={missing_answers}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
