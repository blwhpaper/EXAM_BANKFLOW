# EXAM-CLEAN-008B Source Placement Verification

## Task

- task id: EXAM-CLEAN-008B
- task title: manual source placement verification
- date: 2026-06-25
- branch: `task-exam-clean-008b-manual-source-placement-verification`

## Purpose

Verify that the six Word source files required to retry EXAM-CLEAN-008 have been manually restored to the standardized source paths recorded by EXAM-CLEAN-008A.

This task does not extract questions, read or rewrite question text, generate question records, or run OCR.

## Upstream Sync Check

`git fetch origin main` completed successfully before the source placement checks. After fetch, these refs all pointed to the same commit:

```text
main: ec8671a4c54eb4421eb2de300a3d557e395d7294
origin/main: ec8671a4c54eb4421eb2de300a3d557e395d7294
FETCH_HEAD: ec8671a4c54eb4421eb2de300a3d557e395d7294
```

## Git Ignore Check

`.gitignore` still excludes standardized source files:

```text
datasets/*/_STANDARDIZED_EXAMS/
```

`git status --ignored --short | grep "_STANDARDIZED_EXAMS" || true` returned:

```text
!! datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/
```

The restored Word files remain ignored and were not added to git.

## Target File Verification

| exam_id | role | path | exists | size_bytes | zip_ok | word_document_xml | result |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| E001 | primary paper | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx` | yes | 31733 | yes | yes | OK |
| E001 | answer/explanation support | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/QA_解析版.docx` | yes | 45890 | yes | yes | OK |
| E002 | primary paper | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx` | yes | 31087 | yes | yes | OK |
| E002 | answer/explanation support | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/QA_解析版.docx` | yes | 45821 | yes | yes | OK |
| E010 | primary paper | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/Q_原卷.docx` | yes | 31816 | yes | yes | OK |
| E010 | answer/explanation support | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/QA_解析版.docx` | yes | 52894 | yes | yes | OK |

## Placement Result

- six target Word files present: yes
- all target files readable as `.docx` zip containers: yes
- all target files contain `word/document.xml`: yes
- target files remain ignored by git: yes
- source files staged or tracked by this task: no

## EXAM-CLEAN-008 Retry Decision

EXAM-CLEAN-008 can move from `BLOCKED` to `READY_TO_RETRY` for a future writing extraction retry. This verification only confirms source placement and docx container readability. It does not validate writing prompt content, paragraph boundaries, answers, explanations, or E010 table/media/numbering risks.

