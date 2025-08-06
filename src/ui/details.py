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

def render_link(link: Link) -> HTML:
    return f"""
        <blockquote style="margin-top: 1em; border-left: 2px solid #ccc; padding-left: 1em;">
            <p>
                <a href="{link.link}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit;">
                    <i>"{link.text}"</i>
                </a>
            </p>
            <footer>— {link.author}</footer>
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
