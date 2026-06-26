#!/usr/bin/env python3
"""Validate the EXAM-CLEAN-014 Excel question-bank index."""

import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


REQUIRED_COLUMNS = [
    "record_id",
    "question_type",
    "source_file",
    "source_page_or_section",
    "source_question_number",
    "title_or_prompt",
    "answer",
    "source_trace_status",
    "manual_review_status",
    "manual_review_note",
]
EXPECTED_RECORDS = 8
EXPECTED_READING = 3
EXPECTED_WRITING = 5
NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
}


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


def column_letters_to_index(cell_ref):
    letters = re.match(r"([A-Z]+)", cell_ref)
    if not letters:
        raise ValueError(f"invalid cell reference: {cell_ref}")
    index = 0
    for char in letters.group(1):
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index - 1


def read_cell_value(cell, shared_strings):
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        text = "".join(cell.itertext())
        return text.strip()

    value_node = cell.find("main:v", NS)
    if value_node is None:
        return ""
    raw = value_node.text or ""

    if cell_type == "s":
        return shared_strings[int(raw)]

    return raw.strip()


def load_shared_strings(archive):
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    values = []
    for si in root.findall("main:si", NS):
        values.append("".join(si.itertext()).strip())
    return values


def load_sheet_rows(xlsx_path):
    with zipfile.ZipFile(xlsx_path) as archive:
        required_members = {
            "[Content_Types].xml",
            "_rels/.rels",
            "xl/workbook.xml",
            "xl/_rels/workbook.xml.rels",
            "xl/worksheets/sheet1.xml",
            "xl/styles.xml",
        }
        missing_members = sorted(required_members - set(archive.namelist()))
        if missing_members:
            raise ValueError(f"{xlsx_path}: missing workbook members: {', '.join(missing_members)}")

        shared_strings = load_shared_strings(archive)
        sheet_root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))

    rows = []
    for row in sheet_root.findall(".//main:sheetData/main:row", NS):
        row_values = []
        cells = row.findall("main:c", NS)
        if not cells:
            rows.append(row_values)
            continue

        max_index = max(column_letters_to_index(cell.attrib["r"]) for cell in cells)
        row_values = [""] * (max_index + 1)
        for cell in cells:
            column_index = column_letters_to_index(cell.attrib["r"])
            row_values[column_index] = read_cell_value(cell, shared_strings)
        rows.append(row_values)
    return rows


def main(argv):
    if len(argv) != 3:
        print(
            "Usage: python3 workflow/validation/validate_excel_index.py "
            "<structured_question_bank.jsonl> <question_bank_index.xlsx>",
            file=sys.stderr,
        )
        return 2

    jsonl_path = Path(argv[1])
    xlsx_path = Path(argv[2])

    try:
        records = load_jsonl(jsonl_path)
    except ValueError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    if len(records) != EXPECTED_RECORDS:
        print(f"FAIL expected {EXPECTED_RECORDS} jsonl records, found {len(records)}", file=sys.stderr)
        return 1

    if not xlsx_path.is_file():
        print(f"FAIL Excel index file does not exist: {xlsx_path}", file=sys.stderr)
        return 1

    try:
        rows = load_sheet_rows(xlsx_path)
    except (ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    findings = []
    if not rows:
        findings.append("worksheet is empty")
    else:
        header = rows[0]
        for column in REQUIRED_COLUMNS:
            if column not in header:
                findings.append(f"missing required column {column}")

        data_rows = []
        for row in rows[1:]:
            trimmed = row[: len(header)] + [""] * max(0, len(header) - len(row))
            if any(str(value).strip() for value in trimmed):
                data_rows.append(dict(zip(header, trimmed)))

        if len(data_rows) != EXPECTED_RECORDS:
            findings.append(f"expected {EXPECTED_RECORDS} data rows, found {len(data_rows)}")

        jsonl_by_id = {record["question_id"]: record for record in records}
        seen_ids = set()
        section_counts = Counter()

        for row in data_rows:
            record_id = row.get("record_id", "").strip()
            if not record_id:
                findings.append("row missing record_id")
                continue
            if record_id in seen_ids:
                findings.append(f"duplicate record_id in worksheet: {record_id}")
                continue
            seen_ids.add(record_id)

            record = jsonl_by_id.get(record_id)
            if record is None:
                findings.append(f"worksheet record_id not found in JSONL: {record_id}")
                continue

            section_type = record.get("section_type")
            section_counts[section_type] += 1

            if row.get("question_type", "").strip() != str(record.get("question_type")):
                findings.append(f"question_type mismatch for {record_id}")
            if row.get("source_file", "").strip() != str(record.get("source_file")):
                findings.append(f"source_file mismatch for {record_id}")
            if row.get("source_question_number", "").strip() != str(record.get("source_question_number")):
                findings.append(f"source_question_number mismatch for {record_id}")
            if row.get("source_trace_status", "").strip() != str(record.get("source_trace_status")):
                findings.append(f"source_trace_status mismatch for {record_id}")
            if row.get("manual_review_status", "").strip() != str(record.get("manual_review_status")):
                findings.append(f"manual_review_status mismatch for {record_id}")
            if row.get("manual_review_note", "").strip() != str(record.get("manual_review_note")):
                findings.append(f"manual_review_note mismatch for {record_id}")

            source_page_or_section = row.get("source_page_or_section", "").strip()
            if not source_page_or_section:
                findings.append(f"source_page_or_section empty for {record_id}")
            if record.get("source_page_or_section") not in source_page_or_section:
                findings.append(f"source_page_or_section missing JSONL trace for {record_id}")

            title_or_prompt = row.get("title_or_prompt", "").strip()
            if not title_or_prompt:
                findings.append(f"title_or_prompt empty for {record_id}")

            answer_value = row.get("answer", "").strip()
            if not answer_value:
                findings.append(f"answer empty for {record_id}")

            if section_type == "reading":
                if record.get("passage_id") not in title_or_prompt or record.get("block_id") not in title_or_prompt:
                    findings.append(f"reading row missing passage/block link in title_or_prompt for {record_id}")
                if record.get("answer") != answer_value:
                    findings.append(f"reading answer mismatch for {record_id}")
            elif section_type == "writing":
                prompt_head = str(record.get("question_text", "")).split("。", 1)[0].strip()
                if prompt_head and prompt_head not in title_or_prompt:
                    findings.append(f"writing row missing prompt summary for {record_id}")
                answer = record.get("answer")
                if not isinstance(answer, dict) or str(answer.get("text", "")).strip() not in answer_value:
                    findings.append(f"writing answer cell does not preserve sample answer text for {record_id}")
            else:
                findings.append(f"unsupported section_type in JSONL for {record_id}: {section_type}")

        for record in records:
            if record["question_id"] not in seen_ids:
                findings.append(f"missing worksheet row for record_id={record['question_id']}")

        if section_counts.get("reading", 0) != EXPECTED_READING:
            findings.append(f"expected reading={EXPECTED_READING}, found {section_counts.get('reading', 0)}")
        if section_counts.get("writing", 0) != EXPECTED_WRITING:
            findings.append(f"expected writing={EXPECTED_WRITING}, found {section_counts.get('writing', 0)}")

    if findings:
        print("FAIL")
        for finding in findings:
            print(finding)
        return 1

    print(
        "PASS "
        f"excel_records={EXPECTED_RECORDS} "
        f"reading_records={EXPECTED_READING} "
        f"writing_records={EXPECTED_WRITING} "
        "required_columns=10"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
