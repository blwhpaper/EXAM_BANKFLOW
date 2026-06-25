# Phase 0 Harness & Context Engineering

## Purpose

Phase 0 defines the operating layer that makes later exam-cleaning work repeatable, reviewable, and restartable. It exists to reduce drift before any high-volume content processing begins.

## Task Sequence

### EXAM-HARNESS-000

Audit read-only reference repositories, extract reusable patterns, and document what should and should not be borrowed into `EXAM_BANKFLOW`.

### EXAM-HARNESS-001

Create the lightweight harness skeleton under `workflow/` using the audit results. This task establishes context, rules, templates, run-state examples, and agent routing notes.

This task only builds the skeleton. It does not own schema refinement and does not implement any exam-cleaning pipeline logic.

### EXAM-HARNESS-002

Stabilize task templates, state templates, and handoff/closeout conventions so future sessions can continue work with minimal ambiguity.

### EXAM-HARNESS-003

Define the target data schema, output shapes, and structured conventions needed before cleaning results can be admitted into the repository as stable data assets.

### EXAM-HARNESS-004

Define operator and agent startup rules, review rules, and acceptance expectations for repeated execution across Codex, Claude, GPT, and other approved collaborators.

## Boundary For EXAM-HARNESS-001

`EXAM-HARNESS-001` is limited to harness scaffolding:

- yes: context docs, rules, templates, run-state skeletons, task registry updates
- no: schema detail expansion
- no: cleaning workflow implementation
- no: dataset mutation
