# EXAM-HARNESS-004 Closeout

## Task Metadata

- task id: EXAM-HARNESS-004
- task title: 建立 Codex/Claude/GPT 开工规则与验收规则
- phase: Phase 0｜Harness & Context Engineering
- branch: task-exam-harness-004-agent-rules-validation
- closeout date: 2026-06-25

## Files Changed

- workflow/agents/AGENTS.md
- workflow/validation/README.md
- workflow/validation/MINIMUM_VALIDATION_COMMANDS.md
- workflow/TASK_INDEX.md
- workflow/TASK_STATE.json
- workflow/Task_Closeouts/EXAM-HARNESS-004_Closeout.md

## Summary

- Expanded agent rules from routing notes into operational execution guidance for Codex, Cursor, Claude, GPT-style planning agents, and human reviewers.
- Added explicit forbidden actions, startup flow, standard execution flow, source-trace requirements, validation expectations, and exception handling for OCR uncertainty, missing numbers, images, tables, answer conflicts, and unclear sources.
- Added the validation directory specification and minimum non-interactive validation command list for current harness work and early cleaning tasks.
- Updated task registry state to close Phase 0 harness work and point execution to `EXAM-CLEAN-001`.

## Acceptance Scope

- intended outputs: operational agent rules, validation directory README, minimum validation command surface, updated workflow registry, task closeout
- out of scope kept out: real exam cleaning, dataset edits, complex validators, large scripts, external dependencies, push or merge operations

## Verification Commands

- commands run:
  - git status --short --branch
  - find workflow -maxdepth 3 -type f | sort
  - python3 -m json.tool workflow/TASK_STATE.json
  - grep -n "Forbidden Actions" workflow/agents/AGENTS.md
  - grep -n "Required Startup Flow" workflow/agents/AGENTS.md
  - grep -n "Exception Handling" workflow/agents/AGENTS.md
  - grep -n "Validation Expectations" workflow/agents/AGENTS.md
  - grep -n "schema checks" workflow/validation/README.md
  - grep -n "required fields" workflow/validation/README.md
  - grep -n "source trace" workflow/validation/README.md
  - grep -n "duplicate.*question_id" workflow/validation/README.md
  - grep -n "answer/explanation consistency" workflow/validation/README.md
  - grep -n "output format" workflow/validation/README.md
  - ruby -e 'require "yaml"; YAML.load_file("workflow/schema/QUESTION_RECORD_SCHEMA.yaml"); puts "YAML readable: workflow/schema/QUESTION_RECORD_SCHEMA.yaml"'
  - git diff --check

## Verification Result

- PASS/WARN/FAIL: PASS
- evidence summary: TASK_STATE.json parses as valid JSON, validation files exist under `workflow/validation/`, required rule and validation phrases are present, QUESTION_RECORD_SCHEMA.yaml is readable by Ruby YAML parser, and git diff whitespace check passes.

## Not Done

- deferred work: implementation of full validation scripts; all Phase 1 exam cleaning tasks
- known gaps: schema and output validation remain command/manual-review based until a future task adds actual validators; answer/explanation consistency requires `MANUAL_CHECK` for now.

## Phase Status

- Phase 0 harness status: complete and closed by EXAM-HARNESS-004.
- Phase 1 readiness: ready to enter `EXAM-CLEAN-001` under the rules and validation surface defined here.

## Next Task

- next task: EXAM-CLEAN-001
- recommendation: begin Word exam text extraction and question-type detection without mutating raw input files, using the startup flow and minimum validation commands from this task.
