# EXAM Data Schema

## Purpose

This document defines the canonical data model for exam-level and question-level records in `EXAM_BANKFLOW`. It is a Phase 0 specification only. It does not clean any real exam file and does not introduce a database, runtime, or external dependency.

## Scope Boundary

- apply this schema to future `EXAM-CLEAN-*` outputs
- preserve provenance and uncertainty explicitly
- keep raw-source traceability at both exam and question levels
- do not infer missing facts as confirmed values

## Data Model Layers

1. `exam record`: one source exam paper or paper bundle
2. `section record`: one logical section inside an exam
3. `question record`: one structured question unit
4. `export record`: one derived output artifact linked back to source records

## Exam-Level Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `exam_id` | string | yes | Stable exam identifier used across all outputs. |
| `source_file` | string or string[] | yes | Original source path or ordered source-path list when the exam comes from multiple files. |
| `exam_title` | string | yes | Human-readable exam title from source or minimally normalized title. |
| `subject` | string | yes | Subject label such as `english`. |
| `grade_or_level` | string | no | Grade, school stage, or proficiency level. |
| `year` | integer or string | no | Source-confirmed year only; use uncertainty if partially known. |
| `region` | string | no | Region/city/county/school scope if present in source. |
| `paper_type` | string | no | Example: `midterm`, `final`, `mock`, `unit_test`. |
| `total_score` | number | no | Total paper score if explicitly present. |
| `duration_minutes` | integer | no | Source-confirmed exam duration in minutes. |
| `sections` | object[] | yes | Ordered section list with section ids, titles, and range metadata. |
| `metadata` | object | yes | Normalized metadata container for tags, language, review fields, and status fields. |
| `provenance` | object | yes | Traceability block describing raw inputs, extraction context, and confidence notes. |

## Section Structure

Each section entry in `sections` should contain:

| Field | Type | Required | Description |
|---|---|---|---|
| `section_id` | string | yes | Stable section identifier unique within one exam. |
| `section_title` | string | yes | Display title from source or normalized label. |
| `section_type` | string | yes | Question-family label such as `reading`, `cloze`, `writing`. |
| `question_number_range` | string | no | Example: `21-25`. |
| `instructions` | string | no | Section-level instructions when available. |
| `source_span` | object | yes | Source location span for the section. |

## Metadata Structure

Recommended `metadata` subfields:

- `language`
- `tags`
- `review_status`
- `normalization_version`
- `uncertainty_flags`
- `notes`

## Provenance Structure

Required `provenance` subfields:

- `raw_source_paths`
- `source_type`
- `ingest_method`
- `captured_at`
- `operator`
- `run_id`
- `source_hash` when available
- `confidence_notes`

## Question-Level Fields

The authoritative question schema is defined in `QUESTION_RECORD_SCHEMA.yaml`. Each question record must include the fields below.

| Field | Type | Required | Description |
|---|---|---|---|
| `question_id` | string | yes | Stable question identifier unique across the repository. |
| `exam_id` | string | yes | Parent exam id. Must match exam record. |
| `section_id` | string | yes | Parent section id. |
| `question_number` | string or integer | yes | Display or canonical number inside the exam. |
| `question_type` | string | yes | Canonical type such as `single_choice`, `reading_subquestion`, `writing`. |
| `stem` | string | yes | Question prompt text, preserving source meaning. |
| `options` | object[] or null | conditional | Required for objective choice questions; null otherwise. |
| `answer` | string, string[], object, or null | conditional | Structured answer payload. |
| `explanation` | string or null | conditional | Explanation text or null with status note. |
| `score` | number or null | no | Question score if source-confirmed. |
| `difficulty` | string or null | no | Optional difficulty label when assigned later by workflow. |
| `knowledge_points` | string[] | no | Optional controlled or freeform knowledge-point tags. |
| `source_span` | object | yes | Start/end trace back to original source. |
| `assets` | object[] | no | Linked images, tables, audio references, or attachment descriptors. |
| `normalization_notes` | string[] | yes | Notes describing normalization decisions or unresolved cleanup issues. |
| `validation_status` | object | yes | Validation result block including pass/warn/fail and unresolved items. |

## Shared Conventions

- ids should be ASCII, lowercase, and hyphen-separated where practical
- preserve original wording in content fields; place cleanup rationale in notes fields
- use `null` for unknown scalar values, never fabricated placeholders
- use explicit uncertainty flags instead of silently dropping ambiguity
- derived labels are allowed only when clearly marked as normalized or inferred

## Uncertainty Convention

When source material is incomplete or unclear:

- keep the best source-faithful text available
- mark the relevant field in `metadata.uncertainty_flags` or question-level notes
- include a short explanation in `normalization_notes` or `provenance.confidence_notes`
- do not convert uncertainty into a confirmed value

## Non-Goals

- no dataset import
- no repository-external reference sync
- no SQL schema
- no execution script
- no automated extractor implementation
