# Agent Execution Rules

## Purpose

This document defines how Codex, Cursor, Claude, GPT-style assistants, and human reviewers should execute future `EXAM_BANKFLOW` tasks. It is written for repeatable exam cleaning, question structuring, output validation, and task handoff.

## Role Boundaries

- `Codex`: repository edits, file landing, small scripts when authorized, batch command execution, validation command runs, closeout drafting, and final working-tree evidence.
- `Cursor`: narrow local patching, manual inspection support, focused UI/editor review, and small corrections after a human or lead agent identifies the target lines.
- `Claude`: second-pass reasoning, risk review, schema/format critique, ambiguity review, and non-execution review notes for complex extraction decisions.
- `GPT-style planning agent`: task decomposition, checklist preparation, acceptance judgment, and wording review for instructions or closeouts.
- `Human reviewer`: final authority for uncertain OCR, source interpretation, answer-key conflicts, image/table transcription, acceptance exceptions, and any dataset-facing correction.

No agent may silently transfer responsibility to another tool. The active executor remains responsible for evidence, traceability, and closeout quality.

## Required Startup Flow

Every agent session must begin by reading the current single-source-of-truth files:

1. `workflow/TASK_STATE.json`
2. `workflow/TASK_INDEX.md`
3. active task card or task instructions, when present
4. relevant schema and output rules:
   - `workflow/schema/EXAM_DATA_SCHEMA.md`
   - `workflow/schema/QUESTION_RECORD_SCHEMA.yaml`
   - `workflow/schema/OUTPUT_FORMAT_SPEC.md`
   - `workflow/schema/VALIDATION_RULES.md`
5. relevant operating context:
   - `workflow/context/OPERATING_RULES.md`
   - this file

Before editing, confirm:

- active task id
- active phase
- input files or dataset range explicitly in scope
- output paths to create or modify
- validation commands expected for the task
- closeout path for the task

If the task scope does not explicitly authorize dataset changes, do not modify `datasets/`.

## Standard Execution Flow

For future exam cleaning or structuring tasks, use this order:

1. Read the task card or task instructions.
2. Confirm input range:
   - source dataset folder
   - raw input files
   - question number range or section range
   - expected output formats
3. Inspect source material without overwriting raw files.
4. Generate structured output using the schema and output format rules.
5. Preserve source trace for every exam, section, and question record.
6. Mark uncertainty and missing data explicitly.
7. Run the minimum validation commands defined for the task.
8. Record results in review artifacts or closeout.
9. Write task closeout before changing `workflow/TASK_STATE.json` to the next task.

## Forbidden Actions

Agents must not:

- change question meaning to make text smoother
- fabricate or complete missing stems, options, answers, explanations, scores, dates, source metadata, or provenance
- invent answer keys from general knowledge or model confidence
- mix content from different source files unless the task explicitly defines a multi-source bundle
- merge questions from different exams into one record without traceable source mapping
- overwrite, delete, or rename original/raw input files
- hide uncertainty by silently normalizing damaged OCR
- drop source excerpts or source spans for convenience
- mark a validation check as automated when it was only reviewed manually
- push, merge, or switch tasks unless explicitly instructed

## Source Trace Rules

Every generated output must support trace-back to the raw source.

Minimum trace for exam records:

- `source_file` or ordered `source_file[]`
- `provenance.raw_source_paths`
- `provenance.ingest_method`
- `provenance.run_id` when a run exists
- confidence or uncertainty notes when source quality is imperfect

Minimum trace for question records:

- `question_id`
- `exam_id`
- `section_id`
- `question_number`
- `source_span.source_ref`
- `source_span.locator_type`
- page, paragraph, line, character, or excerpt locator when available
- `normalization_notes` for any cleanup decision

## Exception Handling

Use explicit notes and status fields instead of guessing.

| Situation | Required Handling |
|---|---|
| OCR text is uncertain | Preserve best readable text, add `validation_status.uncertainty`, and note the damaged fragment in `normalization_notes`. |
| Question number is missing | Do not invent a canonical number. Use a temporary traceable placeholder only if the schema/output task allows it, mark `validation_status.state: warn`, and request human review. |
| Question number is duplicated | Keep both records traceable, do not collapse them, mark duplicate-id or numbering issue, and escalate for review before final export. |
| Image-based question | Add an `assets` entry with source reference, keep stem text that is visible, and mark any untranscribed image dependency as uncertainty. |
| Table-based question | Preserve table structure when practical; if flattened, record the transformation in `normalization_notes` and include source span. |
| Answer key conflicts with question/options | Do not choose a winner. Preserve source answer, mark answer status `uncertain`, add issue code such as `ANSWER_CONFLICT`, and require human review. |
| Explanation absent | Set `explanation: null`, set `validation_status.explanation_status: missing_in_source`, and avoid invented rationale. |
| Source is unclear or untrusted | Stop dataset-facing edits if trace cannot be established; mark source status as unresolved and escalate. |
| Multiple source files disagree | Keep per-source notes, do not blend content, and require human decision before canonical output. |

## Validation Expectations

At minimum, each task closeout must record:

- `git status --short`
- JSON parse result for `workflow/TASK_STATE.json`
- relevant file existence checks
- schema/required-field checks available at that stage
- source-trace checks available at that stage
- manual checks explicitly labeled `MANUAL_CHECK` when not automated
- `git diff --check`

Future scripts may live under `workflow/validation/`, but the command surface must remain non-interactive and suitable for Codex, Cursor, Claude-assisted review, and human terminals.

## Handoff And Closeout

Before ending or switching tasks, write a closeout that states:

- task id and branch
- files changed
- commands run
- pass/warn/fail result
- known gaps and manual checks
- whether the current phase is complete
- next task recommendation

Closeout is not optional. If validation is incomplete, mark `WARN` or `FAIL` with the unresolved reason rather than presenting the task as done.
