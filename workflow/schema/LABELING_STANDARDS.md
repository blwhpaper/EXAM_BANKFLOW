# 标注判定标准文档

## 用途
本文档是 EXAM_BANKFLOW 打标的唯一标准依据。
`auto_label.py` 和所有人工标注均以此为准，确保跨会话、跨agent口径一致。
最后更新：2026-07

---

## 一、完形填空 strategy 判定标准

每道完形填空题标注一个 strategy 值。

### logic_relation（逻辑关系）
**判定**：空格词是上下文事件或动作的逻辑结果，需要根据因果、条件、目的等逻辑关系推断。
**特征**：
- 选项多为名词或动词
- 去掉空格后句子逻辑链断裂
- 通常有 so/therefore/as a result/because 等逻辑词，或隐含逻辑关系

**典型例**：
> But she did, and this ____22____ set off an amazing event...
> 选项：decision / hobby / intention / response → 答案 decision（逻辑结果）

---

### context_clue（上下文线索）
**判定**：同段或紧邻句子中有明确的线索词或释义，可直接对应正确选项。
**特征**：
- 原文某处出现与答案同义、近义或解释性的词语
- 线索词和空格词之间有明显呼应关系

**典型例**：
> Betty ____28____ the dog got to safety, they carefully placed her inside their boat.
> 上文已说 noticed the dog → ensure（确保）是上下文给出的逻辑线索

---

### word_discrimination（词义辨析）
**判定**：四个选项语义相近，需细辨差别才能选出最准确的一个。
**特征**：
- 选项属于同一语义场（如都是"获得"类动词，或都是表情感的形容词）
- 不靠逻辑推断，靠词义精确度

**典型例**：
> What a lovely ____34____!
> 选项：animal / boating / reunion / couple → 需辨析哪个词最贴切

---

### action_chain（动作链）
**判定**：空格处是一系列连续动作或事件中的一环，选项是动作、状态词或方式副词。
**特征**：
- 前后文描述了一系列按时间或逻辑顺序展开的动作
- 空格词是其中一个动作节点

**典型例**：
> his mom said ____51____
> 前文动作链：发现乱→质问→说话方式 → gently/firmly 是动作链中的方式环节

---

### emotion_line（情感线）
**判定**：空格处填情感、心理状态、性格评价或情绪反应词。
**特征**：
- 选项均为情感类、心理类或性格类词汇
- 需根据人物处境或故事情节判断情感走向

**典型例**：
> It would have been ____21____ if she didn't feel like participating...
> 选项：funny / strange / wrong / reasonable → 填情感评价词

---

### collocation（固定搭配）
**判定**：答案由固定搭配或词语惯用法决定，换其他选项搭配不成立。
**特征**：
- 选项语义相近，但只有一个能与前后词构成固定搭配
- 通常涉及动词+名词、形容词+名词、动词+介词等固定组合

**典型例**：
> I became ____21____ with an old lady
> engaged in / familiar with / satisfied with → familiar with 是固定搭配

---

## 二、七选五 solution_methods 判定标准

每道七选五题可标注一个或多个 solution_methods 值（数组）。

### pronoun（代词复现）
**判定**：空格前后出现代词（they/them/it/this/these等），正确选项中含与该代词对应的先行词或所指对象。
**特征**：
- 填入选项后，代词指向明确
- 去掉选项后代词指向不明

---

### parallel_contrast（平行对比）
**判定**：空格处的选项与后文（或前文）形成平行结构或转折对比关系。
**特征**：
- 前后有 but/however/while/on the other hand 等对比词，或 and/also/similarly 等并列词
- 选项在结构上与对比/并列对象对称

---

### imperative（祈使句）
**判定**：空格后紧跟祈使句（动词原形开头），或选项本身是祈使结构的小标题。
**特征**：
- 文章为建议/指导类文体
- 每段由一个祈使句小标题引领

---

### parallel_also（also平行）
**判定**：空格后的句子含 also/likewise/similarly，选项与 also 后的内容并列。
**特征**：
- also 后内容是已知信息
- 选项提供与之并列的另一个信息

---

### rhetoric_structure（修辞结构）
**判定**：空格处是设问句或反问句，引出后文的解释、回答或展开。
**特征**：
- 选项通常以疑问句形式出现
- 后文直接回答或解释该问题

---

### summary（总结句）
**判定**：空格处是段落或全文的总结句，概括上文或下文主旨。
**特征**：
- 选项语义覆盖面广，能统领一段或多段内容
- 通常位于段首或段尾

---

## 三、边界情况处理原则

1. **完形填空**：一题只标一个 strategy，选最主要的判断依据
2. **七选五**：可标多个 solution_methods，凡是有效解题依据均标注
3. **无法判断**：strategy 填 `null`，solution_methods 填 `[]`，不强行归类
4. **新增类别**：须先在此文档补充判定标准，再批量打标

---

## 四、auto_label.py 调用规范

- 输入：待标注记录的 JSONL
- 输出：补全 strategy/solution_methods 字段后的 JSONL
- 大批量（>100条）先抽20条试跑，人工确认口径后再全量
- 每次打标后记录：处理条数、各类别分布、uncertain条数

---

## 五、待修复数据记录

### 七选五 source_span.paragraph 标注有误（需人工修正）
| exam_id | 问题描述 |
|---|---|
| E016 | source_span.paragraph 未指向七选五section，enrich_7to5_passage.py无法自动提取 |
| E021 | 同上 |
| E041 | 同上，paragraph指向阅读理解题位置 |

修正方法：手动查原始docx，找到七选五section的起始paragraph编号，更新JSONL对应记录的source_span.paragraph字段。

### question_text 内容错误
| question_id | 问题描述 |
|---|---|
| e006-7to5-q18 | question_text混入文章标题和正文内容，需重新提取 |

### passage_text 空白格式异常（纯数字，无下划线）
| exam_id | 问题描述 |
|---|---|
| E009 | passage_text空白格式为纯数字（如 `   36   `），缺少下划线，导致段落定位失败；answer全为null |
| E030 | 同上，passage_text空白为纯数字格式 |
| E054 | 同上，passage_text空白为纯数字格式 |

修正方法：在enrich_7to5_passage.py中加规范化步骤，将 `\s{2,}(\d{2})\s{2,}` 替换为 `____\1____`，或手动修正这3个exam的passage_text。
