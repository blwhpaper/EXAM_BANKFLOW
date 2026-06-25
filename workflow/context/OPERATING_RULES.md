# EXAM_BANKFLOW Operating Rules

## Core Rules

1. `one active task at a time`
2. `read SOT before edits`
3. `no silent dataset mutation`
4. `every output must be traceable`
5. `task closeout required before switching tasks`
6. `raw/original files must remain recoverable`

## Rule Interpretation

### One Active Task At A Time

Work only against the task identified by `workflow/TASK_STATE.json`. Do not mix harness work with Phase 1 cleaning work inside the same execution window unless the index and state files explicitly advance.

### Read SOT Before Edits

Before making edits, read the current single-source-of-truth files for the task:

- `workflow/TASK_INDEX.md`
- `workflow/TASK_STATE.json`
- any required audit or phase context files named by the active task

### No Silent Dataset Mutation

Dataset changes must never happen implicitly. If a future task requires dataset-facing actions, the change intent, target files, and verification evidence must be recorded in task artifacts or run-state records first.

### Every Output Must Be Traceable

Every generated document, report, transform, or structured output should be attributable to:

- a task id
- a run id when applicable
- the source inputs or decisions that produced it

### Task Closeout Required Before Switching Tasks

Do not leave a task by implication. Record summary, files changed, verification, and next task in a closeout artifact before moving to a different active task.

### Raw/Original Files Must Remain Recoverable

Raw or original exam files are preservation surfaces. Future processing may derive normalized or structured outputs, but original source material must remain intact and recoverable for audit and reprocessing.
