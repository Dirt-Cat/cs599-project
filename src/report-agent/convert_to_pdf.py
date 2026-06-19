"""
Markdown → PDF 转换脚本。
使用 pandoc + wkhtmltopdf 将 Markdown 报告转换为含导航书签的 PDF。

前置依赖：
    # Windows
    winget install pandoc
    winget install wkhtmltopdf
    
    # macOS
    brew install pandoc
    brew install --cask wkhtmltopdf

用法：
    python convert_to_pdf.py                    # 默认转换 docs/CS599_大作业报告.md
    python convert_to_pdf.py --input report.md   # 指定输入文件
    python convert_to_pdf.py --template fancy    # 使用精美模板
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_dependencies():
    """检查 pandoc 和 wkhtmltopdf 是否已安装。"""
    missing = []

    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("pandoc")

    try:
        subprocess.run(["wkhtmltopdf", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # wkhtmltopdf 可能安装在其他路径
        wkhtml = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if Path(wkhtml).exists():
            os.environ["PATH"] += os.pathsep + str(Path(wkhtml).parent)
        else:
            missing.append("wkhtmltopdf")

    return missing


def generate_css(template: str = "default") -> str:
    """生成 PDF 样式 CSS。"""
    css = """
    body {
        font-family: "SimSun", "宋体", serif;
        font-size: 12pt;
        line-height: 1.8;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        color: #333;
    }
    h1 {
        font-size: 22pt;
        text-align: center;
        border-bottom: 2px solid #1a73e8;
        padding-bottom: 10px;
        margin-top: 40px;
    }
    h2 {
        font-size: 16pt;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
        margin-top: 30px;
    }
    h3 {
        font-size: 14pt;
        margin-top: 20px;
    }
    pre {
        background: #f5f5f5;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 15px;
        overflow-x: auto;
        font-size: 9pt;
        line-height: 1.5;
    }
    code {
        background: #f0f0f0;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: "Consolas", "Courier New", monospace;
    }
    pre code {
        background: none;
        padding: 0;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px 12px;
        text-align: left;
    }
    th {
        background: #1a73e8;
        color: white;
    }
    blockquote {
        border-left: 4px solid #1a73e8;
        padding-left: 15px;
        margin: 15px 0;
        color: #555;
        background: #f8f9fa;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    @page {
        margin: 1.5cm;
        @top-center {
            content: "CS599 大作业报告";
        }
        @bottom-center {
            content: counter(page);
        }
    }
    @media print {
        h1 { page-break-before: always; }
        h1:first-of-type { page-break-before: avoid; }
    }
    """
    return css


def convert_markdown_to_pdf(input_path: str, output_path: str, css_path: str = None):
    """使用 pandoc 将 Markdown 转换为 PDF。"""
    cmd = [
        "pandoc",
        input_path,
        "-o", output_path,
        "--pdf-engine=wkhtmltopdf",
        "--toc",  # 生成目录
        "--toc-depth=3",  # 目录深度
        "--metadata", "title=CS599 大作业报告",
        "--metadata", "author=CS599 Student",
        "--metadata", "date=2026-06-22",
        "--from", "markdown+pipe_tables+fenced_code_blocks",
        "--pdf-engine-opt=--enable-local-file-access",
        "--pdf-engine-opt=--footer-center",
        "--pdf-engine-opt=[page]",
        "--pdf-engine-opt=--footer-font-size",
        "--pdf-engine-opt=8",
    ]

    if css_path and Path(css_path).exists():
        cmd.extend(["--pdf-engine-opt=--user-style-sheet", "--pdf-engine-opt=" + css_path])

    print(f"🔄 正在转换：{input_path} → {output_path}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0:
            print(f"✅ PDF 生成成功：{output_path}")
            # 检查文件大小
            size_kb = Path(output_path).stat().st_size / 1024
            print(f"📦 文件大小：{size_kb:.1f} KB")
        else:
            print(f"❌ 转换失败：{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行 pandoc 时出错：{e}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Markdown → PDF 转换")
    parser.add_argument(
        "--input", type=str, default="docs/CS599_大作业报告.md",
        help="输入 Markdown 文件路径"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="输出 PDF 文件路径（默认同目录同名）"
    )
    parser.add_argument(
        "--template", type=str, default="default",
        choices=["default", "fancy"],
        help="PDF 模板样式"
    )
    args = parser.parse_args()

    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"❌ 缺少依赖：{', '.join(missing)}")
        print("\n📥 安装方法：")
        print("   winget install pandoc")
        print("   winget install wkhtmltopdf")
        sys.exit(1)

    # 检查输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 输入文件不存在：{input_path}")
        print("   请先运行：python agent.py --auto")
        sys.exit(1)

    # 设置输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".pdf")

    # 生成 CSS
    css_content = generate_css(args.template)
    css_path = str(input_path.parent / "report-style.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)

    # 转换
    success = convert_markdown_to_pdf(
        str(input_path),
        str(output_path),
        css_path,
    )

    if success:
        print(f"\n🎉 完成！PDF 报告已生成：{output_path}")
        print(f"💡 用 PDF 阅读器打开，查看左侧导航窗格（书签/大纲）")

    # 清理临时 CSS
    # Path(css_path).unlink(missing_ok=True)


if __name__ == "__main__":
    main()