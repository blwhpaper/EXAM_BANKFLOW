# Workflow Validation

## Purpose

`workflow/validation/` is the home for validation notes, command interfaces, and future lightweight scripts used to check exam cleaning outputs. The directory is part of the harness. It should help agents and human reviewers verify structured outputs without mutating raw exam sources.

This directory does not currently implement a full validator. Until future tasks add scripts, validation evidence must combine non-interactive shell commands and clearly labeled `MANUAL_CHECK` items.

## Validation Command Interface

Future validation commands should follow this shape:

```sh
python3 workflow/validation/validate_exam_output.py --input <structured-output> --schema workflow/schema/QUESTION_RECORD_SCHEMA.yaml
```

Expected behavior:

- non-interactive
- read-only by default
- exit `0` for pass, non-zero for fail
- print concise findings to stdout or stderr
- accept explicit input paths
- avoid network access and heavyweight dependencies
- never rewrite source or output files unless a separate task explicitly authorizes fix mode

## Checks To Cover

Future validators should cover at least:

- schema checks against `workflow/schema/EXAM_DATA_SCHEMA.md` and `workflow/schema/QUESTION_RECORD_SCHEMA.yaml`
- required fields checks for exam records and question records
- source trace checks for `source_file`, `provenance`, and `source_span`
- duplicate `question_id` checks within an output batch and, when practical, against existing repository records
- answer/explanation consistency checks using `validation_status.answer_status` and `validation_status.explanation_status`
- output format checks for markdown, YAML, JSON, review checklist, and export manifest naming
- parent-child consistency checks for `exam_id`, `section_id`, and declared sections
- objective-question option and answer-label checks
- uncertainty marker checks for OCR damage, missing numbers, image/table dependencies, and source conflicts
- forbidden-content checks for fabricated placeholders such as unexplained `unknown`, invented answers, or missing source spans

## Minimum Current Stage

For EXAM-HARNESS-004, use `workflow/validation/MINIMUM_VALIDATION_COMMANDS.md` as the current executable validation surface. Any item that cannot yet be automated must be recorded as `MANUAL_CHECK` in the task closeout or review checklist.
