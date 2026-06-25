# EXAM-CLEAN-005 Reading Record Normalization

## task_id

EXAM-CLEAN-005

## purpose

Normalize the expected shape of reading comprehension records after EXAM-CLEAN-004 so later tasks do not collapse reading output into detached stems and answers.

## minimum_complete_record

A reading comprehension record is minimally complete only when it preserves the full parent context and every child choice item:

- `PASSAGE_TEXT`: the complete source passage from `Q_原卷*.docx`, stored as `passage_text`.
- `QUESTIONS`: a non-empty ordered `questions` array under the reading block.
- Each question has `question_number`, `stem`, and exactly four source-backed options labeled `A-D`.
- `Answer`: each objective child question has a confirmed answer label in `A-D`.
- `Explanation`: each explanation is retained when present in the source support; missing explanations must be explicit in validation notes rather than silently dropped.
- `source trace`: block-level source trace must connect passage text, question text, answer support, and any manual review note to repository-local source files/spans.

This means the expected display shape is:

```text
PASSAGE_TEXT
QUESTIONS
  question_number
  stem
  A. option text
  B. option text
  C. option text
  D. option text
  Answer
  Explanation
source trace
```

## normalization_rules

- The reading block, not the detached subquestion, is the final record unit for reading comprehension.
- Do not repeat the full passage inside each child stem.
- Do not display or export reading questions as only `stem + answer`.
- Preserve `explanation` when it exists in the JSONL/source support.
- Preserve `source_trace` at the block level and `source_span` at the child question level when available.
- Options may be whitespace-normalized only when the source text clearly contains the same A-D option content.
- No passage text, question stem, option, answer, or explanation may be fabricated to satisfy structure.

## current_batch_status

`workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl` already contains the minimum complete reading structure for:

- `e001-reading-a`
- `e002-reading-a`

EXAM-CLEAN-005 adds documentation and validation so downstream tasks and reviewers treat `PASSAGE_TEXT + QUESTIONS + A-D options + Answer + Explanation + source trace` as the minimum complete reading comprehension record.

