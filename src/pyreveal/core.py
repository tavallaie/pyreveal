import shutil
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any

from .auto_animate import AutoAnimate
from .background import Background
from .config import MATH_ENGINES, VALID_PLUGINS, build_initialize_options
from .element import Element
from .exceptions import InvalidThemeError, InvalidTransitionError
from .helpers import copy_assets_for_slide, copy_element_assets
from .slide import Slide
from .utils import wrap_in_html_template


class PyReveal:
    VALID_THEMES = [
        "beige",
        "black",
        "black-contrast",
        "blood",
        "dracula",
        "league",
        "moon",
        "night",
        "serif",
        "simple",
        "sky",
        "solarized",
        "white",
        "white-contrast",
    ]
    VALID_TRANSITIONS = [
        "none",
        "slide",
        "fade",
        "convex",
        "concave",
        "zoom",
    ]

    def __init__(
        self, title="Untitled Presentation", theme="black", transition="slide"
    ):
        self.title = title
        self.slides: list[Slide | dict[str, Any]] = []
        self.background: Background | None = None
        self._config: dict[str, Any] = {}
        self._plugins: list[str] = []
        self._math_engine = "katex"
        self._extra_css: list[str] = []
        self._inline_css: str | None = None
        self.set_theme(theme)
        self.set_transition(transition)

    def configure(self, **options: Any) -> "PyReveal":
        """Set Reveal.js ``Reveal.initialize()`` options.

        See https://revealjs.com/config/ for available keys. Theme is set via
        ``set_theme()`` (CSS); ``transition`` can be set here or via
        ``set_transition()``. Options passed here take precedence at render time.
        """
        self._config.update(options)
        return self

    def enable_plugins(
        self, *names: str, math_engine: str = "katex"
    ) -> "PyReveal":
        """Enable bundled reveal.js plugins in the generated HTML.

        Supported: ``notes``, ``highlight``, ``markdown``, ``math``, ``search``, ``zoom``.

        When enabling ``math``, choose an engine: ``katex``, ``mathjax2``,
        ``mathjax3``, or ``mathjax4``.
        """
        if math_engine not in MATH_ENGINES:
            raise ValueError(
                f"Unknown math engine {math_engine!r}. "
                f"Choose from: {', '.join(MATH_ENGINES)}"
            )
        self._math_engine = math_engine
        ordered: list[str] = []
        for name in names:
            if name not in VALID_PLUGINS:
                raise ValueError(
                    f"Unknown plugin {name!r}. Valid plugins: {', '.join(sorted(VALID_PLUGINS))}"
                )
            if name not in ordered:
                ordered.append(name)
        self._plugins = ordered
        return self

    def add_stylesheet(self, path: str) -> "PyReveal":
        """Link an extra CSS file in the generated HTML (relative to output)."""
        self._extra_css.append(path)
        return self

    def add_inline_css(self, css: str) -> "PyReveal":
        """Embed custom CSS in the generated HTML ``<head>``."""
        self._inline_css = css
        return self

    def add_slide(self, slide: Slide) -> None:
        """Add a :class:`Slide` to the presentation."""
        if not isinstance(slide, Slide):
            raise TypeError("Expected instance of Slide.")
        self.slides.append(slide)

    def add_auto_animate_sequence(
        self,
        frames: list[dict[str, Element | str]],
        *,
        easing: str | None = None,
        content_key: str = "_content",
    ) -> "PyReveal":
        """Add consecutive auto-animate slides with auto-matched ``data-id`` keys.

        See :class:`~pyreveal.auto_animate.AutoAnimate` for frame format.
        """
        helper = AutoAnimate(easing=easing)
        for slide in helper.sequence(frames, content_key=content_key):
            self.add_slide(slide)
        return self

    def set_theme(self, theme):
        if theme not in self.VALID_THEMES:
            raise InvalidThemeError(theme, self.VALID_THEMES)
        self.theme = theme

    def set_transition(self, transition):
        if transition not in self.VALID_TRANSITIONS:
            raise InvalidTransitionError(transition, self.VALID_TRANSITIONS)
        self.transition = transition

    def set_background(self, background: Background) -> None:
        """Set a default background for slides that do not define their own."""
        if not isinstance(background, Background):
            raise TypeError("Expected instance of Background class.")
        self.background = background

    def add_group(self, slides: list[Slide]) -> None:
        """Add a vertical stack of slides."""
        if not all(isinstance(slide, Slide) for slide in slides):
            raise TypeError("All items in the group must be instances of Slide.")
        self.slides.append({"type": "group", "slides": slides})

    def _render_nested_slides(self, parent: Slide, children: list[Slide]) -> str:
        outer_bg = parent.background or self.background
        outer_bg_html = outer_bg.generate_html() if outer_bg else ""
        parent_html = parent.render(
            default_background=self.background,
            omit_background=bool(outer_bg),
        )
        children_html = "\n".join(
            child.render(default_background=self.background) for child in children
        )
        return f"<section{outer_bg_html}>\n{parent_html}\n{children_html}\n</section>"

    def _render_slide_item(self, item):
        if isinstance(item, dict) and item.get("type") == "group":
            group_html = "\n".join(
                slide.render(default_background=self.background)
                for slide in item["slides"]
            )
            return f"<section>\n{group_html}\n</section>"

        if not isinstance(item, Slide):
            raise TypeError(f"Unexpected slide item: {item!r}")

        if item.vertical_slides:
            return self._render_nested_slides(item, item.vertical_slides)

        return item.render(default_background=self.background)

    def generate_html(self) -> str:
        rendered = [self._render_slide_item(item) for item in self.slides]

        initialize_options = build_initialize_options(self.transition, self._config)
        return wrap_in_html_template(
            self.title,
            self.theme,
            "\n".join(rendered),
            initialize_options,
            plugins=self._plugins,
            math_engine=self._math_engine,
            extra_css=self._extra_css,
            inline_css=self._inline_css,
        )

    def save_to_string(self) -> str:
        """Return the presentation HTML without writing to disk."""
        return self.generate_html()

    def _iter_slides(self):
        for item in self.slides:
            if isinstance(item, dict) and item.get("type") == "group":
                for slide in item["slides"]:
                    yield slide
            elif isinstance(item, Slide):
                yield item
                yield from item.vertical_slides

    def save_to_file(
        self,
        filename="presentation.html",
        output_dir="presentations",
        *,
        copy_revealjs: bool = True,
        quiet: bool = False,
    ):
        presentations_dir = Path(output_dir)
        presentations_dir.mkdir(parents=True, exist_ok=True)

        assets_dir = presentations_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        for slide in self._iter_slides():
            copy_assets_for_slide(slide, assets_dir, presentations_dir)
            for element in slide.elements:
                copy_element_assets(element, assets_dir, presentations_dir)

        if copy_revealjs:
            revealjs_ref = files("pyreveal") / "revealjs"
            revealjs_dest = presentations_dir / "revealjs"

            with as_file(revealjs_ref) as revealjs_source:
                if not revealjs_dest.exists():
                    shutil.copytree(revealjs_source, revealjs_dest)

        full_path = presentations_dir / filename
        full_path.write_text(self.generate_html(), encoding="utf-8")

        if not quiet:
            print(f"Presentation saved to: {full_path}")