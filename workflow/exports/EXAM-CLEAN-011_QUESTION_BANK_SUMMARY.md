# EXAM-CLEAN-011 Question Bank Summary

## Task And Source

- task_id: EXAM-CLEAN-011
- task_title: Markdown 汇总导出
- source_task: EXAM-CLEAN-010
- source_record_file: `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl`
- export_file: `workflow/exports/EXAM-CLEAN-011_QUESTION_BANK_SUMMARY.md`
- branch: `task-exam-clean-011-markdown-summary-export`
- scope_note: This export is a human-readable, auditable markdown summary generated from the structured question-bank JSONL only. No question text, options, answers, or schema were changed.

## Data Sources

- `workflow/TASK_STATE.json`
- `workflow/TASK_INDEX.md`
- `workflow/schema/EXAM_DATA_SCHEMA.md`
- `workflow/schema/QUESTION_RECORD_SCHEMA.yaml`
- `workflow/schema/OUTPUT_FORMAT_SPEC.md`
- `workflow/schema/VALIDATION_RULES.md`
- `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl`
- `workflow/cleaning/EXAM-CLEAN-010_STRUCTURED_DATA_INGEST.md`
- `workflow/Task_Closeouts/EXAM-CLEAN-010_Closeout.md`
- `workflow/validation/README.md`
- `workflow/validation/MINIMUM_VALIDATION_COMMANDS.md`

## Summary Counts

- total_records: 8
- reading_records: 3
- writing_records: 5
- manual_review_required_records: 0
- manual_review_status_note: `manual_review=0`

## Section Distribution

| section_type | count |
| --- | ---: |
| reading | 3 |
| writing | 5 |

## Manual Review Records

- manual_review=0
- No records in `workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl` have `manual_review_status=required`.

## Record Summary Table

| question_id | exam_id | section | question_type | source_file | source_question_number | answer | manual_review |
| --- | --- | --- | --- | --- | --- | --- | --- |
| e001-reading-a-q1 | E001 | reading | reading_subquestion | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx` | 1. | A | not_required |
| e001-reading-a-q2 | E001 | reading | reading_subquestion | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx` | 2. | C | not_required |
| e001-reading-a-q3 | E001 | reading | reading_subquestion | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx` | 3. | D | not_required |
| e001-writing-q46 | E001 | writing | writing | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx` | 46. | sample_answer | not_required |
| e001-writing-q47 | E001 | writing | writing | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx` | 47. | sample_answer | not_required |
| e002-writing-q46 | E002 | writing | writing | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx` | 46. | sample_answer | not_required |
| e002-writing-q47 | E002 | writing | writing | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx` | 47. | sample_answer | not_required |
| e010-writing-q76 | E010 | writing | writing | `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/Q_原卷.docx` | 76. | sample_answer | not_required |

## Reading Records

### e001-reading-a-q1

- question_id: e001-reading-a-q1
- exam_id: E001
- section: reading
- question_type: reading_subquestion
- source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
- source_question_number: 1.
- source_page_or_section: `Q_原卷.docx paragraphs 74-110; passage_text from paragraphs 75-95; questions from paragraphs 96-110; QA_解析版.docx answer support paragraphs 111-119`
- answer: A
- manual_review: not_required
- manual_review_note: no manual review needed
- answer_alignment:
  - source_trace_status: confirmed
  - validation_state: pass
  - answer_status: confirmed
  - explanation_status: confirmed
  - uncertainty: []
- passage_link:
  - passage_id: e001-reading-a
  - block_id: e001-reading-a
  - passage_ref: `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl#e001-reading-a`
- question_text: What type of tasks is given special priority to by the committee?
- options:
  - A. Tasks reflecting real-life applications.
  - B. Original tasks with complex descriptions.
  - C. Highly demanding tasks for top participants.
  - D. Tasks closely following past competition patterns.
- answer_source:
  - answer_source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/QA_解析版.docx`
  - locator_type: docx_paragraph
  - paragraph: 111-119
  - excerpt: `【答案】1. A2. C3. D`
- source_span:
  - source_ref: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
  - locator_type: docx_paragraph
  - paragraph: 96-100
  - excerpt: `1. What type of tasks is given special priority to by the committee? A. Tasks reflecting real-life applications.`

### e001-reading-a-q2

- question_id: e001-reading-a-q2
- exam_id: E001
- section: reading
- question_type: reading_subquestion
- source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
- source_question_number: 2.
- source_page_or_section: `Q_原卷.docx paragraphs 74-110; passage_text from paragraphs 75-95; questions from paragraphs 96-110; QA_解析版.docx answer support paragraphs 111-119`
- answer: C
- manual_review: not_required
- manual_review_note: no manual review needed
- answer_alignment:
  - source_trace_status: confirmed
  - validation_state: pass
  - answer_status: confirmed
  - explanation_status: confirmed
  - uncertainty: []
- passage_link:
  - passage_id: e001-reading-a
  - block_id: e001-reading-a
  - passage_ref: `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl#e001-reading-a`
