#!/usr/bin/env python3
"""Validate bilingual production logs and build reproducible Word exports.

The English source remains in ``production-log/`` and the Chinese source remains
in ``zh-cn/`` so each deliverable has a single canonical location. This script
uses the Python standard library plus LibreOffice Writer. It checks structural
parity, creates table-preserving Word files, normalises every table to the A4
text width, and validates stable section and placeholder sentinels from OOXML.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import html
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import urlparse
import zipfile
import xml.etree.ElementTree as ET


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


GREEK_COMMANDS = {
    "alpha": "α",
    "beta": "β",
    "Delta": "Δ",
    "epsilon": "ε",
    "varepsilon": "ε",
    "lambda": "λ",
    "mu": "μ",
    "omega": "ω",
    "sigma": "σ",
}
MATH_OPERATOR_COMMANDS = {
    "in": "∈",
    "lVert": "‖",
    "mid": "∣",
    "odot": "⊙",
    "rVert": "‖",
    "sum": "∑",
    "top": "⊤",
}
MATH_NAMED_OPERATORS = {"arg", "ln", "max", "min"}
MATH_ACCENTS = {"bar": "¯", "hat": "ˆ", "tilde": "~"}


class LatexMathParser:
    """Translate the small LaTeX subset used by this project to native MathML."""

    def __init__(self, source: str) -> None:
        self.source = source
        self.index = 0

    def parse(self, stop: str | None = None) -> str:
        atoms: list[str] = []
        while self.index < len(self.source):
            if stop is not None and self.source[self.index] == stop:
                self.index += 1
                return "".join(atoms)
            if self.source[self.index].isspace():
                self.index += 1
                continue
            atom = self.parse_atom()
            subscript: str | None = None
            superscript: str | None = None
            while self.index < len(self.source) and self.source[self.index] in "_^":
                marker = self.source[self.index]
                self.index += 1
                script = self.parse_script()
                if marker == "_":
                    subscript = script
                else:
                    superscript = script
            if subscript is not None and superscript is not None:
                atom = (
                    f"<msubsup>{atom}<mrow>{subscript}</mrow>"
                    f"<mrow>{superscript}</mrow></msubsup>"
                )
            elif subscript is not None:
                atom = f"<msub>{atom}<mrow>{subscript}</mrow></msub>"
            elif superscript is not None:
                atom = f"<msup>{atom}<mrow>{superscript}</mrow></msup>"
            atoms.append(atom)
        if stop is not None:
            raise ValueError(f"Unclosed LaTeX group in {self.source!r}")
        return "".join(atoms)

    def parse_script(self) -> str:
        while self.index < len(self.source) and self.source[self.index].isspace():
            self.index += 1
        if self.index >= len(self.source):
            raise ValueError(f"Missing LaTeX script in {self.source!r}")
        if self.source[self.index] == "{":
            self.index += 1
            return self.parse("}")
        return self.parse_atom()

    def parse_atom(self) -> str:
        char = self.source[self.index]
        if char == "{":
            self.index += 1
            return f"<mrow>{self.parse('}')}</mrow>"
        if char == "}":
            raise ValueError(f"Unexpected closing brace in {self.source!r}")
        if char == "\\":
            return self.parse_command()
        if char.isdigit() or (
            char == "."
            and self.index + 1 < len(self.source)
            and self.source[self.index + 1].isdigit()
        ):
            start = self.index
            self.index += 1
            while self.index < len(self.source) and (
                self.source[self.index].isdigit() or self.source[self.index] == "."
            ):
                self.index += 1
            return f"<mn>{html.escape(self.source[start:self.index])}</mn>"
        if char.isalpha():
            start = self.index
            self.index += 1
            while self.index < len(self.source) and self.source[self.index].isalpha():
                self.index += 1
            return f"<mi>{html.escape(self.source[start:self.index])}</mi>"
        self.index += 1
        return f"<mo>{html.escape(char)}</mo>"

    def parse_command(self) -> str:
        self.index += 1
        start = self.index
        while self.index < len(self.source) and self.source[self.index].isalpha():
            self.index += 1
        command = self.source[start:self.index]
        if not command and self.index < len(self.source):
            command = self.source[self.index]
            self.index += 1

        if command in GREEK_COMMANDS:
            return f"<mi>{GREEK_COMMANDS[command]}</mi>"
        if command in MATH_OPERATOR_COMMANDS:
            return f"<mo>{MATH_OPERATOR_COMMANDS[command]}</mo>"
        if command in MATH_NAMED_OPERATORS:
            return f'<mi mathvariant="normal">{command}</mi>'
        if command in {"left", "right"}:
            return ""
        if command in {"quad", "qquad"}:
            width = "2em" if command == "qquad" else "1em"
            return f'<mspace width="{width}"></mspace>'
        if command == "frac":
            numerator = self.parse_script()
            denominator = self.parse_script()
            return f"<mfrac><mrow>{numerator}</mrow><mrow>{denominator}</mrow></mfrac>"
        if command == "sqrt":
            radicand = self.parse_script()
            return f"<msqrt><mrow>{radicand}</mrow></msqrt>"
        if command in MATH_ACCENTS:
            while self.index < len(self.source) and self.source[self.index].isspace():
                self.index += 1
            accented = self.parse_atom()
            accent = MATH_ACCENTS[command]
            return f'<mover accent="true">{accented}<mo>{accent}</mo></mover>'
        if command in {"mathcal", "mathrm"}:
            content = self.parse_script()
            variant = "script" if command == "mathcal" else "normal"
            return f'<mstyle mathvariant="{variant}">{content}</mstyle>'
        raise ValueError(f"Unsupported LaTeX command \\{command} in {self.source!r}")


def latex_math(value: str, *, display: bool = False) -> str:
    source = value.strip()
    if not source:
        raise ValueError("LaTeX formula cannot be empty")
    parsed = LatexMathParser(source).parse()
    display_attribute = ' display="block"' if display else ""
    css_class = "math-display" if display else "math-inline"
    return (
        f'<math xmlns="http://www.w3.org/1998/Math/MathML"'
        f' class="{css_class}"{display_attribute}><mrow>{parsed}</mrow></math>'
    )


def resolve_link(target: str, source_path: Path | None) -> str:
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("#"):
        return target
    if source_path is None:
        return target
    resolved = (source_path.parent / target).resolve()
    return resolved.as_uri()


def inline_markup(value: str, source_path: Path | None = None) -> str:
    """Render the inline Markdown used across the repository without leaking syntax."""

    replacements: list[str] = []

    def stash(rendered: str) -> str:
        marker = f"\ufff0{len(replacements)}\ufff1"
        replacements.append(rendered)
        return marker

    def replace_placeholder(match: re.Match[str]) -> str:
        return stash(html.escape(match.group(0), quote=False))

    value = PLACEHOLDER_RE.sub(replace_placeholder, value)

    def replace_code(match: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(match.group(2), quote=False)}</code>")

    value = re.sub(r"(`+)(.+?)\1", replace_code, value)

    def replace_math(match: re.Match[str]) -> str:
        return stash(latex_math(match.group(1)))

    # Accept the two common inline delimiters. Code spans have already been
    # stashed, so dollar signs and backslashes inside code remain literal.
    value = re.sub(
        r"(?<!\\)\\\((.+?)(?<!\\)\\\)",
        replace_math,
        value,
    )
    value = re.sub(
        r"(?<!\\)\$(?!\$|\s)(.+?)(?<![\\\s])\$(?!\$)",
        replace_math,
        value,
    )

    def replace_image(match: re.Match[str]) -> str:
        alt = html.escape(match.group(1), quote=True)
        target = resolve_link(match.group(2), source_path)
        return stash(f'<img src="{html.escape(target, quote=True)}" alt="{alt}">')

    value = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, value)

    def replace_link(match: re.Match[str]) -> str:
        label = inline_markup(match.group(1), source_path)
        target = resolve_link(match.group(2), source_path)
        return stash(f'<a href="{html.escape(target, quote=True)}">{label}</a>')

    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, value)

    def replace_auto_link(match: re.Match[str]) -> str:
        target = match.group(1)
        escaped_target = html.escape(target, quote=True)
        label = html.escape(target, quote=False)
        return stash(f'<a href="{escaped_target}">{label}</a>')

    value = re.sub(r"<((?:https?://|mailto:)[^>]+)>", replace_auto_link, value)
    escaped = html.escape(value, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"__(.+?)__", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", escaped)
    # A single underscore is emphasis only when it is not part of a word or
    # filename.  This keeps names such as ``model_run_metadata.json`` intact.
    escaped = re.sub(
        r"(?<![\w_])_([^_\n]+)_(?![\w_])",
        r"<em>\1</em>",
        escaped,
    )
    escaped = escaped.replace(r"\$", "$").replace(r"\*", "*").replace(r"\_", "_")
    for index, rendered in enumerate(replacements):
        escaped = escaped.replace(f"\ufff0{index}\ufff1", rendered)
    return escaped


def display_math_start(line: str) -> tuple[str, str] | None:
    """Return the opening and closing delimiters for a display-math line."""

    stripped = line.strip()
    if stripped.startswith("$$"):
        return "$$", "$$"
    if stripped.startswith(r"\["):
        return r"\[", r"\]"
    return None


def consume_display_math(
    lines: list[str],
    index: int,
) -> tuple[str, int]:
    """Consume a display formula in same-line or multi-line delimiter form."""

    delimiters = display_math_start(lines[index])
    if delimiters is None:
        raise ValueError(f"Line {index + 1} is not a display-math block")
    opening, closing = delimiters
    stripped = lines[index].strip()
    first_line = stripped[len(opening):]

    if first_line.endswith(closing) and first_line[: -len(closing)].strip():
        return first_line[: -len(closing)].strip(), index + 1

    math_lines: list[str] = []
    if first_line.strip():
        math_lines.append(first_line.strip())
    index += 1
    while index < len(lines):
        candidate = lines[index].strip()
        if candidate == closing:
            return " ".join(math_lines), index + 1
        if candidate.endswith(closing):
            before_closing = candidate[: -len(closing)].strip()
            if before_closing:
                math_lines.append(before_closing)
            return " ".join(math_lines), index + 1
        math_lines.append(candidate)
        index += 1
    raise SystemExit(f"Unclosed Markdown display-math block opened with {opening}")


def is_special_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("<!--"):
        return True
    if stripped == "---":
        return True
    if stripped.startswith("```") or display_math_start(stripped) is not None:
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


def markdown_to_html(
    markdown: str,
    language: str,
    source_path: Path | None = None,
) -> str:
    """Convert the repository's Markdown into clean, print-ready HTML."""

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
        if stripped.startswith("```"):
            language_name = stripped[3:].strip()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise SystemExit("Unclosed Markdown code fence")
            index += 1
            if language_name.lower() in {"math", "latex", "tex"}:
                body.append(latex_math("\n".join(code_lines), display=True))
                continue
            class_name = (
                f' class="language-{html.escape(language_name, quote=True)}"'
                if language_name
                else ""
            )
            body.append(
                f"<pre><code{class_name}>"
                + html.escape("\n".join(code_lines), quote=False)
                + "</code></pre>"
            )
            continue
        if display_math_start(stripped) is not None:
            formula, index = consume_display_math(lines, index)
            body.append(latex_math(formula, display=True))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            body.append(
                f"<h{level}>{inline_markup(heading.group(2), source_path)}</h{level}>"
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
                f"<th>{inline_markup(cell, source_path)}</th>" for cell in header_cells
            )
            body.append("</tr></thead><tbody>")
            for row in rows:
                body.append("<tr>")
                body.extend(
                    f"<td>{inline_markup(cell, source_path)}</td>" for cell in row
                )
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
                + inline_markup(" ".join(quote_lines), source_path)
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
            body.extend(
                f"<li>{inline_markup(item, source_path)}</li>" for item in items
            )
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
            body.extend(
                f"<li>{inline_markup(item, source_path)}</li>" for item in items
            )
            body.append("</ol>")
            continue

        paragraph: list[str] = []
        while index < len(lines) and not is_special_start(lines, index):
            paragraph.append(lines[index].strip())
            index += 1
        if paragraph:
            body.append(
                "<p>"
                + inline_markup(" ".join(paragraph), source_path)
                + "</p>"
            )
            continue

        raise SystemExit(
            f"Markdown conversion stalled at line {index + 1}: {lines[index]}"
        )

    lang_code = "zh-CN" if language == "Chinese" else "en"
    css = """
      @page {
        size: A4;
        margin: 1.8cm;
        @bottom-center {
          content: counter(page);
          font-family: Arial, sans-serif;
          font-size: 9pt;
          color: #6b7280;
        }
      }
      body { font-family: Arial, sans-serif; font-size: 10.5pt;
             line-height: 1.42; color: #111827; }
      html[lang="zh-CN"] body {
        font-family: "Arial Unicode MS", "Songti SC", "Heiti SC",
                     "Hiragino Sans GB", sans-serif;
      }
      h1 { font-size: 20pt; color: #12355b; border-bottom: 2px solid #12355b;
           padding-bottom: 8px; }
      h2 { font-size: 15pt; color: #12355b; margin-top: 22px; }
      h3 { font-size: 12pt; color: #234e70; margin-top: 16px; }
      h1, h2, h3 { break-after: avoid-page; page-break-after: avoid; }
      p, li { orphans: 3; widows: 3; }
      p, blockquote { break-inside: avoid-page; page-break-inside: avoid; }
      p:has(+ ol), p:has(+ ul), p:has(+ table), p:has(+ math.math-display) {
        break-after: avoid-page; page-break-after: avoid;
      }
      ol, ul { break-inside: avoid-page; page-break-inside: avoid; }
      code { font-family: "SFMono-Regular", Consolas, "Arial Unicode MS", monospace;
             font-size: 0.92em;
             background: #f3f4f6; border-radius: 3px; padding: 1px 3px; }
      pre { white-space: pre-wrap; overflow-wrap: anywhere; background: #f3f4f6;
            border: 1px solid #d1d5db; border-radius: 4px; padding: 9px;
            page-break-inside: avoid; }
      pre code { background: transparent; padding: 0; }
      a { color: #1d4ed8; text-decoration: underline; }
      img { display: block; max-width: 100%; max-height: 20cm; margin: 10px auto;
            object-fit: contain; page-break-inside: avoid; }
      math { font-family: "STIX Two Math", "Cambria Math", "Times New Roman", serif; }
      math.math-inline { font-size: 1.02em; }
      math.math-display { font-size: 1.12em; margin: 8px auto 12px;
                          break-before: avoid-page; page-break-before: avoid;
                          page-break-inside: avoid; }
      table { width: 100%; border-collapse: collapse; margin: 8px 0 14px;
              font-size: 8.8pt; page-break-inside: auto; }
      thead { display: table-header-group; }
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


WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WORD = f"{{{WORD_NS}}}"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
OFFICE_REL = f"{{{OFFICE_REL_NS}}}"
PACKAGE_REL = f"{{{PACKAGE_REL_NS}}}"
CONTENT_TYPES = f"{{{CONTENT_TYPES_NS}}}"
ET.register_namespace("w", WORD_NS)
ET.register_namespace("r", OFFICE_REL_NS)


def _ensure_paragraph_property(paragraph: ET.Element, property_name: str) -> None:
    """Add a one-value paragraph property while preserving the paragraph text."""

    properties = paragraph.find(f"{WORD}pPr")
    if properties is None:
        properties = ET.Element(f"{WORD}pPr")
        paragraph.insert(0, properties)
    if properties.find(f"{WORD}{property_name}") is None:
        value = ET.SubElement(properties, f"{WORD}{property_name}")
        value.set(f"{WORD}val", "1")


def _paragraph_style(paragraph: ET.Element) -> str:
    style = paragraph.find(f"{WORD}pPr/{WORD}pStyle")
    if style is None:
        return ""
    return style.attrib.get(f"{WORD}val", "")


def _page_number_footer() -> bytes:
    """Return a centred PAGE field for a DOCX footer part."""

    footer = ET.Element(f"{WORD}ftr")
    paragraph = ET.SubElement(footer, f"{WORD}p")
    paragraph_properties = ET.SubElement(paragraph, f"{WORD}pPr")
    alignment = ET.SubElement(paragraph_properties, f"{WORD}jc")
    alignment.set(f"{WORD}val", "center")

    begin_run = ET.SubElement(paragraph, f"{WORD}r")
    begin = ET.SubElement(begin_run, f"{WORD}fldChar")
    begin.set(f"{WORD}fldCharType", "begin")

    instruction_run = ET.SubElement(paragraph, f"{WORD}r")
    instruction = ET.SubElement(instruction_run, f"{WORD}instrText")
    instruction.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    instruction.text = " PAGE "

    separate_run = ET.SubElement(paragraph, f"{WORD}r")
    separate = ET.SubElement(separate_run, f"{WORD}fldChar")
    separate.set(f"{WORD}fldCharType", "separate")

    result_run = ET.SubElement(paragraph, f"{WORD}r")
    result = ET.SubElement(result_run, f"{WORD}t")
    result.text = "1"

    end_run = ET.SubElement(paragraph, f"{WORD}r")
    end = ET.SubElement(end_run, f"{WORD}fldChar")
    end.set(f"{WORD}fldCharType", "end")
    return ET.tostring(footer, encoding="utf-8", xml_declaration=True)


def resolve_soffice(explicit_path: str | None) -> Path:
    """Locate LibreOffice Writer for a table-preserving HTML-to-DOCX export."""

    candidates = []
    if explicit_path:
        candidates.append(Path(explicit_path))
    discovered = shutil.which("soffice")
    if discovered:
        candidates.append(Path(discovered))
    candidates.append(Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"))

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise SystemExit(
        "LibreOffice 'soffice' was not found. Install LibreOffice, put soffice "
        "on PATH, or pass --soffice /absolute/path/to/soffice."
    )


def run_soffice_convert(soffice: Path, html_path: Path, output_dir: Path) -> Path:
    """Convert one HTML file to DOCX using an isolated LibreOffice profile."""

    profile = output_dir / "libreoffice-profile"
    export_dir = output_dir / "word-export"
    profile.mkdir()
    export_dir.mkdir()
    command = [
        str(soffice),
        f"-env:UserInstallation={profile.resolve().as_uri()}",
        "--headless",
        "--convert-to",
        "docx:Office Open XML Text",
        "--outdir",
        str(export_dir),
        str(html_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    converted = export_dir / html_path.with_suffix(".docx").name
    if result.returncode != 0 or not converted.exists():
        details = (result.stderr or result.stdout).strip()
        raise SystemExit(f"LibreOffice DOCX conversion failed: {details}")
    return converted


def _scaled_widths(widths: list[int], target: int) -> list[int]:
    """Scale integer column widths to an exact total while preserving ratios."""

    total = sum(widths)
    if total <= 0:
        widths = [1] * len(widths)
        total = len(widths)
    raw = [width * target / total for width in widths]
    scaled = [max(1, int(value)) for value in raw]
    remainder = target - sum(scaled)
    order = sorted(
        range(len(widths)),
        key=lambda index: raw[index] - int(raw[index]),
        reverse=remainder > 0,
    )
    for offset in range(abs(remainder)):
        index = order[offset % len(order)]
        scaled[index] += 1 if remainder > 0 else -1
    return scaled


def _scaled_widths_with_floor(widths: list[int], target: int) -> list[int]:
    """Scale widths while reserving space for IDs and other narrow columns."""

    if not widths:
        return []
    floors = [int(target * 0.17)] + [int(target * 0.08)] * (len(widths) - 1)
    reserved = sum(floors)
    if reserved >= target:
        return _scaled_widths([1] * len(widths), target)
    additions = _scaled_widths(widths, target - reserved)
    return [floor + addition for floor, addition in zip(floors, additions, strict=True)]


def normalize_docx_table_geometry(path: Path) -> None:
    """Fit tables and add stable pagination features to the Word export."""

    with zipfile.ZipFile(path, "r") as source_archive:
        entries = [
            (item, source_archive.read(item.filename))
            for item in source_archive.infolist()
        ]
    payloads = {item.filename: payload for item, payload in entries}
    root = ET.fromstring(payloads["word/document.xml"])

    section = root.find(f".//{WORD}sectPr")
    if section is None:
        raise SystemExit("DOCX table audit failed: no section geometry found")
    page_size = section.find(f"{WORD}pgSz")
    page_margin = section.find(f"{WORD}pgMar")
    if page_size is None or page_margin is None:
        raise SystemExit("DOCX table audit failed: incomplete page geometry")
    page_width = int(page_size.attrib[f"{WORD}w"])
    left_margin = int(page_margin.attrib[f"{WORD}left"])
    right_margin = int(page_margin.attrib[f"{WORD}right"])
    usable_width = page_width - left_margin - right_margin
    if usable_width <= 0:
        raise SystemExit("DOCX table audit failed: nonpositive usable page width")

    body = root.find(f".//{WORD}body")
    if body is None:
        raise SystemExit("DOCX layout audit failed: no document body found")

    body_children = list(body)
    for index, child in enumerate(body_children):
        if child.tag != f"{WORD}p":
            continue
        style = _paragraph_style(child)
        next_child = body_children[index + 1] if index + 1 < len(body_children) else None
        next_style = (
            _paragraph_style(next_child)
            if next_child is not None and next_child.tag == f"{WORD}p"
            else ""
        )
        if (
            style.startswith("Heading")
            or (next_child is not None and next_child.tag == f"{WORD}tbl")
            or next_style == "BlockQuotation"
        ):
            _ensure_paragraph_property(child, "keepNext")

    tables = root.findall(f".//{WORD}tbl")
    for table in tables:
        grid = table.find(f"{WORD}tblGrid")
        if grid is None:
            continue
        columns = grid.findall(f"{WORD}gridCol")
        if not columns:
            continue
        original_widths = [
            int(column.attrib.get(f"{WORD}w", "1")) for column in columns
        ]
        scaled_widths = _scaled_widths_with_floor(original_widths, usable_width)
        for column, width in zip(columns, scaled_widths, strict=True):
            column.set(f"{WORD}w", str(width))

        table_properties = table.find(f"{WORD}tblPr")
        if table_properties is None:
            table_properties = ET.Element(f"{WORD}tblPr")
            table.insert(0, table_properties)
        table_width = table_properties.find(f"{WORD}tblW")
        if table_width is None:
            table_width = ET.SubElement(table_properties, f"{WORD}tblW")
        table_width.set(f"{WORD}type", "dxa")
        table_width.set(f"{WORD}w", str(usable_width))
        table_indent = table_properties.find(f"{WORD}tblInd")
        if table_indent is None:
            table_indent = ET.SubElement(table_properties, f"{WORD}tblInd")
        table_indent.set(f"{WORD}type", "dxa")
        table_indent.set(f"{WORD}w", "0")
        table_layout = table_properties.find(f"{WORD}tblLayout")
        if table_layout is None:
            table_layout = ET.SubElement(table_properties, f"{WORD}tblLayout")
        table_layout.set(f"{WORD}type", "fixed")

        rows = table.findall(f"{WORD}tr")
        for row_index, row in enumerate(rows):
            row_properties = row.find(f"{WORD}trPr")
            if row_properties is None:
                row_properties = ET.Element(f"{WORD}trPr")
                row.insert(0, row_properties)
            for row_height in row_properties.findall(f"{WORD}trHeight"):
                row_properties.remove(row_height)
            for repeated_header in row_properties.findall(f"{WORD}tblHeader"):
                row_properties.remove(repeated_header)
            if row_index == 0:
                repeated_header = ET.SubElement(row_properties, f"{WORD}tblHeader")
                repeated_header.set(f"{WORD}val", "1")
            cannot_split = row_properties.find(f"{WORD}cantSplit")
            if cannot_split is None:
                cannot_split = ET.SubElement(row_properties, f"{WORD}cantSplit")
            cannot_split.set(f"{WORD}val", "1")
            column_index = 0
            for cell in row.findall(f"{WORD}tc"):
                cell_properties = cell.find(f"{WORD}tcPr")
                if cell_properties is None:
                    cell_properties = ET.Element(f"{WORD}tcPr")
                    cell.insert(0, cell_properties)
                if column_index == 0 and cell_properties.find(f"{WORD}noWrap") is None:
                    ET.SubElement(cell_properties, f"{WORD}noWrap")
                span_element = cell_properties.find(f"{WORD}gridSpan")
                span = (
                    int(span_element.attrib.get(f"{WORD}val", "1"))
                    if span_element is not None
                    else 1
                )
                end_index = min(column_index + span, len(scaled_widths))
                cell_width_value = sum(scaled_widths[column_index:end_index])
                cell_width = cell_properties.find(f"{WORD}tcW")
                if cell_width is None:
                    cell_width = ET.SubElement(cell_properties, f"{WORD}tcW")
                cell_width.set(f"{WORD}type", "dxa")
                cell_width.set(f"{WORD}w", str(cell_width_value))
                column_index = end_index
                if row_index == 0:
                    for paragraph in cell.findall(f".//{WORD}p"):
                        _ensure_paragraph_property(paragraph, "keepNext")

    relationship_path = "word/_rels/document.xml.rels"
    relationship_payload = payloads[relationship_path]
    relationship_root = ET.fromstring(relationship_payload)
    relationship_ids = {
        relationship.attrib.get("Id", "")
        for relationship in relationship_root.findall(f"{PACKAGE_REL}Relationship")
    }
    footer_relationship_id = "rIdPageNumberFooter"
    if footer_relationship_id in relationship_ids:
        raise SystemExit("DOCX layout audit failed: footer relationship ID collision")
    relationship_closing = b"</Relationships>"
    if relationship_closing not in relationship_payload:
        raise SystemExit("DOCX layout audit failed: malformed relationship part")
    footer_relationship = (
        f'<Relationship Id="{footer_relationship_id}" '
        f'Type="{OFFICE_REL_NS}/footer" Target="footer1.xml"/>'
    ).encode("utf-8")
    payloads[relationship_path] = relationship_payload.replace(
        relationship_closing,
        footer_relationship + relationship_closing,
        1,
    )

    footer_reference = ET.Element(f"{WORD}footerReference")
    footer_reference.set(f"{OFFICE_REL}id", footer_relationship_id)
    footer_reference.set(f"{WORD}type", "default")
    section.insert(0, footer_reference)
    page_margin.set(f"{WORD}footer", "425")

    content_types_path = "[Content_Types].xml"
    content_types_payload = payloads[content_types_path]
    content_types_root = ET.fromstring(content_types_payload)
    footer_part_name = "/word/footer1.xml"
    has_footer_type = any(
        override.attrib.get("PartName") == footer_part_name
        for override in content_types_root.findall(f"{CONTENT_TYPES}Override")
    )
    if not has_footer_type:
        content_types_closing = b"</Types>"
        if content_types_closing not in content_types_payload:
            raise SystemExit("DOCX layout audit failed: malformed content-types part")
        footer_override = (
            '<Override PartName="/word/footer1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.footer+xml"/>'
        ).encode("utf-8")
        content_types_payload = content_types_payload.replace(
            content_types_closing,
            footer_override + content_types_closing,
            1,
        )
    payloads[content_types_path] = content_types_payload

    payloads["word/document.xml"] = ET.tostring(
        root, encoding="utf-8", xml_declaration=True
    )
    temporary_path = path.with_suffix(".table-geometry.docx")
    with zipfile.ZipFile(
        temporary_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as output_archive:
        for item, original_payload in entries:
            output_archive.writestr(
                item,
                payloads.get(item.filename, original_payload),
            )
        output_archive.writestr("word/footer1.xml", _page_number_footer())
    temporary_path.replace(path)


def extract_docx_text(path: Path) -> str:
    """Extract paragraph text directly from OOXML for sentinel validation."""

    with zipfile.ZipFile(path, "r") as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs = []
    for paragraph in root.findall(f".//{WORD}p"):
        paragraphs.append(
            "".join(node.text or "" for node in paragraph.findall(f".//{WORD}t"))
        )
    return "\n".join(paragraphs)


def set_docx_east_asia_font(path: Path, font_name: str) -> None:
    """Force a valid OOXML East Asian font throughout the converted DOCX.

    LibreOffice can serialise a CSS fallback list as one invalid Word font name
    (for example ``Arial Unicode MS;Songti SC;...``).  Merely adding a missing
    ``w:eastAsia`` attribute does not repair those existing values, so replace
    every value and add the attribute only where it is absent.
    """

    font_bytes = html.escape(font_name, quote=True).encode("utf-8")
    font_attribute_patterns = {
        attribute: re.compile(rb"\bw:" + attribute + rb'="[^"]*"')
        for attribute in (b"ascii", b"hAnsi", b"eastAsia", b"cs")
    }
    rfonts_pattern = re.compile(rb"<w:rFonts\b([^>]*)/>")
    with zipfile.ZipFile(path, "r") as source_archive:
        entries = [
            (
                item,
                source_archive.read(item.filename),
            )
            for item in source_archive.infolist()
        ]

    temporary_path = path.with_suffix(".east-asia-font.docx")
    with zipfile.ZipFile(
        temporary_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as output_archive:
        for item, payload in entries:
            if item.filename.startswith("word/") and item.filename.endswith(".xml"):
                payload = rfonts_pattern.sub(
                    lambda match: b"<w:rFonts"
                    + _force_font_attributes(
                        match.group(1), font_attribute_patterns, font_bytes
                    )
                    + b"/>",
                    payload,
                )
            output_archive.writestr(item, payload)
    temporary_path.replace(path)


def _force_font_attributes(
    attributes: bytes,
    patterns: dict[bytes, re.Pattern[bytes]],
    font_name: bytes,
) -> bytes:
    """Replace or add every Word script-specific font attribute."""

    updated = attributes
    for attribute, pattern in patterns.items():
        replacement = b'w:' + attribute + b'="' + font_name + b'"'
        if pattern.search(updated):
            updated = pattern.sub(replacement, updated)
        else:
            updated += b" " + replacement
    return updated


def build_document(document: Document, source_text: str, soffice: Path) -> None:
    html_text = markdown_to_html(source_text, document.language, document.source)
    with tempfile.TemporaryDirectory(prefix="epq-production-log-") as temp_dir:
        temp = Path(temp_dir)
        html_path = temp / f"{document.output.stem}.html"
        html_path.write_text(html_text, encoding="utf-8")
        converted = run_soffice_convert(soffice, html_path, temp)
        normalize_docx_table_geometry(converted)
        if document.language == "Chinese":
            set_docx_east_asia_font(converted, "STSong")

        round_trip = extract_docx_text(converted)
        sentinels = (
            document.title_sentinel,
            "PL-00.01",
            "PL-17.03",
            "{{CANDIDATE_FULL_NAME}}",
            "0.00098301",
            "5,402",
            "{{SUPERVISOR_FINAL_PACKAGE_CHECK}}",
        )
        missing = [sentinel for sentinel in sentinels if sentinel not in round_trip]
        if missing:
            raise SystemExit(
                f"Word round-trip validation failed for {document.output.name}: "
                f"missing {missing}"
            )
        shutil.copy2(converted, document.output)

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
    parser.add_argument(
        "--soffice",
        help="absolute path to LibreOffice soffice (otherwise resolved from PATH)",
    )
    args = parser.parse_args()

    english, chinese = validate_pair()
    if args.check_only:
        return
    soffice = resolve_soffice(args.soffice)
    for document, source_text in zip(DOCUMENTS, (english, chinese), strict=True):
        build_document(document, source_text, soffice)


if __name__ == "__main__":
    main()
