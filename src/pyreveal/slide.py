from __future__ import annotations

from html import escape

from .background import Background


class Slide:
    def __init__(
        self,
        content: str | None = None,
        title: str | None = None,
        background: Background | None = None,
        *,
        slide_id: str | None = None,
        transition: str | None = None,
        state: str | None = None,
        auto_slide: int | None = None,
        auto_animate: bool = False,
        auto_animate_easing: str | None = None,
        visibility: str | None = None,
        notes: str | None = None,
        markdown: str | None = None,
        attributes: dict[str, str] | None = None,
    ):
        self.content = content or ""
        self.title = title
        self.background = background
        self.slide_id = slide_id
        self.transition = transition
        self.state = state
        self.auto_slide = auto_slide
        self.auto_animate = auto_animate
        self.auto_animate_easing = auto_animate_easing
        self.visibility = visibility
        self.notes = notes
        self.markdown = markdown
        self.attributes = attributes or {}
        self.elements = []
        self.vertical_slides: list[Slide] = []

    def add_element(self, element) -> None:
        self.elements.append(element)

    def add_vertical_slide(self, slide: Slide) -> None:
        if isinstance(slide, Slide):
            self.vertical_slides.append(slide)
        else:
            raise ValueError("Invalid slide type. Expected an instance of Slide.")

    def set_background(self, background: Background) -> None:
        self.background = background

    def _section_attributes(self) -> str:
        attrs: list[str] = []
        if self.slide_id:
            attrs.append(f'id="{escape(self.slide_id)}"')
        if self.transition:
            attrs.append(f'data-transition="{escape(self.transition)}"')
        if self.state:
            attrs.append(f'data-state="{escape(self.state)}"')
        if self.auto_slide is not None:
            attrs.append(f'data-autoslide="{self.auto_slide}"')
        if self.auto_animate:
            attrs.append("data-auto-animate")
        if self.auto_animate_easing:
            attrs.append(
                f'data-auto-animate-easing="{escape(self.auto_animate_easing)}"'
            )
        if self.visibility:
            attrs.append(f'data-visibility="{escape(self.visibility)}"')
        if self.markdown is not None:
            attrs.append("data-markdown")
        for key, value in self.attributes.items():
            attrs.append(f'{escape(key)}="{escape(value)}"')
        return (" " + " ".join(attrs)) if attrs else ""

    def _notes_html(self) -> str:
        if not self.notes:
            return ""
        return f'<aside class="notes">{self.notes}</aside>'

    def _markdown_html(self) -> str:
        if self.markdown is None:
            return ""
        return (
            '<script type="text/template">\n'
            f"{self.markdown}\n"
            "</script>"
        )

    def generate_html(
        self,
        default_background: Background | None = None,
        *,
        omit_background: bool = False,
    ) -> str:
        background = None if omit_background else (self.background or default_background)
        background_html = background.generate_html() if background else ""
        section_attrs = self._section_attributes()
        elements_html = "".join(
            element.generate_html() for element in self.elements
        )
        body = self._markdown_html() if self.markdown is not None else self.content
        return (
            f"<section{background_html}{section_attrs}>"
            f"{body}{elements_html}{self._notes_html()}"
            f"</section>"
        )

    def render(
        self,
        default_background: Background | None = None,
        *,
        omit_background: bool = False,
    ) -> str:
        return self.generate_html(
            default_background=default_background,
            omit_background=omit_background,
        )