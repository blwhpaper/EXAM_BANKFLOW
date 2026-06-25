# EXAM-CLEAN-007 Closeout

## Task Metadata

- task id: EXAM-CLEAN-007
- task title: question records validation hardening
- phase: Phase 1｜Exam Cleaning Pipeline
- branch: task-exam-clean-007-question-records-validation-hardening
- closeout date: 2026-06-25

## Files Changed

- added:
  - `workflow/runs/EXAM-CLEAN-007_RUN_STATE.yaml`
  - `workflow/Task_Closeouts/EXAM-CLEAN-007_Closeout.md`
- modified:
  - `workflow/validation/validate_question_records_slice.py`
  - `workflow/validation/README.md`
  - `workflow/validation/MINIMUM_VALIDATION_COMMANDS.md`
  - `workflow/TASK_INDEX.md`
  - `workflow/TASK_STATE.json`

## Summary

- summary: Hardened the question-records slice validator so future records must satisfy minimum structure, provenance, objective-option, answer, reading-block linkage, and manual-review consistency rules instead of merely carrying field-shaped data.
- data mutation: no EXAM-CLEAN-006 question-record data was changed.
- dependencies: Python standard library only.

## Hard Rules Added

- JSONL parseability: every non-empty line must parse as a JSON object.
- required fields: schema-level fields must exist and be non-empty, including `question_id`, `exam_id`, `section_id`, `question_number`, `question_type`, `stem`, `source_span`, `normalization_notes`, and `validation_status`.
- unique IDs: duplicate `question_id` values fail validation.
- source trace: `source_file`, `source_page_or_section`, `source_question_number`, and `source_trace_status` are required.
- source trace status enum: accepted values are `READY`, `NEEDS_MANUAL_REVIEW`, `EXCLUDED`, `UNKNOWN`, plus existing repository-compatible `confirmed`.
- choice questions: `single_choice`, `multiple_choice`, and `reading_subquestion` records must have complete A-D options with non-empty text.
- answer consistency: choice answers must reference existing option labels; single-choice answers must contain exactly one label.
- reading linkage: reading/comprehension records must carry `reading_block_id`, `block_id`, or `passage_id`, and that id must resolve in `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl`.
- passage context: reading records must retain either `passage_text` or `passage_ref`.
- manual review logic: `NEEDS_MANUAL_REVIEW` requires a concrete `manual_review_note`; `READY` or existing `confirmed` records fail if the manual-review note still carries obvious unresolved markers such as `TODO`, `TBD`, `UNKNOWN`, or `NEEDS_MANUAL_REVIEW`.
- unsupported structured answers: object answers are reported as WARN/TODO instead of silently treated as fully validated.

## Validation Commands

- commands run:
  - `python3 workflow/validation/validate_question_records_slice.py workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl`
  - `python3 workflow/validation/validate_reading_blocks.py workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl`
  - `python3 -m json.tool workflow/TASK_STATE.json >/dev/null`
  - `git diff --check`
  - `git status --short --branch`

## Verification Result

- PASS/WARN/FAIL: PASS
- evidence summary:
  - question-record validator returned `PASS question_records=3 manual_review=0 reading_questions=3 reading_blocks_indexed=2`.
  - reading-block validator returned `PASS reading_blocks=2 questions=6`.
  - `TASK_STATE.json` parsed successfully with `python3 -m json.tool`.
  - `git diff --check` passed.
  - `git status --short --branch` returned:

```text
## task-exam-clean-007-question-records-validation-hardening
 M workflow/TASK_INDEX.md
 M workflow/TASK_STATE.json
 M workflow/validation/MINIMUM_VALIDATION_COMMANDS.md
 M workflow/validation/README.md
 M workflow/validation/validate_question_records_slice.py
?? workflow/Task_Closeouts/EXAM-CLEAN-007_Closeout.md
?? workflow/runs/EXAM-CLEAN-007_RUN_STATE.yaml
```

## Boundaries Respected

- no bulk question-record creation
- no OCR
- no schema framework rebuild
- no EXAM-CLEAN-006 record mutation
- no simplification of reading comprehension into detached stem/answer records
- no EXAM-CLEAN-008 batch cleaning
- no Git commit

## Next Task

- next task: EXAM-CLEAN-008
- recommendation: proceed after human review of this validator hardening and closeout.
