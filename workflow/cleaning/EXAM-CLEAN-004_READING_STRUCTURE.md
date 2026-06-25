# EXAM-CLEAN-004 Reading Structure

## task_id

EXAM-CLEAN-004

## purpose

Define the first passage-first reading structure for EXAM_BANKFLOW so reading comprehension output keeps the passage and its subquestions in one auditable record.

## output_record_unit

Each JSONL line in `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl` is one reading block, not one detached question.

The block is the parent unit:

- `reading_block_id`: stable lowercase id for the passage block.
- `exam_id`: parent exam id.
- `section_id`: stable section id reused by child questions.
- `section_label`: human-readable passage label, for example `Reading Passage A`.
- `passage_title`: source-visible or minimally normalized title.
- `passage_text`: complete passage text extracted from `Q_原卷*.docx`.
- `questions`: ordered child reading subquestions.
- `source_trace`: block-level source trace covering passage, questions, and answer support.
- `assets`: source-linked media/table dependencies if any are used.
- `normalization_notes`: block-level cleanup decisions.
- `validation_status`: block-level validation result.

## child_question_shape

Questions remain question-like children, but they no longer carry passage context by repetition. Each child contains:

- `question_id`
- `question_number`
- `question_type: reading_subquestion`
- `stem`
- `options`
- `answer`
- `explanation`
- `score`
- `source_question_number`
- `source_span`
- `normalization_notes`
- `validation_status`

## source_policy

- `passage_text`, stems, options, and question source spans must come from `Q_原卷*.docx`.
- `QA_解析版.docx` may confirm answers and explanations only.
- `A_答案*.docx` may support answers only when no better explanation source exists.
- PDF files, images, and audio are not OCRed or transcribed in this task.
- Any table or media dependency that cannot be represented faithfully triggers manual review instead of guessed text.

## difference_from_EXAM-CLEAN-003

EXAM-CLEAN-003 emitted six `reading_subquestion` sample records:

- three E001 Passage A subquestions
- three E002 Passage A subquestions

Those records were traceable but detached: each record repeated passage context in the `stem` and did not preserve the full source passage as the parent context.

EXAM-CLEAN-004 corrects this by emitting:

- one `e001-reading-a` block containing the full E001 Passage A text and its three child questions
- one `e002-reading-a` block containing the full E002 Passage A text and its three child questions

This makes reading extraction suitable for later batch processing because the passage, child questions, source spans, answers, and normalization decisions remain together.

## first_batch_result

- reading blocks: 2
- child questions: 6
- passage_text source: `Q_原卷.docx` only
- answer/explanation support: `QA_解析版.docx`
- block validation status: pass
- manual review blocks emitted: 0

