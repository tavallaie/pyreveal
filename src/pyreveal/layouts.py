from __future__ import annotations

from .element import Element


class Layout(Element):
    """Reveal.js layout container (``r-stack``, ``r-hstack``, ``r-vstack``)."""

    LAYOUT_CLASSES = {
        "stack": "r-stack",
        "hstack": "r-hstack",
        "vstack": "r-vstack",
    }

    def __init__(
        self,
        layout: str = "stack",
        children: list[Element] | None = None,
        *,
        gap: str | None = None,
        **kwargs,
    ):
        if layout not in self.LAYOUT_CLASSES:
            raise ValueError(
                f"Unknown layout {layout!r}. "
                f"Choose from: {', '.join(self.LAYOUT_CLASSES)}"
            )
        attributes = kwargs.pop("attributes", {})
        classes = [self.LAYOUT_CLASSES[layout]]
        if gap:
            classes.append(gap)
        if "class" in attributes:
            classes.insert(0, attributes.pop("class"))
        attributes["class"] = " ".join(classes)
        super().__init__(tag="div", attributes=attributes, **kwargs)
        for child in children or []:
            self.add_child(child)


class Stack(Layout):
    def __init__(self, children: list[Element] | None = None, **kwargs):
        super().__init__("stack", children=children, **kwargs)


class HStack(Layout):
    def __init__(self, children: list[Element] | None = None, **kwargs):
        super().__init__("hstack", children=children, **kwargs)


class VStack(Layout):
    def __init__(self, children: list[Element] | None = None, **kwargs):
        super().__init__("vstack", children=children, **kwargs)


class FitText(Element):
    """Text sized to fill its container (``r-fit-text``)."""

    def __init__(self, content: str, tag: str = "h2", **kwargs):
        attributes = kwargs.pop("attributes", {})
        attributes["class"] = "r-fit-text"
        super().__init__(tag=tag, content=content, attributes=attributes, **kwargs)