# Minimum Validation Commands

## Purpose

These commands define the current minimum validation flow for harness tasks and future early `EXAM-CLEAN-*` tasks. Commands must be non-interactive and must not open editors such as `vi`.

Run commands from the repository root:

```sh
cd /Users/apple/Projects/EXAM_BANKFLOW
```

## Repository State

```sh
git status --short
```

```sh
git status --short --branch
```

## File Inventory

```sh
find workflow -maxdepth 3 -type f | sort
```

## JSON Readability

```sh
python3 -m json.tool workflow/TASK_STATE.json
```

For future structured JSON outputs:

```sh
python3 -m json.tool path/to/output.structured.json
```

## EXAM-CLEAN-007 Question Records Hardening

For every question-records slice, run at least:

```sh
python3 workflow/validation/validate_question_records_slice.py workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl
```

```sh
python3 workflow/validation/validate_reading_blocks.py workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl
```

```sh
python3 -m json.tool workflow/TASK_STATE.json >/dev/null
```

```sh
git diff --check
```

## EXAM-CLEAN-009 Answer Alignment

For mixed reading/writing question-record answer audits, run:

```sh
python3 workflow/validation/validate_answer_alignment.py workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl workflow/records/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.jsonl
```

## EXAM-CLEAN-010 Structured Data Ingest

For the structured question-bank slice, run:

```sh
python3 workflow/validation/validate_structured_question_bank.py workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl
```

## EXAM-CLEAN-011 Markdown Summary Export

For the markdown summary export, run:

```sh
python3 workflow/validation/validate_markdown_summary_export.py workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl workflow/exports/EXAM-CLEAN-011_QUESTION_BANK_SUMMARY.md
```

## EXAM-CLEAN-012 Word Summary Export

For the Word summary export, run:

```sh
python3 workflow/validation/validate_word_summary_export.py workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl workflow/exports/EXAM-CLEAN-012_QUESTION_BANK_SUMMARY.docx
```

## EXAM-CLEAN-013 Manual Review QA

For the manual review QA layer, run:

```sh
python3 workflow/validation/validate_manual_review_qa.py workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl workflow/cleaning/EXAM-CLEAN-013_MANUAL_REVIEW_QA.md
```

## EXAM-CLEAN-014 Excel Index

For the Excel total index, run:

```sh
python3 workflow/validation/validate_excel_index.py workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl workflow/exports/EXAM-CLEAN-014_QUESTION_BANK_INDEX.xlsx
```

## Basic Grep Checks

Check that agent rules contain the required execution and safety language:

```sh
grep -n "Forbidden Actions" workflow/agents/AGENTS.md
grep -n "Required Startup Flow" workflow/agents/AGENTS.md
grep -n "Exception Handling" workflow/agents/AGENTS.md
grep -n "Validation Expectations" workflow/agents/AGENTS.md
```

Check that validation docs name the required check families:

```sh
grep -n "schema checks" workflow/validation/README.md
grep -n "required fields" workflow/validation/README.md
grep -n "source trace" workflow/validation/README.md
grep -n "duplicate.*question_id" workflow/validation/README.md
grep -n "answer/explanation consistency" workflow/validation/README.md
grep -n "output format" workflow/validation/README.md
```

Check task state and index references:

```sh
grep -n "EXAM-HARNESS-004" workflow/TASK_INDEX.md workflow/TASK_STATE.json workflow/Task_Closeouts/EXAM-HARNESS-004_Closeout.md
grep -n "EXAM-CLEAN-001" workflow/TASK_INDEX.md workflow/TASK_STATE.json workflow/Task_Closeouts/EXAM-HARNESS-004_Closeout.md
```

## YAML Readability

Ruby includes a standard YAML parser on common macOS developer systems:

```sh
ruby -e 'require "yaml"; YAML.load_file("workflow/schema/QUESTION_RECORD_SCHEMA.yaml"); puts "YAML readable: workflow/schema/QUESTION_RECORD_SCHEMA.yaml"'
```

If Ruby is unavailable, record:

```text
MANUAL_CHECK: YAML readability not automatically verified because no standard YAML parser was available in the active runtime.
```

Do not claim YAML schema validation has passed unless a real parser or future validator successfully reads the file.

## Whitespace And Patch Safety

```sh
git diff --check
```

## Current Manual Checks

- `MANUAL_CHECK`: confirm AGENTS.md rules are operational, not just broad principles.
- `MANUAL_CHECK`: confirm no real exam data under `datasets/` changed during harness tasks unless explicitly authorized.
- `MANUAL_CHECK`: confirm any future structured output keeps source trace for each exam, section, and question.
- `MANUAL_CHECK`: confirm answer/explanation consistency when no automated validator exists.
- `MANUAL_CHECK`: confirm image and table questions are traceable to assets or source spans before acceptance.
