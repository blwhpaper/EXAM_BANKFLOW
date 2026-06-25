# EXAM-CLEAN-002 Source Trace Rules

## task_id

EXAM-CLEAN-002

## purpose

Define the minimum source trace contract that all later question records must follow when EXAM-CLEAN-003 and later tasks start cleaning real exam content.

## required_fields

- `source_file`: repository-relative path to the concrete source file actually used for the question text or answer/support evidence. Prefer the standardized file path under `_STANDARDIZED_EXAMS/`; if a later task must inspect the original bundle, keep that original path in notes or provenance but do not replace the standardized `source_file` silently.
- `source_page_or_section`: page/section/paragraph/line-style locator that points to where the question was found. For DOCX-first work, use the best available ordered section/paragraph locator. For PDF support files, only record this after a human/manual process establishes it; do not invent page numbers.
- `source_question_number`: the visible source-side question number or label exactly as shown in the chosen source. If missing or duplicated, preserve the ambiguous display form and mark the trace status as non-final.
- `source_trace_status`: one of `confirmed`, `partial`, `ambiguous`, `missing`, `unsupported_format`.
- `manual_review_note`: required whenever the trace uses `partial`, `ambiguous`, `missing`, or `unsupported_format`, or whenever multiple candidate source files exist for the same question.

## source_selection_order

- 1. Use `Q_原卷*.docx` as the primary `source_file` for question stem/options/instructions whenever an in-scope Word source exists and only one candidate Q file is present.
- 2. Use `QA_解析版.docx` only as a supporting trace source unless the later task explicitly records why the original Q file is insufficient for a specific field.
- 3. Use `A_答案*.docx` only for answer/explanation/support fields, never as the sole source for stem text.
- 4. Keep `PDF_*` files as support-only trace references in this batch unless a later human/manual workflow authorizes non-OCR page-level tracing.
- 5. Never use audio files as question-text trace sources in this batch.
- 6. Never cite `meta.txt` or CSV control files as the content source for a question; they only justify scope, folder mapping, and provenance.

## source_trace_status_rules

- `confirmed`: one clear in-scope Word source file is selected, the question number is visible, and the locator is reviewable.
- `partial`: the file is known but the exact page/section/number locator is incomplete; later output may continue only if the missing detail is explicitly noted and the question remains reviewable.
- `ambiguous`: multiple candidate Q files, conflicting source files, unknown-source bundles, or duplicated numbering prevent a single unambiguous citation.
- `missing`: no trustworthy source file or locator can be established for the question record. Dataset-facing output must stop for that item.
- `unsupported_format`: the only useful evidence is in PDF/audio/image-like material that this batch is not authorized to OCR or transcribe automatically.

## mandatory_handoff_warnings

- unknown-source standardized folders such as `E024` must stay out of `READY` question cleaning until provenance is manually confirmed.
- bundles with multiple `Q_原卷*` files such as `E035`, `E038`, and `E049` require a later explicit file-order or file-selection note before question slicing begins.
- bundles with in-scope PDF support files such as `E006`, `E018`, `E036`, `E045`, `E047`, and `E048` may cite those PDFs only as secondary/supporting evidence with `source_trace_status: unsupported_format` or `partial` until manual trace is established.
- no later task may treat file names alone as proof of question text, answer content, or question numbering.