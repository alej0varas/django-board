HTML_TRANSLATION_TABLE = {
    # to avoid conflicts '&': '&amp;' will be separated
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',  # single quote
    '"': '&quot;'  # double quote
}


def main(text):
    final_lines = list()
    safe_lines = escape_html(text).splitlines()

    for line in safe_lines:
        line = process_quotes(line)

        final_lines.append(line)

    return('\n'.join(final_lines))


def escape_html(text):
    """A function that replaces HTML symbols by it's safe equivalent."""

    safe_text = text.translate(str.maketrans({'&': '&amp;'}))
    safe_text = text.translate(str.maketrans(HTML_TRANSLATION_TABLE))
    return(safe_text)


def unescape_html(text):
    """A function that replaces escaped HTML symbols
    by it's original equivalent."""

    unescaped_text = text

    for original, safe in HTML_TRANSLATION_TABLE.items():
        unescaped_text = unescaped_text.replace(safe, original)
    unescaped_text = unescaped_text.replace('&amp;', '&')

    return(unescaped_text)


def process_quotes(text):
    """A function that wraps string that starts with '> '
    in <blockquote> HTML tag."""

    if text.startswith('&gt; '):
        text = text.replace('&gt; ', '<blockquote>', 1) + '</blockquote>'

    return(text)
