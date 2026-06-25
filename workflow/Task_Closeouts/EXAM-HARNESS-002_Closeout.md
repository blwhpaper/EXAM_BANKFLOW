# EXAM-HARNESS-002 Closeout

## Task Metadata

- task id: EXAM-HARNESS-002
- task title: 建立任务模板、状态模板与交接模板
- phase: Phase 0｜Harness & Context Engineering
- branch: task-exam-harness-002-task-state-templates
- closeout date: 2026-06-25

## Files Changed

- workflow/templates/TASK_CARD_TEMPLATE.md
- workflow/templates/RUN_STATE_TEMPLATE.yaml
- workflow/templates/REVIEW_CHECKLIST_TEMPLATE.md
- workflow/templates/SESSION_HANDOFF_TEMPLATE.md
- workflow/templates/TASK_CLOSEOUT_TEMPLATE.md
- workflow/runs/RUN_STATE.example.yaml
- workflow/TASK_INDEX.md
- workflow/TASK_STATE.json
- workflow/Task_Closeouts/EXAM-HARNESS-002_Closeout.md

## Summary

- Added executable task, run-state, and review templates for single-item, batch, and phase-slice work.
- Strengthened handoff and closeout templates so run scope, validation, and next-step data align with run-state fields.
- Updated workflow registry files to mark EXAM-HARNESS-002 complete and point to EXAM-HARNESS-003 next.

## Acceptance Scope

- intended outputs: task card template, run-state template, review checklist template, aligned handoff/closeout templates, updated example run-state, updated task registry, task closeout
- out of scope kept out: dataset edits, reference repo edits, schema design, Phase 1 execution, actual exam cleaning outputs

## Verification Commands

- commands run:
  - python3 -m json.tool workflow/TASK_STATE.json
  - git diff --check
  - git status --short

## Verification Result

- PASS/WARN/FAIL: PASS
- evidence summary: TASK_STATE.json is valid JSON, diff check passes, and working tree contains only EXAM-HARNESS-002-related files.

## Not Done

- deferred work: EXAM-HARNESS-003 schema and output format specification
- known gaps: no sample task card or run instance was generated because this task only defines templates

## Next Task

- next task: EXAM-HARNESS-003
- recommendation: define the dataset schema and output conventions using these templates as the execution envelope
