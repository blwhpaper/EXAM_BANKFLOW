#!/usr/bin/env python3
"""Validate passage-first reading block JSONL records."""

import json
import sys
from pathlib import Path


OPTION_LABELS = {"A", "B", "C", "D"}


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
        if isinstance(label, str) and label.strip() and is_non_empty_string(text):
            labels.add(label.strip().upper())
    return labels


def question_number(question):
    number = question.get("question_number")
    return "<missing>" if number in (None, "") else str(number)


def validate_question(block_id, question):
    errors = []
    number = question_number(question)

    for field in ("question_number", "stem", "options", "answer"):
        value = question.get(field)
        if field in ("stem", "answer"):
            missing = not is_non_empty_string(value)
        elif field == "options":
            missing = not isinstance(value, list) or not value
        else:
            missing = value in (None, "")
        if missing:
            errors.append(f"{block_id} q{number}: missing field {field}")

    labels = option_labels(question.get("options"))
    missing_labels = sorted(OPTION_LABELS - labels)
    extra_labels = sorted(labels - OPTION_LABELS)
    if missing_labels:
        errors.append(
            f"{block_id} q{number}: missing option labels {','.join(missing_labels)}"
        )
    if extra_labels:
        errors.append(
            f"{block_id} q{number}: unexpected option labels {','.join(extra_labels)}"
        )

    answer = question.get("answer")
    if isinstance(answer, str):
        normalized_answer = answer.strip().upper()
        if normalized_answer not in OPTION_LABELS:
            errors.append(f"{block_id} q{number}: answer not in A-D ({answer})")
    elif answer is not None:
        errors.append(f"{block_id} q{number}: answer is not a string")

    return errors


def validate_block(block, line_number):
    block_id = block.get("reading_block_id") or f"line {line_number}"
    errors = []

    if not is_non_empty_string(block.get("passage_text")):
        errors.append(f"{block_id}: missing field passage_text")
    if not isinstance(block.get("source_trace"), dict) or not block.get("source_trace"):
        errors.append(f"{block_id}: missing field source_trace")

    questions = block.get("questions")
    if not isinstance(questions, list) or not questions:
        errors.append(f"{block_id}: missing field questions")
        return errors

    for question in questions:
        if not isinstance(question, dict):
            errors.append(f"{block_id}: question entry is not an object")
            continue
        errors.extend(validate_question(block_id, question))

    return errors


def main(argv):
    if len(argv) != 2:
        print(
            "FAIL usage: python3 workflow/validation/validate_reading_blocks.py "
            "<reading-blocks.jsonl>",
            file=sys.stderr,
        )
        return 2

    input_path = Path(argv[1])
    if not input_path.is_file():
        print(f"FAIL input file not found: {input_path}", file=sys.stderr)
        return 2

    errors = []
    block_count = 0
    question_count = 0

    with input_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                block = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(block, dict):
                errors.append(f"line {line_number}: block entry is not an object")
                continue
            block_count += 1
            questions = block.get("questions")
            if isinstance(questions, list):
                question_count += len(questions)
            errors.extend(validate_block(block, line_number))

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS reading_blocks={block_count} questions={question_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
