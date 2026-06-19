"""
CS599 大作业报告自动生成 Agent。
使用 LangGraph 编排 7 个章节，逐章调用 DeepSeek API 生成内容，
最终合成完整 Markdown 报告。

用法：
    python agent.py                    # 交互模式，逐章确认
    python agent.py --auto             # 全自动生成（不暂停）
    python agent.py --chapter 1        # 只生成第 1 章
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import TypedDict, Annotated, Sequence, Literal
from pathlib import Path

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, SystemMessage

from prompts import (
    SYSTEM_PROMPT,
    COVER_META,
    CHAPTER_PROMPTS,
)

# ── 加载环境变量 ──
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

if not DEEPSEEK_API_KEY:
    print("❌ 错误：请设置 DEEPSEEK_API_KEY 环境变量")
    print("   cp .env.example .env  # 然后编辑 .env 填入真实 Key")
    sys.exit(1)

# ── 初始化 LLM ──
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=4096,
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

# ── 状态定义 ──
class ReportState(TypedDict):
    chapters: dict          # { "1": "内容", "2": "内容", ... }
    current_chapter: str    # 当前章节编号
    completed: list[str]    # 已完成章节列表
    errors: list[str]       # 错误列表
    status: str             # "idle" | "generating" | "done" | "error"


def generate_chapter(state: ReportState) -> ReportState:
    """生成单个章节内容。"""
    chapter_id = state["current_chapter"]
    chapter_info = CHAPTER_PROMPTS[chapter_id]

    print(f"\n{'=' * 60}")
    print(f"📝 正在生成第 {chapter_id} 章：{chapter_info['title']}")
    print(f"{'=' * 60}")

    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=chapter_info["prompt"]),
        ]
        response = llm.invoke(messages)
        content = response.content

        state["chapters"][chapter_id] = {
            "title": chapter_info["title"],
            "content": content,
            "generated_at": datetime.now().isoformat(),
        }
        state["completed"].append(chapter_id)
        state["errors"] = []

        print(f"✅ 第 {chapter_id} 章生成完成（{len(content)} 字）")

    except Exception as e:
        error_msg = f"第 {chapter_id} 章生成失败：{e}"
        state["errors"].append(error_msg)
        print(f"❌ {error_msg}")

    return state


def router(state: ReportState) -> Literal["generate", "done"]:
    """路由：决定下一个章节或结束。"""
    chapter_order = list(CHAPTER_PROMPTS.keys())
    current_idx = chapter_order.index(state["current_chapter"])

    if current_idx + 1 < len(chapter_order):
        next_chapter = chapter_order[current_idx + 1]
        state["current_chapter"] = next_chapter
        return "generate"
    else:
        state["status"] = "done"
        return "done"


def build_workflow() -> StateGraph:
    """构建 LangGraph 工作流。"""
    workflow = StateGraph(ReportState)

    workflow.add_node("generate", generate_chapter)
    workflow.add_node("done", lambda s: s)

    workflow.set_entry_point("generate")
    workflow.add_conditional_edges(
        "generate",
        router,
        {"generate": "generate", "done": "done"},
    )
    workflow.add_edge("done", END)

    return workflow.compile(checkpointer=MemorySaver())


def compile_report(state: ReportState) -> str:
    """将各章节合成为完整 Markdown 报告。"""
    lines = []
    lines.append("# CS599 大作业报告")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 封面
    lines.append("## 封面")
    lines.append("")
    lines.append("| 字段 | 内容 |")
    lines.append("|------|------|")
    for key, value in COVER_META.items():
        label = {
            "course": "课程名称",
            "project_name": "项目名称",
            "direction": "方向",
            "student_id": "学号",
            "name": "姓名",
            "major": "专业",
            "instructor": "指导教师",
            "date": "提交日期",
        }.get(key, key)
        lines.append(f"| {label} | {value} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 目录（占位，PDF 转换时自动生成）
    lines.append("# 目录")
    lines.append("")
    for cid, info in CHAPTER_PROMPTS.items():
        lines.append(f"- [第{cid}章 {info['title']}](#第{cid}章)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 各章节
    chapter_order = list(CHAPTER_PROMPTS.keys())
    for cid in chapter_order:
        if cid in state["chapters"]:
            ch = state["chapters"][cid]
            lines.append(f"# 第{cid}章 {ch['title']}")
            lines.append("")
            lines.append(ch["content"])
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)


def save_report(markdown_content: str, output_dir: str = "docs") -> str:
    """保存报告到文件。"""
    output_path = Path(output_dir) / "CS599_大作业报告.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"\n📄 报告已保存到：{output_path}")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="CS599 报告自动生成 Agent")
    parser.add_argument(
        "--auto", action="store_true", help="全自动生成，不暂停确认"
    )
    parser.add_argument(
        "--chapter", type=str, help="只生成指定章节（如 1, 2, 3）"
    )
    parser.add_argument(
        "--output", type=str, default="docs", help="输出目录（默认 docs）"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("🎓 CS599 大作业报告自动生成 Agent")
    print(f"📅 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 初始化状态
    state: ReportState = {
        "chapters": {},
        "current_chapter": "1",
        "completed": [],
        "errors": [],
        "status": "generating",
    }

    # 单章模式
    if args.chapter:
        if args.chapter not in CHAPTER_PROMPTS:
            print(f"❌ 无效章节编号：{args.chapter}（有效值：{list(CHAPTER_PROMPTS.keys())}）")
            sys.exit(1)
        state["current_chapter"] = args.chapter
        state = generate_chapter(state)
        state["status"] = "done"
    else:
        # 全量生成
        workflow = build_workflow()
        chapter_order = list(CHAPTER_PROMPTS.keys())

        for i, cid in enumerate(chapter_order):
            state["current_chapter"] = cid

            if not args.auto:
                input(f"\n⏳ 按 Enter 生成第 {cid} 章（{CHAPTER_PROMPTS[cid]['title']}）...")

            state = generate_chapter(state)

            if state["errors"]:
                print(f"⚠️ 第 {cid} 章生成出错，继续下一章...")

        state["status"] = "done"

    # 编译并保存
    if state["completed"]:
        markdown = compile_report(state)
        output_path = save_report(markdown, args.output)
        print(f"\n✅ 完成！共生成 {len(state['completed'])}/{len(CHAPTER_PROMPTS)} 章")
        print(f"📄 报告路径：{output_path}")
        print(f"\n💡 下一步：")
        print(f"   python convert_to_pdf.py  # 将 Markdown 转换为 PDF")
    else:
        print("\n❌ 没有生成任何章节，请检查 API Key 和网络连接。")

    if state["errors"]:
        print(f"\n⚠️ 错误列表：")
        for err in state["errors"]:
            print(f"   - {err}")


if __name__ == "__main__":
    main()