# Validation Rules

## Purpose

These validation rules define the minimum acceptance checks for structured exam outputs in `EXAM_BANKFLOW`. They are written as repository rules, not as executable scripts.

## Core Acceptance Rules

1. required field checks must pass for exam and question records
2. `question_id` must be unique across the output set
3. `exam_id` must match between the exam record and every child question record
4. objective question `options` and `answer` must be structurally valid
5. subjective question `answer` and `explanation` may be empty only with explicit state labels
6. uncertain source content must keep an uncertainty marker
7. no fabricated stem, answer, explanation, score, year, or source metadata

## Required Field Checks

Exam records must include:

- `exam_id`
- `source_file`
- `exam_title`
- `subject`
- `sections`
- `metadata`
- `provenance`

Question records must include:

- `question_id`
- `exam_id`
- `section_id`
- `question_number`
- `question_type`
- `stem`
- `source_span`
- `normalization_notes`
- `validation_status`

## Identifier Rules

- `exam_id` must be stable within one exam bundle
- `question_id` must be unique across the repository or at minimum unique within the exported batch with no collisions against existing records
- `section_id` must resolve to a declared section in the parent exam record

## Exam/Question Consistency

- every question's `exam_id` must equal the parent exam `exam_id`
- question ordering should be reconcilable to the exam section ordering
- question counts should not exceed or contradict declared section ranges without a warning note

## Objective Question Rules

For `single_choice` and `multiple_choice`:

- `options` must be present
- `options` must contain at least two entries
- each option should have a label and text
- `answer` must reference valid option labels or a documented structured answer object
- if the source answer is missing, `validation_status.answer_status` must be `missing_in_source` or `uncertain`

## Subjective Question Rules

For `short_answer`, `writing`, and similar non-choice types:

- `options` should be null or empty
- `answer` may be null
- `explanation` may be null
- null `answer` or `explanation` must be paired with explicit status fields
- absence of source answer is not a failure if clearly marked and traceable

## Uncertainty Rules

Use uncertainty markers when:

- OCR or extraction damaged a phrase
- numbering is ambiguous
- year, score, or section title is only partially visible
- answer key alignment is not fully confirmed

Minimum handling:

- add an uncertainty entry to `validation_status.uncertainty` or exam metadata
- mention the issue in `normalization_notes` or `provenance.confidence_notes`
- preserve the unresolved text instead of silently repairing it

## Non-Fabrication Rules

The workflow must not invent:

- question stem text
- option text
- answer keys
- explanation text
- score values
- year values
- provenance/source claims

When content cannot be confirmed:

- leave the field null when schema allows
- keep the source excerpt
- mark the uncertainty

## Validation Outcomes

- `pass`: all required checks pass and no unresolved material issue remains
- `warn`: structure is usable but unresolved uncertainty or missing non-critical fields remain
- `fail`: required fields are missing, ids collide, parent-child linkage breaks, or fabricated content is detected

## Review Responsibility

Future implementation tasks may automate these checks, but until then the human or agent reviewer must record the result in the run artifact and task closeout.
