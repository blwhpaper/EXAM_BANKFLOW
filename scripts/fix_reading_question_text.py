#!/usr/bin/env python3
"""
fix_reading_question_text.py
从原始 docx 重新提取阅读理解的 question_text 和 options。

只处理疑似脏数据（question_text 长度>300 或混入选项格式）。
source_span.paragraph 指向题干所在段落（0-indexed）。

用法：
  python scripts/fix_reading_question_text.py --exam E006 --dry-run
  python scripts/fix_reading_question_text.py
  python scripts/fix_reading_question_text.py --force   # 覆盖所有 reading 记录
"""

import argparse
import json
import re
import sys
from pathlib import Path

from docx import Document

PROJECT_ROOT = Path(__file__).resolve().parent.parent
JSONL_PATH   = PROJECT_ROOT / "workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl"

# 选项行：A. xxx B. xxx（紧凑）或 A. xxx（单独一行）
_OPT_INLINE = re.compile(
    r'([A-D])[\.．]\s*(.+?)\s{2,}([B-D])[\.．]\s*(.+?)(?:\s{2,}([C-D])[\.．]\s*(.+?)(?:\s{2,}([D])[\.．]\s*(.+?))?)?$'
)
_OPT_SINGLE = re.compile(r'^([A-D])[\.．]\s*(.+)$')

# 停止条件
_NEXT_QNUM  = re.compile(r'^\d{1,2}[\.．]\s*\S')   # 下一题题号
_ANSWER_ONLY = re.compile(r'^[A-G]$')               # 单字母答案行
_NEW_SECTION = re.compile(
    r'^(第[一二三四五六七八九十百\d]+[节部分题]|'
    r'[A-G]\s*Section|语言运用|写作|书面表达|听力|完形填空|阅读理解)'
)


def parse_options_from_paragraphs(paras: list, start: int) -> tuple[list[dict], int]:
    """
    从 start 段往下扫，提取 A/B/C/D 选项，返回 (options_list, next_index)。
    options_list: [{"label": "A", "text": "..."}, ...]
    next_index: 扫完选项后下一个未消费的段落索引
    """
    collected: dict[str, str] = {}
    i = start
    while i < len(paras) and len(collected) < 4:
        t = paras[i].text.strip()
        i += 1
        if not t:
            continue
        # 停止条件
        if _NEXT_QNUM.match(t) or _ANSWER_ONLY.match(t) or _NEW_SECTION.match(t):
            i -= 1  # 退回，不消费这行
            break

        # 尝试紧凑格式：一行内含多个选项
        # 支持无空格直连 "A. xxxB. xxx" 和有空格 "A. xxx  B. xxx"
        # 在非空白字符后、B/C/D 选项字母前切分
        parts = re.split(r'(?<=\S)\s*(?=[B-D][\.．]\s)', t)
        if len(parts) > 1:
            matched_parts = []
            for p in parts:
                m = _OPT_SINGLE.match(p.strip())
                if m:
                    matched_parts.append((m.group(1), m.group(2).strip()))
            if matched_parts and len(matched_parts) == len(parts):
                for label, text in matched_parts:
                    if label not in collected:
                        collected[label] = text
                continue

        # 单行单选项
        m = _OPT_SINGLE.match(t)
        if m:
            label, text = m.group(1), m.group(2).strip()
            if label not in collected:
                collected[label] = text
            continue

        # 非选项行且已收集到选项 → 停止（这行是文章段落）
        if collected:
            i -= 1
            break

    options = [
        {"label": lbl, "text": collected[lbl], "is_correct_candidate": None}
        for lbl in ["A", "B", "C", "D"] if lbl in collected
    ]
    return options, i


def is_dirty(r: dict) -> bool:
    qt = r.get("question_text") or ""
    if len(qt) > 300:
        return True
    if re.search(r'\b[A-D][\.．]\s*\w.{10,}\s{2,}[B-D][\.．]', qt):
        return True
    return False


