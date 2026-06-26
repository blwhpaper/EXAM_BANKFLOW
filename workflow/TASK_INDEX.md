# EXAM_BANKFLOW Task Index

## Execution Order

- First complete `Phase 0｜Harness & Context Engineering`
- Then complete `Phase 1｜Exam Cleaning Pipeline`
- Then enter `Phase 2 / EXAM-BANK`

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
| EXAM-CLEAN-015 | 人工复核与错误回修 | DONE |

Phase 1 已闭环。Phase 1 产物是首批题库清洗样板与验证链，不是完整题库系统。

## Phase 2 / EXAM-BANK

Phase 2 目标：建设可检索、可组题、可导出的高考英语题库系统，并支持未来新增题目的增量入库机制。

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-BOOT-001 | Phase 2 路线图与任务索引入壳 | DONE |

### Phase 2A｜CORE：题库底座

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-CORE-001 | 全量源文件与题型覆盖审计 | TODO |
| EXAM-BANK-CORE-002 | 题库 Schema v2：source / task / item / tag 四层结构 | TODO |
| EXAM-BANK-CORE-003 | 题库状态流：raw_detected -> ready_for_selection | TODO |
| EXAM-BANK-CORE-004 | 题型插件接口：reading / cloze / grammar / writing | TODO |

### Phase 2B｜READING-MVP：阅读题库可用版

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-READING-001 | 阅读理解全量抽取入库：passage + question + options + answers | TODO |
| EXAM-BANK-READING-002 | 阅读答案对齐与 source trace 校验 | TODO |
| EXAM-BANK-READING-003 | 阅读一级标签：细节 / 词汇 / 主旨 / 推理 | TODO |
| EXAM-BANK-READING-004 | 阅读题库 QA：缺项、错位、标签异常、答案异常 | TODO |
| EXAM-BANK-READING-005 | 阅读题库 Release v1：ready_for_selection 冻结 | TODO |

### Phase 2C｜READING-ADVANCED：阅读细分标签

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-READING-006 | 阅读二级标签规范：定义、边界、例题、反例 | TODO |
| EXAM-BANK-READING-007 | 阅读二级标签试标与规则修订 | TODO |
| EXAM-BANK-READING-008 | 阅读二级标签批量补全 | TODO |
| EXAM-BANK-READING-009 | 阅读二级标签 QA 与冲突修复 | TODO |
| EXAM-BANK-READING-010 | 阅读题库 Release v2：细分标签冻结 | TODO |

### Phase 2D｜READING-USE：阅读检索与专项组题

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-QUERY-001 | Reading Index v1 | TODO |
| EXAM-BANK-QUERY-002 | Reading Query CLI v1 | TODO |
| EXAM-BANK-BUILDER-001 | Reading Set Builder：按四大类与二级标签组题 | TODO |
| EXAM-BANK-EXPORT-001 | Reading Export Pack：学生版 / 教师版 / 答案版 / 标签报告 | TODO |

### Phase 2E｜CLOZE：完形填空题库

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-CLOZE-001 | 完形填空全量抽取入库：passage + blanks + options + answers | TODO |
| EXAM-BANK-CLOZE-002 | 完形答案对齐与 source trace 校验 | TODO |
| EXAM-BANK-CLOZE-003 | 完形语言点一级标签 | TODO |
| EXAM-BANK-CLOZE-004 | 完形 QA 与 Release v1 | TODO |
| EXAM-BANK-CLOZE-005 | Cloze Query & Set Builder | TODO |

### Phase 2F｜GRAMMAR：语法填空题库

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-GRAMMAR-001 | 语法填空全量抽取入库：passage + blanks + answers | TODO |
| EXAM-BANK-GRAMMAR-002 | 语法填空答案对齐与 source trace 校验 | TODO |
| EXAM-BANK-GRAMMAR-003 | 语法点标签：非谓语 / 从句 / 时态语态 / 词性转换等 | TODO |
| EXAM-BANK-GRAMMAR-004 | 语法填空 QA 与 Release v1 | TODO |
| EXAM-BANK-GRAMMAR-005 | Grammar Query & Set Builder | TODO |

### Phase 2G｜WRITING：写作题库

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-WRITING-001 | 应用文写作全量入库：genre / scenario / purpose / requirements | TODO |
| EXAM-BANK-WRITING-002 | 读后续写全量入库：given text / characters / conflict / openings | TODO |
| EXAM-BANK-WRITING-003 | 写作任务标签：体裁、主题、能力点、训练目标 | TODO |
| EXAM-BANK-WRITING-004 | 写作 QA 与 Release v1 | TODO |
| EXAM-BANK-WRITING-005 | Writing Query & Task Pack Builder | TODO |

### Phase 2H｜MASTER：统一索引与综合组卷

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-MASTER-001 | Master Index v1：阅读 / 完形 / 语法 / 写作统一索引 | TODO |
| EXAM-BANK-MASTER-002 | Global Query CLI：跨题型检索 | TODO |
| EXAM-BANK-MASTER-003 | Exam Paper Builder：综合训练卷组卷器 | TODO |
| EXAM-BANK-MASTER-004 | Master Export Pack：Word / Markdown / Excel 全格式导出 | TODO |

### Phase 2I｜QA-RELEASE：质量控制与发布

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-QA-001 | 重复题与相似题检测 | TODO |
| EXAM-BANK-QA-002 | 难度、主题、体裁标签补全 | TODO |
| EXAM-BANK-QA-003 | 答案解析绑定：原解析优先，AI 解析需标记 | TODO |
| EXAM-BANK-QA-004 | 人工复核队列与返修机制 | TODO |
| EXAM-BANK-QA-005 | 题库系统 Final Review Package | TODO |
| EXAM-BANK-QA-006 | Phase 2 总验收 closeout | TODO |

### Phase 2J｜INGEST：新增题目增量入库机制

| ID | Task | Status |
|---|---|---|
| EXAM-BANK-INGEST-001 | 新增题源投递区与 batch manifest 规范 | TODO |
| EXAM-BANK-INGEST-002 | 新增题源自动盘点与题型识别 | TODO |
| EXAM-BANK-INGEST-003 | 新增题目增量抽取 Pipeline | TODO |
| EXAM-BANK-INGEST-004 | 新增题目答案对齐、标签与 QA Pipeline | TODO |
| EXAM-BANK-INGEST-005 | 新增题目合并入 Released Bank 与 Master Index | TODO |
| EXAM-BANK-INGEST-006 | 新增题目 Release closeout 与版本记录 | TODO |

当前下一任务：`EXAM-BANK-CORE-001`。
