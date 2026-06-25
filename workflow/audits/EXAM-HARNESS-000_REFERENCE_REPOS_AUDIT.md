# EXAM-HARNESS-000 Reference Repos Audit

## Executive Summary

This audit reviewed five read-only reference repositories under `_reference_repos/` to identify harness engineering, context engineering, skill packaging, and workflow management patterns that can be adapted for `EXAM_BANKFLOW`.

The strongest transferable direction for `EXAM_BANKFLOW` is not to recreate a full agent platform. Instead, it should adopt a lightweight file-backed harness layer around the existing exam-ingestion workflow: task briefs, scoped context files, durable run state, review checklists, and append-only audit artifacts. The most borrowable patterns come from:

- `context-engineering-intro`: small-context planning pipeline based on `INITIAL.md` plus execution-ready plans.
- `agent-skills-for-context-engineering`: filesystem-backed context, progressive disclosure, append-only operational artifacts, and explicit run ledgers.
- `awesome-agent-harness`: taxonomy, curation rules, and verification-report discipline for keeping a workflow catalog auditable.
- `OpenHarness`: skill discovery, permission-aware prompt assembly, and task metadata concepts, but only at the conceptual level.
- `learn-harness-engineering`: explicit five-subsystem harness model, short root instruction files, feature-state tracking, initialization lifecycle, and session handoff templates.

For `EXAM_BANKFLOW`, the right architecture is a repository-local operating layer for long-running cleaning work, not a generalized multi-agent runtime. The recommended next step is to formalize repo-local harness files in `workflow/` while keeping dataset content, scripts, and runtime configuration unchanged.

## Audited Repositories

### 1. `awesome-agent-harness`

- Nature: curated catalog repo, not an execution harness.
- Strengths:
  - Strong single-source-of-truth discipline via `data/projects.yaml`.
  - Clear docs taxonomy and mirrored README generation.
  - Dated verification reports under `reports/verification/`.
  - Explicit inclusion criteria in `docs/curation_policy.md`.
- Most relevant observed files:
  - `_reference_repos/awesome-agent-harness/README.md`
  - `_reference_repos/awesome-agent-harness/docs/curation_policy.md`
  - `_reference_repos/awesome-agent-harness/reports/verification/2026-06-21.md`

### 2. `OpenHarness`

- Nature: full agent runtime and personal agent platform.
- Strengths:
  - Separation of prompts, tools, tasks, permissions, memory, skills, plugins, and UI.
  - Runtime system prompt assembly that injects only relevant sections.
  - Project/user/plugin skill discovery model.
  - Background task metadata with status/progress/note fields.
- Most relevant observed files:
  - `_reference_repos/OpenHarness/README.md`
  - `_reference_repos/OpenHarness/src/openharness/prompts/context.py`
  - `_reference_repos/OpenHarness/src/openharness/skills/loader.py`
  - `_reference_repos/OpenHarness/src/openharness/tasks/types.py`
  - `_reference_repos/OpenHarness/src/openharness/tools/task_update_tool.py`
  - `_reference_repos/OpenHarness/src/openharness/skills/bundled/content/plan.md`

### 3. `context-engineering-intro`

- Nature: context-engineering template and AI coding workflow starter.
- Strengths:
  - Very direct file-based workflow: `CLAUDE.md` -> `INITIAL.md` -> `PRPs/` -> execute.
  - Command split between planning and execution.
  - Reusable PRP template with validation loops.
  - Lightweight agent specialization via separate command/agent markdown files.
- Most relevant observed files:
  - `_reference_repos/context-engineering-intro/README.md`
  - `_reference_repos/context-engineering-intro/CLAUDE.md`
  - `_reference_repos/context-engineering-intro/PRPs/templates/prp_base.md`
  - `_reference_repos/context-engineering-intro/use-cases/ai-coding-workflows-foundation/README.md`
  - `_reference_repos/context-engineering-intro/use-cases/ai-coding-workflows-foundation/commands/create-plan.md`
  - `_reference_repos/context-engineering-intro/use-cases/ai-coding-workflows-foundation/agents/validator.md`

### 4. `agent-skills-for-context-engineering`

- Nature: skill library plus examples and a file-based researcher operating system.
- Strengths:
  - Progressive disclosure through modular `SKILL.md` design.
  - Strong filesystem-context patterns for scratchpads, plans, and offloaded outputs.
  - Durable run directories with `THREAD.md`, reports, proposals, sources, and closure records.
  - Example systems that explain why each file exists.
