# EXAM-CLEAN-001 First Cleaning Scope

## task_id

EXAM-CLEAN-001

## phase

Phase 1｜Exam Cleaning Pipeline

## purpose

Define the first-batch exam cleaning scope before any dataset-facing cleaning work starts. This task establishes the input range, output range, execution boundaries, abnormal-case handling, validation requirements, and handoff criteria for the next task.

This task is a scope-definition task only. It does not clean real exam questions, generate question records, modify schema files, or implement extraction/OCR/table-processing automation.

## input_scope

- dataset root: `datasets/2026_quyixian_english`
- source family in scope for the first cleaning batch: raw exam materials under the current dataset, to be inspected by the next task without mutating originals
- source types in scope for later first-batch cleaning decisions: Word exam paper text and directly paired answer/supporting material when present in the same dataset bundle
- workflow inputs used by this task:
  - `workflow/TASK_STATE.json`
  - `workflow/TASK_INDEX.md`
  - `workflow/context/WORKFLOW_OVERVIEW.md`
  - `workflow/context/OPERATING_RULES.md`
  - `workflow/context/PHASE_1_EXAM_CLEANING.md`
  - `workflow/agents/AGENTS.md`
  - `workflow/schema/EXAM_DATA_SCHEMA.md`
  - `workflow/schema/QUESTION_RECORD_SCHEMA.yaml`
  - `workflow/schema/OUTPUT_FORMAT_SPEC.md`
  - `workflow/schema/VALIDATION_RULES.md`
  - `workflow/validation/MINIMUM_VALIDATION_COMMANDS.md`

## excluded_scope

- no real exam question cleaning in EXAM-CLEAN-001
- no question record generation
- no canonical markdown/YAML/JSON exam exports
- no schema changes under `workflow/schema/`
- no raw dataset mutation, overwrite, rename, or deletion
- no OCR, image recognition, table extraction, or extraction pipeline implementation
- no work beyond the handoff boundary to EXAM-CLEAN-002

## output_scope

EXAM-CLEAN-001 produces workflow-only scope and state artifacts:

- `workflow/cleaning/EXAM-CLEAN-001_FIRST_SCOPE.md`
- `workflow/runs/EXAM-CLEAN-001_RUN_STATE.yaml`
- `workflow/Task_Closeouts/EXAM-CLEAN-001_Closeout.md`
- status-only updates to:
  - `workflow/TASK_INDEX.md`
  - `workflow/TASK_STATE.json`

No dataset-side output is produced by this task.

## cleaning_boundaries

- The first cleaning batch must preserve every raw/original source file.
- The next task may define text-cleaning rules, but must not fabricate stems, options, answers, explanations, scores, dates, or provenance.
- Any future normalized text must remain traceable to its source file and, where available, page/paragraph/line/excerpt locators.
- Source order should be preserved unless a later task records a reviewable reason for reordering.
- Cleaning decisions must be recorded as normalization notes or run-state decisions when they affect review, traceability, or later structured output.
- EXAM-CLEAN-001 itself stops at scope definition and does not inspect, parse, clean, or transform individual exam questions.

## source_trace_requirements

Future first-batch cleaning work must retain traceability at minimum through:

- source dataset path
- raw source file path or ordered source file list
- ingest/extraction method used by the task that actually performs cleaning
- run id when a run artifact exists
- section/question source span when available
- uncertainty or confidence notes for damaged, ambiguous, image-based, table-based, or conflicting source material

If trace cannot be established for a source item, dataset-facing output must stop for that item and the issue must be escalated for human review.

## abnormal_case_handling

- OCR or extraction uncertainty: do not repair silently; preserve the best source-faithful text and mark uncertainty in the future run artifact or output notes.
- missing question number: do not invent a canonical number; use only a traceable temporary marker if a later task explicitly allows it.
- duplicate question number: keep the duplicates distinguishable and escalate before final structured export.
- image-based question: record the source dependency and require human review unless the source text is fully available.
- table-based question: preserve table structure where practical; if flattened later, record the transformation.
- answer/source conflict: preserve the conflicting source facts and mark the answer as uncertain; do not choose a winner.
- missing explanation: keep `explanation: null` only in future structured outputs and record the missing-source status.
- unclear or untrusted source: stop dataset-facing edits until traceability is resolved.

## validation_requirements

EXAM-CLEAN-001 validation is limited to workflow artifact checks because no exam content is cleaned.

Required commands:

- `git status --short --branch`
- `python3 -m json.tool workflow/TASK_STATE.json`
- `test -f workflow/cleaning/EXAM-CLEAN-001_FIRST_SCOPE.md`
- `test -f workflow/runs/EXAM-CLEAN-001_RUN_STATE.yaml`
- `test -f workflow/Task_Closeouts/EXAM-CLEAN-001_Closeout.md`
- `grep -n "EXAM-CLEAN-001" workflow/TASK_INDEX.md workflow/TASK_STATE.json workflow/cleaning/EXAM-CLEAN-001_FIRST_SCOPE.md workflow/runs/EXAM-CLEAN-001_RUN_STATE.yaml workflow/Task_Closeouts/EXAM-CLEAN-001_Closeout.md`
- `grep -n "EXAM-CLEAN-002" workflow/TASK_INDEX.md workflow/TASK_STATE.json workflow/cleaning/EXAM-CLEAN-001_FIRST_SCOPE.md workflow/Task_Closeouts/EXAM-CLEAN-001_Closeout.md`

Manual acceptance checks:

- confirm no files under `datasets/` were changed
- confirm no question records or structured exam exports were generated
- confirm no schema files were modified

## handoff_to_next_task

- next_task: EXAM-CLEAN-002
- handoff summary: EXAM-CLEAN-002 should begin from this scope definition and define the text cleaning rule surface for the first batch.
- EXAM-CLEAN-002 must continue to preserve raw files, source trace, non-fabrication rules, and explicit uncertainty handling.
- EXAM-CLEAN-002 must not assume EXAM-CLEAN-001 cleaned or extracted any real exam content.
