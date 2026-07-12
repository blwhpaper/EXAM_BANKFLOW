#!/usr/bin/env python3
"""
enrich_7to5_passage.py
为 section_type=reading_7to5 的记录从原始 docx 重新提取 passage_text，
保留段落结构（段落间用 \n 分隔）。

source_span.paragraph 指向七选五 section header（0-indexed），
脚本从该段落向下扫描，跳过指令行，提取文章正文直到遇到 A-G 选项行。

用法：
  python scripts/enrich_7to5_passage.py --exam E006 --dry-run   # 验证单场
  python scripts/enrich_7to5_passage.py                          # 全量运行
  python scripts/enrich_7to5_passage.py --force                  # 强制覆盖已有
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from docx import Document

PROJECT_ROOT = Path(__file__).resolve().parent.parent
JSONL_PATH   = PROJECT_ROOT / "workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl"

# 章节标题：跳过不纳入正文
_SECTION_HEADER = re.compile(
    r'^(第[一二三四五六七八九十百\d]+[节部分题]|'
    r'[A-G]\s*Section|'
    r'语言运用|写作|书面表达|听力|注意事项)'
)

# 七选五前的指令行：跳过
_INSTRUCTION = re.compile(
    r'阅读下面短文|从短文后的选项|选出可以填入|选项中有两项为多余'
)

# A-G 选项行（七选五备选句）：遇到即停止采集文章
_7TO5_OPTION = re.compile(r'^[A-G][\.．]\s*\S')

# 阅读理解选项行（A-D 四选一）：遇到也停止（上文阅读溢出）
_READING_OPTION = re.compile(r'^\d+[\.\s]\s*[A-D][\.．\s]')


def load_records(jsonl_path: Path) -> list[dict]:
    records = []
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def extract_7to5_passage(docx_path: Path, section_para: int) -> str:
    """
    从 section_para（0-indexed）向下扫描，找到七选五指令行后再采集文章段落，
    遇到 A-G 选项行或下一个章节 header 停止。

    两阶段策略：
    1. 预热阶段：从 section_para 开始，扫描至多 10 行找到 section header 或指令行
    2. 采集阶段：跳过指令行后的段落即为正文，遇 A-G 选项停止

    返回用 \\n 连接的段落文本，若未找到七选五入口则返回空串。
    """
    doc = Document(str(docx_path))
    paras = doc.paragraphs

    # 阶段 1：找七选五入口（section header 或指令行）
    entry_found = False
    i = section_para
    limit = min(section_para + 15, len(paras))
    while i < limit:
        t = paras[i].text.strip()
        i += 1
        if not t:
            continue
        if _SECTION_HEADER.match(t) or _INSTRUCTION.search(t):
            entry_found = True
            break

    if not entry_found:
        return ""

    # 阶段 2：采集正文段落
    texts = []
    while i < len(paras):
        t = paras[i].text.strip()
        i += 1

        if not t:
            continue

        # 遇到 A-G 选项 → 文章结束
        if _7TO5_OPTION.match(t):
            break

        # 遇到阅读理解 A-D 选项 → 已进入别的 section，停止
        if _READING_OPTION.match(t):
            break

        # 下一个章节 header → 停止
        if _SECTION_HEADER.match(t):
            break

        # 指令行继续跳过（可能有多行指令）
        if _INSTRUCTION.search(t):
            continue

        texts.append(t)

    return "\n".join(texts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exam", help="只处理指定 exam_id（测试用）")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅打印提取结果，不写入文件")
    parser.add_argument("--force", action="store_true",
                        help="强制重提取，忽略已有 passage_text")
    args = parser.parse_args()

    records = load_records(JSONL_PATH)

    # 筛选七选五记录（跳过 dirty 数据）
    target = [r for r in records
              if r.get("section_type") == "reading_7to5"
              and r.get("data_quality") != "dirty"]
    if args.exam:
        target = [r for r in target if r.get("exam_id") == args.exam]

    print(f"待处理 reading_7to5 记录：{len(target)} 条", flush=True)

    # 按 (exam_id, source_file, paragraph) 分组 —— 同一 paragraph = 同一篇文章
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in target:
        span = r.get("source_span", {})
        key = (r["exam_id"], r.get("source_file", ""), span.get("paragraph", ""))
        groups[key].append(r)

    print(f"分组数（exam_id + source_file + paragraph）：{len(groups)}", flush=True)

    id_to_record: dict[str, dict] = {r["question_id"]: r for r in records}

    updated = 0
    skipped = 0
    errors  = 0

    for (exam_id, source_file, para_str), group in sorted(groups.items()):
        # 人工校对过的跳过
        if any(r.get("passage_text_verified") for r in group):
            skipped += len(group)
            continue

        # 已全部有 passage_text 且未强制覆盖则跳过
        if not args.force and all(r.get("passage_text") for r in group):
            skipped += len(group)
            continue

        # 解析 section paragraph（0-indexed）
        try:
            section_para = int(para_str)
        except (ValueError, TypeError) as e:
            print(f"  [跳过] {exam_id}: paragraph 解析失败 ({e})")
            errors += len(group)
            continue

        # 定位 docx
        docx_abs = PROJECT_ROOT / source_file
        if not docx_abs.exists():
            print(f"  [跳过] {exam_id}: 文件不存在 {docx_abs}")
            errors += len(group)
            continue

        # 提取文章
        try:
            passage = extract_7to5_passage(docx_abs, section_para)
        except Exception as e:
            print(f"  [错误] {exam_id} 提取失败: {e}")
            errors += len(group)
            continue

        if not passage:
            print(f"  [警告] {exam_id} para={section_para}: 提取结果为空，跳过")
            errors += len(group)
            continue

        para_count = passage.count("\n") + 1
        print(f"\n{'='*60}")
        print(f"exam_id  : {exam_id}")
        print(f"文件     : {Path(source_file).name}")
        print(f"起始段落 : {section_para}  ({len(group)} 道题)")
        print(f"段落数   : {para_count}")
        print(f"提取正文↓\n{passage}\n")

        if args.dry_run:
            continue

        for r in group:
            if args.force or not r.get("passage_text"):
                id_to_record[r["question_id"]]["passage_text"] = passage
                updated += 1
            else:
                skipped += 1

    if args.dry_run:
        print("\n[dry-run 模式，不写入文件]")
        return

    if updated == 0:
        print("\n没有需要更新的记录，文件未修改。")
        return

    # 原子写回
    tmp = JSONL_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(JSONL_PATH)

    print(f"\n完成：已更新 {updated} 条，跳过 {skipped} 条，失败 {errors} 条")
    print(f"文件已写回：{JSONL_PATH}")


if __name__ == "__main__":
    main()
