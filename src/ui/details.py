from collections.abc import Sequence
from typing import assert_never
import gradio

from chat.types import Citation, Link, Quote


HTML = str


def render_citation(citation: Citation) -> HTML:
    return f"""
        <blockquote style="margin-top: 1em; border-left: 2px solid #ccc; padding-left: 1em;">
            <p><i>"{citation.text}"</i></p>
            <footer>— {citation.author}</footer>
        </blockquote>
    """

from typing import Literal
from html import escape
from .types import Link

def render_link(link: Link) -> HTML:
    safe_url    = escape(link.link, quote=True)
    safe_text   = escape(link.text)
    safe_author = escape(link.author)

    return f"""
        <blockquote style="margin-top: 1em; border-left: 2px solid #ccc; padding-left: 1em;">
            <p>
                <a href="{safe_url}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit;">
                    <i>"{safe_text}"</i>
                </a>
            </p>
            <footer>— {safe_author}</footer>
        </blockquote>
    """



def render_quote(quote: Quote) -> HTML:
    match quote:
        case Link():
            return render_link(quote)
        case Citation():
            return render_citation(quote)

    assert_never(quote)


def render_quotes(quotes: Sequence[Quote], title: str = "Citations"):
    if len(quotes) == 0:
        return ""

    rendered_quotes = "\n".join(render_quote(quote) for quote in quotes)
    return gradio.HTML(f"""
        <details>
            <summary>
            {title}
            </summary>
            {rendered_quotes}
        </details>
    """)
