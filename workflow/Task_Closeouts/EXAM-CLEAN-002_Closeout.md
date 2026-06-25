# EXAM-CLEAN-002 Closeout

## task_id

EXAM-CLEAN-002

## branch

`task-exam-clean-002-input-inventory-source-trace`

## summary

Established the first-batch input inventory, source trace rules, task run state, and workflow handoff artifacts for later exam cleaning work. This task did not clean questions, run OCR, generate question records, or modify dataset content.

## files_changed

- `workflow/cleaning/EXAM-CLEAN-002_INPUT_INVENTORY.md`
- `workflow/cleaning/EXAM-CLEAN-002_SOURCE_TRACE.md`
- `workflow/runs/EXAM-CLEAN-002_RUN_STATE.yaml`
- `workflow/Task_Closeouts/EXAM-CLEAN-002_Closeout.md`
- `workflow/TASK_INDEX.md`
- `workflow/TASK_STATE.json`

## inventory_result

- READY: 84
- NEEDS_MANUAL_REVIEW: 16
- EXCLUDED: 87
- UNKNOWN: 0

## key_handoff_points

- Batch inclusion is anchored to `datasets/2026_quyixian_english/_整理清单/_BATCH1_WORD_PROCESSING_LIST.csv`.
- Later cleaning should start only from `READY` Word files inside the standardized bundles.
- `source_file`, `source_page_or_section`, `source_question_number`, `source_trace_status`, and `manual_review_note` are mandatory trace fields for later question records.
- `Q_原卷*.docx` is the primary stem source; `QA_解析版.docx` and `A_答案*.docx` are supporting sources only.
- Unknown-source bundles, multi-`Q_` bundles, and PDF-dependent bundles must stay in manual-review paths until explicitly resolved.

## warnings

- WARN: `E024` is an unknown-source standardized bundle and must not be promoted to `READY`.
- WARN: `E035`, `E038`, and `E049` each have multiple `Q_原卷*` files and require explicit source-file selection before question slicing.
- WARN: `E006`, `E018`, `E036`, `E045`, `E047`, and `E048` contain PDF support files that may only be cited as manual-review trace evidence in later tasks.

## validation

- `git status --short --branch`: PASS
- `python3 -m json.tool workflow/TASK_STATE.json`: PASS
- `test -f workflow/cleaning/EXAM-CLEAN-002_INPUT_INVENTORY.md`: PASS
- `test -f workflow/cleaning/EXAM-CLEAN-002_SOURCE_TRACE.md`: PASS
- `test -f workflow/runs/EXAM-CLEAN-002_RUN_STATE.yaml`: PASS
- `test -f workflow/Task_Closeouts/EXAM-CLEAN-002_Closeout.md`: PASS
- `grep -n "EXAM-CLEAN-002" workflow/TASK_INDEX.md workflow/TASK_STATE.json`: PASS
- `grep -n "source_trace" workflow/cleaning/EXAM-CLEAN-002_SOURCE_TRACE.md workflow/runs/EXAM-CLEAN-002_RUN_STATE.yaml`: PASS

## next_task_recommendation

EXAM-CLEAN-003 may start, but only against the `READY` inventory subset and only if it follows the source trace rules landed in `workflow/cleaning/EXAM-CLEAN-002_SOURCE_TRACE.md`.
