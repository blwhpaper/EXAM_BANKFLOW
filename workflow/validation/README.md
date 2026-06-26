# Workflow Validation

## Purpose

`workflow/validation/` is the home for validation notes, command interfaces, and future lightweight scripts used to check exam cleaning outputs. The directory is part of the harness. It should help agents and human reviewers verify structured outputs without mutating raw exam sources.

This directory does not implement a full repository-wide validator. Validation evidence must combine non-interactive shell commands, task-specific validators, and clearly labeled `MANUAL_CHECK` items where automation does not yet exist.

## Validation Command Interface

Future validation commands should follow this shape:

```sh
python3 workflow/validation/validate_exam_output.py --input <structured-output> --schema workflow/schema/QUESTION_RECORD_SCHEMA.yaml
```

Expected behavior:

- non-interactive
- read-only by default
- exit `0` for pass, non-zero for fail
- print concise findings to stdout or stderr
- accept explicit input paths
- avoid network access and heavyweight dependencies
- never rewrite source or output files unless a separate task explicitly authorizes fix mode

## Checks To Cover

Future validators should cover at least:

- schema checks against `workflow/schema/EXAM_DATA_SCHEMA.md` and `workflow/schema/QUESTION_RECORD_SCHEMA.yaml`
- required fields checks for exam records and question records
- source trace checks for `source_file`, `provenance`, and `source_span`
- duplicate `question_id` checks within an output batch and, when practical, against existing repository records
- answer/explanation consistency checks using `validation_status.answer_status` and `validation_status.explanation_status`
- output format checks for markdown, YAML, JSON, review checklist, and export manifest naming
- parent-child consistency checks for `exam_id`, `section_id`, and declared sections
- objective-question option and answer-label checks
- uncertainty marker checks for OCR damage, missing numbers, image/table dependencies, and source conflicts
- forbidden-content checks for fabricated placeholders such as unexplained `unknown`, invented answers, or missing source spans

## Current Executable Validators

### EXAM-CLEAN-007 Question Records Hardening

Run these commands from the repository root for every question-records slice before closeout:

```sh
python3 workflow/validation/validate_question_records_slice.py workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl
python3 workflow/validation/validate_reading_blocks.py workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl
python3 -m json.tool workflow/TASK_STATE.json >/dev/null
git diff --check
```

`validate_question_records_slice.py` checks JSONL parseability, required question/provenance fields, unique `question_id`, source trace status enums, complete A-D options for choice questions, answer-to-option consistency, reading block linkage against `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl`, and manual-review note consistency.

### EXAM-CLEAN-009 Answer Alignment

Run this additional validator when a task audits answer-field alignment across mixed question types:

```sh
python3 workflow/validation/validate_answer_alignment.py \
  workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl \
  workflow/records/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.jsonl
```

`validate_answer_alignment.py` checks that objective questions use source-backed label answers, subjective questions use source-backed answer objects, READY/confirmed records keep answer-source locators, and unresolved answer states are explicitly routed to manual review instead of silent placeholders.

### EXAM-CLEAN-010 Structured Data Ingest

Run this validator when EXAM-CLEAN-006 and EXAM-CLEAN-008 are merged into the structured question-bank slice:

```sh
python3 workflow/validation/validate_structured_question_bank.py \
  workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl
```

`validate_structured_question_bank.py` checks JSONL parseability, unique `question_id`, required structured-ingest fields, non-empty answers, reading passage/block trace retention, `options: null` for writing records, manual-review counts, and input/output record-count reconciliation against the EXAM-CLEAN-006 and EXAM-CLEAN-008 source slices.

### EXAM-CLEAN-011 Markdown Summary Export

Run this validator when the EXAM-CLEAN-010 structured question-bank JSONL is exported into the markdown review surface:

```sh
python3 workflow/validation/validate_markdown_summary_export.py \
  workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl \
  workflow/exports/EXAM-CLEAN-011_QUESTION_BANK_SUMMARY.md
```

`validate_markdown_summary_export.py` checks JSONL parseability, summary markdown existence, record-count reconciliation, per-record `question_id` presence, reading/writing distribution consistency, manual-review count consistency, and preservation of answer-alignment-visible plus source-trace-visible fields in the markdown export.

### EXAM-CLEAN-012 Word Summary Export

Run this validator when the EXAM-CLEAN-010 structured question-bank JSONL is exported into the Word review surface:

```sh
python3 workflow/validation/validate_word_summary_export.py \
  workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl \
  workflow/exports/EXAM-CLEAN-012_QUESTION_BANK_SUMMARY.docx
```

`validate_word_summary_export.py` checks JSONL parseability, fixed 8-record input scope, docx existence, non-empty real-docx readability through `python-docx`, task-id marker presence, per-record marker presence, reading/writing distribution summary, preservation of reading A-D options plus confirmed answers, preservation of writing prompts plus confirmed-answer prose, and a manual-review flag reminder for human readability checks.

### EXAM-CLEAN-013 Manual Review QA

Run this validator when the EXAM-CLEAN-010 structured question-bank JSONL is audited into the EXAM-CLEAN-013 human-review record:

```sh
python3 workflow/validation/validate_manual_review_qa.py \
  workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl \
  workflow/cleaning/EXAM-CLEAN-013_MANUAL_REVIEW_QA.md
```

`validate_manual_review_qa.py` checks JSONL parseability, fixed 8-record input scope, QA markdown existence, full 8-record `record_id` coverage, reading/writing distribution consistency, per-record `qa_status` presence, allowed `qa_status` enums (`PASS`, `WARN`, `NEEDS_REVIEW`), and per-record `question_type` plus `source_trace_status` consistency against the structured JSONL.

### EXAM-CLEAN-014 Excel Index

Run this validator when the EXAM-CLEAN-010 structured question-bank JSONL is exported into the Excel retrieval/review index:

```sh
python3 workflow/validation/validate_excel_index.py \
  workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl \
  workflow/exports/EXAM-CLEAN-014_QUESTION_BANK_INDEX.xlsx
```

`validate_excel_index.py` checks JSONL parseability, fixed 8-record input scope, real-xlsx zip structure, required 10-column header presence, full 8-record `record_id` coverage, reading/writing distribution consistency, field-level trace consistency against the JSONL, reading passage/block visibility, and writing prompt-summary plus sample-answer preservation.

### EXAM-CLEAN-015 Review Package

Run this validator when the EXAM-CLEAN-010 structured question-bank JSONL is handed off through the final EXAM-CLEAN-015 review package:

```sh
python3 workflow/validation/validate_review_package.py \
  workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl \
  workflow/cleaning/EXAM-CLEAN-015_REVIEW_PACKAGE.md
```

`validate_review_package.py` checks JSONL parseability, review-package markdown existence, presence of all 11 required review-package sections, record-count reconciliation, `reading=3` and `writing=5` consistency, explicit reference to the Markdown, Word, Excel, and manual-review QA prerequisite artifacts, and presence of core source-trace plus answer-alignment summary markers required for final handoff.

## Minimum Current Stage

For EXAM-HARNESS-004, use `workflow/validation/MINIMUM_VALIDATION_COMMANDS.md` as the current executable validation surface. Any item that cannot yet be automated must be recorded as `MANUAL_CHECK` in the task closeout or review checklist.