def load_records(path: Path) -> list[dict]:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exam",    help="只处理指定 exam_id")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force",   action="store_true", help="处理全部 reading 记录（不限脏数据）")
    args = parser.parse_args()

    records = load_records(JSONL_PATH)

    targets = [r for r in records if r.get("section_type") == "reading"]
    if args.exam:
        targets = [r for r in targets if r.get("exam_id") == args.exam]
    if not args.force:
        targets = [r for r in targets if is_dirty(r)]

    print(f"待修复记录：{len(targets)} 条", flush=True)

    # 按 (exam_id, source_file) 分组，共用同一个 docx 对象
    from collections import defaultdict
    by_file: dict[tuple, list[dict]] = defaultdict(list)
    for r in targets:
        key = (r["exam_id"], r.get("source_file", ""))
        by_file[key].append(r)

    id_to_record = {r["question_id"]: r for r in records}

    updated = skipped = errors = 0

    for (exam_id, source_file), group in sorted(by_file.items()):
        docx_abs = PROJECT_ROOT / source_file
        if not docx_abs.exists():
            print(f"  [跳过] {exam_id}: 文件不存在 {docx_abs}")
            skipped += len(group)
            continue

        try:
            doc = Document(str(docx_abs))
            paras = doc.paragraphs
        except Exception as e:
            print(f"  [错误] {exam_id} 打开文件失败: {e}")
            errors += len(group)
            continue

        for r in sorted(group, key=lambda r: int(r.get("source_question_number") or 0)):
            qnum = r.get("source_question_number")
            para_idx = r.get("source_span", {}).get("paragraph")
            if para_idx is None:
                print(f"  [跳过] {exam_id} Q{qnum}: 无 source_span.paragraph")
                skipped += 1
                continue

            try:
                para_idx = int(para_idx)
            except (ValueError, TypeError):
                print(f"  [跳过] {exam_id} Q{qnum}: paragraph 非整数")
                skipped += 1
                continue

            if para_idx >= len(paras):
                print(f"  [跳过] {exam_id} Q{qnum}: paragraph={para_idx} 越界（共{len(paras)}段）")
                skipped += 1
                continue

            # 取题干：只取 source_span.paragraph 这一段
            qt_raw = paras[para_idx].text.strip()
            # 清理：去掉题号前缀（如 "2. "）
            qt_clean = re.sub(r'^\d{1,2}[\.．]\s*', '', qt_raw).strip()

            # 若重建后题干本身是选项行（paragraph 指向错误），跳过
            if _OPT_SINGLE.match(qt_clean):
                print(f"  [跳过] {exam_id} Q{qnum}: para={para_idx} 指向选项行，非题干，需人工修正")
                skipped += 1
                continue

            # 往下提取选项
            options, _ = parse_options_from_paragraphs(paras, para_idx + 1)

            old_qt = r.get("question_text") or ""
            old_opts = r.get("options") or []

            if args.dry_run or args.exam:
                print(f"\n  Q{qnum} (para={para_idx})")
                print(f"    旧 qt[:{min(80,len(old_qt))}]: {old_qt[:80]!r}")
                print(f"    新 qt: {qt_clean!r}")
                print(f"    旧 options: {[o.get('label') for o in old_opts]}")
                print(f"    新 options: {[(o['label'], o['text'][:40]) for o in options]}")

            if not args.dry_run:
                id_to_record[r["question_id"]]["question_text"] = qt_clean
                if options:
                    id_to_record[r["question_id"]]["options"] = options
                updated += 1

    if args.dry_run:
        print("\n[dry-run 模式，不写回文件]")
        return

    if updated == 0:
        print("没有需要更新的记录，文件未修改。")
        return

    tmp = JSONL_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(JSONL_PATH)
    print(f"\n完成：更新 {updated} 条，跳过 {skipped} 条，失败 {errors} 条")
    print(f"文件已写回：{JSONL_PATH}")


if __name__ == "__main__":
    main()
