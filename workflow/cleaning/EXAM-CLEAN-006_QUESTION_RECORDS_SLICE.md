# EXAM-CLEAN-006 Question Records Slice

## task_id

EXAM-CLEAN-006

## purpose

Create a minimal question-record ingestion slice from already audited reading blocks. The purpose is structural validation, not full-batch cleaning.

## source basis

- source reading blocks: `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl`
- normalization reference: `workflow/cleaning/EXAM-CLEAN-005_READING_RECORD_NORMALIZATION.md`
- option audit reference: `workflow/cleaning/EXAM-CLEAN-005_READING_OPTION_AUDIT.md`
- selected block: `e001-reading-a`
- selected questions: `e001-reading-a-q1` through `e001-reading-a-q3`

`e001-reading-a` was selected because EXAM-CLEAN-005 confirms it has passage text, three ordered child questions, complete A-D options, confirmed A/C/D answers, retained explanations, and confirmed source trace.

## output shape

Each JSONL line in `workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl` is one question record. Because this is a reading comprehension slice, every record keeps both child-question data and parent-passage linkage:

- `passage_id` and `block_id`
- `passage_ref`
- full `passage_text`
- `question_text` and schema-compatible `stem`
- `options` array with complete A-D option text
- `answer`
- `source_file`
- `source_page_or_section`
- `source_question_number`
- `source_trace_status`
- `manual_review_status`
- `manual_review_note`

This is intentionally duplicative for the slice so validation can prove that a detached question record still preserves original reading context.

## boundaries

- no OCR
- no image recognition
- no new source extraction
- no invented passage text, question text, option text, answer, explanation, or source locator
- no full-batch expansion beyond `e001-reading-a`
- no historical closeout edits
- no schema framework rewrite

## manual review policy

Missing, uncertain, or conflicting fields must use `source_trace_status: NEEDS_MANUAL_REVIEW` and a concrete `manual_review_note`. The selected slice has no such records because all three answers and source traces are confirmed by EXAM-CLEAN-004/005.

## validation

Validation command:

```bash
python3 workflow/validation/validate_question_records_slice.py workflow/records/EXAM-CLEAN-006_QUESTION_RECORDS_SLICE.jsonl
```

Expected result:

```text
PASS question_records=3 manual_review=0
```
