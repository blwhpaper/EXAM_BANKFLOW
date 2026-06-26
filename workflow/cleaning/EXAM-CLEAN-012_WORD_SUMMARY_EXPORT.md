# EXAM-CLEAN-012 Word Summary Export

## Task

- task_id: EXAM-CLEAN-012
- task_title: Word 汇总导出
- branch: `task-exam-clean-012-word-summary-export`
- date: 2026-06-25

## Inputs

- `workflow/TASK_STATE.json`
- `workflow/TASK_INDEX.md`
- `workflow/schema/EXAM_DATA_SCHEMA.md`
- `workflow/schema/QUESTION_RECORD_SCHEMA.yaml`
- `workflow/schema/OUTPUT_FORMAT_SPEC.md`
- `workflow/schema/VALIDATION_RULES.md`
- `workflow/validation/README.md`
- `workflow/validation/MINIMUM_VALIDATION_COMMANDS.md`
- `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl`
- `workflow/exports/EXAM-CLEAN-011_QUESTION_BANK_SUMMARY.md`
- `workflow/Task_Closeouts/EXAM-CLEAN-011_Closeout.md`

## Outputs

- `workflow/exports/EXAM-CLEAN-012_QUESTION_BANK_SUMMARY.docx`
- `workflow/cleaning/EXAM-CLEAN-012_WORD_SUMMARY_EXPORT.md`
- `workflow/runs/EXAM-CLEAN-012_RUN_STATE.yaml`
- `workflow/Task_Closeouts/EXAM-CLEAN-012_Closeout.md`
- `workflow/validation/validate_word_summary_export.py`

## Export Rules

1. Read the 8-record source only from `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl`.
2. Preserve source order, `question_id`, `source_question_number`, `section_type`, and answers without rewriting.
3. Include a summary block with `EXAM-CLEAN-012`, `total_records: 8`, and `reading=3`, `writing=5`.
4. For every reading record, print source trace, passage/context, question, options A-D, and confirmed answer.
5. For every writing record, print source trace, prompt/task, and confirmed answer or answer note.
6. Preserve answer-source-backed content only; do not invent missing source details.
7. Generate a real `.docx` with `python-docx`; do not fabricate a zipped placeholder.
8. Keep the export human-readable first and validator-checkable second.
9. Ensure the Word export is explicitly staged even if `workflow/exports/` is ignored.

## Field Mapping

| Word block | JSONL source |
| --- | --- |
| record heading | `question_id`, `exam_id`, `source_question_number` |
| source trace | `source_file`, `source_page_or_section`, `source_span`, `answer_source` |
| passage/context | `source_page_or_section`, `source_span.excerpt` |
| question | `question_text` |
| options A-D | `options[]` |
| confirmed answer | `answer` or `answer.text` |
| answer note | `validation_status.answer_status` plus manual note when no prose answer exists |

## Not Done

- No JSONL mutation.
- No new questions.
- No answer editing.
- No source backfill outside recorded traces.
- No HTML export.
- No Excel export.
- No commit.

## Risks

- Reading records do not carry a full standalone passage body in the JSONL, so the Word export uses source-backed context and excerpt fields for `Passage/Context`.
- Writing sample answers are long prose blocks; later manual edits to the docx could break validator expectations if content drifts.
- `workflow/exports/` may be ignored, so staging must be checked explicitly.
