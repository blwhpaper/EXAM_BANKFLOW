# Phase 2 / EXAM-BANK Roadmap

## 1. Phase 2 总目标

Phase 2 builds a searchable, selectable, and exportable Gaokao English question-bank system from the accepted Phase 1 cleaning assets and future approved sources.

The system must support:

- stable source trace from every released item back to source material
- type-specific extraction and QA for reading, cloze, grammar, and writing
- released records that can be indexed for retrieval and selection
- task-set and exam-paper assembly after records are released
- export packs for student, teacher, answer, tag, and index views
- incremental intake for future new questions through Phase 2J / INGEST

## 2. Phase 2 与 Phase 1 的边界

Phase 1 produced the first cleaned sample records, validation chain, exports, and review package. It proved the cleaning and review path, but it is not the complete question-bank product.

Phase 2 starts after Phase 1 closeout and owns the bank architecture, full-type expansion, release workflow, indexing, selection, export, and incremental ingest mechanism.

Phase 2 may read Phase 1 outputs as reference inputs in later tasks, but Phase 2 boot work does not alter those outputs.

## 3. Phase 2 不做什么

Phase 2 boot and roadmap work must not:

- extract new reading, cloze, grammar, or writing records
- modify existing released or sample question-bank records
- regenerate existing Phase 1 exports
- bypass answer alignment, QA, or release gates
- implement query, builder, or export code before the relevant tasks
- write newly added questions directly into released records
- expand Phase 3 into an execution queue

## 4. 数据层级原则

The Phase 2 data model is organized in four layers:

- `source`: the provenance-bearing file, paper, answer key, batch, or submitted source unit.
- `task-or-passage`: the section-level work unit, such as a reading passage, cloze passage, grammar passage, writing prompt, or source task.
- `item-or-question`: the selectable question, blank, prompt, or scoring target.
- `tag`: the controlled labels used for retrieval, QA, selection, difficulty, theme, genre, ability, and release reporting.

Records must preserve parent-child links across these layers. A selectable item must not lose its source or task/passage context.

## 5. 状态流原则

Every source, task/passage, and item/question moves through an auditable status flow:

`raw_detected` -> `inventoried` -> `type_detected` -> `extracted` -> `answer_aligned` -> `tagged_major` -> `tagged_minor_optional` -> `qa_passed` -> `released` -> `indexed` -> `ready_for_selection`

No item can be selected for builders before `ready_for_selection`. Any exception must be recorded in QA and closeout evidence.

## 6. 阅读理解原则

Reading comprehension uses a passage/question two-layer structure:

- passage layer: source trace, text, metadata, theme, genre, difficulty, and passage-level tags
- question layer: stem, options, answer, source trace, major tag, optional minor tag, and QA status

一级标签先行. The first stable reading tags are `细节`, `词汇`, `主旨`, and `推理`.

二级标签逐步细化. Minor tags are defined, tested, revised, then batch-filled only after Phase 2B produces a released reading MVP.

## 7. 未来新增题原则

New questions must not be written directly into released records.

All future additions must enter through:

1. inbox submission area
2. batch manifest
3. ingest inventory
4. type detection
5. extraction pipeline
6. answer alignment
7. tagging
8. QA
9. release approval
10. merge into released bank and master index

Phase 2J / INGEST owns this mechanism and its closeout/version records.

## 8. 完整 Phase 2 阶段列表

- Phase 2A｜CORE
- Phase 2B｜READING-MVP
- Phase 2C｜READING-ADVANCED
- Phase 2D｜READING-USE
- Phase 2E｜CLOZE
- Phase 2F｜GRAMMAR
- Phase 2G｜WRITING
- Phase 2H｜MASTER
- Phase 2I｜QA-RELEASE
- Phase 2J｜INGEST

## 9. 每个阶段下的完整任务列表

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

## 10. 第一批执行顺序

1. `EXAM-BANK-CORE-001`
2. `EXAM-BANK-CORE-002`
3. `EXAM-BANK-CORE-003`
4. `EXAM-BANK-CORE-004`
5. `EXAM-BANK-READING-001`

The immediate next task is `EXAM-BANK-CORE-001`.

## 11. 防漂移规则

- One active task at a time.
- Read `workflow/TASK_STATE.json`, `workflow/TASK_INDEX.md`, and this Phase 2 roadmap before edits.
- Do not mutate existing question-bank records unless the active task explicitly authorizes it.
- Do not create released records without source trace, answer alignment, QA evidence, and release status.
- Do not let query, builder, or export tasks consume unreleased records.
- Do not write new incoming questions directly into released records.
- Do not expand Phase 3 tasks during Phase 2 execution.
- Close out every task before advancing `current_task` or `next_task`.

## 12. 验收口径

Phase 2 boot acceptance requires:

- `workflow/context/PHASE_2_EXAM_BANK.md` exists and includes Phase 2A through Phase 2J.
- `workflow/TASK_INDEX.md` keeps Phase 0 and Phase 1 completed records and adds Phase 2 tasks.
- `EXAM-BANK-BOOT-001` is marked `DONE`.
- all Phase 2 roadmap tasks after boot are marked `TODO`.
- `workflow/TASK_STATE.json` points to `EXAM-BANK-CORE-001`.
- no existing question-bank records or exports are changed.
- required validation commands pass and are recorded in closeout.
