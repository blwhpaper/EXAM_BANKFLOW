#!/usr/bin/env python3
"""Validate question-record JSONL slices.

The validator intentionally stays lightweight and repository-local: it uses
only the Python standard library and enforces the minimum provenance, answer,
option, and reading-block linkage rules needed before a slice can move forward.
"""

import json
import sys
from pathlib import Path


OPTION_LABELS = {"A", "B", "C", "D"}
CHOICE_QUESTION_TYPES = {"single_choice", "multiple_choice", "reading_subquestion"}
READING_QUESTION_TYPES = {"reading_subquestion"}
ALLOWED_SOURCE_TRACE_STATUSES = {
    "READY",
    "NEEDS_MANUAL_REVIEW",
    "EXCLUDED",
    "UNKNOWN",
    # Existing EXAM-CLEAN-006/004 records use this confirmed-source wording.
    "confirmed",
}
READY_EQUIVALENT_STATUSES = {"READY", "confirmed"}
TODO_MARKERS = ("TODO", "TBD", "UNKNOWN", "NEEDS_MANUAL_REVIEW")
REQUIRED_FIELDS = (
    "question_id",
    "exam_id",
    "section_id",
    "question_number",
    "question_type",
    "stem",
    "source_span",
    "normalization_notes",
    "validation_status",
)
TRACE_FIELDS = (
    "source_file",
    "source_page_or_section",
    "source_question_number",
    "source_trace_status",
)
DEFAULT_READING_BLOCKS_PATH = (
    Path(__file__).resolve().parents[1]
    / "records"
    / "EXAM-CLEAN-004_READING_BLOCKS.jsonl"
)