- Most relevant observed files:
  - `_reference_repos/agent-skills-for-context-engineering/README.md`
  - `_reference_repos/agent-skills-for-context-engineering/skills/filesystem-context/SKILL.md`
  - `_reference_repos/agent-skills-for-context-engineering/examples/digital-brain-skill/HOW-SKILLS-BUILT-THIS.md`
  - `_reference_repos/agent-skills-for-context-engineering/researcher/runs/20260515-035228-executable-autonomous-research-frameworks/THREAD.md`

### 5. `learn-harness-engineering`

- Nature: project-based harness engineering course plus scaffoldable harness templates and examples.
- Strengths:
  - Clear five-subsystem harness model: instructions, state, verification, scope, lifecycle.
  - Strong emphasis on short entrypoint instruction files instead of monolithic context.
  - Ready-to-copy templates for `AGENTS.md`, `feature_list.json`, `progress.md`, `init.sh`, and `session-handoff.md`.
  - Concrete project examples showing agent-readable workspaces and one-feature-at-a-time execution discipline.
- Most relevant observed files:
  - `_reference_repos/learn-harness-engineering/README.md`
  - `_reference_repos/learn-harness-engineering/CLAUDE.md`
  - `_reference_repos/learn-harness-engineering/skills/harness-creator/SKILL.md`
  - `_reference_repos/learn-harness-engineering/skills/harness-creator/templates/agents.md`
  - `_reference_repos/learn-harness-engineering/skills/harness-creator/templates/init.sh`
  - `_reference_repos/learn-harness-engineering/skills/harness-creator/templates/progress.md`
  - `_reference_repos/learn-harness-engineering/skills/harness-creator/templates/session-handoff.md`
  - `_reference_repos/learn-harness-engineering/projects/project-03/solution/AGENTS.md`
  - `_reference_repos/learn-harness-engineering/projects/project-03/solution/feature_list.json`
  - `_reference_repos/learn-harness-engineering/projects/project-03/solution/session-handoff.md`

## Borrowable Patterns

### 1. File-backed context instead of prompt-bloat

- Source: `agent-skills-for-context-engineering`, `OpenHarness`
- Why it fits:
  - `EXAM_BANKFLOW` is a long-horizon workflow with many intermediate judgments.
  - Exam cleaning needs persistent notes, mismatch findings, and review evidence more than chat-history accumulation.
- Proposed adaptation:
  - Keep live context thin.
  - Store run notes, parsing anomalies, alignment issues, and reviewer decisions as files under `workflow/`.

### 2. Progressive disclosure for workflow instructions

- Source: `agent-skills-for-context-engineering`
- Why it fits:
  - Not every task needs all repo instructions.
  - Different phases need different context: intake, cleaning, question-splitting, answer alignment, export, QA.
- Proposed adaptation:
  - Create a top-level workflow brief plus phase-specific instructions that are loaded only when relevant.

### 3. `INITIAL`/plan/execution split

- Source: `context-engineering-intro`
- Why it fits:
  - This repo will have recurring operational tasks, not one-off ad hoc work.
  - Planning artifacts reduce drift across long cleaning batches.
- Proposed adaptation:
  - Use one intake brief per work item and one execution plan per batch or sub-batch.

### 4. Reviewable templates with validation gates

- Source: `context-engineering-intro` PRP template, validator agent pattern
- Why it fits:
  - Cleaning pipelines fail quietly when validation is informal.
  - This workflow needs explicit “what to verify before marking done”.
- Proposed adaptation:
  - Add checklist templates for schema conformity, answer alignment, question-count sanity, and export integrity.

### 5. Single-source-of-truth registries

- Source: `awesome-agent-harness`
- Why it fits:
  - `EXAM_BANKFLOW` will accumulate workflow components and task types over time.
  - Registries make the workflow auditable and easier to extend.
- Proposed adaptation:
  - Use one index file for workflow tasks and one index for standard operating patterns/templates instead of scattering ad hoc notes.

### 6. Dated verification or review reports

- Source: `awesome-agent-harness`, `agent-skills-for-context-engineering`
- Why it fits:
  - Cleaning quality needs evidence trails.
  - Review artifacts are useful even without scripts.
- Proposed adaptation:
  - Save dated audit/review reports under `workflow/reviews/` or task-scoped run directories.

### 7. Locked vs editable surfaces

- Source: `agent-skills-for-context-engineering` researcher `THREAD.md`
- Why it fits:
  - This repo has stable policy files and volatile run artifacts.
  - Explicit boundaries reduce accidental edits to core standards.
- Proposed adaptation:
  - Mark policy/spec files as stable references; keep working notes and run results in separate task/run folders.

