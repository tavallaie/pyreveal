from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING, Any

from .background import Background
from .choices import FragmentEffect
from .coerce import (
    apply_slide_options,
    coerce_background,
    coerce_slide_visibility,
    coerce_transition,
    normalize_vertical_slides,
    split_slide_kwargs,
)
from .content import BulletList, Content, Heading, Paragraph, as_content

if TYPE_CHECKING:
    from .element import CodeElement, Element, Fragment, ImageElement

_ASSIGNABLE = frozenset({"title", "subtitle", "heading", "markdown"})


class Slide:
    """One reveal.js slide.

    Prefer building with ``Slide()`` and ``title`` / ``text`` / ``heading``.
    HTML is also accepted: ``Slide("<h1>Hi</h1>")`` or ``Slide(content="…")``.
    """

    def __init__(
        self,
        *blocks: Content | str,
        **kwargs: Any,
    ):
        ctor, options = split_slide_kwargs(kwargs)

        content = ctor.pop("content", None)
        self._blocks: list[Content] = [as_content(block) for block in blocks]
        if content is not None:
            self._blocks.append(as_content(content))

        self.background = None
        bg = ctor.pop("background", None)
        if bg is not None:
            self.background = coerce_background(bg)

        self.slide_id = ctor.pop("slide_id", None)
        transition = ctor.pop("transition", None)
        self.transition = (
            coerce_transition(transition) if transition is not None else None
        )
        self.state = ctor.pop("state", None)
        self.auto_slide = ctor.pop("auto_slide", None)
        self.auto_animate = ctor.pop("auto_animate", False)
        self.auto_animate_easing = ctor.pop("auto_animate_easing", None)
        visibility = ctor.pop("visibility", None)
        self.visibility = (
            coerce_slide_visibility(visibility) if visibility is not None else None
        )
        self.notes = ctor.pop("notes", None)
        self.markdown = ctor.pop("markdown", None)
        self.attributes = ctor.pop("attributes", None) or {}

        if ctor:
            unknown = ", ".join(sorted(ctor))
            raise TypeError(f"Unknown slide field(s): {unknown}")

        self.elements: list = []
        self._vertical: list[Slide] = []
        apply_slide_options(self, **options)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in _ASSIGNABLE and isinstance(value, str):
            if name == "title":
                self._set_heading(1, value)
            elif name == "subtitle":
                self._set_subtitle(value)
            elif name == "heading":
                self._set_heading(2, value)
            elif name == "markdown":
                super().__setattr__("markdown", value)
            return
        super().__setattr__(name, value)

    @property
    def content(self) -> str:
        return "".join(block.to_html() for block in self._blocks)

    @content.setter
    def content(self, value: str) -> None:
        self._blocks = [as_content(value)] if value else []

    @property
    def id(self) -> str | None:
        """Slide DOM id for hash deep links (alias for ``slide_id``)."""
        return self.slide_id

    @id.setter
    def id(self, value: str) -> None:
        self.slide_id = value

    @property
    def vertical(self) -> list[Slide]:
        """Vertical child slides (reorder by assigning a new list)."""
        return self._vertical

    @vertical.setter
    def vertical(self, slides: list[Slide | str]) -> None:
        self._vertical = normalize_vertical_slides(slides)

    # --- Content slots --------------------------------------------------------

    def _find_heading(self, level: int) -> int | None:
        for index, block in enumerate(self._blocks):
            if isinstance(block, Heading) and block.level == level:
                return index
        return None

    def _get_heading(self, level: int) -> str | None:
        index = self._find_heading(level)
        if index is None:
            return None
        block = self._blocks[index]
        assert isinstance(block, Heading)
        return block.text

    def _set_heading(self, level: int, text: str) -> None:
        index = self._find_heading(level)
        if index is not None:
            self._blocks[index] = Heading(text, level=level)
            return
        if level == 1:
            self._blocks.insert(0, Heading(text, level=1))
        else:
            self._blocks.append(Heading(text, level=level))

    def _find_subtitle(self) -> int | None:
        title_index = self._find_heading(1)
        if title_index is None:
            return None
        for index in range(title_index + 1, len(self._blocks)):
            if isinstance(self._blocks[index], Paragraph):
                return index
        return None

    def _get_subtitle(self) -> str | None:
        index = self._find_subtitle()
        if index is None:
            return None
        block = self._blocks[index]
        assert isinstance(block, Paragraph)
        return block.text

    def _set_subtitle(self, text: str) -> None:
        index = self._find_subtitle()
        if index is not None:
            self._blocks[index] = Paragraph(text)
            return
        title_index = self._find_heading(1)
        insert_at = (title_index + 1) if title_index is not None else len(self._blocks)
        self._blocks.insert(insert_at, Paragraph(text))

    def title(
        self,
        text: str | None = None,
        *,
        subtitle: str | None = None,
        level: int = 1,
    ) -> Slide | str | None:
        """Set or read the slide title (``<h1>`` by default)."""
        if text is None and subtitle is None:
            return self._get_heading(level)
        if text is not None:
            self._set_heading(level, text)
        if subtitle is not None:
            self._set_subtitle(subtitle)
        return self

    def subtitle(self, text: str | None = None) -> Slide | str | None:
        """Set or read the subtitle paragraph."""
        if text is None:
            return self._get_subtitle()
        self._set_subtitle(text)
        return self

    def heading(
        self,
        text: str | None = None,
        *,
        level: int = 2,
    ) -> Slide | str | None:
        """Set or read a section heading (``<h2>`` by default)."""
        if text is None:
            return self._get_heading(level)
        self._set_heading(level, text)
        return self

    def text(self, *paragraphs: str) -> Slide:
        """Append paragraph(s)."""
        for paragraph in paragraphs:
            self._blocks.append(Paragraph(paragraph))
        return self

    def bullets(
        self,
        items: list[str] | None = None,
        *,
        ordered: bool = False,
    ) -> Slide | list[str] | None:
        """Set or append a bullet list."""
        if items is None:
            for block in reversed(self._blocks):
                if isinstance(block, BulletList):
                    return block.items
            return None
        self._blocks.append(BulletList(items, ordered=ordered))
        return self

    def code(
        self,
        source: str,
        *,
        language: str = "python",
        line_numbers: bool = False,
    ) -> Slide:
        from .element import CodeElement

        self.element(CodeElement(source, language=language, line_numbers=line_numbers))
        return self

    def image(
        self,
        src: str,
        *,
        caption: str | None = None,
        alt: str = "",
        stretch: bool = False,
        preview: bool = False,
        preview_src: str | None = None,
    ) -> Slide:
        from .element import ImageElement

        self.element(
            ImageElement(
                src,
                alt_text=alt,
                stretch=stretch,
                preview=preview,
                preview_src=preview_src,
            )
        )
        if caption:
            self.text(caption)
        return self

    # --- One-shot factories (optional shortcuts) ------------------------------

    @classmethod
    def make_title(
        cls,
        text: str,
        *,
        subtitle: str | None = None,
        level: int = 1,
        **kwargs: Any,
    ) -> Slide:
        slide = cls(**kwargs)
        slide.title(text, subtitle=subtitle, level=level)
        return slide

    @classmethod
    def make_heading(cls, text: str, *, level: int = 2, **kwargs: Any) -> Slide:
        slide = cls(**kwargs)
        slide.heading(text, level=level)
        return slide

    @classmethod
    def make_text(cls, *paragraphs: str, **kwargs: Any) -> Slide:
        slide = cls(**kwargs)
        slide.text(*paragraphs)
        return slide

    @classmethod
    def make_bullets(
        cls,
        items: list[str],
        *,
        title: str | None = None,
        ordered: bool = False,
        **kwargs: Any,
    ) -> Slide:
        slide = cls(**kwargs)
        if title:
            slide.heading(title)
        slide.bullets(items, ordered=ordered)
        return slide

    @classmethod
    def make_code(
        cls,
        code: str,
        *,
        title: str | None = None,
        language: str = "python",
        line_numbers: bool = False,
        **kwargs: Any,
    ) -> Slide:
        slide = cls(**kwargs)
        if title:
            slide.heading(title)
        slide.code(code, language=language, line_numbers=line_numbers)
        return slide

    @classmethod
    def make_image(
        cls,
        src: str,
        *,
        title: str | None = None,
        caption: str | None = None,
        alt: str = "",
        stretch: bool = False,
        preview: bool = False,
        preview_src: str | None = None,
        **kwargs: Any,
    ) -> Slide:
        slide = cls(**kwargs)
        if title:
            slide.heading(title)
        slide.image(
            src,
            caption=caption,
            alt=alt,
            stretch=stretch,
            preview=preview,
            preview_src=preview_src,
        )
        return slide

    @classmethod
    def from_markdown(cls, markdown: str, **kwargs: Any) -> Slide:
        slide = cls(**kwargs)
        slide.markdown = markdown
        return slide

    @classmethod
    def section(
        cls,
        main: str | Slide,
        *children: str | Slide,
        **kwargs: Any,
    ) -> Slide:
        """Horizontal slide with optional vertical children."""
        if isinstance(main, str):
            slide = cls.make_heading(main, **kwargs)
        else:
            slide = main
            if kwargs:
                apply_slide_options(slide, **kwargs)
        if children:
            slide.vertical = list(children)
        return slide

    # --- Fluent builders ------------------------------------------------------

    def add(self, *items: Content | str) -> Slide:
        for item in items:
            self._blocks.append(as_content(item))
        return self

    def element(self, element) -> Slide:
        self.elements.append(element)
        return self

    def add_element(self, element) -> None:
        self.element(element)

    def fragment(
        self,
        text: str,
        *,
        effect: FragmentEffect | str | None = FragmentEffect.NONE,
        index: int | None = None,
        **kwargs,
    ) -> Slide:
        from .element import Fragment

        return self.element(
            Fragment(text, effect=effect, index=index, **kwargs)
        )

    def note(self, text: str) -> Slide:
        self.notes = text
        return self

    def bg(
        self,
        background: str | dict[str, Any] | Background | None = None,
        /,
        **kwargs: Any,
    ) -> Slide:
        self.background = coerce_background(background, **kwargs)
        return self

    def set_background(
        self,
        background: str | dict[str, Any] | Background | None = None,
        /,
        **kwargs: Any,
    ) -> None:
        self.background = coerce_background(background, **kwargs)

    def add_vertical_slide(self, slide: Slide | str) -> None:
        self._vertical.extend(normalize_vertical_slides([slide]))

    # --- Rendering ------------------------------------------------------------

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

    def _body_html(self) -> str:
        if self.markdown is not None:
            return self._markdown_html()
        return self.content

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
        return (
            f"<section{background_html}{section_attrs}>"
            f"{self._body_html()}{elements_html}{self._notes_html()}"
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