- question_text: What is a must for a task submission?
- options:
  - A. Being encrypted by hand before uploading.
  - B. Applying accessible basic rules of algorithms.
  - C. Being kept from potential IOI 2026 contestants.
  - D. Providing solutions in the author’s native language.
- answer_source:
  - answer_source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/QA_解析版.docx`
  - locator_type: docx_paragraph
  - paragraph: 111-119
  - excerpt: `【答案】1. A2. C3. D`
- source_span:
  - source_ref: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
  - locator_type: docx_paragraph
  - paragraph: 101-105
  - excerpt: `2. What is a must for a task submission? C. Being kept from potential IOI 2026 contestants.`

### e001-reading-a-q3

- question_id: e001-reading-a-q3
- exam_id: E001
- section: reading
- question_type: reading_subquestion
- source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
- source_question_number: 3.
- source_page_or_section: `Q_原卷.docx paragraphs 74-110; passage_text from paragraphs 75-95; questions from paragraphs 96-110; QA_解析版.docx answer support paragraphs 111-119`
- answer: D
- manual_review: not_required
- manual_review_note: no manual review needed
- answer_alignment:
  - source_trace_status: confirmed
  - validation_state: pass
  - answer_status: confirmed
  - explanation_status: confirmed
  - uncertainty: []
- passage_link:
  - passage_id: e001-reading-a
  - block_id: e001-reading-a
  - passage_ref: `workflow/records/EXAM-CLEAN-004_READING_BLOCKS.jsonl#e001-reading-a`
- question_text: What can authors expect after submitting their tasks?
- options:
  - A. Competing in the IOI 2026 event.
  - B. A fully-funded trip to attend IOI 2026.
  - C. Receiving a financial reward from the host.
  - D. Recognition posted on the event’s website.
- answer_source:
  - answer_source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/QA_解析版.docx`
  - locator_type: docx_paragraph
  - paragraph: 111-119
  - excerpt: `【答案】1. A2. C3. D`
- source_span:
  - source_ref: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
  - locator_type: docx_paragraph
  - paragraph: 106-110
  - excerpt: `3. What can authors expect after submitting their tasks? D. Recognition posted on the event’s website.`

## Writing Records

### e001-writing-q46

- question_id: e001-writing-q46
- exam_id: E001
- section: writing
- question_type: writing
- source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
- source_question_number: 46.
- source_page_or_section: `Q_原卷.docx paragraphs 217-227; QA_解析版.docx answer support paragraphs 335-365`
- manual_review: not_required
- manual_review_note: source prompt, sample answer, and explanation support are present in Q/QA paragraph ranges; no manual review needed for this record
- answer_alignment:
  - source_trace_status: READY
  - validation_state: pass
  - answer_status: confirmed
  - explanation_status: confirmed
  - uncertainty: []
- writing_task: 假定你是李华，你和交换生Michael约好周六一起去市图书馆，但因突发状况无法赴约。请你给他写封邮件，内容包括：1.道歉并解释原因；2.提出弥补方案。注意：1.写作词数应为80个左右；2.请按如下格式在答题卡的相应位置作答。Dear Michael, ... Yours, Li Hua
- answer_reference_status: confirmed sample_answer object preserved from JSONL
- answer:

```text
Dear Michael,
I am writing to sincerely apologize that I cannot go with you to the city library this Saturday as planned. Unfortunately, a sudden family situation has come up, and I need to stay at home to help out.
I feel really sorry for the change and any inconvenience it may cause. How about we reschedule our trip to next Saturday? If that doesn’t work for you, please let me know when you are available. I will try my best to adjust.
I look forward to hearing from you.
Yours,
Li Hua
```

- answer_source:
  - answer_source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/QA_解析版.docx`
  - locator_type: docx_paragraph
  - paragraph: 346-352
  - excerpt: `【答案】 Dear Michael, I am writing to sincerely apologize... Yours, Li Hua`
- source_span:
  - source_ref: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
  - locator_type: docx_paragraph
  - paragraph: 217-227
  - excerpt: `46. 假定你是李华，你和交换生Michael约好周六一起去市图书馆，但因突发状况无法赴约。请你给他写封邮件...`

### e001-writing-q47

