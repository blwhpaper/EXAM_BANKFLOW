#!/usr/bin/env python3
"""
fill_answers.py
从答案文件批量回填 answer=null 的记录。

优先级：A_答案.docx > QA_解析版.docx > A_答案_*.docx（跳过 PDF）

用法：
  python scripts/fill_answers.py --dry-run          # 只打印不写回
  python scripts/fill_answers.py --exam E009        # 单卷测试
  python scripts/fill_answers.py                    # 全量
  python scripts/fill_answers.py --force            # 覆盖已有 answer
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from docx import Document

PROJECT_ROOT = Path(__file__).resolve().parent.parent
JSONL_PATH   = PROJECT_ROOT / "workflow/records/EXAM-CLEAN-010_STRUCTURED_QUESTION_BANK.jsonl"
EXAMS_ROOT   = PROJECT_ROOT / "datasets/2026_quyixian_english/_STANDARDIZED_EXAMS"

# 匹配 "21. D。..." 或 "36. G。..."（七选五 A-G）或 "21．D．..." 等
_ANSWER_LINE = re.compile(r'^(\d{1,2})[\.．]\s*([A-G])[。．\s]')


def find_answer_file(exam_dir: Path) -> Path | None:
    """按优先级返回第一个可用的答案 docx 文件。"""
    candidates = [
        exam_dir / "A_答案.docx",
        exam_dir / "QA_解析版.docx",
    ]
    # 支持 A_答案_1.docx, A_答案_2.docx 等（如 E052）
    candidates += sorted(exam_dir.glob("A_答案_*.docx"))
    candidates += sorted(exam_dir.glob("QA_解析版_*.docx"))

    for p in candidates:
        if p.exists():
            return p
    return None


def extract_answers(docx_path: Path) -> dict[int, str]:
    """扫描 docx 全文，提取题号→答案字母映射。"""
    doc = Document(str(docx_path))
    answers: dict[int, str] = {}
    for para in doc.paragraphs:
        t = para.text.strip()
        if not t:
            continue
        m = _ANSWER_LINE.match(t)
        if m:
            qnum = int(m.group(1))
            letter = m.group(2).upper()
            if qnum not in answers:  # 优先保留第一次出现
                answers[qnum] = letter
    return answers


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
    parser.add_argument("--dry-run", action="store_true", help="只打印不写回")
    parser.add_argument("--force",   action="store_true", help="覆盖已有 answer")
    args = parser.parse_args()

    records = load_records(JSONL_PATH)

    # 筛选目标记录
    target_sections = {"cloze", "reading_7to5", "reading"}
    targets = [
        r for r in records
        if r.get("section_type") in target_sections
        and (args.force or not r.get("answer"))
    ]
    if args.exam:
        targets = [r for r in targets if r.get("exam_id") == args.exam]

    print(f"待回填记录：{len(targets)} 条", flush=True)

    # 按 exam_id 分组（同一 exam 共用一个答案文件）
    by_exam: dict[str, list[dict]] = defaultdict(list)
    for r in targets:
        by_exam[r["exam_id"]].append(r)

    print(f"涉及 exam 数：{len(by_exam)}", flush=True)

    id_to_record: dict[str, dict] = {r["question_id"]: r for r in records}

    total_matched = 0
    total_missed  = 0
    total_skipped = 0

    for exam_id in sorted(by_exam):
        # 找 exam 目录
        exam_dirs = sorted(EXAMS_ROOT.glob(f"{exam_id}_*"))
        if not exam_dirs:
            print(f"\n[跳过] {exam_id}: 目录未找到")
            total_skipped += len(by_exam[exam_id])
            continue

        exam_dir = exam_dirs[0]
        ans_file = find_answer_file(exam_dir)
        if ans_file is None:
            print(f"\n[跳过] {exam_id}: 无可用答案文件（仅 PDF 或无文件）")
            total_skipped += len(by_exam[exam_id])
            continue

        try:
            answer_map = extract_answers(ans_file)
        except Exception as e:
            print(f"\n[错误] {exam_id} 提取失败: {e}")
            total_skipped += len(by_exam[exam_id])
            continue

        group = sorted(by_exam[exam_id],
                       key=lambda r: int(r.get("source_question_number") or 0))

        matched = []
        missed  = []
        for r in group:
            try:
                qnum = int(r.get("source_question_number") or 0)
            except ValueError:
                missed.append(r)
                continue
            if qnum in answer_map:
                matched.append((r, answer_map[qnum]))
            else:
                missed.append(r)

        print(f"\n{'='*56}")
        print(f"exam_id  : {exam_id}")
        print(f"答案文件 : {ans_file.name}  (提取 {len(answer_map)} 题)")
        print(f"匹配成功 : {len(matched)} 条  未匹配: {len(missed)} 条")

        for r, ans in matched:
            qnum = r.get("source_question_number")
            section = r.get("section_type")
            print(f"  {qnum:>3} → {ans}  [{section}]")

        if missed:
            miss_nums = [r.get("source_question_number") for r in missed]
            print(f"  未匹配题号: {miss_nums}")

        total_matched += len(matched)
        total_missed  += len(missed)

        if args.dry_run:
            continue

        for r, ans in matched:
            id_to_record[r["question_id"]]["answer"] = ans

    print(f"\n{'='*56}")
    print(f"汇总：匹配 {total_matched} 条，未匹配 {total_missed} 条，跳过 {total_skipped} 条")

    if args.dry_run:
        print("[dry-run 模式，不写回文件]")
        return

    if total_matched == 0:
        print("没有需要更新的记录，文件未修改。")
        return

    tmp = JSONL_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(JSONL_PATH)
    print(f"文件已写回：{JSONL_PATH}")


if __name__ == "__main__":
    main()