### 8. Lightweight task state metadata

- Source: `OpenHarness`
- Why it fits:
  - Work items can remain active across multiple sessions.
  - Minimal fields like status, progress, note, and last reviewer are enough.
- Proposed adaptation:
  - Use Markdown or YAML status files instead of building a runtime task manager.

### 9. Five-subsystem harness decomposition

- Source: `learn-harness-engineering`
- Why it fits:
  - It translates abstract harness engineering into a small operational checklist.
  - `EXAM_BANKFLOW` can adopt the structure without adopting platform complexity.
- Proposed adaptation:
  - Organize future workflow docs around instructions, state, verification, scope, and lifecycle.

### 10. One-feature-at-a-time or one-batch-at-a-time discipline

- Source: `learn-harness-engineering`
- Why it fits:
  - Exam workflows are vulnerable to mixed-scope edits and silent partial completion.
  - A narrow active unit reduces ambiguity and simplifies review.
- Proposed adaptation:
  - Work one source batch or one workflow improvement unit at a time, with explicit done criteria.

### 11. Initialization as its own phase

- Source: `learn-harness-engineering`
- Why it fits:
  - Long-running operational repos drift unless startup checks are standardized.
  - Even without scripts, the repo needs a repeatable “before work starts” sequence.
- Proposed adaptation:
  - Document a startup checklist that confirms source scope, active task, prior state, and review expectations before edits begin.

### 12. Feature list as harness primitive

- Source: `learn-harness-engineering`
- Why it fits:
  - The `feature_list.json` concept maps well to workflow capability tracking or task acceptance criteria.
  - It forces explicit pass/fail evidence rather than vague progress language.
- Proposed adaptation:
  - Use a structured workflow-state registry or checklist for future harness tasks and batch-level readiness.

## Non-borrowable Patterns

### 1. Full platform/runtime architecture

- Source: `OpenHarness`
- Reason not to borrow:
  - Too large relative to current repo needs.
  - Would introduce platform-building work instead of improving exam workflow governance.

### 2. General-purpose multi-agent/swarm orchestration

- Source: `OpenHarness`, some `context-engineering-intro` examples
- Reason not to borrow:
  - `EXAM_BANKFLOW` needs determinism and traceability more than parallel autonomous delegation.
  - Multi-agent coordination adds failure modes without immediate payoff.

### 3. Marketplace/plugin packaging as an early priority

- Source: `agent-skills-for-context-engineering`, `OpenHarness`
- Reason not to borrow:
  - Repo-local harness files are enough for now.
  - Packaging skills as plugins before workflow standards exist would be premature.

### 4. Heavy benchmark/eval lab infrastructure

- Source: `agent-skills-for-context-engineering/researcher/benchmarks`
- Reason not to borrow:
  - Valuable conceptually, but too expensive for the current maturity level.
  - Start with human-readable review checklists and spot-check reports first.

### 5. Generated README/catalog publication workflow

- Source: `awesome-agent-harness`
- Reason not to borrow:
  - Useful for knowledge-base curation, but `EXAM_BANKFLOW` is not a public catalog repo.
  - The spirit of verification is useful; the publication machinery is not.

### 6. Broad project-wide AI coding rules copied verbatim

- Source: `context-engineering-intro/CLAUDE.md`
- Reason not to borrow:
  - It is oriented to application coding and test/lint loops.
  - This repo currently needs operational workflow rules, not framework-specific coding conventions.

### 7. Generic scaffold scripts used as-is

- Source: `learn-harness-engineering`
- Reason not to borrow:
  - The templates assume software-build verification flows such as `npm`, `pytest`, or `cargo`.
  - `EXAM_BANKFLOW` should borrow the lifecycle pattern, but not the default implementation commands unchanged.

## Recommended EXAM_BANKFLOW Architecture

The recommended architecture is a repo-local workflow harness built around task packages, phase-specific context, and durable review artifacts.

### Proposed layers

1. Policy layer
- Stable definitions of what counts as valid intake, cleaned output, split questions, aligned answers, and export readiness.

2. Task layer
- One task brief per harness task containing objective, scope, constraints, inputs, outputs, and review criteria.

3. Context layer
- Phase-specific files for intake, normalization, segmentation, alignment, export, and QA.
- Only the relevant phase file should be loaded during work.

4. Run-state layer
- Per-run or per-batch folders storing status, notes, anomalies, decisions, and review conclusions.

5. Review layer
- Human-readable checklists and dated reports that make quality decisions explicit.

6. Lifecycle layer
- Explicit startup, handoff, and clean-state expectations so each session is restartable without relying on chat history.

