# EXAM-CLEAN-004 Closeout

## Task Metadata

- task id: EXAM-CLEAN-004
- task title: 阅读理解结构化抽取
- phase: Phase 1｜Exam Cleaning Pipeline
- branch: task-exam-clean-004-reading-passage-blocks
- closeout date: 2026-06-25

## Files Changed

- files changed:
  - `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl`
  - `workflow/cleaning/EXAM-CLEAN-004_READING_STRUCTURE.md`
  - `workflow/cleaning/EXAM-CLEAN-004_MANUAL_REVIEW.md`
  - `workflow/runs/EXAM-CLEAN-004_RUN_STATE.yaml`
  - `workflow/Task_Closeouts/EXAM-CLEAN-004_Closeout.md`
  - `workflow/schema/READING_BLOCK_SCHEMA.yaml`
  - `workflow/TASK_INDEX.md`
  - `workflow/TASK_STATE.json`

## Summary

- summary: Converted the EXAM-CLEAN-003 detached reading subquestion samples into passage-first reading blocks. E001 Reading Passage A and E002 Reading Passage A now each have complete `passage_text` from `Q_原卷.docx` and nested child questions with confirmed answers/explanations from `QA_解析版.docx`.

## Reading Block Results

- reading blocks: 2
- questions: 6
- blocks by exam:
  - E001: 1 block, 3 questions
  - E002: 1 block, 3 questions
- passage_text completeness: complete for emitted blocks
- passage_text source:
  - E001: `Q_原卷.docx` paragraphs 75-95
  - E002: `Q_原卷.docx` paragraphs 72-80
- answer/explanation support:
  - E001: `QA_解析版.docx` paragraphs 111-119
  - E002: `QA_解析版.docx` paragraphs 90-98

## Acceptance Scope

- intended outputs:
  - passage-first JSONL records
  - reading block structure documentation
  - manual review and deferred-scope documentation
  - lightweight reading block schema
  - run-state and task closeout
  - task index/state update to EXAM-CLEAN-005
- out of scope kept out:
  - no E010 reading block extraction
  - no PDF OCR or image recognition
  - no table-dependent extraction
  - no dataset file mutation
  - no NEEDS_MANUAL_REVIEW, EXCLUDED, or UNKNOWN source cleaning

## Manual Review

- emitted reading blocks requiring manual review: 0
- deferred reading scopes requiring manual review before extraction: 1
- manual review reason summary:
  - E010 is deferred because EXAM-CLEAN-003 identified a table, media objects, and question-numbering gap risk.
  - E001/E002 future media-dependent items remain manual-review triggers, but emitted Passage A blocks are text-complete.
  - E002 glued option labels were normalized only where unambiguous and recorded in notes.

## Verification Commands

- commands run:
  - `git status --short --branch`
  - `python3 -m json.tool workflow/TASK_STATE.json`
  - `test -f workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl`
  - `test -f workflow/cleaning/EXAM-CLEAN-004_READING_STRUCTURE.md`
  - `test -f workflow/cleaning/EXAM-CLEAN-004_MANUAL_REVIEW.md`
  - `test -f workflow/runs/EXAM-CLEAN-004_RUN_STATE.yaml`
  - `test -f workflow/Task_Closeouts/EXAM-CLEAN-004_Closeout.md`
  - `python3 - <<'PY' ... reading block JSONL check ... PY`
  - `grep -n "EXAM-CLEAN-004\|EXAM-CLEAN-005" workflow/TASK_INDEX.md workflow/TASK_STATE.json`
  - `git diff --check`

## Verification Result

- PASS/WARN/FAIL: PASS
- evidence summary:
  - `TASK_STATE.json` is valid JSON.
  - All required EXAM-CLEAN-004 output files exist.
  - JSONL required-field check passed with `reading blocks ok 2 questions ok 6`.
  - Task index/state references for EXAM-CLEAN-004 and EXAM-CLEAN-005 are present.
  - `git diff --check` passed.

## Not Done

- deferred work:
  - E010 reading extraction after table/media/numbering review.
  - full reading B-D extraction for E001/E002.
  - 七选五 extraction for EXAM-CLEAN-005.
- known gaps:
  - No automated semantic validator exists yet for passage completeness beyond source-span and length checks.
  - E002 option-label normalization still requires reviewer awareness in later batch automation.

## Next Task

- next task: EXAM-CLEAN-005
- recommendation: Start 七选五 structure extraction using the same parent-child discipline where section-level context must stay attached to child blanks/options.

