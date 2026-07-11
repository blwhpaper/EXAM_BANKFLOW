# EXAM_BANKFLOW Agent 操作规范

## Word导出规则（雷打不动）

任何agent导出Word文档时，必须调用 `scripts/export.py`，禁止自行编写格式代码。

### 调用方式
```bash
# 单卷完形填空
python scripts/export.py --type cloze --exam E005 --out output.docx

# 全部完形填空
python scripts/export.py --type cloze --out output.docx

# 七选五
python scripts/export.py --type reading_7to5 --exam E005 --out output.docx

# 细分类别（只附excerpt片段）
python scripts/export.py --type cloze --subtype cloze_lexical --out output.docx
```

### 禁止事项
- 禁止在调用时修改任何格式参数
- 禁止自行用python-docx或其他库另写导出逻辑
- 格式修改必须改 `scripts/export.py` 本身，改后同步更新 `specs/export_reference.py`

## 数据层规则

- `passage_text_verified=True` 的记录禁止覆盖
- 运行 `enrich_cloze_passage.py --force` 前确认不会影响verified记录
- 阅读理解原文尚未补全，暂不支持导出附原文

## 阅读理解 passage_text 补全规则

- 脚本：`scripts/enrich_reading_passage.py`
- 篇章识别：显式标签行（`^[A-D]\.?$`）或隐式首篇（`阅读下列短文`/`阅读下面短文` 后直接开始）
- 跳过条件：`options` 少于 4 个、`passage_text_verified=True`、`data_quality="dirty"`
- `options=None` 的记录属于上游清洗缺失，标记待修复，不强行提取
