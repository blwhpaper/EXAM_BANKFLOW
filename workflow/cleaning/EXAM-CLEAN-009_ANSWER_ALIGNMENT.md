# EXAM-CLEAN-009 Answer Alignment Audit

## Task

- task id: EXAM-CLEAN-009
- task title: 答案对齐
- branch: `task-exam-clean-009-answer-alignment`
- date: 2026-06-25

## Input Scope

This audit uses only the repository-local files authorized for EXAM-CLEAN-009:

- `workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl`
- `workflow/records/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.jsonl`
- `workflow/cleaning/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.md`
- `workflow/cleaning/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.md`
- `workflow/Task_Closeouts/EXAM-CLEAN-006_Closeout.md`
- `workflow/Task_Closeouts/EXAM-CLEAN-008_Closeout.md`
- `workflow/schema/QUESTION_RECORD_SCHEMA.yaml`

No new questions were added. No OCR, answer guessing, ingestion, or export work was performed.

## Audit Goal

Confirm that the first batch of question records is answer-ready for a later ingestion task by checking:

1. whether each record already contains a usable answer field;
2. whether reading and writing answers use schema-compatible shapes;
3. whether answer provenance is traceable to source-backed Q/QA material;
4. whether `source_trace_status` is sufficient to support answer confidence;
5. whether unresolved cases are explicitly routed to manual review instead of guessed.

## Slice Summary

| slice | question type focus | records | answer shape | manual review |
| --- | --- | ---: | --- | ---: |
| `EXAM-CLEAN-006` | reading comprehension | 3 | objective label string | 0 |
| `EXAM-CLEAN-008` | writing | 5 | `sample_answer` object | 0 |
| total | mixed | 8 | mixed by type, schema-compatible | 0 |

## Alignment Findings

### 1. Existing Answer Coverage

- total records audited: 8
- records with populated `answer`: 8
- records with missing `answer`: 0
- records with equivalent alternate fields such as `correct_answer` or `answer_key`: 0
- result: all audited records already use the canonical `answer` field; no alternate answer-field migration was needed

### 2. Schema Alignment By Question Type

- reading records (`e001-reading-a-q1` through `e001-reading-a-q3`) use `question_type: reading_subquestion`, complete A-D `options`, and single-label `answer` strings. This is compatible with the question-record schema for objective questions.
- writing records (`e001-writing-q46`, `e001-writing-q47`, `e002-writing-q46`, `e002-writing-q47`, `e010-writing-q76`) use `question_type: writing`, `options: null`, and object-valued `answer` payloads carrying `answer_type`, source, and full sample-answer text. This is compatible with the schema’s allowed `object` answer shape for subjective items.
- no record required conversion to `correct_answer` or `answer_key`.

### 3. Answer Provenance Traceability

Every audited record includes:

- top-level source fields: `source_file`, `source_page_or_section`, `source_question_number`
- `source_span` for the prompt location
- `source_trace.answer_source_file`
- `source_trace.answer_source_span` with paragraph locator and excerpt

Reading records trace answers to `QA_解析版.docx` answer paragraphs 111-119 for E001 reading block `e001-reading-a`.

Writing records trace sample answers to the matching `QA_解析版.docx` paragraph ranges cited in EXAM-CLEAN-008.

Result: answer provenance is traceable for all 8 records.

### 4. Source Trace Confidence

- EXAM-CLEAN-006 uses `source_trace_status: confirmed`
- EXAM-CLEAN-008 uses `source_trace_status: READY`
- both status values are already treated as accepted/ready-equivalent by the current repository validator
- all 8 records also carry `validation_status.answer_status: confirmed`

Result: the current repository state is sufficient to support answer confidence for this batch, although the wording is not yet normalized across tasks.

## Record-Level Audit Table

| question_id | question_type | answer present | answer shape | answer source trace | source_trace_status | manual review |
| --- | --- | --- | --- | --- | --- | --- |
| `e001-reading-a-q1` | reading_subquestion | yes | label `A` | yes | `confirmed` | no |
| `e001-reading-a-q2` | reading_subquestion | yes | label `C` | yes | `confirmed` | no |
| `e001-reading-a-q3` | reading_subquestion | yes | label `D` | yes | `confirmed` | no |
| `e001-writing-q46` | writing | yes | `sample_answer` object | yes | `READY` | no |
| `e001-writing-q47` | writing | yes | `sample_answer` object | yes | `READY` | no |
| `e002-writing-q46` | writing | yes | `sample_answer` object | yes | `READY` | no |
| `e002-writing-q47` | writing | yes | `sample_answer` object | yes | `READY` | no |
| `e010-writing-q76` | writing | yes | `sample_answer` object | yes | `READY` | no |

## Manual Review Decision

- `manual_review_status: required`: 0
- `source_trace_status: NEEDS_MANUAL_REVIEW`: 0
- guessed answers introduced: 0

No record was escalated to manual review because all audited answers were already source-backed in the on-disk repo.

## Task Output For EXAM-CLEAN-010

This task prepares, but does not execute, later ingestion work:

- answer field coverage is complete for the audited batch
- objective and subjective answer shapes are distinguishable and traceable
- no missing-answer blocker remains in the two audited slices
- no ingestion, export, or new-question work was performed

## Validation

Commands run for EXAM-CLEAN-009:

```bash
git status --short --branch
python3 -m json.tool workflow/TASK_STATE.json >/dev/null
python3 workflow/validation/validate_question_records_slice.py workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl
python3 workflow/validation/validate_question_records_slice.py workflow/records/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.jsonl
python3 workflow/validation/validate_answer_alignment.py workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl workflow/records/EXAM-CLEAN-008_QUESTION_RECORDS_SLICE.jsonl
git diff --check
```

Expected answer-alignment result:

```text
PASS answer_alignment_records=8 confirmed_answers=8 manual_review=0 missing_answers=0
```
