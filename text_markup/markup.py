from .safe_html import escape_html
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


DEFAULT_FORMATTERS = [
    format_bold,
    format_emphasized,
    format_underline,
    format_strikethrough,
    format_quotes,
    format_multiline_code,
    format_inline_code,
    format_spoilers,
    format_hyphens_to_dashes,
    escape_formatting,
]


def get_markup(text, formatters=DEFAULT_FORMATTERS):
    """Main markup function. Pass the text to format and
    formatters (optionally)."""

    safe_text = escape_html(text)

    for formatter in formatters:
        safe_text = formatter(safe_text)

    return(safe_text)
