from __future__ import annotations

import re
from html import escape
from typing import TYPE_CHECKING, Any

from .content import looks_like_html

if TYPE_CHECKING:
    from .background import Background
    from .element import Element
    from .slide import Slide

_TAG_OPEN = re.compile(r"^<(\w+)([^>]*)>", re.DOTALL)

_MATCH_DEFAULT_TAGS = {
    "title": "h2",
    "heading": "h2",
    "subtitle": "p",
    "body": "p",
}


def coerce_animate_match(key: str, value: str | dict[str, Any] | Element) -> Element:
    """Turn plain text or a small dict into a matched Element."""
    from .element import Element

    if isinstance(value, Element):
        element = value
        if element.data_id is not None and element.data_id != key:
            raise ValueError(
                f"Element data_id {element.data_id!r} does not match key {key!r}"
            )
        element.set_data_id(key)
        return element

    if isinstance(value, str):
        tag = _MATCH_DEFAULT_TAGS.get(key, "h2")
        element = Element(tag=tag, content=value)
        element.set_data_id(key)
        return element

    if isinstance(value, dict):
        text = value.get("text")
        if not isinstance(text, str):
            raise TypeError(
                f"animate frame {key!r} dict must include a 'text' string"
            )
        tag = value.get("tag", _MATCH_DEFAULT_TAGS.get(key, "h2"))
        element = Element(tag=tag, content=text)
        element.set_data_id(key)
        return element

    raise TypeError(
        f"animate frame values must be str, dict, or Element, got {type(value).__name__}"
    )


class AutoAnimate:
    """Build consecutive slides with matching ``data-id`` values for reveal.js auto-animate."""

    def __init__(self, easing: str | None = None):
        self.easing = easing

    @staticmethod
    def match(key: str, element: Element) -> Element:
        """Assign *key* as ``data-id`` on *element* for cross-slide matching."""
        element.set_data_id(key)
        return element

    @staticmethod
    def text(key: str, text: str, *, tag: str | None = None) -> Element:
        """Build a matched element from plain text (preferred for hand-built slides)."""
        return coerce_animate_match(
            key,
            {"text": text, "tag": tag} if tag is not None else text,
        )

    @staticmethod
    def html(key: str, markup: str) -> str:
        """Inject ``data-id`` into an HTML string."""
        markup = markup.strip()
        match = _TAG_OPEN.match(markup)
        if not match:
            raise ValueError(
                "markup must begin with an HTML tag to attach a data-id, "
                f"got: {markup[:40]!r}"
            )
        tag, attrs = match.group(1), match.group(2)
        if "data-id=" in attrs:
            raise ValueError(f"markup already contains data-id: {markup[:60]!r}")
        rest = markup[match.end() :]
        return f'<{tag}{attrs} data-id="{escape(key)}">{rest}'

    def slide(
        self,
        *,
        body: str = "",
        content: str = "",
        matches: dict[str, Element] | None = None,
        notes: str | None = None,
        background: Background | None = None,
    ) -> Slide:
        """Create one auto-animate slide with keyed elements."""
        from .content import as_content
        from .slide import Slide

        extra = body or content
        slide = Slide(
            notes=notes,
            background=background,
            auto_animate=True,
            auto_animate_easing=self.easing,
        )
        if extra:
            slide.add(as_content(extra))
        for key, element in (matches or {}).items():
            if element.data_id is not None and element.data_id != key:
                raise ValueError(
                    f"Element data_id {element.data_id!r} does not match key {key!r}"
                )
            element.set_data_id(key)
            slide.add_element(element)
        return slide

    def sequence(
        self,
        frames: list[dict[str, Any]],
        *,
        content_key: str = "_content",
    ) -> list[Slide]:
        """Create auto-animate slides from keyed dicts per frame.

        Values can be plain text (preferred), HTML strings, Elements, or dicts.
        """
        slides: list[Slide] = []
        for frame in frames:
            body = ""
            matches: dict[str, Element] = {}
            for key, value in frame.items():
                if key == content_key:
                    if not isinstance(value, str):
                        raise TypeError(
                            f"Frame entry {content_key!r} must be a string, "
                            f"got {type(value).__name__}"
                        )
                    body = value
                elif isinstance(value, str) and looks_like_html(value):
                    body += self.html(key, value)
                else:
                    matches[key] = coerce_animate_match(key, value)
            slides.append(self.slide(body=body, matches=matches or None))
        return slides