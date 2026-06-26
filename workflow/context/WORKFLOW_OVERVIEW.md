# EXAM_BANKFLOW Workflow Overview

## Project Goal

The goal of `EXAM_BANKFLOW` is to organize raw exam materials into auditable, reusable, and ingestible data assets. The workflow must preserve provenance, make operator decisions reviewable, and support later structured storage without losing the original source context.

## Current Stage

Current stage: `Phase 2 / EXAM-BANK`.

Phase 0 / EXAM-HARNESS is complete and remains the governance shell. Phase 1 / EXAM-CLEAN is complete for `EXAM-CLEAN-001` through `EXAM-CLEAN-015`; its outputs are the first cleaned sample records, exports, validation checks, and review package. Phase 1 did not create a complete searchable exam-bank system.

Phase 2 builds that system: a searchable, selectable, and exportable Gaokao English question bank with auditable source trace, release status, query surfaces, set builders, export packs, and a future incremental ingest path for newly added questions.

## Active Pointer

- current phase: `Phase 2 / EXAM-BANK`
- current task: `EXAM-BANK-CORE-001`
- next task: `EXAM-BANK-CORE-001`
- Phase 2 roadmap: `workflow/context/PHASE_2_EXAM_BANK.md`

## Future Stage

Phase 3 is reserved as a future operations/productization placeholder after Phase 2 is accepted. Phase 3 tasks are not expanded into the executable queue in the current workflow.

## Out Of Scope

The workflow must not:

- directly modify raw exam source files
- skip the task index or task state registry
- bypass acceptance or closeout requirements

## Reference Repo Boundary

This project borrows structure and operating patterns from the Phase 0 audit of reference repositories. It does not copy scaffold scripts, runtime loaders, or platform code from those repositories. The boundary is deliberate: adopt the architecture logic, keep implementation repo-local and lightweight.

## Operating Model

The lightweight harness follows five practical subsystems adapted from the audit:

- instructions: phase briefs, operating rules, and agent routing
- state: task index, task state, and run-state snapshots
- verification: checklists, acceptance records, and diff checks
- scope: one active task at a time with explicit boundaries
- lifecycle: work start, session handoff, and task closeout
