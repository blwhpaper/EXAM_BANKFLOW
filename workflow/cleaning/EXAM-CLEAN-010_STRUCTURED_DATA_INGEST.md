# EXAM-CLEAN-010 Structured Data Ingest

## Task

- task id: EXAM-CLEAN-010
- task title: 结构化数据入库
- branch: `task-exam-clean-010-structured-data-ingest`
- date: 2026-06-25

## Input Scope

This ingest uses only the repository-local input slices authorized for EXAM-CLEAN-010:

- `workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl`
- `workflow/records/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.jsonl`
- `workflow/cleaning/EXAM-CLEAN-009_ANSWER_ALIGNMENT.md`

No OCR was performed. No new question content was added. No text, option, answer, or explanation was fabricated. No markdown or Word export work was performed.

## Ingest Goal

Create one structured, traceable, validator-backed question-bank slice that:

1. preserves the question-level provenance required by the task;
2. carries forward only EXAM-CLEAN-006 and EXAM-CLEAN-008 records;
3. preserves answer shapes already confirmed in EXAM-CLEAN-009;
4. keeps reading-block trace for reading items and avoids fabricated options for writing items;
5. leaves any unresolved source-trace issue explicit through `source_trace_status` and `manual_review_note`.

## Field Mapping

| structured field | source field |
| --- | --- |
| `question_id` | `question_id` |
| `exam_id` | `exam_id` |
| `source_file` | `source_file` |
| `source_page_or_section` | `source_page_or_section` |
| `source_question_number` | `source_question_number` |
| `section_type` | derived from `question_type` as `reading` or `writing` |
| `passage_id` | preserved from reading records when present |
| `question_text` | `question_text` |
| `options` | `options` |
| `answer` | `answer` |
| `answer_source` | `source_trace.answer_source_file` + `source_trace.answer_source_span` |
| `source_trace_status` | `source_trace_status` |
| `manual_review_note` | `manual_review_note` |

Additional trace fields preserved for validator support:

- `question_type`
- `source_span`
- `validation_status`
- `manual_review_status`
- reading records only: `block_id`, `passage_ref`

## Output Summary

| source slice | records ingested | section type |
| --- | ---: | --- |
| `EXAM-CLEAN-006` | 3 | reading |
| `EXAM-CLEAN-008` | 5 | writing |
| total | 8 | mixed |

## Ingest Decisions

- Reading records keep `passage_id`, `block_id`, and `passage_ref` so each item still resolves to the audited reading block.
- Writing records keep `options: null`; no placeholder options were introduced.
- Objective reading answers remain label strings.
- Writing answers remain source-backed `sample_answer` objects.
- `source_trace_status` values were preserved as-is from source records (`confirmed` and `READY`) because the task requires retention, not silent normalization.
- `manual_review_note` was retained verbatim for every record.

## Validation Target

The structured validator for EXAM-CLEAN-010 must check:

- JSONL parseability
- unique `question_id`
- required fields
- non-empty `answer`
- reading trace presence
- no fabricated writing options
- explicit manual-review counts
- input/output count reconciliation against EXAM-CLEAN-006 and EXAM-CLEAN-008