def is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def is_non_empty_value(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def display_question_id(record, line_number):
    question_id = record.get("question_id")
    if is_non_empty_string(question_id):
        return question_id.strip()
    return "<missing>"


def issue(line_number, question_id, message):
    return f"line {line_number} question_id={question_id}: {message}"


def option_label_map(options):
    labels = {}
    if not isinstance(options, list):
        return labels
    for index, option in enumerate(options, start=1):
        if not isinstance(option, dict):
            continue
        label = option.get("label")
        text = option.get("text")
        if is_non_empty_string(label):
            labels[label.strip().upper()] = (text, index)
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


def is_reading_question(record):
    question_type = str(record.get("question_type") or "").strip()
    return question_type in READING_QUESTION_TYPES or "reading" in question_type or "comprehension" in question_type


def is_choice_question(record):
    question_type = str(record.get("question_type") or "").strip()
    return question_type in CHOICE_QUESTION_TYPES or record.get("options") is not None


def normalize_answer_labels(answer):
    if isinstance(answer, str):
        cleaned = (
            answer.strip()
            .upper()
            .replace(",", "")
            .replace("，", "")
            .replace("/", "")
            .replace("、", "")
            .replace(" ", "")
        )
        return list(cleaned) if cleaned else []
    if isinstance(answer, list):
        labels = []
        for item in answer:
            if not is_non_empty_string(item):
                return None
            labels.append(item.strip().upper())
        return labels
    return None


def reading_block_reference(record):
    for field in ("reading_block_id", "block_id", "passage_id"):
        value = record.get(field)
        if is_non_empty_string(value):
            return field, value.strip()
    return None, None


def load_reading_block_ids(path):
    block_ids = set()
    errors = []
    if not path.is_file():
        return block_ids, [f"reading block file not found: {path}"]

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                block = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(block, dict):
                errors.append(f"{path}:{line_number}: reading block entry is not an object")
                continue
            block_id = block.get("reading_block_id")
            if is_non_empty_string(block_id):
                block_ids.add(block_id.strip())
            else:
                errors.append(f"{path}:{line_number}: missing reading_block_id")
    return block_ids, errors


def validate_required_fields(record, line_number, question_id):
    errors = []
    for field in REQUIRED_FIELDS:
        value = record.get(field)
        if not is_non_empty_value(value):
            errors.append(issue(line_number, question_id, f"missing required field {field}"))
    for field in TRACE_FIELDS:
        value = record.get(field)
        if field == "source_question_number":
            missing = not is_non_empty_value(value)
        else:
            missing = not is_non_empty_string(value)
        if missing:
            errors.append(issue(line_number, question_id, f"missing source trace field {field}"))
    return errors


def validate_source_trace_status(record, line_number, question_id):
    errors = []
    status = record.get("source_trace_status")
    if not is_non_empty_string(status):
        return errors
    if status not in ALLOWED_SOURCE_TRACE_STATUSES:
        allowed = ", ".join(sorted(ALLOWED_SOURCE_TRACE_STATUSES))
        errors.append(
            issue(
                line_number,
                question_id,
                f"source_trace_status must be one of {allowed} (got {status})",
            )
        )
    return errors


def validate_choice_record(record, line_number, question_id):
    errors = []
    warnings = []
    options = record.get("options")
    if not isinstance(options, list) or not options:
        errors.append(issue(line_number, question_id, "choice question missing options"))
        return errors, warnings

    labels = option_label_map(options)
    label_set = set(labels)
    missing_labels = sorted(OPTION_LABELS - label_set)
    extra_labels = sorted(label_set - OPTION_LABELS)
    if missing_labels:
        errors.append(
            issue(
                line_number,
                question_id,
                f"missing option labels {','.join(missing_labels)}",
            )
        )
    if extra_labels:
        errors.append(
            issue(
                line_number,
                question_id,
                f"unexpected option labels {','.join(extra_labels)}",
            )
        )
    for label in sorted(OPTION_LABELS & label_set):
        text, index = labels[label]
        if not is_non_empty_string(text):
            errors.append(
                issue(
                    line_number,
                    question_id,
                    f"option {label} at options[{index}] has empty text",
                )
            )

    answer = record.get("answer")
    answer_labels = normalize_answer_labels(answer)
    question_type = record.get("question_type")
    if answer_labels:
        invalid = [label for label in answer_labels if label not in label_set]
        if invalid:
            errors.append(
                issue(
                    line_number,
                    question_id,
                    f"answer references missing option labels {','.join(invalid)}",
                )
            )
        if question_type == "single_choice" and len(answer_labels) != 1:
            errors.append(
                issue(
                    line_number,
                    question_id,
                    f"single_choice answer must contain exactly one option label (got {answer})",
                )
            )
    elif answer_labels is None and answer is not None:
        warnings.append(
            issue(
                line_number,
                question_id,
                "structured choice answer is not fully validated; TODO define object answer rule",
            )
        )
    elif not needs_manual_review(record):
        errors.append(issue(line_number, question_id, "missing answer without manual review status"))

    return errors, warnings


def validate_reading_linkage(record, line_number, question_id, reading_block_ids):
    errors = []
    field, block_id = reading_block_reference(record)
    if not block_id:
        errors.append(
            issue(
                line_number,
                question_id,
                "reading/comprehension question missing reading_block_id/block_id/passage_id",
            )
        )
        return errors
    if block_id not in reading_block_ids:
        errors.append(
            issue(
                line_number,
                question_id,
                f"{field}={block_id} not found in reading blocks index",
            )
        )
    if not (
        is_non_empty_string(record.get("passage_text"))
        or is_non_empty_string(record.get("passage_ref"))
    ):
        errors.append(issue(line_number, question_id, "missing passage_text or passage_ref"))
    return errors


def validate_manual_review_logic(record, line_number, question_id):
    errors = []
    note = record.get("manual_review_note")
    status = record.get("source_trace_status")
    if "manual_review_note" not in record:
        errors.append(issue(line_number, question_id, "missing manual_review_note field"))
        return errors

    if status == "NEEDS_MANUAL_REVIEW" and not is_non_empty_string(note):
        errors.append(
            issue(
                line_number,
                question_id,
                "NEEDS_MANUAL_REVIEW requires a concrete manual_review_note",
            )
        )
    if status in READY_EQUIVALENT_STATUSES and is_non_empty_string(note):
        normalized_note = note.upper()
        marker_hits = [marker for marker in TODO_MARKERS if marker in normalized_note]
        if marker_hits:
            errors.append(
                issue(
                    line_number,
                    question_id,
                    f"ready/confirmed record has unresolved manual_review_note marker {','.join(marker_hits)}",
                )
            )
    return errors


def validate_record(record, line_number, reading_block_ids):
    question_id = display_question_id(record, line_number)
    errors = []
    warnings = []

    errors.extend(validate_required_fields(record, line_number, question_id))
    errors.extend(validate_source_trace_status(record, line_number, question_id))

    question_text = record.get("question_text") or record.get("stem")
    if not is_non_empty_string(question_text):
        errors.append(issue(line_number, question_id, "missing question_text/stem"))

    if is_choice_question(record):
        choice_errors, choice_warnings = validate_choice_record(record, line_number, question_id)
        errors.extend(choice_errors)
        warnings.extend(choice_warnings)
    elif record.get("options") not in (None, []):
        warnings.append(
            issue(
                line_number,
                question_id,
                "non-choice options present; TODO define validation rule for this question_type",
            )
        )

    if is_reading_question(record):
        errors.extend(
            validate_reading_linkage(record, line_number, question_id, reading_block_ids)
        )

    errors.extend(validate_manual_review_logic(record, line_number, question_id))

    return errors, warnings


def main(argv):
    if len(argv) not in (2, 3):
        print(
            "FAIL usage: python3 workflow/validation/validate_question_records_slice.py "
            "<question-records.jsonl> [reading-blocks.jsonl]",
            file=sys.stderr,
        )
        return 2

    input_path = Path(argv[1])
    if not input_path.is_file():
        print(f"FAIL input file not found: {input_path}", file=sys.stderr)
        return 2

    reading_blocks_path = Path(argv[2]) if len(argv) == 3 else DEFAULT_READING_BLOCKS_PATH
    reading_block_ids, reading_block_errors = load_reading_block_ids(reading_blocks_path)
    errors = []
    warnings = []
    record_count = 0
    manual_review_count = 0
    question_ids = {}
    reading_question_count = 0
    errors.extend(reading_block_errors)

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
            question_id = display_question_id(record, line_number)
            if is_non_empty_string(record.get("question_id")):
                if question_id in question_ids:
                    errors.append(
                        issue(
                            line_number,
                            question_id,
                            f"duplicate question_id also seen on line {question_ids[question_id]}",
                        )
                    )
                else:
                    question_ids[question_id] = line_number
            if needs_manual_review(record):
                manual_review_count += 1
            if is_reading_question(record):
                reading_question_count += 1
            record_errors, record_warnings = validate_record(
                record, line_number, reading_block_ids
            )
            errors.extend(record_errors)
            warnings.extend(record_warnings)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print("WARN")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    print(
        "PASS "
        f"question_records={record_count} "
        f"manual_review={manual_review_count} "
        f"reading_questions={reading_question_count} "
        f"reading_blocks_indexed={len(reading_block_ids)}"
    )
    if warnings:
        print("WARN")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
