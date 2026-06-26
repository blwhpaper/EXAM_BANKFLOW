# EXAM-CLEAN-011 Markdown Summary Export

## Task

- task_id: EXAM-CLEAN-011
- task_title: Markdown 汇总导出
- branch: `task-exam-clean-011-markdown-summary-export`
- date: 2026-06-25

## Inputs

- `workflow/TASK_STATE.json`
- `workflow/TASK_INDEX.md`
- `workflow/schema/EXAM_DATA_SCHEMA.md`
- `workflow/schema/QUESTION_RECORD_SCHEMA.yaml`
- `workflow/schema/OUTPUT_FORMAT_SPEC.md`
- `workflow/schema/VALIDATION_RULES.md`
- `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl`
- `workflow/cleaning/EXAM-CLEAN-010_STRUCTURED_DATA_INGEST.md`
- `workflow/Task_Closeouts/EXAM-CLEAN-010_Closeout.md`
- `workflow/validation/README.md`
- `workflow/validation/MINIMUM_VALIDATION_COMMANDS.md`

## Outputs

- `workflow/exports/EXAM-CLEAN-011_QUESTION_BANK_SUMMARY.md`
- `workflow/cleaning/EXAM-CLEAN-011_MARKDOWN_SUMMARY_EXPORT.md`
- `workflow/runs/EXAM-CLEAN-011_RUN_STATE.yaml`
- `workflow/Task_Closeouts/EXAM-CLEAN-011_Closeout.md`
- `workflow/validation/validate_markdown_summary_export.py`

## Export Rules

1. Read only `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl` as the structured content source.
2. Do not change question text, options, answer values, source spans, or answer-source data.
3. Preserve record order from the JSONL input.
4. Print explicit count summaries for total records, reading records, writing records, and manual-review records.
5. Print one summary table row for every record with `question_id`, `exam_id`, `section`, `question_type`, `source_file`, `source_question_number`, `answer`, and `manual_review`.
6. For reading records, include `passage_id`, `block_id`, `passage_ref`, question text, A-D options, answer, `answer_status`, `source_trace_status`, `answer_source`, and `source_span`.
7. For writing records, include writing task text, answer or reference-answer status, `answer_status`, `source_trace_status`, `answer_source`, and `source_span`.
8. If `manual_review_status=required` exists in any future input, list those records in a dedicated manual-review section. For this export, write explicit `manual_review=0`.
9. Keep answer-alignment-visible fields in markdown by printing `validation_state`, `answer_status`, `explanation_status`, and `source_trace_status`.
10. Keep source-trace-visible fields in markdown by printing `source_file`, `source_page_or_section`, `answer_source`, `source_span`, and reading linkage fields.

## Field Mapping

| markdown field | JSONL source |
| --- | --- |
| `question_id` | `question_id` |
| `exam_id` | `exam_id` |
| `section` | `section_type` |
| `question_type` | `question_type` |
| `source_file` | `source_file` |
| `source_question_number` | `source_question_number` |
| `source_page_or_section` | `source_page_or_section` |
| `answer` | `answer` or `answer.answer_type` display label for writing records |
| `manual_review` | `manual_review_status` |
| `manual_review_note` | `manual_review_note` |
| `validation_state` | `validation_status.state` |
| `answer_status` | `validation_status.answer_status` |
| `explanation_status` | `validation_status.explanation_status` |
| `source_trace_status` | `source_trace_status` |
| `uncertainty` | `validation_status.uncertainty` |
| `passage_id` | `passage_id` |
| `block_id` | `block_id` |
| `passage_ref` | `passage_ref` |
| `question_text` / `writing_task` | `question_text` |
| `options` | `options` |
| `answer_source` | `answer_source` |
| `source_span` | `source_span` |

## Not Done

- No OCR.
- No new questions.
- No source repair.
- No answer inference.
- No Word export.
- No HTML export.
- No schema change.
- No JSONL mutation.

## Risks

- The markdown export is intentionally redundant; future edits must maintain record-count consistency with the JSONL source.
- Writing answers are long prose blocks, so copy/paste review can introduce accidental drift if humans edit the markdown manually later.
- `source_trace_status` values remain mixed (`confirmed` and `READY`) because this task preserves upstream truth instead of normalizing it.
