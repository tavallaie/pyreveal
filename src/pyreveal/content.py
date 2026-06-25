from __future__ import annotations

import re
from abc import ABC, abstractmethod
from html import escape

_HTML_TAG_RE = re.compile(r"<[a-zA-Z][^>]*>")


def looks_like_html(text: str) -> bool:
    return bool(_HTML_TAG_RE.search(text.strip()))


class Content(ABC):
    """Structured slide body content (rendered to HTML)."""

    @abstractmethod
    def to_html(self) -> str:
        raise NotImplementedError


class RawHTML(Content):
    """Raw HTML block (escape hatch — prefer slide.title(), slide.text(), etc.)."""

    def __init__(self, html: str):
        self.html = html

    def to_html(self) -> str:
        return self.html


class Heading(Content):
    def __init__(self, text: str, level: int = 2):
        if level not in range(1, 7):
            raise ValueError("heading level must be between 1 and 6")
        self.text = text
        self.level = level

    def to_html(self) -> str:
        tag = f"h{self.level}"
        return f"<{tag}>{escape(self.text)}</{tag}>"


class Paragraph(Content):
    def __init__(self, text: str):
        self.text = text

    def to_html(self) -> str:
        return f"<p>{escape(self.text)}</p>"


class BulletList(Content):
    def __init__(self, items: list[str], *, ordered: bool = False):
        self.items = items
        self.ordered = ordered

    def to_html(self) -> str:
        tag = "ol" if self.ordered else "ul"
        items = "".join(f"<li>{escape(item)}</li>" for item in self.items)
        return f"<{tag}>{items}</{tag}>"


def as_content(value: Content | str) -> Content:
    if isinstance(value, Content):
        return value
    if looks_like_html(value):
        return RawHTML(value)
    return Paragraph(value)