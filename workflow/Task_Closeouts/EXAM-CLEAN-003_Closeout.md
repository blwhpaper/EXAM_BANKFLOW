# EXAM-CLEAN-003 Closeout

## Task Metadata

- task id: EXAM-CLEAN-003
- task title: 题型边界识别与首批 Word-first 清洗
- phase: Phase 1｜Exam Cleaning Pipeline
- branch: task-exam-clean-003-ready-word-first-batch-cleaning
- closeout date: 2026-06-25

## Files Changed

- files changed:
  - `workflow/cleaning/EXAM-CLEAN-003_BOUNDARY_MAP.md`
  - `workflow/cleaning/EXAM-CLEAN-003_FIRST_BATCH_PLAN.md`
  - `workflow/records/EXAM-CLEAN-003_SAMPLE_RECORDS.jsonl`
  - `workflow/runs/EXAM-CLEAN-003_RUN_STATE.yaml`
  - `workflow/Task_Closeouts/EXAM-CLEAN-003_Closeout.md`
  - `workflow/TASK_INDEX.md`
  - `workflow/TASK_STATE.json`

## Summary

- summary: Selected E001, E002, and E010 as the first Word-first batch. Produced boundary mapping for all three and emitted six sample question records from the safest text-only reading ranges: E001 Reading A questions 1-3 and E002 Reading A questions 1-3.

## Acceptance Scope

- intended outputs:
  - first-batch selection rationale
  - question-type and section boundary map
  - small JSONL question-record sample
  - source trace fields on every JSONL record
  - run-state and task closeout
  - task index/state update to EXAM-CLEAN-004
- out of scope kept out:
  - no full-library cleaning
  - no PDF OCR or image recognition
  - no dataset file mutation
  - no records for NEEDS_MANUAL_REVIEW, EXCLUDED, or UNKNOWN bundles
  - no E010 question records because table/media and numbering-gap boundaries need manual confirmation

## Sample Record Results

- sample records: 6
- records by exam:
  - E001: 3
  - E002: 3
- source trace status:
  - confirmed: 6
  - partial: 0
  - ambiguous: 0
  - missing: 0
  - unsupported_format: 0
- sample-record manual review count: 0
- boundary-level manual review trigger count: 7
- manual review reason summary:
  - embedded media dependency in E001/E002/E010 if future items rely on images
  - E001 reading display numbering starts at 1 inside the section and needs an explicit canonical numbering policy later
  - E002 option labels are glued in places and require recorded normalization
  - E010 has table dependency, media dependency, and a question-numbering gap around question 28

## Verification Commands

- commands run:
  - `git status --short --branch`
  - `python3 -m json.tool workflow/TASK_STATE.json`
  - `test -f workflow/cleaning/EXAM-CLEAN-003_BOUNDARY_MAP.md`
  - `test -f workflow/cleaning/EXAM-CLEAN-003_FIRST_BATCH_PLAN.md`
  - `test -f workflow/records/EXAM-CLEAN-003_SAMPLE_RECORDS.jsonl`
  - `test -f workflow/runs/EXAM-CLEAN-003_RUN_STATE.yaml`
  - `test -f workflow/Task_Closeouts/EXAM-CLEAN-003_Closeout.md`
  - `python3 - <<'PY' ... source trace JSONL check ... PY`
  - `grep -n "EXAM-CLEAN-003\|EXAM-CLEAN-004" workflow/TASK_INDEX.md workflow/TASK_STATE.json`
  - `git diff --check`

## Verification Result

- PASS/WARN/FAIL: PASS
- evidence summary:
  - `TASK_STATE.json` is valid JSON.
  - All required EXAM-CLEAN-003 output files exist.
  - JSONL source-trace check passed with `jsonl records ok 6`.
  - Task index/state references for EXAM-CLEAN-003 and EXAM-CLEAN-004 are present.
  - `git diff --check` passed.

## Not Done

- deferred work:
  - full reading extraction for EXAM-CLEAN-004
  - 七选五 extraction for EXAM-CLEAN-005
  - cloze extraction for EXAM-CLEAN-006
  - grammar fill extraction for EXAM-CLEAN-007
  - writing extraction for EXAM-CLEAN-008
- known gaps:
  - E010 needs manual review before record output because table/media and numbering boundaries are not clean enough for this first sample.
  - Passage-level representation should be formalized in EXAM-CLEAN-004 because reading subquestions rely on shared passage context.

## Next Task

- next task: EXAM-CLEAN-004
- recommendation: Use the E001/E002 sample records as the first reusable Word-first extraction口径, then expand reading extraction with explicit passage context handling and strict manual-review triggers.
