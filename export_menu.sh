#!/bin/bash
PROJ=/Volumes/KIOXIA_1TB/01_PROJECTS/EXAM_BANKFLOW

echo "=== EXAM_BANKFLOW 导出菜单 ==="
echo ""
echo "题型："
echo "  1) 完形填空 (cloze)"
echo "  2) 七选五 (reading_7to5)"
echo "  3) 阅读理解 (reading)"
read -p "请选择 [1-3]: " type_choice

case $type_choice in
  1) TYPE="cloze" ;;
  2) TYPE="reading_7to5" ;;
  3) TYPE="reading" ;;
  *) echo "无效选择"; exit 1 ;;
esac

echo ""
read -p "指定试卷编号？（留空=全部，例如 E005）: " EXAM

echo ""
if [ "$TYPE" = "reading_7to5" ]; then
  echo "按解题方法筛选（七选五）："
  echo "  1) 不筛选（全部）"
  echo "  2) pronoun（代词复现）"
  echo "  3) parallel_contrast（平行对比）"
  echo "  4) imperative（祈使句）"
  echo "  5) parallel_also（also平行）"
  echo "  6) rhetoric_structure（修辞结构）"
  echo "  7) summary（总结句）"
  read -p "请选择 [1-7]: " strategy_choice

  case $strategy_choice in
    1) STRATEGY="" ;;
    2) STRATEGY="--method pronoun" ;;
    3) STRATEGY="--method parallel_contrast" ;;
    4) STRATEGY="--method imperative" ;;
    5) STRATEGY="--method parallel_also" ;;
    6) STRATEGY="--method rhetoric_structure" ;;
    7) STRATEGY="--method summary" ;;
    *) STRATEGY="" ;;
  esac
elif [ "$TYPE" = "reading" ]; then
  echo "按题型筛选（阅读理解）："
  echo "  1) 不筛选（全部）"
  echo "  2) detail（细节题）"
  echo "  3) inference_contrast（对比推断）"
  echo "  4) inference_generalization（归纳推断）"
  echo "  5) inference_rhetorical（修辞推断）"
  echo "  6) inference_syllogism（演绎推断）"
  echo "  7) inference_logic（逻辑推断）"
  echo "  8) main_idea_title（主旨标题）"
  echo "  9) main_idea_paragraph（段落主旨）"
  echo "  10) main_idea_global（全文主旨）"
  echo "  11) vocabulary（词义猜测）"
  read -p "请选择 [1-11]: " strategy_choice

  case $strategy_choice in
    1) STRATEGY="" ;;
    2) STRATEGY="--subtype detail" ;;
    3) STRATEGY="--subtype inference_contrast" ;;
    4) STRATEGY="--subtype inference_generalization" ;;
    5) STRATEGY="--subtype inference_rhetorical" ;;
    6) STRATEGY="--subtype inference_syllogism" ;;
    7) STRATEGY="--subtype inference_logic" ;;
    8) STRATEGY="--subtype main_idea_title" ;;
    9) STRATEGY="--subtype main_idea_paragraph" ;;
    10) STRATEGY="--subtype main_idea_global" ;;
    11) STRATEGY="--subtype vocabulary" ;;
    *) STRATEGY="" ;;
  esac
else
  echo "按策略筛选（完形填空可用）："
  echo "  1) 不筛选（全部）"
  echo "  2) logic_relation（逻辑关系）"
  echo "  3) context_clue（上下文线索）"
  echo "  4) word_discrimination（词义辨析）"
  echo "  5) action_chain（动作链）"
  echo "  6) emotion_line（情感线）"
  echo "  7) collocation（搭配）"
  read -p "请选择 [1-7]: " strategy_choice

  case $strategy_choice in
    1) STRATEGY="" ;;
    2) STRATEGY="--strategy logic_relation" ;;
    3) STRATEGY="--strategy context_clue" ;;
    4) STRATEGY="--strategy word_discrimination" ;;
    5) STRATEGY="--strategy action_chain" ;;
    6) STRATEGY="--strategy emotion_line" ;;
    7) STRATEGY="--strategy collocation" ;;
    *) STRATEGY="" ;;
  esac
fi

echo ""
read -p "限制题目数量？（留空=不限，例如 10）: " LIMIT
[ -n "$LIMIT" ] && LIMIT_ARG="--limit $LIMIT" || LIMIT_ARG=""

echo ""
read -p "输出文件名（留空=自动命名）: " OUTNAME
if [ -z "$OUTNAME" ]; then
  STRATEGY_LABEL=$([ -n "$STRATEGY" ] && echo "$strategy_choice" || echo "all")
  OUTNAME="${TYPE}_${EXAM:-all}_${STRATEGY_LABEL}.docx"
else
  [[ "$OUTNAME" != *.docx ]] && OUTNAME="${OUTNAME}.docx"
fi

OUTPATH=$PROJ/output/$OUTNAME
mkdir -p $PROJ/output

CMD="python3 $PROJ/scripts/export.py --type $TYPE ${EXAM:+--exam $EXAM} $STRATEGY $LIMIT_ARG --out $OUTPATH"
echo ""
echo "执行：$CMD"
echo ""
eval $CMD

echo ""
echo "✓ 输出：$OUTPATH"
open $OUTPATH
