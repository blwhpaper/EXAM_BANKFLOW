# EXAM-CLEAN-003 Boundary Map

## task_id

EXAM-CLEAN-003

## boundary_method

The selected documents were inspected as DOCX text only. Paragraph numbers are ordered `word/document.xml` paragraph positions, used as reviewable locators for this Word-first pass. PDF files, images, and audio were not OCRed, transcribed, or used as question-text sources.

## selected_exam_boundaries

### E001

- folder: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语`
- primary source: `Q_原卷.docx`
- support source: `QA_解析版.docx`
- meta status: `OK_Q_QA`
- Q source shape: 240 non-empty paragraphs, 0 tables, 4 media objects
- QA source shape: 396 non-empty paragraphs, 0 tables, 5 media objects

| section | Q paragraph boundary | detected numbering | cleanability |
| --- | --- | --- | --- |
| Listening | 2-70 | 1-20 | not cleaned; audio/listening context outside this Word-first sample |
| Reading first section | 71-170 | source displays reading questions 1-15 | partially cleanable; Passage A questions 1-3 emitted as sample records |
| Reading second section / 七选五 | 171-186 | 16-20 confirmed in QA answer block | defer to EXAM-CLEAN-005; no records here |
| Language use, cloze | 187-210 | 21-35 | defer to EXAM-CLEAN-006 |
| Language use, grammar fill | 211-216 | 36-45 in QA answer block | defer to EXAM-CLEAN-007 |
| Writing | 217-240 | 46-47 | defer to EXAM-CLEAN-008 |

Manual review triggers for E001:

- Any future item that depends on the 4 embedded media objects must be manually reviewed before record output.
- Reading question display numbering starts at `1` inside the reading section while later answer blocks continue `16-47`; later batch cleaning must preserve source display numbering and define any canonical renumbering explicitly.

### E002

- folder: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语`
- primary source: `Q_原卷.docx`
- support source: `QA_解析版.docx`
- meta status: `OK_Q_QA`
- Q source shape: 227 non-empty paragraphs, 0 tables, 4 media objects
- QA source shape: 381 non-empty paragraphs, 0 tables, 4 media objects

| section | Q paragraph boundary | detected numbering | cleanability |
| --- | --- | --- | --- |
| Listening | 8-67 | 1-20 | not cleaned; audio/listening context outside this Word-first sample |
| Reading first section | 68-156 | source displays reading questions 1-15 | partially cleanable; Passage A questions 1-3 emitted as sample records |
| Reading second section / 七选五 | 157-175 | 16-20 confirmed in QA answer block | defer to EXAM-CLEAN-005 |
| Language use, cloze | 176-198 | 21-35 | defer to EXAM-CLEAN-006 |
| Language use, grammar fill | 199-203 | 36-45 in QA answer block | defer to EXAM-CLEAN-007 |
| Writing | 204-227 | 46-47 | defer to EXAM-CLEAN-008 |

Manual review triggers for E002:

- Any future item that depends on the 4 embedded media objects must be manually reviewed before record output.
- Passage A option labels are partially glued in the Word text, for example `AAt` and `Park.B.`; this is cleanable only when the label split is visually unambiguous and recorded in `normalization_notes`.

### E010

- folder: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语`
- primary source: `Q_原卷.docx`
- support source: `QA_解析版.docx`
- meta status: `OK_Q_QA`
- Q source shape: 260 non-empty paragraphs, 1 table, 2 media objects
- QA source shape: 485 non-empty paragraphs, 1 table, 4 media objects

| section | Q paragraph boundary | detected numbering | cleanability |
| --- | --- | --- | --- |
| Listening | 3-64 | 1-20 | not cleaned; listening context outside this Word-first sample |
| Reading first section | 65-162 | source displays reading questions 1-15 | boundary identified, but no records emitted because Passage A includes a table-dependent price item |
| Reading second section / 七选五 | 163-177 | 16-20 confirmed in QA answer block | defer to EXAM-CLEAN-005 |
| Language/knowledge use | 178-249 | 21-65 with a visible gap around 28 in plain paragraph extraction | manual review required before records |
| Later grammar/text fill | 250-251 | 66 onward in QA answer block | manual review required before records |
| Writing | 252-260 | 76 | defer; numbering gap must be confirmed before structured output |

Manual review triggers for E010:

- The Q file contains a table; table-dependent questions cannot be cleaned until the table structure is preserved or manually approved.
- The Q file contains media objects; image-dependent content must not be inferred from file presence.
- Plain paragraph extraction shows question numbering jumping from 27 to 29 in the third part and writing at 76; this requires source-side boundary confirmation before record output.

## reusable_boundary_rules

- A section is `cleanable` only when one primary `Q_原卷*.docx` source is selected, the question number is visible, the stem/options are present in text, and answer support does not conflict.
- A section is `partially cleanable` when its boundary is clear but only a small safe range is emitted for this task.
- A section is `manual review` when any question depends on a table, image, missing paragraph text, duplicated/missing numbering, or conflicting answer support.
- `QA_解析版.docx` may confirm answers and explanations but must not replace the Q source for question text.
- `A_答案*.docx` is not used in this selected batch because all emitted sample records use QA support.

## manual_review_count

- boundary-level manual review triggers: 7
- sample-record manual review notes: 0

The 7 boundary-level triggers are: E001 media dependency, E001 reading display/canonical numbering policy, E002 media dependency, E002 glued option-label normalization, E010 table dependency, E010 media dependency, and E010 numbering gap.
