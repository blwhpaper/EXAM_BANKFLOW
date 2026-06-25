# EXAM-CLEAN-004 Manual Review

## task_id

EXAM-CLEAN-004

## review_policy

Reading blocks are emitted only when the passage text is complete in `Q_原卷*.docx`, the child question numbering is continuous inside the selected passage, options can be reliably split, and answer support confirms the selected answers without conflict.

If any of those conditions fails, the block is deferred instead of guessed.

## emitted_blocks_review_status

| exam_id | block_id | status | reason |
| --- | --- | --- | --- |
| E001 | e001-reading-a | pass | Passage A text is present in `Q_原卷.docx` paragraphs 75-95; questions 1-3 and QA support are confirmed. |
| E002 | e002-reading-a | pass | Passage A text is present in `Q_原卷.docx` paragraphs 72-80; questions 1-3 and QA support are confirmed. Option label spacing was normalized and recorded. |

## deferred_or_manual_review_items

| exam_id | scope | status | reason |
| --- | --- | --- | --- |
| E010 | Reading Passage A and later reading ranges | deferred_manual_review | E010 was intentionally not extracted in EXAM-CLEAN-004 because EXAM-CLEAN-003 identified one table, media objects, and a question-numbering gap around the third part. The task boundary says not to hard-extract E010 when table/media/numbering risk exists. |
| E001 | future media-dependent items | manual_review_trigger | EXAM-CLEAN-003 identified embedded media objects. This task extracted only text-complete Passage A, which does not depend on those media objects. |
| E002 | future media-dependent items | manual_review_trigger | EXAM-CLEAN-003 identified embedded media objects. This task extracted only text-complete Passage A, which does not depend on those media objects. |
| E002 | option label spacing | resolved_with_note | Passage A options were glued in source paragraphs 82-89. Labels were split only where visually unambiguous and the normalization is recorded in the JSONL. |

## manual_review_count

- emitted reading blocks requiring manual review: 0
- deferred reading scopes requiring manual review before extraction: 1
- review-trigger notes carried forward: 3

## triggers_for_future_reading_batches

- passage text absent from `Q_原卷*.docx`
- passage depends on a table, image, chart, or other media object
- source question numbering is missing, duplicated, or discontinuous
- options are glued in a way that cannot be split reliably from text alone
- answer or explanation support conflicts with the Q source
- only PDF/image evidence is available for the passage or question text

