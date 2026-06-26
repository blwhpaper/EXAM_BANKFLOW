# EXAM-CLEAN-008 Question Records Slice

## Task

- task id: EXAM-CLEAN-008
- task title: writing question structured extraction
- retry branch: `task-exam-clean-008-retry-writing-question-records`
- date: 2026-06-25

## Retry Context

EXAM-CLEAN-008 first opened the writing slice but emitted zero records because the standardized Word sources were absent from the on-disk repo.

EXAM-CLEAN-008A recorded the missing source inventory and target restore paths.

EXAM-CLEAN-008B verified that the required six Word files were restored, non-empty, readable as `.docx` zip containers, and still ignored by git.

This retry uses only those restored standardized Word files.

## Actual Extraction Scope

| exam_id | source question range | emitted records | status |
| --- | --- | ---: | --- |
| E001 | writing questions 46-47 | 2 | READY |
| E002 | writing questions 46-47 | 2 | READY |
| E010 | writing question 76 | 1 | READY |

Total emitted question records: 5.

## Source Files

- E001 Q: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
- E001 QA: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/QA_解析版.docx`
- E002 Q: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx`
- E002 QA: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/QA_解析版.docx`
- E010 Q: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/Q_原卷.docx`
- E010 QA: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/QA_解析版.docx`

## Records Emitted

| question_id | source range | answer support | result |
| --- | --- | --- | --- |
| `e001-writing-q46` | E001 Q paragraphs 217-227 | E001 QA paragraphs 346-365 | READY |
| `e001-writing-q47` | E001 Q paragraphs 228-240 | E001 QA paragraphs 379-396 | READY |
| `e002-writing-q46` | E002 Q paragraphs 204-214 | E002 QA paragraphs 332-350 | READY |
| `e002-writing-q47` | E002 Q paragraphs 215-227 | E002 QA paragraphs 364-381 | READY |
| `e010-writing-q76` | E010 Q paragraphs 252-260 | E010 QA paragraphs 468-485 | READY |

## Record Policy

- `question_type` is `writing`.
- `options` is `null`.
- `answer` is stored as a source-backed `sample_answer` object from `QA_解析版.docx`.
- `explanation` is summarized from the source-backed QA analysis paragraphs.
- `source_trace_status` is `READY` because the prompt, sample answer, and explanation support are all visible in the cited Word paragraph ranges.
- `score` is taken from the visible section score: 15 for application/proposal writing and 25 for continuation writing.

## Manual Review

- READY: 5
- NEEDS_MANUAL_REVIEW: 0
- EXCLUDED: 0

No emitted record requires manual review. E010 had previous table/media/numbering warnings for other ranges, but the writing prompt 76 and matching QA support are visible in the restored Word files.

## Boundaries Respected

- no OCR
- no question text, answer, explanation, score, or source locator was fabricated
- no reading comprehension records were emitted
- no cloze records were emitted
- no Word source files were modified or staged
- EXAM-CLEAN-009 was not advanced

