#!/usr/bin/env python3
"""Build clean English and Chinese PDF copies for writing-tutor review."""

from __future__ import annotations

import shutil
import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_documents import markdown_to_html


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "文书老师查看_PDF"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

def print_pdf(markdown: str, language: str, source: Path, output: Path) -> None:
    html = markdown_to_html(markdown, language, source)
    with tempfile.TemporaryDirectory(prefix="epq-teacher-pdf-") as temp_dir:
        temp = Path(temp_dir)
        html_path = temp / "document.html"
        profile = temp / "chrome-profile"
        html_path.write_text(html, encoding="utf-8")
        command = [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--no-pdf-header-footer",
            "--print-to-pdf=" + str(output),
            "--user-data-dir=" + str(profile),
            html_path.as_uri(),
        ]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=8)
        except subprocess.TimeoutExpired:
            # Chrome on macOS can leave its headless browser process open after
            # the PDF has already been written. End that temporary process group.
            os.killpg(process.pid, signal.SIGTERM)
            stdout, stderr = process.communicate(timeout=5)
        if process.returncode not in (0, -signal.SIGTERM) and not output.exists():
            raise SystemExit(stderr or stdout)

    if not output.exists() or output.stat().st_size < 10_000:
        raise SystemExit(f"PDF was not created correctly: {output}")
    if output.read_bytes()[:5] != b"%PDF-":
        raise SystemExit(f"Invalid PDF header: {output}")


def main() -> None:
    if not CHROME.exists():
        raise SystemExit(f"Google Chrome was not found at {CHROME}")

    weekly_en = ROOT / "production-log/weekly-work-log-en.md"
    weekly_zh = ROOT / "zh-cn/weekly-work-log-zh-cn.md"
    production_en = ROOT / "production-log/teacher-production-log-en.md"
    production_zh = ROOT / "zh-cn/teacher-production-log-zh-cn.md"
    report_en = ROOT / "report/final-report.md"
    report_zh = ROOT / "zh-cn/final-report-zh-cn.md"
    appendix_en = ROOT / "appendix/appendix-pack-en.md"
    documents = (
        (weekly_en, "English", "01_Weekly_Work_Log_English.pdf"),
        (weekly_zh, "Chinese", "02_每周项目工作日志_中文.pdf"),
        (production_en, "English", "03_Production_Log_English.pdf"),
        (production_zh, "Chinese", "04_Production_Log_中文.pdf"),
        (report_en, "English", "05_Final_Report_English.pdf"),
        (report_zh, "Chinese", "06_最终报告_中文.pdf"),
        (appendix_en, "English", "07_Appendix_English.pdf"),
    )
    with tempfile.TemporaryDirectory(prefix="epq-teacher-pdfs-") as temp_dir:
        temp_output = Path(temp_dir)
        for source, language, filename in documents:
            markdown = source.read_text(encoding="utf-8")
            output = temp_output / filename
            print_pdf(markdown, language, source, output)
            print(f"Built {output.name}: {output.stat().st_size} bytes")

        OUTPUT_DIR.mkdir(exist_ok=True)
        expected = {filename for _, _, filename in documents}
        for child in OUTPUT_DIR.iterdir():
            if child.name not in expected:
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        for _, _, filename in documents:
            shutil.copy2(temp_output / filename, OUTPUT_DIR / filename)

    non_pdf = [item.name for item in OUTPUT_DIR.iterdir() if item.suffix.lower() != ".pdf"]
    if non_pdf:
        raise SystemExit(f"Teacher folder contains non-PDF files: {non_pdf}")


if __name__ == "__main__":
    main()