### Directory shape to aim for later

```text
workflow/
  TASK_INDEX.md
  tasks/
    EXAM-HARNESS-001.md
  context/
    WORKFLOW_OVERVIEW.md
    PHASE_INTAKE.md
    PHASE_NORMALIZATION.md
    PHASE_SEGMENTATION.md
    PHASE_ALIGNMENT.md
    PHASE_EXPORT.md
    PHASE_QA.md
  templates/
    TASK_BRIEF_TEMPLATE.md
    RUN_STATE_TEMPLATE.yaml
    REVIEW_CHECKLIST_TEMPLATE.md
    BATCH_REPORT_TEMPLATE.md
  runs/
    2026-xx-xx_batch-id/
      THREAD.md
      run-state.yaml
      notes.md
      anomalies.md
      review.md
  audits/
    EXAM-HARNESS-000_REFERENCE_REPOS_AUDIT.md
```

This architecture is intentionally file-first and low-automation. It preserves provenance, supports long-running work, and can later power scripts without requiring them now.

## Recommended Files to Create

These are recommendations only for follow-up work, not part of this task.

- `workflow/context/WORKFLOW_OVERVIEW.md`
  - Concise map of the entire exam-processing lifecycle, major boundaries, and invariant rules.

- `workflow/context/PHASE_INTAKE.md`
  - What to record when a new source batch enters the system.

- `workflow/context/PHASE_NORMALIZATION.md`
  - Rules for filename normalization, metadata normalization, and source hygiene.

- `workflow/context/PHASE_SEGMENTATION.md`
  - Standards for splitting papers into question units and preserving order.

- `workflow/context/PHASE_ALIGNMENT.md`
  - Rules for answer-key alignment, ambiguity handling, and exception logging.

- `workflow/context/PHASE_EXPORT.md`
  - Required output contract and export validation points.

- `workflow/context/PHASE_QA.md`
  - Spot-check procedure, reviewer sign-off, and release criteria.

- `workflow/templates/TASK_BRIEF_TEMPLATE.md`
  - Template for future harness tasks with objective, constraints, source scope, and deliverables.

- `workflow/templates/RUN_STATE_TEMPLATE.yaml`
  - Minimal task/run metadata: status, owner, source batch, current phase, blockers, next action.

- `workflow/templates/REVIEW_CHECKLIST_TEMPLATE.md`
  - Repeatable manual verification structure.

- `workflow/templates/BATCH_REPORT_TEMPLATE.md`
  - Dated report format for batch-level auditability.

- `workflow/runs/<run-id>/THREAD.md`
  - Durable run narrative inspired by the researcher OS pattern, but simplified for exam batches.

- `workflow/templates/SESSION_HANDOFF_TEMPLATE.md`
  - Compact handoff file recording completed work, verification evidence, blockers, and next step.

- `workflow/templates/WORK_START_CHECKLIST.md`
  - Initialization checklist inspired by `init.sh` and startup rules, but documentation-first rather than command-first.

## Risks and Constraints

- The repository is not yet ready for a full automation harness; over-design would slow real workflow progress.
- Dataset handling is sensitive; run artifacts must reference datasets without altering or duplicating them.
- Review burden can grow quickly if every run artifact is too verbose; templates should stay compact.
- A file-first system only works if naming, locations, and update discipline are consistent.
- Borrowed patterns must remain domain-specific; generic AI-agent terminology can obscure concrete exam-workflow needs.
- Some `learn-harness-engineering` examples are app-build-centric; their structure is portable, but their exact commands and artifact names are not.
- The current task explicitly excludes dataset edits, scripts, configs, and broad repo docs, so this audit stops at architecture recommendations.

## Next Task Proposal

### Recommended next task: `EXAM-HARNESS-001`

Yes, the repo is ready to move into `EXAM-HARNESS-001`, but the scope should stay narrow.

### Proposed goal

Create the first repo-local harness skeleton for `EXAM_BANKFLOW` without touching datasets or building cleaning logic.

### Suggested scope

- Create `workflow/context/` phase files.
- Create `workflow/templates/` templates for task brief, run state, and review checklist.
- Add one example run skeleton under `workflow/runs/`.
- Keep all artifacts documentation-only.

### Suggested non-goals

- No cleaning scripts.
- No dataset mutation.
- No README/AGENTS/config changes unless separately approved.
- No plugin or runtime framework setup.

### Exit criteria

- A future operator can start a batch using only repo-local workflow files.
- Each major phase has explicit instructions and review expectations.
- Run-state and review artifacts have a consistent home and format.
