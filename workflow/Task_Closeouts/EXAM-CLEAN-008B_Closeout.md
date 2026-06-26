# EXAM-CLEAN-008B Closeout

## Task Metadata

- task id: EXAM-CLEAN-008B
- task title: manual source placement verification
- phase: Phase 1｜Exam Cleaning Pipeline
- branch: task-exam-clean-008b-manual-source-placement-verification
- closeout date: 2026-06-25

## Files Changed

- added:
  - `workflow/cleaning/EXAM-CLEAN-008B_SOURCE_PLACEMENT_VERIFICATION.md`
  - `workflow/runs/EXAM-CLEAN-008B_RUN_STATE.yaml`
  - `workflow/Task_Closeouts/EXAM-CLEAN-008B_Closeout.md`
- modified:
  - `workflow/TASK_INDEX.md`
  - `workflow/TASK_STATE.json`

## Summary

- summary: Verified the six manually restored standardized Word files required for an EXAM-CLEAN-008 retry. All six files exist at the expected inventory paths, are non-empty, open as `.docx` zip containers, and contain `word/document.xml`. The `_STANDARDIZED_EXAMS/` directory remains ignored by git, and no source files were staged or added.

## Source Placement Results

| file | result | size_bytes | docx_container |
| --- | --- | ---: | --- |
| E001 `Q_原卷.docx` | OK | 31733 | valid, has `word/document.xml` |
| E001 `QA_解析版.docx` | OK | 45890 | valid, has `word/document.xml` |
| E002 `Q_原卷.docx` | OK | 31087 | valid, has `word/document.xml` |
| E002 `QA_解析版.docx` | OK | 45821 | valid, has `word/document.xml` |
| E010 `Q_原卷.docx` | OK | 31816 | valid, has `word/document.xml` |
| E010 `QA_解析版.docx` | OK | 52894 | valid, has `word/document.xml` |

## Upstream Sync

- `git fetch origin main`: PASS
- `main`, `origin/main`, and `FETCH_HEAD` all resolved to `ec8671a4c54eb4421eb2de300a3d557e395d7294`.

## Task State Result

- EXAM-CLEAN-008: changed from `BLOCKED` to `READY_TO_RETRY`
- EXAM-CLEAN-008B: `DONE`
- EXAM-CLEAN-009: remains `TODO`
- current task: EXAM-CLEAN-008
- next task: EXAM-CLEAN-008

## Boundaries Respected

- no question extraction
- no question records generated
- no prompt text read or rewritten
- no OCR
- no Word source files added to git
- no ignored files deleted
- no EXAM-CLEAN-009 advancement

## Validation Commands

- commands run:
  - `git status --short --branch`
  - `python3 -m json.tool workflow/TASK_STATE.json >/dev/null`
  - `test -f` checks for the six target Word files
  - `find datasets/2026_quyixian_english/_STANDARDIZED_EXAMS -iname "*.docx" | sort`
  - `python3` zipfile check for size > 0 and `word/document.xml`
  - `git status --ignored --short | grep "_STANDARDIZED_EXAMS" || true`
  - `grep -n "EXAM-CLEAN-008B\|EXAM-CLEAN-008" workflow/TASK_INDEX.md workflow/TASK_STATE.json`
  - `git diff --check`

## Verification Result

- PASS/WARN/FAIL: PASS
- evidence summary:
  - `git status --short --branch` showed branch `task-exam-clean-008b-manual-source-placement-verification` with only expected workflow edits and task-state updates.
  - `python3 -m json.tool workflow/TASK_STATE.json >/dev/null` passed.
  - `test -f` checks returned `OK` for all six target Word files.
  - `find datasets/2026_quyixian_english/_STANDARDIZED_EXAMS -iname "*.docx" | sort` listed the restored standardized Word tree and included all six target files.
  - The Python zipfile check returned `OK` for all six target files with `size > 0`, `zip_ok=True`, and `document_xml=True`.
  - `git status --ignored --short | grep "_STANDARDIZED_EXAMS" || true` returned `!! datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/`, confirming the restored sources remain ignored.
  - `grep -n "EXAM-CLEAN-008B\|EXAM-CLEAN-008" workflow/TASK_INDEX.md workflow/TASK_STATE.json` confirmed EXAM-CLEAN-008 is `READY_TO_RETRY`, EXAM-CLEAN-008B is `DONE`, and current/next task remains EXAM-CLEAN-008.
  - `git diff --check` passed.

## Not Done

- deferred work:
  - EXAM-CLEAN-008 writing extraction retry
  - content-level verification of writing prompt text, paragraph boundaries, answer/support alignment, and E010 table/media/numbering risk
- known gaps:
  - This task only verifies placement and container readability; it does not validate the semantic content of the Word files.

## Next Task

- next task: EXAM-CLEAN-008
- recommendation: Retry EXAM-CLEAN-008 using the restored Word files, preserving source trace and manual-review boundaries.