- question_id: e001-writing-q47
- exam_id: E001
- section: writing
- question_type: writing
- source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
- source_question_number: 47.
- source_page_or_section: `Q_原卷.docx paragraphs 228-240; QA_解析版.docx answer support paragraphs 366-396`
- manual_review: not_required
- manual_review_note: source prompt, continuation openings, sample answer, and explanation support are present in Q/QA paragraph ranges; no manual review needed for this record
- answer_alignment:
  - source_trace_status: READY
  - validation_state: pass
  - answer_status: confirmed
  - explanation_status: confirmed
  - uncertainty: []
- writing_task: 阅读下面材料，根据其内容和所给段落开头语续写两段，使之构成一篇完整的短文。Karachi’s Liaquat Market was filled with the usual afternoon chaos... At that moment, Ahmed determined to help. ... Months later, that young man appeared again, accompanied by his mother.
- answer_reference_status: confirmed sample_answer object preserved from JSONL
- answer:

```text
At that moment, Ahmed determined to help. He looked into the young man’s despairing eyes and thought of his own mother. Without hesitation, he took out a small envelope from under the counter — the day’s earnings. “Here,” he said, placing the money into the man’s trembling hands. “Take this for the medicine. Go quickly.” The man stared, speechless with gratitude, then nodded firmly and rushed out into the busy market.
Months later, that young man appeared again, accompanied by his mother. She walked slowly but with a warm smile, with her health visibly improved. The young man, now neatly dressed, held out Ahmed’s envelope — now thicker with added notes. “Because of you, my mother is well,” he said. Ahmed tried to refuse the extra money, but the man insisted gently, “Please, let this also help someone else.” As they left, Zara waved goodbye, her sun drawing now bright with color. Ahmed watched them go, understanding that the truest wealth is not in money, but in the moment one heart chooses to light another’s way.
```

- answer_source:
  - answer_source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/QA_解析版.docx`
  - locator_type: docx_paragraph
  - paragraph: 379-380
  - excerpt: `【答案】 At that moment, Ahmed determined to help... Months later, that young man appeared again...`
- source_span:
  - source_ref: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E001_2025_河南开封市_期末_高三_英语/Q_原卷.docx`
  - locator_type: docx_paragraph
  - paragraph: 228-240
  - excerpt: `47. 阅读下面材料，根据其内容和所给段落开头语续写两段... At that moment, Ahmed determined to help. Months later...`

### e002-writing-q46

- question_id: e002-writing-q46
- exam_id: E002
- section: writing
- question_type: writing
- source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx`
- source_question_number: 46.
- source_page_or_section: `Q_原卷.docx paragraphs 204-214; QA_解析版.docx answer support paragraphs 321-350`
- manual_review: not_required
- manual_review_note: source prompt, sample answer, and explanation support are present in Q/QA paragraph ranges; no manual review needed for this record
- answer_alignment:
  - source_trace_status: READY
  - validation_state: pass
  - answer_status: confirmed
  - explanation_status: confirmed
  - uncertainty: []
- writing_task: 假定你是李华，上周六你校举办了校园科技小发明展示活动。请你给美国朋友Tom 写一封邮件分享这次经历，内容包括：1．展示活动现场情况；2．你的感受。注意：1.写作词数应为80个左右；2．请按如下格式在答题卡的相应位置作答。Dear Tom, ... Yours, Li Hua
- answer_reference_status: confirmed sample_answer object preserved from JSONL
- answer:

```text
Dear Tom,
I’m writing to share an exciting experience with you. Last Saturday, our school held a campus science and technology invention show.
The show was wonderful. Many students showed their small inventions, such as a smart flower pot and a portable book light. Teachers and students walked around, asking questions and praising the great ideas. I was deeply impressed by my classmates’ creativity and hard work.
This show not only made me more interested in science but also let me know the importance of practice. I hope we can have such activities together someday.
Yours,
Li Hua
```

- answer_source:
  - answer_source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/QA_解析版.docx`
  - locator_type: docx_paragraph
  - paragraph: 332-337
  - excerpt: `【答案】Dear Tom, I’m writing to share an exciting experience with you... Yours, Li Hua`
- source_span:
  - source_ref: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx`
  - locator_type: docx_paragraph
  - paragraph: 204-214
  - excerpt: `46. 假定你是李华，上周六你校举办了校园科技小发明展示活动。请你给美国朋友Tom写一封邮件...`

### e002-writing-q47

- question_id: e002-writing-q47
- exam_id: E002
- section: writing
- question_type: writing
- source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx`
- source_question_number: 47.
- source_page_or_section: `Q_原卷.docx paragraphs 215-227; QA_解析版.docx answer support paragraphs 351-381`
- manual_review: not_required
- manual_review_note: source prompt, continuation openings, sample answer, and explanation support are present in Q/QA paragraph ranges; no manual review needed for this record
- answer_alignment:
  - source_trace_status: READY
  - validation_state: pass
  - answer_status: confirmed
  - explanation_status: confirmed
  - uncertainty: []
