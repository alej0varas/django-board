import unittest
from .formatters import (
    format_bold,
    format_emphasized,
    format_underline,
    format_strikethrough,
    format_quotes,
    format_inline_code,
    format_multiline_code,
    format_spoilers,
    format_hyphens_to_dashes,
    escape_formatting,
)


class QuotesTests(unittest.TestCase):
    """Quotes formatting tests."""

    def test_quote_only(self):
        """Test one-line text with quote."""
        text = format_quotes("&gt; quoted text")
        self.assertEqual(text, "<blockquote>quoted text</blockquote>")

    def test_quote_with_other_text(self):
        text = format_quotes("line 1\n&gt; quoted line\nline 3")

        quoted_text = "line 1\n" \
                      "<blockquote>quoted line</blockquote>\n" \
                      "line 3"

        self.assertEqual(text, quoted_text)

    def test_wrongly_quoted_text(self):
        text = format_quotes("some text &gt; quote")
        self.assertEqual(text, "some text &gt; quote")


class BoldTextTests(unittest.TestCase):
    """Bold text formatting tests."""

    def test_whole_line_bold(self):
        text = format_bold("**bold text**")
        self.assertEqual(text, "<strong>bold text</strong>")

    def test_inline_bold(self):
        text = format_bold("normal **bold** normal")
        self.assertEqual(text, "normal <strong>bold</strong> normal")

    def test_multiline_bold(self):
        text = format_bold("**start\n\nend**")
        self.assertEqual(text, "<strong>start\n\nend</strong>")


class EmphasizedTextTests(unittest.TestCase):
    """Emphasized text formatting tests."""""

    def test_whole_line_emphasized(self):
        text = format_emphasized("*emphasized text*")
        self.assertEqual(text, "<em>emphasized text</em>")

    def test_inline_emphasized(self):
        text = format_emphasized("normal *emphasized* normal")
        self.assertEqual(text, "normal <em>emphasized</em> normal")

    def test_multiline_emphasized(self):
        text = format_emphasized("*emphasized\nemphasized\nemphasized*")
        self.assertEqual(
            text,
            "<em>emphasized\nemphasized\nemphasized</em>")


class UnderlineTextTests(unittest.TestCase):
    """Underline text formatting tests."""

    def test_whole_line_underlined(self):
        text = format_underline("__underlined text__")
        self.assertEqual(text, "<u>underlined text</u>")

    def test_inline_underline(self):
        text = format_underline("normal __underlined__ normal")
        self.assertEqual(text, "normal <u>underlined</u> normal")

    def test_multiline_underline(self):
        text = format_underline("__line 1\nline 2\nline 3__")
        self.assertEqual(text, "<u>line 1\nline 2\nline 3</u>")


class StrikethroughTests(unittest.TestCase):
    """Strikethrough text formatting tests."""

    def test_whole_line_strikethrough(self):
        text = format_strikethrough("~~strikethrough~~")
        self.assertEqual(text, "<del>strikethrough</del>")

    def test_inline_strikethrough(self):
        text = format_strikethrough("normal ~~strikethrough~~ normal")
        self.assertEqual(text, "normal <del>strikethrough</del> normal")

    def test_multiline_strikethrough(self):
        text = format_strikethrough("~~line 1\nline 2\nline 3~~")
        self.assertEqual(text, "<del>line 1\nline 2\nline 3</del>")


class InlineCodeTests(unittest.TestCase):
    """Monospaced text formatting tests. Uses `inline text`."""

    def test_whole_line_code(self):
        text = format_inline_code("`code code code`")
        self.assertEqual(text, "<code>code code code</code>")

    def test_inline_code(self):
        text = format_inline_code("normal text `monospaced` normal text")

        self.assertEqual(text,
                         "normal text <code>monospaced</code> normal text")

    def test_multiline_code_dont_work(self):
        text = format_inline_code("`code\ncode`")
        self.assertEqual(text, "`code\ncode`")


class MultilineCodeTests(unittest.TestCase):
    """Monospaced text formatting tests. Uses ```multi-line text```."""

    def test_code_only(self):
        text = format_multiline_code("```line 1\nline 2\nline 3```")

        self.assertEqual(text,
                         "<pre><code>line 1\nline 2\nline 3</code></pre>")

    def test_code_with_other_text(self):
        text = format_multiline_code(
            "normal text ```multi-line\ncode``` normal text")

        self.assertEqual(
            text,
            "normal text <pre><code>multi-line\ncode</code></pre> normal text")


