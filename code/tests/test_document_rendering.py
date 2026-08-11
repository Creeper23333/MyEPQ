from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "production-log"))

from build_documents import inline_markup, latex_math, markdown_to_html


QLIKE_FORMULA = (
    r"v_t=\max(y_t^2,\varepsilon),\quad "
    r"\hat v_t=\max(\hat y_t^2,\varepsilon),\quad "
    r"QLIKE=\frac1m\sum_{t=1}^m"
    r"\left(\frac{v_t}{\hat v_t}-\ln\frac{v_t}{\hat v_t}-1\right)"
)


class DocumentRenderingTests(unittest.TestCase):
    def test_qlike_formula_converts_to_native_mathml(self) -> None:
        rendered = latex_math(QLIKE_FORMULA, display=True)
        self.assertIn("<math", rendered)
        self.assertIn("<mfrac>", rendered)
        self.assertIn('mathvariant="normal">max</mi>', rendered)
        self.assertNotIn(r"\frac", rendered)
        self.assertNotIn(r"\max", rendered)

        inline = inline_markup(
            r"Dollar $x_t^2$ and parenthesised \(y_t^2\)."
        )
        self.assertEqual(inline.count('class="math-inline"'), 2)
        self.assertEqual(inline.count("<msubsup>"), 2)

        literal = inline_markup(r"`$not_math$`, \$5 and \$10")
        self.assertIn("<code>$not_math$</code>", literal)
        self.assertIn("$5 and $10", literal)
        self.assertNotIn("<math", literal)
        self.assertEqual(
            inline_markup("The range is $5 to $10."),
            "The range is $5 to $10.",
        )
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            latex_math("  ")

    def test_markdown_display_math_does_not_leak_latex_source(self) -> None:
        markdown = f"# Formula\n\n$$\n{QLIKE_FORMULA}\n$$\n"
        rendered = markdown_to_html(markdown, "English", ROOT / "report/final-report.md")
        self.assertIn('display="block"', rendered)
        self.assertNotIn(r"\frac", rendered)
        self.assertNotIn(r"\varepsilon", rendered)

        samples = (
            "$$\nx_t^2\n$$",
            "$$x_t^2$$",
            "\\[\nx_t^2\n\\]",
            "\\[x_t^2\\]",
            "```math\nx_t^2\n```",
            "```latex\nx_t^2\n```",
        )
        for markdown in samples:
            with self.subTest(markdown=markdown):
                rendered = markdown_to_html(markdown, "English")
                self.assertIn('class="math-display"', rendered)
                self.assertIn("<msubsup>", rendered)
                self.assertNotIn("<pre>", rendered)


if __name__ == "__main__":
    unittest.main()
