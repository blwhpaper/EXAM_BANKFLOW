# Phase 1 Exam Cleaning Pipeline

## Entry Condition

Phase 1 can start only after the Phase 0 harness and context infrastructure are in place. No Phase 1 task should begin while Phase 0 core files, task routing, and closeout discipline remain unfinished.

## High-Level Flow

Phase 1 covers the end-to-end path from raw exam materials to structured, reviewable data assets:

1. identify raw source files and their provenance
2. pair related materials such as paper, answer key, and supporting files
3. standardize naming so runs and outputs are consistent
4. convert Word/PDF sources into machine-usable intermediate text or document forms
5. extract content and detect exam structure
6. transform extracted material into structured records suitable for storage
7. load validated outputs into the repository's structured data layer
8. perform human review and acceptance before task closeout

## Phase Constraints

Phase 1 must preserve auditability:

- each run should identify the input set it worked on
- each transform should be reviewable
- acceptance should happen only after checks and manual review points are completed

## Dependency On Phase 0

Phase 1 depends on Phase 0 for:

- task and phase routing
- operating rules
- run-state recording
- handoff and closeout templates
- acceptance discipline