class SpoilersTests(unittest.TestCase):
    """Spoilered text tests."""

    def test_spoiler_only(self):
        text = format_spoilers('%%spoiler%%')
        self.assertEqual(text, '<span class="spoiler">spoiler</span>')

    def test_inline_spoiler(self):
        text = format_spoilers('normal %%spoilered%% normal')
        self.assertEqual(
            text,
            'normal <span class="spoiler">spoilered</span> normal')

    def test_multiline_spoiler(self):
        text = format_spoilers('%%line 1\nline 2\nline 3%%')
        self.assertEqual(
            text,
            '<span class="spoiler">line 1\nline 2\nline 3</span>')


class HyphensToDashesTests(unittest.TestCase):
    """Tests for converting hyphens surrounded by spaces to dashes."""

    def test_hyphen_surrounded_by_spaces(self):
        text = format_hyphens_to_dashes("to - dash")
        self.assertEqual(text, "to — dash")

    def test_hyphen_at_beginning_of_line(self):
        text = format_hyphens_to_dashes("- to dash")
        self.assertEqual(text, "— to dash")

    def test_hyphen_at_end_of_line(self):
        text = format_hyphens_to_dashes("to dash -")
        self.assertEqual(text, "to dash —")

    def test_single_hyphen(self):
        text = format_hyphens_to_dashes("-")
        self.assertEqual(text, "—")

    def test_hyphen_between_two_chars(self):
        text = format_hyphens_to_dashes("a-b")
        self.assertEqual(text, "a-b")


class BasicEscapingTests(unittest.TestCase):
    """Tests for escaping characters and avoiding formatting."""

    def test_escaping_quotes(self):
        text = escape_formatting('\&gt;escaped quote')
        self.assertEqual(text, '&gt;escaped quote')

    def test_escaping_bold(self):
        text = escape_formatting('\*\*not bold\*\*')
        self.assertEqual(text, '**not bold**')

    def test_escaping_emphasized(self):
        text = escape_formatting('\*not emphasized\*')
        self.assertEqual(text, '*not emphasized*')

    def test_escaping_underlined(self):
        text = escape_formatting('\_\_not underlined\_\_')
        self.assertEqual(text, '__not underlined__')

    def test_escaping_strikethrough(self):
        text = escape_formatting('\~\~not strikethrough\~\~')
        self.assertEqual(text, '~~not strikethrough~~')

    def test_escaping_inline_code(self):
        text = escape_formatting('\`not monospaced\`')
        self.assertEqual(text, '`not monospaced`')

    def test_escaping_multiline_code(self):
        text = escape_formatting('\`\`\`not\nmultiline code\`\`\`')
        self.assertEqual(text, '```not\nmultiline code```')

    def test_escaping_spoilers(self):
        text = escape_formatting('\%\%not spoiler\%\%')
        self.assertEqual(text, '%%not spoiler%%')

    def test_escaping_hyphens(self):
        text = escape_formatting('a \- b')
        self.assertEqual(text, 'a - b')


class ComplexEscapingTests(unittest.TestCase):
    """Complex and mixed tests for escaping characters."""

    def test_escape_bold_and_emphasized_text(self):
        text = escape_formatting("\*\*\*not bold nor emphasized\*\*\*")
        self.assertEqual(text, "***not bold nor emphasized***")

    def test_escape_bold_and_underlined_text(self):
        text = escape_formatting("\_\_\*\*not bold nor underlined\*\*\_\_")
        self.assertEqual(text, "__**not bold nor underlined**__")

    def test_escape_bold_and_strikedthrough_text(self):
        text = escape_formatting("\~\~\*\*not bold nor strikedthrough\*\*\~\~")
        self.assertEqual(text, "~~**not bold nor strikedthrough**~~")

    def test_escape_bold_inline_code(self):
        text = escape_formatting("\`\*\*not bold code\*\*\`")
        self.assertEqual(text, "`**not bold code**`")

    def test_escape_bold_multiline_code(self):
        text = escape_formatting("\`\`\`\*\*not bold code\*\*\`\`\`")
        self.assertEqual(text, "```**not bold code**```")

    def test_escape_bold_spoilered_text(self):
        text = escape_formatting("\%\%\*\*not bold spoiler\*\*\%\%")
        self.assertEqual(text, "%%**not bold spoiler**%%")

















if __name__ == '__main__':
    unittest.main()
