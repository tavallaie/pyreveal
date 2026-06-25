from __future__ import annotations

import re
from html import escape
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .background import Background
    from .element import Element
    from .slide import Slide

_TAG_OPEN = re.compile(r"^<(\w+)([^>]*)>", re.DOTALL)


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
    def html(key: str, markup: str) -> str:
        """Return HTML with ``data-id`` injected into the first opening tag."""
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
        content: str = "",
        matches: dict[str, Element] | None = None,
        notes: str | None = None,
        background: Background | None = None,
    ) -> Slide:
        """Create one auto-animate slide with keyed elements."""
        from .slide import Slide

        slide = Slide(
            content=content,
            background=background,
            notes=notes,
            auto_animate=True,
            auto_animate_easing=self.easing,
        )
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
        frames: list[dict[str, Element | str]],
        *,
        content_key: str = "_content",
    ) -> list[Slide]:
        """Create a series of auto-animate slides from keyed element dicts per frame.

        Each frame maps a match key to an :class:`~pyreveal.element.Element`.
        Use *content_key* (default ``"_content"``) for extra HTML on a frame.
        """
        slides: list[Slide] = []
        for frame in frames:
            content = ""
            matches: dict[str, Element] = {}
            for key, value in frame.items():
                if key == content_key:
                    if not isinstance(value, str):
                        raise TypeError(
                            f"Frame entry {content_key!r} must be a string, "
                            f"got {type(value).__name__}"
                        )
                    content = value
                elif isinstance(value, str):
                    content += self.html(key, value)
                else:
                    matches[key] = value
            slides.append(
                self.slide(content=content, matches=matches or None)
            )
        return slides