#!/usr/bin/env python3
"""Validate bilingual production logs and build reproducible Word exports.

The English source remains in ``production-log/`` and the Chinese source remains
in ``zh-cn/`` so each deliverable has a single canonical location. This script
uses only the Python standard library plus the macOS system command ``textutil``.
It checks structural parity before producing either Word file, then converts each
Word file back to text and checks stable section and placeholder sentinels.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import html
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent
ZH_ROOT = ROOT.parent / "zh-cn"


@dataclass(frozen=True)
class Document:
    language: str
    source: Path
    output: Path
    title_sentinel: str


DOCUMENTS = (
    Document(
        language="English",
        source=ROOT / "complete-production-log-en.md",
        output=ROOT / "complete-production-log-en.docx",
        title_sentinel="Complete Production Log",
    ),
    Document(
        language="Chinese",
        source=ZH_ROOT / "complete-production-log-zh-cn.md",
        output=ZH_ROOT / "complete-production-log-zh-cn.docx",
        title_sentinel="完整生产日志",
    ),
)

PAIR_RE = re.compile(r"<!--\s*PAIR:\s*([A-Z0-9.-]+)\s*-->")
PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
FIELD_ROW_RE = re.compile(r"^\|\s*(PL-[0-9.]+-[A-Z])\s*\|", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(PL-[0-9.]+)\s+(.+)$", re.MULTILINE)
TABLE_SEPARATOR_RE = re.compile(
    r"^\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$"
)


def read_source(document: Document) -> str:
    if not document.source.exists():
        raise SystemExit(f"Missing source: {document.source}")
    return document.source.read_text(encoding="utf-8")


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        raise ValueError(f"Not a Markdown table row: {line}")
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def table_shapes(text: str) -> list[tuple[int, tuple[int, ...]]]:
    """Return row and column shapes for every Markdown table in order."""

    lines = text.splitlines()
    shapes: list[tuple[int, tuple[int, ...]]] = []
    index = 0
    while index < len(lines):
        if (
            lines[index].lstrip().startswith("|")
            and index + 1 < len(lines)
            and TABLE_SEPARATOR_RE.match(lines[index + 1].strip())
        ):
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                rows.append(split_table_row(lines[index]))
                index += 1
            shapes.append((len(rows), tuple(len(row) for row in rows)))
            continue
        index += 1
    return shapes


def line_structure(text: str) -> list[tuple[str, int | str]]:
    """Return a language-independent signature for every Markdown source line."""

    signature: list[tuple[str, int | str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        pair = PAIR_RE.fullmatch(stripped)
        heading = re.match(r"^(#{1,6})\s+(PL-[0-9.]+)\s+", stripped)
        if not stripped:
            signature.append(("blank", 0))
        elif pair:
            signature.append(("pair", pair.group(1)))
        elif heading:
            signature.append(("heading", f"{len(heading.group(1))}:{heading.group(2)}"))
        elif stripped == "---":
            signature.append(("rule", 0))
        elif stripped.startswith("|"):
            row = split_table_row(stripped)
            kind = "table-separator" if TABLE_SEPARATOR_RE.match(stripped) else "table-row"
            signature.append((kind, len(row)))
        elif stripped.startswith(">"):
            signature.append(("quote", 0))
        elif re.match(r"^[-*]\s+", stripped):
            signature.append(("unordered-item", 0))
        elif re.match(r"^\d+\.\s+", stripped):
            signature.append(("ordered-item", 0))
        else:
            signature.append(("paragraph-line", 0))
    return signature


def validate_pair() -> tuple[str, str]:
    english = read_source(DOCUMENTS[0])
    chinese = read_source(DOCUMENTS[1])

    checks = {
        "ordered PAIR IDs": (
            PAIR_RE.findall(english),
            PAIR_RE.findall(chinese),
        ),
        "ordered heading IDs": (
            [match[1] for match in HEADING_RE.findall(english)],
            [match[1] for match in HEADING_RE.findall(chinese)],
        ),
        "ordered field-row IDs": (
            FIELD_ROW_RE.findall(english),
            FIELD_ROW_RE.findall(chinese),
        ),
        "ordered table shapes": (
            table_shapes(english),
            table_shapes(chinese),
        ),
        "line-level block structure": (
            line_structure(english),
            line_structure(chinese),
        ),
        "ordered placeholder sequence": (
            PLACEHOLDER_RE.findall(english),
            PLACEHOLDER_RE.findall(chinese),
        ),
    }
    for label, (left, right) in checks.items():
        if left != right:
            raise SystemExit(f"Bilingual parity failed for {label}")

    english_placeholders = PLACEHOLDER_RE.findall(english)
    chinese_placeholders = PLACEHOLDER_RE.findall(chinese)
    if Counter(english_placeholders) != Counter(chinese_placeholders):
        missing = Counter(english_placeholders) - Counter(chinese_placeholders)
        extra = Counter(chinese_placeholders) - Counter(english_placeholders)
        raise SystemExit(
            "Bilingual placeholder parity failed: "
            f"missing in Chinese={dict(missing)}, extra in Chinese={dict(extra)}"
        )

    pair_ids = PAIR_RE.findall(english)
    if len(pair_ids) != len(set(pair_ids)):
        duplicates = [item for item, count in Counter(pair_ids).items() if count > 1]
        raise SystemExit(f"Duplicate PAIR IDs: {duplicates}")
    if not pair_ids or pair_ids[0] != "PL-00.01" or pair_ids[-1] != "PL-17.03":
        raise SystemExit("PAIR coverage must run from PL-00.01 through PL-17.03")

    print(
        "Parity passed: "
        f"{len(pair_ids)} paired units, "
        f"{len(FIELD_ROW_RE.findall(english))} field rows, "
        f"{len(table_shapes(english))} tables, "
        f"{len(english_placeholders)} placeholder occurrences "
        f"({len(set(english_placeholders))} unique)."
    )
    return english, chinese


def inline_markup(value: str) -> str:
    escaped = html.escape(value, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def is_special_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("<!--"):
        return True
    if stripped == "---":
        return True
    if re.match(r"^#{1,6}\s+", stripped):
        return True
    if stripped.startswith(">"):
        return True
    if re.match(r"^[-*]\s+", stripped):
        return True
    if re.match(r"^\d+\.\s+", stripped):
        return True
    if (
        stripped.startswith("|")
        and index + 1 < len(lines)
        and TABLE_SEPARATOR_RE.match(lines[index + 1].strip())
    ):
        return True
    return False


def markdown_to_html(markdown: str, language: str) -> str:
    """Convert the limited Markdown used by these documents into clean HTML."""

    lines = markdown.splitlines()
    body: list[str] = []
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("<!--"):
            index += 1
            continue
        if stripped == "---":
            body.append("<hr>")
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            body.append(
                f"<h{level}>{inline_markup(heading.group(2))}</h{level}>"
            )
            index += 1
            continue

        if (
            stripped.startswith("|")
            and index + 1 < len(lines)
            and TABLE_SEPARATOR_RE.match(lines[index + 1].strip())
        ):
            header_cells = split_table_row(lines[index])
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                rows.append(split_table_row(lines[index]))
                index += 1
            body.append("<table><thead><tr>")
            body.extend(
                f"<th>{inline_markup(cell)}</th>" for cell in header_cells
            )
            body.append("</tr></thead><tbody>")
            for row in rows:
                body.append("<tr>")
                body.extend(f"<td>{inline_markup(cell)}</td>" for cell in row)
                body.append("</tr>")
            body.append("</tbody></table>")
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            body.append(
                "<blockquote><p>"
                + inline_markup(" ".join(quote_lines))
                + "</p></blockquote>"
            )
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        if unordered:
            items: list[str] = []
            while index < len(lines):
                match = re.match(r"^[-*]\s+(.+)$", lines[index].strip())
                if not match:
                    break
                items.append(match.group(1))
                index += 1
            body.append("<ul>")
            body.extend(f"<li>{inline_markup(item)}</li>" for item in items)
            body.append("</ul>")
            continue

        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ordered:
            items = []
            while index < len(lines):
                match = re.match(r"^\d+\.\s+(.+)$", lines[index].strip())
                if not match:
                    break
                items.append(match.group(1))
                index += 1
            body.append("<ol>")
            body.extend(f"<li>{inline_markup(item)}</li>" for item in items)
            body.append("</ol>")
            continue

        paragraph: list[str] = []
        while index < len(lines) and not is_special_start(lines, index):
            paragraph.append(lines[index].strip())
            index += 1
        if paragraph:
            body.append("<p>" + inline_markup(" ".join(paragraph)) + "</p>")
            continue

        raise SystemExit(
            f"Markdown conversion stalled at line {index + 1}: {lines[index]}"
        )

    lang_code = "zh-CN" if language == "Chinese" else "en"
    css = """
      @page { size: A4; margin: 1.8cm; }
      body { font-family: Arial, "PingFang SC", sans-serif; font-size: 10.5pt;
             line-height: 1.42; color: #111827; }
      h1 { font-size: 20pt; color: #12355b; border-bottom: 2px solid #12355b;
           padding-bottom: 8px; }
      h2 { font-size: 15pt; color: #12355b; margin-top: 22px; }
      h3 { font-size: 12pt; color: #234e70; margin-top: 16px; }
      p, li { orphans: 2; widows: 2; }
      table { width: 100%; border-collapse: collapse; margin: 8px 0 14px;
              font-size: 8.8pt; page-break-inside: auto; }
      tr { page-break-inside: avoid; }
      th { background: #dbeafe; color: #102a43; font-weight: bold; }
      th, td { border: 1px solid #7b8794; padding: 5px; vertical-align: top; }
      blockquote { border-left: 4px solid #60a5fa; margin-left: 0;
                   padding: 4px 12px; background: #eff6ff; }
      hr { border: 0; border-top: 1px solid #9ca3af; margin: 20px 0; }
    """
    return (
        "<!doctype html><html lang=\""
        + lang_code
        + "\"><head><meta charset=\"utf-8\"><style>"
        + css
        + "</style></head><body>"
        + "".join(body)
        + "</body></html>"
    )


def run_textutil(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["textutil", *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit("macOS textutil was not found") from exc
    except subprocess.CalledProcessError as exc:
        raise SystemExit(
            f"textutil failed ({exc.returncode}): {exc.stderr.strip()}"
        ) from exc


def build_document(document: Document, source_text: str) -> None:
    html_text = markdown_to_html(source_text, document.language)
    with tempfile.TemporaryDirectory(prefix="epq-production-log-") as temp_dir:
        html_path = Path(temp_dir) / f"{document.language.lower()}.html"
        html_path.write_text(html_text, encoding="utf-8")
        document.output.unlink(missing_ok=True)
        run_textutil(
            [
                "-convert",
                "docx",
                "-output",
                str(document.output),
                str(html_path),
            ]
        )

    round_trip = run_textutil(
        ["-convert", "txt", "-stdout", str(document.output)]
    ).stdout
    sentinels = (
        document.title_sentinel,
        "PL-00.01",
        "PL-17.03",
        "{{CANDIDATE_FULL_NAME}}",
        "0.00098502",
        "5,356",
        "{{SUPERVISOR_FINAL_PACKAGE_CHECK}}",
    )
    missing = [sentinel for sentinel in sentinels if sentinel not in round_trip]
    if missing:
        raise SystemExit(
            f"Word round-trip validation failed for {document.output.name}: "
            f"missing {missing}"
        )

    digest = hashlib.sha256(document.output.read_bytes()).hexdigest()
    print(
        f"Built {document.output.name}: {document.output.stat().st_size} bytes, "
        f"round-trip passed, sha256={digest}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate bilingual parity without generating Word files",
    )
    args = parser.parse_args()

    english, chinese = validate_pair()
    if args.check_only:
        return
    for document, source_text in zip(DOCUMENTS, (english, chinese), strict=True):
        build_document(document, source_text)


if __name__ == "__main__":
    main()
