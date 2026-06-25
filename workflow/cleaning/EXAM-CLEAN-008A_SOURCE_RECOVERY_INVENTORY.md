# EXAM-CLEAN-008A Source Recovery Inventory

## Task

- task id: EXAM-CLEAN-008A
- task title: standardized Word source recovery
- date: 2026-06-25

## Purpose

EXAM-CLEAN-008 needs standardized Word sources before writing prompts can be extracted. This task checks whether those sources exist in the current repo, whether they are ignored, and where a human should restore them.

This task does not extract questions, create question records, run OCR, or fabricate missing source content.

## Repository Source State

- current dataset root: `datasets/2026_quyixian_english`
- actual directories present:
  - `datasets/2026_quyixian_english/_整理清单`
- absent directories:
  - `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS`
  - `datasets/2026_quyixian_english/_ORIGINAL_EXTRACTED`
  - `datasets/2026_quyixian_english/_ORIGINAL_ZIPS`
- `.docx` files found by `find . -iname "*.docx" | sort`: none
- untracked source files found by `git ls-files --others --exclude-standard | sort`: none
- ignored source files found by `git status --ignored --short`: none

## Git Ignore Finding

`.gitignore` intentionally excludes the likely source-file locations:

```text
datasets/*/_ORIGINAL_ZIPS/
datasets/*/_ORIGINAL_EXTRACTED/
datasets/*/_STANDARDIZED_EXAMS/
```

`git check-ignore -v` confirms that a restored standardized source such as:

```text
datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx
```

would be ignored by the rule `datasets/*/_STANDARDIZED_EXAMS/`.

## EXAM-CLEAN-008 Required Standardized Sources

| exam_id | standardized folder | required source | expected repo path | current state |
| --- | --- | --- | --- | --- |
| E001 | `E001_2025_河南开封市_期末_高三_英语` | primary paper | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx` | missing |
| E001 | `E001_2025_河南开封市_期末_高三_英语` | answer/explanation support | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/QA_解析版.docx` | missing |
| E002 | `E002_2025_河南2月测评_期末_高三_英语` | primary paper | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx` | missing |
| E002 | `E002_2025_河南2月测评_期末_高三_英语` | answer/explanation support | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/QA_解析版.docx` | missing |
| E010 | `E010_2025_福建厦门双十中学_开学考_高三_英语` | primary paper | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/Q_原卷.docx` | missing |
| E010 | `E010_2025_福建厦门双十中学_开学考_高三_英语` | answer/explanation support | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/QA_解析版.docx` | missing |

## Candidate External Sources From Existing CSV Manifests

These entries are not source files in the current repo. They are manifest references that identify likely external/original source locations.

| exam_id | original folder key | original Q candidate | original QA candidate |
| --- | --- | --- | --- |
| E001 | `00b28d2f-c00f-4163-b41d-662ea357909d/00b28d2f-c00f-4163-b41d-662ea357909d` | `精品解析：河南开封市2025-2026学年上学期高三英语期末考试试题（原卷版）.docx` | `精品解析：河南开封市2025-2026学年上学期高三英语期末考试试题（解析版）.docx` |
| E002 | `0132a410-0eea-46f7-8b82-8c35252335f2/0132a410-0eea-46f7-8c35252335f2` | `精品解析：河南2025-2026学年上学期高三年级2月测评期末英语试题（原卷版）.docx` | `精品解析：河南2025-2026学年上学期高三年级2月测评期末英语试题（解析版）.docx` |
| E010 | `310569c4-df4b-4a06-a72c-9dc36a9aa513/310569c4-df4b-4a06-a72c-9dc36a9aa513` | `精品解析：福建省厦门双十中学2025-2026学年高三上学期开学英语试题（原卷版）.docx` | `精品解析：福建省厦门双十中学2025-2026学年高三上学期开学英语试题（解析版）.docx` |

## Required Human Recovery Action

Restore or mount the real source files before retrying EXAM-CLEAN-008:

1. Recreate `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/` from the original standardized source bundle, or provide an external source manifest with stable local paths.
2. Ensure E001, E002, and E010 each contain `Q_原卷.docx` and `QA_解析版.docx` at the expected standardized paths or record the actual replacement paths before extraction.
3. Keep the files ignored unless project governance explicitly decides that Word sources should be tracked in git.
4. After restoration, rerun `find . -iname "*.docx" | sort` and the EXAM-CLEAN-008 source checks before creating any writing question record.

## EXAM-CLEAN-008 Retry Status

EXAM-CLEAN-008 remains `BLOCKED`. It is not `READY_TO_RETRY` because no required Word source file is present in the current on-disk repo.

