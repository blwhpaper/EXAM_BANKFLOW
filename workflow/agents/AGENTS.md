# Agent Routing Notes

## Role Boundaries

- `Codex`: file landing, script work, repository edits, batch checks, and verification command execution
- `Cursor`: small-scope human review support and narrow patch application when manual inspection is helpful
- `Claude`: external review framing, risk identification, and second-pass critique of workflow decisions
- `GPT`: task design support, acceptance judgment, and structure review for future workflow tasks

## Shared Constraint

No agent may exceed repository boundaries to silently modify `datasets/`. Dataset-facing work must be explicitly authorized by the active task scope and must remain traceable through task or run artifacts.

## Collaboration Use

Agent assistance should improve review quality, not weaken accountability. Final repository state still needs:

- clear task ownership
- traceable file changes
- explicit verification evidence
- closeout before task switching
