# EXAM-CLEAN-008 Question Records Slice

## Task

- task id: EXAM-CLEAN-008
- task title: writing question structured extraction
- date: 2026-06-25

## Scope Decision

EXAM-CLEAN-008 was opened as the next Phase 1 slice after EXAM-CLEAN-006 question records and EXAM-CLEAN-007 validator hardening.

The current authoritative task index names EXAM-CLEAN-008 as `写作题结构化抽取`. It does not point to cloze extraction. This slice therefore does not process cloze or any non-writing section.

## Source Inputs Read

- `workflow/cleaning/EXAM-CLEAN-002_SOURCE_TRACE.md`
- `workflow/cleaning/EXAM-CLEAN-003_BOUNDARY_MAP.md`
- `workflow/cleaning/EXAM-CLEAN-003_FIRST_BATCH_PLAN.md`
- `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl`
- `workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl`
- `workflow/Task_Closeouts/EXAM-CLEAN-006_Closeout.md`
- `workflow/Task_Closeouts/EXAM-CLEAN-007_Closeout.md`
- `workflow/runs/EXAM-CLEAN-007_RUN_STATE.yaml`
- `datasets/2026_quyixian_english/_整理清单/_STANDARDIZED_EXAMS_INDEX_FINAL.csv`

## Candidate Writing Range

The only source-backed writing boundaries already present in workflow artifacts are from EXAM-CLEAN-003:

| exam_id | source scope | writing candidate | status |
| --- | --- | --- | --- |
| E001 | `Q_原卷.docx` paragraphs 217-240 | source question numbers 46-47 | deferred, not emitted |
| E002 | `Q_原卷.docx` paragraphs 204-227 | source question numbers 46-47 | deferred, not emitted |
| E010 | `Q_原卷.docx` paragraphs 252-260 | source question number 76 | deferred, not emitted because EXAM-CLEAN-003 marked table/media/numbering risk |

## Blocking Finding

The current on-disk repo does not contain `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/`. The tracked dataset files are the inventory CSV files under `datasets/2026_quyixian_english/_整理清单/`.

Because the primary Word sources are absent from the current working tree, this task cannot inspect the actual writing prompts in `Q_原卷.docx` and cannot confirm answer or scoring support from `QA_解析版.docx`.

## Record Output

`workflow/records/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.jsonl` intentionally contains zero question records.

No placeholder writing records were emitted because a valid question record requires a non-fabricated `stem`/`question_text`, source locator, question number, answer status, and manual-review metadata. The current repo only preserves writing section boundaries, not the writing prompt text itself.

## Manual Review Boundary

The following candidate ranges require manual source review before question-record creation:

| exam_id | candidate | manual_review_note |
| --- | --- | --- |
| E001 | writing 46-47 | NEEDS_MANUAL_REVIEW: primary source path and paragraph range are known from EXAM-CLEAN-003, but `Q_原卷.docx` is absent from the current on-disk repo, so prompt text cannot be verified. |
| E002 | writing 46-47 | NEEDS_MANUAL_REVIEW: primary source path and paragraph range are known from EXAM-CLEAN-003, but `Q_原卷.docx` is absent from the current on-disk repo, so prompt text cannot be verified. |
| E010 | writing 76 | NEEDS_MANUAL_REVIEW: EXAM-CLEAN-003 already recorded table/media/numbering risk, and the current on-disk repo does not contain the Word source needed to resolve it. |

## Non-Fabrication Checks

- no OCR was run
- no source Word content was guessed
- no writing prompt, answer, explanation, score, or page number was invented
- no reading block was converted into a writing question record
- no cloze item was processed
- no historical EXAM-CLEAN-001 through EXAM-CLEAN-007 outputs were modified

## Handoff

EXAM-CLEAN-008 remains blocked until the standardized Word sources are available in the working tree or a later task provides source-backed writing prompt text with paragraph locators.

