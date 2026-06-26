# EXAM-CLEAN-014 Excel 总索引

## Task

- task_id: EXAM-CLEAN-014
- task_title: Excel 总索引
- branch: `task-exam-clean-014-review-package`
- date: 2026-06-25

## Inputs

- `workflow/TASK_STATE.json`
- `workflow/TASK_INDEX.md`
- `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl`
- `workflow/exports/EXAM-CLEAN-011_QUESTION_BANK_SUMMARY.md`
- `workflow/exports/EXAM-CLEAN-012_QUESTION_BANK_SUMMARY.docx`
- `workflow/cleaning/EXAM-CLEAN-013_MANUAL_REVIEW_QA.md`
- `workflow/validation/README.md`
- `workflow/validation/MINIMUM_VALIDATION_COMMANDS.md`

## Outputs

- `workflow/exports/EXAM-CLEAN-014_QUESTION_BANK_INDEX.xlsx`
- `workflow/cleaning/EXAM-CLEAN-014_EXCEL_INDEX.md`
- `workflow/runs/EXAM-CLEAN-014_RUN_STATE.yaml`
- `workflow/Task_Closeouts/EXAM-CLEAN-014_Closeout.md`
- `workflow/validation/validate_excel_index.py`

## Index Rules

1. Read all 8 records directly from `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl`.
2. Preserve source order and keep one Excel row per JSONL record.
3. Keep the required 10 columns: `record_id`, `question_type`, `source_file`, `source_page_or_section`, `source_question_number`, `title_or_prompt`, `answer`, `source_trace_status`, `manual_review_status`, `manual_review_note`.
4. Keep `reading=3` and `writing=5` exactly.
5. Reading rows must expose `passage_id` and `block_id` linkage inside the index surface so passage/block relationships remain human-visible.
6. Writing rows must expose a prompt summary derived from the JSONL `question_text`, not an empty placeholder.
7. `answer` must come from the JSONL: reading rows keep the confirmed label answer; writing rows keep the sample-answer prose from `answer.text`.
8. Do not rewrite the JSONL, markdown export, Word export, or manual review QA content.
9. Generate a real `.xlsx` workbook rather than a placeholder text file.
10. Force-stage the Excel export if `workflow/exports/` is ignored.

## Field Mapping

| Excel column | JSONL source |
| --- | --- |
| `record_id` | `question_id` |
| `question_type` | `question_type` |
| `source_file` | `source_file` |
| `source_page_or_section` | `source_page_or_section` with reading `passage_ref` visibility retained inline |
| `source_question_number` | `source_question_number` |
| `title_or_prompt` | reading: `passage_id` + `block_id` + `question_text`; writing: prompt summary from `question_text` |
| `answer` | reading: `answer`; writing: `answer.text` |
| `source_trace_status` | `source_trace_status` |
| `manual_review_status` | `manual_review_status` |
| `manual_review_note` | `manual_review_note` |

## Not Done

- No JSONL mutation.
- No markdown export mutation.
- No Word export mutation.
- No manual review QA mutation.
- No new questions.
- No answer edits.
- No OCR.
- No expansion beyond the cleaned first-batch records.
- No commit.

## Risks

- Writing answer cells are intentionally long because the index must stay traceable to the actual JSONL sample-answer content.
- The workbook is generated from standard OOXML parts, so later manual edits in Excel must preserve the required header names and row count for validator compatibility.
