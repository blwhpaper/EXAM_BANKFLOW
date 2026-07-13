#!/usr/bin/env python3
"""
export_menu.py  —  交互式导出入口
用法：python3 scripts/export_menu.py
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPORT_SCRIPT = PROJECT_ROOT / "scripts" / "export.py"

# export.py 额外参数（按需填充）
_extra: list[str] = []


def ask(prompt, options: list[tuple[str, str]]) -> str:
    """显示编号菜单，返回用户选中的值。"""
    print(f"\n{prompt}")
    for i, (label, _) in enumerate(options, 1):
        print(f"  {i}. {label}")
    while True:
        raw = input("请输入编号：").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1][1]
        print("  ⚠ 请输入有效编号")


def ask_int(prompt, allow_empty=True) -> str | None:
    """询问整数，允许留空。"""
    raw = input(prompt).strip()
    if not raw and allow_empty:
        return None
    if raw.isdigit():
        return raw
    print("  ⚠ 已忽略（非整数）")
    return None


def main():
    print("=" * 40)
    print("  EXAM_BANKFLOW 导出助手")
    print("=" * 40)

    # 第一层：题型
    section_type = ask("选择题型：", [
        ("阅读理解", "reading"),
        ("七选五",   "reading_7to5"),
        ("完形填空", "cloze"),
    ])

    subtype = None
    method = None  # 七选五 solution_methods 筛选

    if section_type == "reading_7to5":
        method = ask("选择七选五解题方法：", [
            ("代词复现",   "pronoun"),
            ("平行对比",   "parallel_contrast"),
            ("祈使句结构", "imperative"),
            ("also平行",   "parallel_also"),
            ("修辞结构",   "rhetoric_structure"),
            ("总结句",     "summary"),
            ("全部七选五", ""),
        ]) or None

    elif section_type == "reading":
        # 第二层：大类
        category = ask("选择阅读题大类：", [
            ("推理题",   "inference"),
            ("细节题",   "detail"),
            ("词汇题",   "vocabulary"),
            ("主旨题",   "main_idea"),
            ("全部阅读", ""),
        ])

        if category == "inference":
            subtype = ask("选择推理题细分：", [
                ("对比结构推理",   "inference_contrast"),
                ("三段论推理",     "inference_syllogism"),
                ("逻辑推理",       "inference_logic"),
                ("修辞推理",       "inference_rhetorical"),
                ("归纳推理",       "inference_generalization"),
                ("全部推理题",     "inference"),
            ])
        elif category == "main_idea":
            subtype = ask("选择主旨题细分：", [
                ("全文主旨",   "main_idea_global"),
                ("最佳标题",   "main_idea_title"),
                ("段落主旨",   "main_idea_paragraph"),
                ("全部主旨题", "main_idea"),
            ])
        elif category:
            subtype = category
        # category == "" → subtype stays None → 全部阅读

    # 数量限制
    limit_raw = ask_int("\n输出几道题？（直接回车 = 全量）：")

    # 指定试卷
    exam_raw = input("指定试卷编号？（如 E008，直接回车跳过）：").strip().upper() or None

    # 输出路径
    default_out = PROJECT_ROOT / "output.docx"
    out_raw = input(f"\n输出文件路径？（回车默认：{default_out}）：").strip()
    out_path = out_raw if out_raw else str(default_out)

    # 组装命令
    cmd = [sys.executable, str(EXPORT_SCRIPT), "--type", section_type, "--out", out_path]
    if subtype:
        cmd += ["--subtype", subtype]
    if method:
        cmd += ["--method", method]
    if limit_raw:
        cmd += ["--limit", limit_raw]
    if exam_raw:
        cmd += ["--exam", exam_raw]

    print("\n" + "=" * 40)
    print("执行命令：")
    print("  " + " ".join(cmd))
    print("=" * 40 + "\n")

    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    if result.returncode == 0:
        print(f"\n✓ 完成，文件已输出至：{out_path}")
    else:
        print("\n✗ 导出失败，请检查错误信息。")


if __name__ == "__main__":
    main()
