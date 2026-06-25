from __future__ import annotations

import shutil
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any
from .auto_animate import AutoAnimate
from .background import Background
from .coerce import coerce_background
from .choices import (
    CustomPlugin,
    KeyboardBinding,
    MathEngine,
    Plugin,
    ScrollLayout,
    ScrollSnap,
    SlideNumber,
    Theme,
    Transition,
    View,
    coerce_keyboard_bindings,
    coerce_math_engine,
    coerce_plugin,
    coerce_slide_number,
    coerce_theme,
    coerce_transition,
)
from .config import build_initialize_options
from .element import Element
from .exceptions import InvalidThemeError, InvalidTransitionError
from .helpers import copy_assets_for_slide, copy_element_assets
from .slide import Slide
from .utils import wrap_in_html_template


class Presentation:
    """Object-oriented entry point for building a reveal.js deck."""

    Theme = Theme
    Transition = Transition
    Plugin = Plugin
    MathEngine = MathEngine
    View = View
    SlideNumber = SlideNumber
    ScrollLayout = ScrollLayout
    ScrollSnap = ScrollSnap
    CustomPlugin = CustomPlugin
    KeyboardBinding = KeyboardBinding

    def __init__(
        self,
        title: str = "Untitled Presentation",
        *,
        theme: Theme | str = Theme.BLACK,
        transition: Transition | str = Transition.SLIDE,
    ):
        self._document_title = title
        self.slides: list[Slide | dict[str, Any]] = []
        self.background: Background | None = None
        self._config: dict[str, Any] = {}
        self._plugins: list[str] = []
        self._custom_plugins: list[CustomPlugin] = []
        self._math_engine = MathEngine.KATEX.value
        self._extra_css: list[str] = []
        self._inline_css: str | None = None
        self._extra_head: str | None = None
        self._extra_scripts: list[str] = []
        self._inline_js: str | None = None
        self.set_theme(theme)
        self.set_transition(transition)

    # --- Fluent configuration -------------------------------------------------

    def configure(self, **options: Any) -> Presentation:
        """Set Reveal.js ``Reveal.initialize()`` options."""
        self._config.update(options)
        return self

    def navigation(
        self,
        *,
        hash: bool = True,
        controls: bool = True,
        progress: bool = True,
        touch: bool = True,
        overview: bool = True,
        keyboard: bool = True,
        jump_to_slide: bool = True,
    ) -> Presentation:
        """Common navigation options for the exported deck."""
        return self.configure(
            hash=hash,
            controls=controls,
            progress=progress,
            touch=touch,
            overview=overview,
            keyboard=keyboard,
            jumpToSlide=jump_to_slide,
        )

    def deep_links(
        self,
        *,
        hash: bool = True,
        respond_to_hash_changes: bool = True,
        history: bool = False,
    ) -> Presentation:
        """Enable hash URLs and slide deep linking."""
        return self.configure(
            hash=hash,
            respondToHashChanges=respond_to_hash_changes,
            history=history,
        )

    def slide_numbers(
        self,
        format: bool | SlideNumber | str = SlideNumber.C_SLASH_T,
        *,
        show: str = "all",
    ) -> Presentation:
        """Show slide numbers using a reveal.js format string."""
        return self.configure(
            slideNumber=coerce_slide_number(format),
            showSlideNumber=show,
        )

    def scroll_view(
        self,
        *,
        layout: ScrollLayout | str = ScrollLayout.FULL,
        snap: ScrollSnap | str | bool = ScrollSnap.MANDATORY,
        progress: str | bool = "auto",
        activation_width: int = 435,
    ) -> Presentation:
        """Enable reveal.js scroll view."""
        snap_value: str | bool
        if isinstance(snap, ScrollSnap):
            snap_value = snap.value
        elif snap is False:
            snap_value = False
        else:
            snap_value = str(snap)

        layout_value = layout.value if isinstance(layout, ScrollLayout) else layout

        return self.configure(
            view=View.SCROLL.value,
            scrollLayout=layout_value,
            scrollSnap=snap_value,
            scrollProgress=progress,
            scrollActivationWidth=activation_width,
        )

    def print_view(self) -> Presentation:
        """Use reveal.js print layout (pair with browser PDF export)."""
        return self.configure(view=View.PRINT.value)

    def presentation_size(
        self,
        width: int = 960,
        height: int = 700,
        *,
        margin: float = 0.04,
        min_scale: float = 0.2,
        max_scale: float = 2.0,
    ) -> Presentation:
        """Set the logical slide dimensions reveal.js scales from."""
        return self.configure(
            width=width,
            height=height,
            margin=margin,
            minScale=min_scale,
            maxScale=max_scale,
        )

    def preview_links(self, enabled: bool = True) -> Presentation:
        """Enable global link lightbox previews (``previewLinks``)."""
        return self.configure(previewLinks=enabled)

    def auto_slide(
        self,
        interval_ms: int | bool = 5000,
        *,
        stoppable: bool = True,
        loop: bool = False,
    ) -> Presentation:
        """Enable deck-wide auto-advance (reveal.js ``autoSlide``).

        Pass an interval in milliseconds for kiosk-style decks, ``0`` to only
        honor per-slide ``data-autoslide``, or ``False`` to disable globally.
        """
        return self.configure(
            autoSlide=interval_ms,
            autoSlideStoppable=stoppable,
            loop=loop,
        )

    def auto_progression(
        self,
        interval_ms: int | bool = 5000,
        *,
        stoppable: bool = True,
        loop: bool = False,
    ) -> Presentation:
        """Alias for :meth:`auto_slide` (reveal.js auto-progression)."""
        return self.auto_slide(
            interval_ms, stoppable=stoppable, loop=loop
        )

    def parallax_background(
        self,
        image: str,
        *,
        size: str | None = None,
        repeat: str | None = None,
        position: str | None = None,
        horizontal: int | None = None,
        vertical: int | None = None,
    ) -> Presentation:
        """Enable deck-wide parallax scrolling background.

        Maps to reveal.js ``parallaxBackground*`` options. Use a large
        ``size`` (e.g. ``"2100px 900px"``) so the image can scroll.
        """
        options: dict[str, Any] = {"parallaxBackgroundImage": image}
        if size is not None:
            options["parallaxBackgroundSize"] = size
        if repeat is not None:
            options["parallaxBackgroundRepeat"] = repeat
        if position is not None:
            options["parallaxBackgroundPosition"] = position
        if horizontal is not None:
            options["parallaxBackgroundHorizontal"] = horizontal
        if vertical is not None:
            options["parallaxBackgroundVertical"] = vertical
        return self.configure(**options)

    def keyboard_bindings(
        self,
        bindings: dict[int | str, KeyboardBinding | str | None],
        *,
        condition: str | None = None,
    ) -> Presentation:
        """Override default reveal.js keyboard shortcuts.

        Keys are [key codes](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode)
        (e.g. ``13`` for Enter). Values are :class:`KeyboardBinding` members,
        matching action strings, or ``None`` to disable a default binding.
        """
        config: dict[str, Any] = {
            "keyboard": coerce_keyboard_bindings(bindings),
        }
        if condition is not None:
            if condition != "focused":
                raise ValueError(
                    "keyboard condition must be 'focused' or None"
                )
            config["keyboardCondition"] = condition
        return self.configure(**config)

    def plugins(
        self,
        *names: Plugin | str | CustomPlugin,
        math_engine: MathEngine | str = MathEngine.KATEX,
    ) -> Presentation:
        return self.enable_plugins(*names, math_engine=math_engine)

    def enable_plugins(
        self,
        *names: Plugin | str | CustomPlugin,
        math_engine: MathEngine | str = MathEngine.KATEX,
    ) -> Presentation:
        self._math_engine = coerce_math_engine(math_engine)
        ordered: list[str] = []
        custom: list[CustomPlugin] = list(self._custom_plugins)
        for name in names:
            if isinstance(name, CustomPlugin):
                if name not in custom:
                    custom.append(name)
                continue
            plugin = coerce_plugin(name)
            if plugin not in ordered:
                ordered.append(plugin)
        self._plugins = ordered
        self._custom_plugins = custom
        return self

    def stylesheet(self, path: str) -> Presentation:
        return self.add_stylesheet(path)

    def add_stylesheet(self, path: str) -> Presentation:
        self._extra_css.append(path)
        return self

    def css(self, css: str) -> Presentation:
        return self.add_inline_css(css)

    def add_inline_css(self, css: str) -> Presentation:
        self._inline_css = css
        return self

    def extra_head(self, html: str) -> Presentation:
        """Inject raw HTML into ``<head>`` (import maps, meta tags, etc.)."""
        self._extra_head = html
        return self

    def script(self, path: str) -> Presentation:
        """Add a ``<script type=\"module\">`` tag after Reveal initializes."""
        self._extra_scripts.append(path)
        return self

    def inline_js(self, js: str) -> Presentation:
        """Add an inline ``<script>`` block after Reveal initializes."""
        self._inline_js = js
        return self

    def bg(
        self,
        background: str | dict[str, Any] | Background | None = None,
        /,
        **kwargs: Any,
    ) -> Presentation:
        return self.set_background(background, **kwargs)

    def set_background(
        self,
        background: str | dict[str, Any] | Background | None = None,
        /,
        **kwargs: Any,
    ) -> Presentation:
        self.background = coerce_background(background, **kwargs)
        return self

    def set_theme(self, theme: Theme | str) -> Presentation:
        try:
            self.theme = coerce_theme(theme)
        except ValueError as exc:
            raise InvalidThemeError(
                theme, [member.value for member in Theme]
            ) from exc
        return self

    def set_transition(self, transition: Transition | str) -> Presentation:
        try:
            self.transition = coerce_transition(transition)
        except ValueError as exc:
            raise InvalidTransitionError(
                transition, [member.value for member in Transition]
            ) from exc
        return self

    # --- Slide assembly -------------------------------------------------------

    def add(self, *slides: Slide) -> Presentation:
        """Add one or more pre-built slides to the deck."""
        if not slides:
            raise TypeError("add() requires at least one Slide.")
        for slide in slides:
            if not isinstance(slide, Slide):
                raise TypeError("Expected Slide.")
            self.slides.append(slide)
        return self

    def slide(self, slide: Slide) -> Presentation:
        """Add a slide (alias for :meth:`add`)."""
        return self.add(slide)

    def add_slide(self, slide: Slide) -> None:
        self.add(slide)

    def section(self, parent: Slide, *children: Slide) -> Presentation:
        """Add a horizontal slide that already has vertical children attached."""
        if children:
            parent.vertical = [*parent.vertical, *children]
        return self.add(parent)

    def add_group(self, slides: list[Slide]) -> None:
        if not slides:
            raise ValueError("add_group() requires at least one slide.")
        self.add(Slide.section(slides[0], *slides[1:]))

    def animate(
        self,
        frames: list[dict[str, Any]],
        *,
        easing: str | None = None,
        content_key: str = "_content",
    ) -> Presentation:
        return self.add_auto_animate_sequence(
            frames, easing=easing, content_key=content_key
        )

    def add_auto_animate_sequence(
        self,
        frames: list[dict[str, Any]],
        *,
        easing: str | None = None,
        content_key: str = "_content",
    ) -> Presentation:
        helper = AutoAnimate(easing=easing)
        for slide in helper.sequence(frames, content_key=content_key):
            self.add(slide)
        return self

    # --- Export ---------------------------------------------------------------

    def html(self) -> str:
        return self.generate_html()

    def generate_html(self) -> str:
        rendered = [self._render_slide_item(item) for item in self.slides]
        initialize_options = build_initialize_options(self.transition, self._config)
        return wrap_in_html_template(
            self._document_title,
            self.theme,
            "\n".join(rendered),
            initialize_options,
            plugins=self._plugins,
            custom_plugins=self._custom_plugins,
            math_engine=self._math_engine,
            extra_css=self._extra_css,
            inline_css=self._inline_css,
            extra_head=self._extra_head,
            extra_scripts=self._extra_scripts,
            inline_js=self._inline_js,
        )

    def save_to_string(self) -> str:
        return self.generate_html()

    @staticmethod
    def pdf_print_url(path: str | Path) -> str:
        """Build a ``?print-pdf`` URL for browser PDF export of a saved deck."""
        target = Path(path)
        return f"{target.as_posix()}?print-pdf"

    def save(
        self,
        path: str | Path = "presentation.html",
        *,
        output_dir: str | None = None,
        copy_revealjs: bool = True,
        quiet: bool = False,
        pdf_hint: bool = False,
    ) -> Presentation:
        target = Path(path)
        if output_dir is None and target.parent not in (Path("."), Path("")):
            return self.save_to_file(
                target.name,
                str(target.parent),
                copy_revealjs=copy_revealjs,
                quiet=quiet,
                pdf_hint=pdf_hint,
            )
        return self.save_to_file(
            target.name,
            output_dir or "presentations",
            copy_revealjs=copy_revealjs,
            quiet=quiet,
            pdf_hint=pdf_hint,
        )

    def save_to_file(
        self,
        filename: str = "presentation.html",
        output_dir: str = "presentations",
        *,
        copy_revealjs: bool = True,
        quiet: bool = False,
        pdf_hint: bool = False,
    ) -> Presentation:
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
            dist_reveal = revealjs_dest / "dist" / "reveal.js"

            with as_file(revealjs_ref) as revealjs_source:
                if not dist_reveal.exists():
                    if revealjs_dest.exists():
                        shutil.rmtree(revealjs_dest)
                    shutil.copytree(revealjs_source, revealjs_dest)

        full_path = presentations_dir / filename
        full_path.write_text(self.generate_html(), encoding="utf-8")

        if not quiet:
            print(f"Presentation saved to: {full_path}")
            if pdf_hint:
                print(f"PDF export URL: {self.pdf_print_url(full_path)}")
        return self

    # --- Internal rendering ---------------------------------------------------

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

        if item.vertical:
            return self._render_nested_slides(item, item.vertical)

        return item.render(default_background=self.background)

    def _iter_slides(self):
        for item in self.slides:
            if isinstance(item, dict) and item.get("type") == "group":
                for slide in item["slides"]:
                    yield slide
            elif isinstance(item, Slide):
                yield item
                yield from item.vertical