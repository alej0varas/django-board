import re


ESCAPING_TABLE = [
    ('\>', '>'),
    ('\*', '*'),
    ('\`', '`'),
    ('\_', '_'),
    ('\~', '~'),
    ('\%', '%'),
    ('\-', '-'),
]


def make_formatter_by_regex(pattern, repl, text, flags=0):
    def formatter():
        formatted_text = re.sub(pattern, repl, text, flags=flags)
        return(formatted_text)
    return(formatter)


def format_quotes(text):
    formatted_lines = []

    for line in text.splitlines():
        formatter = make_formatter_by_regex(
            '^&gt;\s?(?P<quoted>.*)$',  # "&gt; QUOTE" ("> QUOTE")
            '<blockquote>\g<quoted></blockquote>', line)
        formatted_lines.append(formatter())

    return("\n".join(formatted_lines))


def format_bold(text):
    formatter = make_formatter_by_regex(
        '\*\*(?P<boldtext>.+?(?=\*\*))\*\*',  # **BOLD TEXT**
        '<strong>\g<boldtext></strong>', text, flags=re.DOTALL)
    return(formatter())


def format_emphasized(text):
    formatter = make_formatter_by_regex('\*(?P<emphasized>[^\*]+)\*',  # *EM*
                                        '<em>\g<emphasized></em>', text)
    return(formatter())


def format_underline(text):
    formatter = make_formatter_by_regex(
        '__(?P<underlined>.+?(?=__))__',  # __underlined__
        '<u>\g<underlined></u>', text, flags=re.DOTALL)
    return(formatter())


def format_strikethrough(text):
    formatter = make_formatter_by_regex(
        '~~(?P<strikethrough>.+?(?=~~))~~',
        '<del>\g<strikethrough></del>', text, flags=re.DOTALL)
    return(formatter())


def format_inline_code(text):
    formatter = make_formatter_by_regex('`(?P<code>.+)`',  # `CODE`
                                        '<code>\g<code></code>', text)
    return(formatter())


def format_multiline_code(text):
    formatter = make_formatter_by_regex(  # ``CODE
        '```(?P<code>(.|\n)+)```',         # ...``
        '<pre><code>\g<code></code></pre>', text, flags=re.DOTALL)
    return(formatter())


def format_spoilers(text):
    formatter = make_formatter_by_regex(
        '%%(?P<spoilered>.+?(?=%%))%%',  # %%spoiler (\n)%%
        '<span class="spoiler">\g<spoilered></span>',
        text, flags=re.DOTALL)
    return(formatter())


def format_hyphens_to_dashes(text):
    formatter = make_formatter_by_regex(
        '(?P<before>\s|\A)-(?P<after>\s|\Z)',  # "a - a" or "- a"
        '\g<before>—\g<after>', text)
    return(formatter())


def escape_formatting(text):
    for unescaped, escaped in ESCAPING_TABLE:
        text = text.replace(unescaped, escaped)
    return(text)
