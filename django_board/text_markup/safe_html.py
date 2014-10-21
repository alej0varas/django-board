HTML_TRANSLATION_TABLE = [
    # to avoide conflicts ('&', '&amp;') will be separated
    ('<', '&lt;'),
    ('>', '&gt;'),
    ("'", '&#39;'),  # single quote
    ('"', '&quot'),  # double quote
]


def escape_html(text):
    """Replace HTML symbols by it's safe equivalent."""

    safe_text = text.translate(str.maketrans({'&': '&amp;'}))
    safe_text = text.translate(str.maketrans(
        dict(HTML_TRANSLATION_TABLE)
        ))

    return(safe_text)


def unescape_html(text):
    """Replace escaped HTML symbols by it's original equivalent."""

    unescaped_text = text

    for original, safe in HTML_TRANSLATION_TABLE:
        unescaped_text = unescaped_text.replace(safe, original)
    unescaped_text = unescaped_text.replace('&amp;', '&')

    return(unescaped_text)
