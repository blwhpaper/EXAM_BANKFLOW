#!/usr/bin/env python3
"""Validate the EXAM-CLEAN-012 Word summary export."""

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

try:
    from docx import Document
except ModuleNotFoundError:
    Document = None


def rerun_with_bundled_python():
    current = Path(__file__).resolve()
    candidates = [
        Path(
            "/Users/johntsin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
        ),
        Path.home()
        / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3",
    ]
    for candidate in candidates:
        if not candidate.is_file():
            continue
        env = os.environ.copy()
        env["EXAM_DOCX_VALIDATOR_REEXEC"] = "1"
        result = subprocess.run([str(candidate), str(current), *sys.argv[1:]], env=env)
        return result.returncode
    print(
        "FAIL python-docx is unavailable in system python3 and no bundled runtime was found",
        file=sys.stderr,
    )
    return 1


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
        findings.append(f"missing docx content for {label}: {needle}")


def main(argv):
    if Document is None:
        if os.environ.get("EXAM_DOCX_VALIDATOR_REEXEC") == "1":
            print("FAIL python-docx import failed inside bundled runtime", file=sys.stderr)
            return 1
        return rerun_with_bundled_python()

    if len(argv) != 3:
        print(
            "Usage: python3 workflow/validation/validate_word_summary_export.py "
            "<structured_question_bank.jsonl> <summary.docx>",
            file=sys.stderr,
        )
        return 2

    jsonl_path = Path(argv[1])
    docx_path = Path(argv[2])

    try:
        records = load_jsonl(jsonl_path)
    except ValueError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    if len(records) != 8:
        print(f"FAIL expected 8 jsonl records, found {len(records)}", file=sys.stderr)
        return 1

    if not docx_path.is_file():
        print(f"FAIL docx file does not exist: {docx_path}", file=sys.stderr)
        return 1

    if docx_path.stat().st_size <= 0:
        print(f"FAIL docx file is empty: {docx_path}", file=sys.stderr)
        return 1

    try:
        document = Document(docx_path)
    except Exception as exc:
        print(f"FAIL docx could not be opened by python-docx: {exc}", file=sys.stderr)
        return 1

    text = "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text)
    findings = []
    counts = Counter(record.get("section_type") for record in records)

    require(text, "EXAM-CLEAN-012", findings, "task identifier")
    require(text, "total_records: 8", findings, "total record count")
    require(text, "reading=3", findings, "reading distribution")
    require(text, "writing=5", findings, "writing distribution")

    for index, record in enumerate(records, start=1):
        require(text, record["question_id"], findings, f"question_id {record['question_id']}")
        require(
            text,
            f"Record {index}",
            findings,
            f"record marker {record['question_id']}",
        )
        require(
            text,
            f"Question Number: {record['source_question_number']}",
            findings,
            f"question number {record['question_id']}",
        )
        require(
            text,
            f"Source Trace: {record['source_file']}",
            findings,
            f"source trace {record['question_id']}",
        )

        if record["section_type"] == "reading":
            require(text, "Passage/Context:", findings, "reading passage heading")
            require(text, f"Question: {record['question_text']}", findings, f"reading question {record['question_id']}")
            for option in record["options"]:
                require(
                    text,
                    f"{option['label']}. {option['text']}",
                    findings,
                    f"option {record['question_id']} {option['label']}",
                )
            require(
                text,
                f"Confirmed Answer: {record['answer']}",
                findings,
                f"reading answer {record['question_id']}",
            )
        elif record["section_type"] == "writing":
            require(text, f"Prompt/Task: {record['question_text']}", findings, f"writing prompt {record['question_id']}")
            answer = record.get("answer")
            if isinstance(answer, dict) and answer.get("text"):
                require(
                    text,
                    "Confirmed Answer:",
                    findings,
                    f"writing answer heading {record['question_id']}",
                )
                require(text, answer["text"], findings, f"writing answer text {record['question_id']}")
            else:
                require(
                    text,
                    "Answer Note:",
                    findings,
                    f"writing answer note {record['question_id']}",
                )
        else:
            findings.append(f"unsupported section_type in JSONL: {record['section_type']}")

    if findings:
        print("FAIL")
        for finding in findings:
            print(finding)
        return 1

    print(
        "PASS "
        f"jsonl_records={len(records)} "
        f"docx_sections={len(document.sections)} "
        f"word_records={len(records)} "
        f"reading_records={counts.get('reading', 0)} "
        f"writing_records={counts.get('writing', 0)} "
        "manual_review=required"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
