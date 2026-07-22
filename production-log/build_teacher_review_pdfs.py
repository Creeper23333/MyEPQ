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

def print_pdf(markdown: str, language: str, output: Path) -> None:
    html = markdown_to_html(markdown, language)
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

    OUTPUT_DIR.mkdir(exist_ok=True)
    for child in OUTPUT_DIR.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()

    weekly_en = (ROOT / "production-log/weekly-work-log-en.md").read_text(encoding="utf-8")
    weekly_zh = (ROOT / "zh-cn/weekly-work-log-zh-cn.md").read_text(encoding="utf-8")
    production_en = (ROOT / "production-log/teacher-production-log-en.md").read_text(
        encoding="utf-8"
    )
    production_zh = (ROOT / "zh-cn/teacher-production-log-zh-cn.md").read_text(
        encoding="utf-8"
    )

    documents = (
        (weekly_en, "English", OUTPUT_DIR / "01_Weekly_Work_Log_English.pdf"),
        (weekly_zh, "Chinese", OUTPUT_DIR / "02_每周项目工作日志_中文.pdf"),
        (production_en, "English", OUTPUT_DIR / "03_Production_Log_English.pdf"),
        (production_zh, "Chinese", OUTPUT_DIR / "04_Production_Log_中文.pdf"),
    )
    for markdown, language, output in documents:
        print_pdf(markdown, language, output)
        print(f"Built {output.name}: {output.stat().st_size} bytes")

    non_pdf = [item.name for item in OUTPUT_DIR.iterdir() if item.suffix.lower() != ".pdf"]
    if non_pdf:
        raise SystemExit(f"Teacher folder contains non-PDF files: {non_pdf}")


if __name__ == "__main__":
    main()
