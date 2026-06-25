# EXAM-CLEAN-003 First Batch Plan

## task_id

EXAM-CLEAN-003

## purpose

Select a small READY Word-first batch with clear primary question sources, define what can be cleaned safely now, and produce the first reusable sample question records without expanding into full-library cleaning.

## selection_inputs

- `workflow/cleaning/EXAM-CLEAN-002_INPUT_INVENTORY.md`
- `workflow/cleaning/EXAM-CLEAN-002_SOURCE_TRACE.md`
- standardized folders under `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/`
- each selected folder `meta.txt`

## selected_first_batch

| exam_id | standardized_folder | primary_question_source | support_source | why_selected |
| --- | --- | --- | --- | --- |
| E001 | `E001_2025_河南开封市_期末_高三_英语` | `Q_原卷.docx` | `QA_解析版.docx` | READY in inventory; single Q Word source; QA support present; no PDF/audio support; meta present; file naming clear. |
| E002 | `E002_2025_河南2月测评_期末_高三_英语` | `Q_原卷.docx` | `QA_解析版.docx` | READY in inventory; single Q Word source; QA support present; no PDF/audio support; meta present; file naming clear. |
| E010 | `E010_2025_福建厦门双十中学_开学考_高三_英语` | `Q_原卷.docx` | `QA_解析版.docx` | READY in inventory; single Q Word source; QA support present; no PDF/audio support; meta present; useful as a boundary case because the Word source contains table/media dependencies and a non-standard section structure. |

## clean_now_scope

This task cleans only a tiny sample range:

| exam_id | section | source_range | record_range | status |
| --- | --- | --- | --- | --- |
| E001 | Reading, First Section, Passage A | `Q_原卷.docx` paragraphs 74-110; answer support in `QA_解析版.docx` paragraphs 111-119 | reading A questions 1-3 | sample records emitted |
| E002 | Reading, First Section, Passage A | `Q_原卷.docx` paragraphs 71-89; answer support in `QA_解析版.docx` paragraphs 90-98 | reading A questions 1-3 | sample records emitted |

## defer_scope

| exam_id | deferred_range | reason |
| --- | --- | --- |
| E001 | listening 1-20 | Listening text depends on audio context and is outside the Word-first text-cleaning sample. |
| E001 | reading B-D, seven选五 16-20, cloze 21-35, grammar 36-45, writing 46-47 | Deferred to keep this task as a first sample only. Later tasks should process by dedicated section type. |
| E002 | listening 1-20 | Listening text depends on audio context and is outside the Word-first text-cleaning sample. |
| E002 | reading B-D, seven选五 16-20, cloze 21-35, grammar 36-45, writing 46-47 | Deferred to keep this task as a first sample only. Later tasks should process by dedicated section type. |
| E010 | all question records | Not emitted in this task because the Word file contains 1 table and 2 media files, and the detected question sequence around the third part requires manual boundary confirmation before sample records are safe. |

## record_policy

- Use `Q_原卷.docx` as the primary source for stems, options, section instructions, and source spans.
- Use `QA_解析版.docx` only to confirm answers and brief explanation text.
- Preserve source display numbering in `source_question_number`.
- Use paragraph locators because this batch is DOCX-first and no page map is available.
- Mark any option-label spacing normalization in `normalization_notes`.
- Do not create records for image/table-dependent items or missing/ambiguous question numbers.

## next_task_handoff

EXAM-CLEAN-004 should begin from the confirmed reading boundaries here and expand reading extraction with explicit passage-level handling, because reading subquestions need passage context in addition to per-question stems.
