# EXAM_BANKFLOW Workflow Overview

## Project Goal

The goal of `EXAM_BANKFLOW` is to organize raw exam materials into auditable, reusable, and ingestible data assets. The workflow must preserve provenance, make operator decisions reviewable, and support later structured storage without losing the original source context.

## Current Stage

Current stage: `Phase 0 Harness & Context Engineering`.

This phase establishes the lightweight operating layer for future work:

- context files that define boundaries and phase intent
- task/state files that act as the single source of truth
- run-state and handoff templates for durable execution records
- agent routing notes and closeout discipline

## Next Stage

Next stage: `Phase 1 Exam Cleaning Pipeline`.

Phase 1 will use the Phase 0 harness to process raw exam files through identification, normalization, extraction, structuring, review, and acceptance steps.

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
