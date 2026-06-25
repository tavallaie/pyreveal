from __future__ import annotations

from html import escape

from .style import Style


class Element:
    def __init__(
        self,
        tag: str = "div",
        content: str | None = None,
        style: Style | None = None,
        data_id: str | None = None,
        attributes: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.content = content or ""
        self.attributes = attributes or {}
        self.style = style or Style()
        self.data_id = data_id
        self.children: list[Element] = []

    def add_child(self, child_element: Element) -> None:
        if not isinstance(child_element, Element):
            raise ValueError("Child element must be an instance of Element.")
        self.children.append(child_element)

    def _style_attr(self) -> str:
        css = self.style.generate_css()
        return f' style="{css}"' if css.strip() else ""

    def _data_id_attr(self) -> str:
        return f' data-id="{escape(self.data_id)}"' if self.data_id else ""

    def _attributes_str(self) -> str:
        parts = [f'{escape(k)}="{escape(v)}"' for k, v in self.attributes.items()]
        return (" " + " ".join(parts)) if parts else ""

    def generate_html(self) -> str:
        children_html = "".join(child.generate_html() for child in self.children)
        return (
            f"<{self.tag}{self._attributes_str()}{self._data_id_attr()}"
            f"{self._style_attr()}>{self.content}{children_html}</{self.tag}>"
        )

    def set_data_id(self, data_id: str) -> None:
        self.data_id = data_id

    def get_data_id(self) -> str | None:
        return self.data_id


class Fragment(Element):
    """Stepped reveal fragment (reveal.js ``.fragment``)."""

    VALID_EFFECTS = frozenset(
        {
            "",
            "grow",
            "shrink",
            "fade-out",
            "fade-right",
            "fade-up",
            "fade-down",
            "fade-left",
            "fade-in-then-out",
            "fade-in-then-semi-out",
            "highlight-red",
            "highlight-blue",
            "highlight-green",
        }
    )

    def __init__(
        self,
        content: str,
        effect: str = "",
        index: int | None = None,
        tag: str = "span",
        **kwargs,
    ):
        if effect not in self.VALID_EFFECTS:
            raise ValueError(f"Unsupported fragment effect: {effect!r}")
        class_name = "fragment" if not effect else f"fragment {effect}"
        attributes = kwargs.pop("attributes", {})
        attributes["class"] = class_name
        super().__init__(tag=tag, content=content, attributes=attributes, **kwargs)
        self.fragment_index = index

    def generate_html(self) -> str:
        index_attr = (
            f' data-fragment-index="{self.fragment_index}"'
            if self.fragment_index is not None
            else ""
        )
        children_html = "".join(child.generate_html() for child in self.children)
        return (
            f"<{self.tag}{self._attributes_str()}{index_attr}{self._data_id_attr()}"
            f"{self._style_attr()}>{self.content}{children_html}</{self.tag}>"
        )


class SpeakerNotes:
    """Speaker notes rendered as ``<aside class=\"notes\">``."""

    def __init__(self, text: str):
        self.text = text

    def generate_html(self) -> str:
        return f'<aside class="notes">{self.text}</aside>'


class ImageElement(Element):
    def __init__(self, image_url: str, alt_text: str = "", **kwargs):
        super().__init__(content=image_url, tag="img", **kwargs)
        self.alt_text = alt_text

    def generate_html(self) -> str:
        children_html = "".join(child.generate_html() for child in self.children)
        return (
            f'<img src="{escape(self.content)}" alt="{escape(self.alt_text)}"'
            f"{self._data_id_attr()}{self._style_attr()} />{children_html}"
        )


class VideoElement(Element):
    def __init__(self, video_url: str, **kwargs):
        super().__init__(content=video_url, tag="video", **kwargs)

    def generate_html(self) -> str:
        children_html = "".join(child.generate_html() for child in self.children)
        return (
            f'<video src="{escape(self.content)}"{self._data_id_attr()}'
            f'{self._style_attr()}>{children_html}</video>'
        )


class CodeElement(Element):
    """Syntax-highlighted code block (requires the highlight plugin)."""

    def __init__(
        self,
        code: str,
        language: str | None = None,
        line_numbers: bool = False,
        **kwargs,
    ):
        super().__init__(tag="pre", content="", **kwargs)
        self.code = code
        self.language = language
        self.line_numbers = line_numbers

    def generate_html(self) -> str:
        lang_class = f"language-{escape(self.language)}" if self.language else ""
        data_attrs = ' data-trim data-noescape'
        if self.line_numbers:
            data_attrs += ' data-line-numbers'
        code_tag = (
            f'<code class="{lang_class}"{data_attrs}>{escape(self.code)}</code>'
            if lang_class
            else f"<code{data_attrs}>{escape(self.code)}</code>"
        )
        return (
            f"<pre{self._data_id_attr()}{self._style_attr()}>{code_tag}</pre>"
        )


class MarkdownElement(Element):
    """Inline Markdown block (requires the markdown plugin)."""

    def __init__(self, markdown: str, **kwargs):
        super().__init__(tag="div", content="", attributes={"data-markdown": ""}, **kwargs)
        self.markdown = markdown

    def generate_html(self) -> str:
        return (
            f'<section data-markdown>'
            f"<script type=\"text/template\">\n{self.markdown}\n</script>"
            f"</section>"
        )