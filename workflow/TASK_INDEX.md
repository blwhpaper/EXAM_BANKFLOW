# EXAM_BANKFLOW Task Index

## Execution Order

- First complete `Phase 0｜Harness & Context Engineering`
- Then enter `Phase 1｜Exam Cleaning Pipeline`

## Current Dataset

- `datasets/2026_quyixian_english`

## Phase 0｜Harness & Context Engineering

| ID | Task | Status |
|---|---|---|
| EXAM-HARNESS-000 | Top 5 参考仓库本地审计与模式提炼 | DONE |
| EXAM-HARNESS-001 | 基于审计结果落盘轻量 harness 骨架 | DONE |
| EXAM-HARNESS-002 | 建立任务模板、状态模板与交接模板 | DONE |
| EXAM-HARNESS-003 | 建立题库数据 schema 与输出格式规范 | DONE |
| EXAM-HARNESS-004 | 建立 Codex/Claude/GPT 开工规则与验收规则 | DONE |

## Phase 1｜Exam Cleaning Pipeline

| ID | Task | Status |
|---|---|---|
| EXAM-CLEAN-001 | 首批试卷清洗范围定义与执行边界落盘 | DONE |
| EXAM-CLEAN-002 | input inventory and source trace | DONE |
| EXAM-CLEAN-003 | 题型边界识别与切分 | DONE |
| EXAM-CLEAN-004 | 阅读理解结构化抽取 | DONE |
| EXAM-CLEAN-005 | 阅读理解记录规范化与选项完整性修复 | DONE |
| EXAM-CLEAN-006 | question records 入库结构试切片 | DONE |
| EXAM-CLEAN-007 | question records validation hardening | DONE |
| EXAM-CLEAN-008 | 写作题结构化抽取 | DONE |
| EXAM-CLEAN-008A | standardized Word source recovery | DONE |
| EXAM-CLEAN-008B | manual source placement verification | DONE |
| EXAM-CLEAN-008C | post-retry task pointer repair | DONE |
| EXAM-CLEAN-009 | 答案对齐 | DONE |
| EXAM-CLEAN-010 | 结构化数据入库 | DONE |
| EXAM-CLEAN-011 | Markdown 汇总导出 | DONE |
| EXAM-CLEAN-012 | Word 汇总导出 | DONE |
| EXAM-CLEAN-013 | 人工复核 QA | DONE |
| EXAM-CLEAN-014 | Excel 总索引 | DONE |
| EXAM-CLEAN-015 | 人工复核与错误回修 | TODO |
