# Output Format Specification

## Purpose

This document defines the output formats that future `EXAM-CLEAN-*` tasks must produce after extraction and normalization. The same content may be emitted in multiple forms, but all forms must point back to the same `exam_id`, `question_id`, and source trace.

## Supported Output Forms

1. canonical markdown output
2. structured YAML output
3. structured JSON output
4. review checklist output

## Canonical Markdown Output

The markdown version is the primary human-review surface.

Recommended structure:

```md
# {exam_title}

- exam_id: {exam_id}
- source_file: {source_file}
- subject: {subject}
- grade_or_level: {grade_or_level}
- year: {year}
- region: {region}
- paper_type: {paper_type}

## Sections

### {section_title} ({section_id})

#### Question {question_number} [{question_id}]

- question_type: {question_type}
- score: {score}
- answer_status: {validation_status.answer_status}
- explanation_status: {validation_status.explanation_status}
- uncertainty: {metadata or validation uncertainty summary}

**Stem**
{stem}

**Options**
- A. ...
- B. ...

**Answer**
{answer or explicit missing note}

**Explanation**
{explanation or explicit missing note}

**Normalization Notes**
- ...

**Source Span**
- source_ref: ...
- locator: ...
```

Markdown rules:

- preserve exam and question order from source
- do not omit missing values silently; print explicit status notes
- include source span and uncertainty notes for reviewer traceability
- keep formatting readable without requiring a renderer-specific extension

## Structured YAML/JSON Output

Structured exports are the machine-facing source of truth for later indexing.

Top-level layout:

```text
exam/
  exam_record
  questions[]
  exports[]
```

Required top-level keys:

- `exam_record`
- `questions`
- `exports`

`exam_record` must follow `EXAM_DATA_SCHEMA.md`.

Each item in `questions` must follow `QUESTION_RECORD_SCHEMA.yaml`.

Each item in `exports` should include:

- `export_id`
- `exam_id`
- `format`
- `file_path`
- `generated_from`
- `generated_at`

Serialization rules:

- YAML for hand-edited reviewable artifacts
- JSON for strict machine interchange
- no field omission for required keys
- use `null` instead of invented strings such as `unknown`
- arrays must remain ordered when source order matters

## Review Checklist Output

Every cleaning run that emits structured content should also emit a review checklist compatible with `workflow/templates/REVIEW_CHECKLIST_TEMPLATE.md`.

Checklist should verify:

- source files identified correctly
- exam metadata captured without fabrication
- question counts and numbering reconcile
- answer/explanation presence states are explicit
- uncertainty markers are preserved
- export files map to the declared naming convention

## File Naming Rules

All filenames should be deterministic and traceable.

Recommended naming patterns:

- clean intermediate markdown: `{exam_id}.clean.md`
- canonical exam markdown: `{exam_id}.canonical.md`
- structured YAML: `{exam_id}.structured.yaml`
- structured JSON: `{exam_id}.structured.json`
- review checklist: `{exam_id}.review.md`
- export manifest entry id: `{exam_id}-{format}`

If task outputs are grouped by run, prepend or folder-scope by `run_id` rather than changing `exam_id`.

## Directory Intent

Suggested future directory intent only:

- `workflow/` for harness specifications
- `datasets/.../clean/` for normalized human-readable outputs
- `datasets/.../structured/` for YAML/JSON records
- `datasets/.../review/` for review surfaces

This task does not create dataset-side directories.

## Forbidden Output Behavior

- no undocumented ad hoc field names
- no hidden derived answers
- no dropping reviewer-critical uncertainty
- no file names that hide the source exam identity