- writing_task: 阅读下面材料，根据其内容和所给段落开头语续写两段，使之构成一篇完整的短文。Lily and Emma sat behind their table at the community square... Lily stared in shock. ... When the fair ended, they raised $200 for the shelter.
- answer_reference_status: confirmed sample_answer object preserved from JSONL
- answer:

```text
Lily stared in shock. She couldn’t believe someone liked her lopsided cat keychain. The little girl’s mum smiled and paid for it, praising the unique design. Encouraged by this, Lily’s eyes lit up and her hands stopped shaking. She and Emma worked together smoothly after that — Lily drew cute doodles on wooden crafts while Emma made delicate paper flowers, and their booth soon attracted more people. Kids loved Lily’s funny and warm drawings, and many adults bought them as small gifts. Lily no longer felt discouraged, her heart filled with joy and confidence.
When the fair ended, they raised $200 for the shelter. The two girls hugged each other excitedly, proud of what they had achieved together. They took the money to the local animal shelter the next day, where they saw cute homeless cats and dogs. The staff thanked them warmly, saying the money would buy food and toys for the pets. Lily looked at her remaining wooden crafts and smiled, knowing her imperfect drawings could bring warmth and help to others. She realized that everyone has their own strengths, and working together makes kindness more powerful.
```

- answer_source:
  - answer_source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/QA_解析版.docx`
  - locator_type: docx_paragraph
  - paragraph: 364-365
  - excerpt: `【答案】 Lily stared in shock... When the fair ended, they raised $200 for the shelter...`
- source_span:
  - source_ref: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E002_2025_河南2月测评_期末_高三_英语/Q_原卷.docx`
  - locator_type: docx_paragraph
  - paragraph: 215-227
  - excerpt: `47. 阅读下面材料，根据其内容和所给段落开头语续写两段... Lily stared in shock. When the fair ended...`

### e010-writing-q76

- question_id: e010-writing-q76
- exam_id: E010
- section: writing
- question_type: writing
- source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/Q_原卷.docx`
- source_question_number: 76.
- source_page_or_section: `Q_原卷.docx paragraphs 252-260; QA_解析版.docx answer support paragraphs 459-485`
- manual_review: not_required
- manual_review_note: source prompt, sample answer, and explanation support are present in Q/QA paragraph ranges; previous E010 table/media risk does not affect this visible writing prompt record
- answer_alignment:
  - source_trace_status: READY
  - validation_state: pass
  - answer_status: confirmed
  - explanation_status: confirmed
  - uncertainty: []
- writing_task: 假定你是国际学校学生李华，校英文报正在组织“AI赋能高中体育选修课”创意提案征集活动。请以此为主题写一篇短文投稿。内容包括：（1）你的提案及理由；（2）预期效果。注意:（1）写作词数应为80个左右；（2）请在答题纸的相应位置作答。Proposal for AI-empowered PE Elective Courses
- answer_reference_status: confirmed sample_answer object preserved from JSONL
- answer:

```text
Proposal for AI-empowered PE Elective Courses
As a student passionate about innovation, I propose integrating AI into PE electives. My suggestion is to develop an AI system that designs personalized training plans based on students’ fitness levels and tracks their progress through wearable devices.
Traditional PE classes often adopt a “one-size-fits-all” approach, which may not suit everyone. AI can analyze individual data to create tailored exercises, ensuring safer and more effective workouts. It also provides instant feedback to correct movements, reducing injury risks.
This approach will improve overall fitness and help students build sustainable exercise habits. Let’s embrace AI to make PE smarter and healthier!
```

- answer_source:
  - answer_source_file: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/QA_解析版.docx`
  - locator_type: docx_paragraph
  - paragraph: 468-472
  - excerpt: `【答案】 Proposal for AI-empowered PE Elective Courses As a student passionate about innovation...`
- source_span:
  - source_ref: `datasets/2026_quyixian_english/_STANDARDIZED_EXAMS/E010_2025_福建厦门双十中学_开学考_高三_英语/Q_原卷.docx`
  - locator_type: docx_paragraph
  - paragraph: 252-260
  - excerpt: `76. 假定你是国际学校学生李华，校英文报正在组织“AI赋能高中体育选修课”创意提案征集活动...`
