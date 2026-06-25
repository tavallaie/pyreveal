import shutil
from importlib.resources import as_file, files
from pathlib import Path

from .background import Background, ImageBackground, VideoBackground
from .exceptions import (
    DuplicateSlideTitleError,
    EmptySlideContentError,
    InvalidThemeError,
    InvalidTransitionError,
    SlideGroupNotFoundError,
)
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
        self.slides = []
        self.background = None
        self.set_theme(theme)
        self.set_transition(transition)

    def add_slide(
        self, slide=None, content=None, title=None, group=None, background=None
    ):
        if slide is not None:
            if not isinstance(slide, Slide):
                raise TypeError("Expected instance of Slide.")
            self.slides.append(slide)
            return

        if content is None:
            raise TypeError("Either a Slide instance or content string is required.")

        if not content.strip():
            raise EmptySlideContentError()

        new_slide = Slide(content=content, title=title, background=background)

        if group:
            if not any(
                isinstance(item, Slide) and item.title == group for item in self.slides
            ):
                raise SlideGroupNotFoundError(group)

            for item in self.slides:
                if (
                    isinstance(item, dict)
                    and item.get("type") == "group"
                    and item.get("parent_title") == group
                ):
                    item["slides"].append(new_slide)
                    return

            self.slides.append(
                {"type": "group", "parent_title": group, "slides": [new_slide]}
            )
            return

        if title and any(
            isinstance(item, Slide) and item.title == title for item in self.slides
        ):
            raise DuplicateSlideTitleError(title)

        self.slides.append(new_slide)

    def set_theme(self, theme):
        if theme not in self.VALID_THEMES:
            raise InvalidThemeError(theme, self.VALID_THEMES)
        self.theme = theme

    def set_transition(self, transition):
        if transition not in self.VALID_TRANSITIONS:
            raise InvalidTransitionError(transition, self.VALID_TRANSITIONS)
        self.transition = transition

    def set_background(self, background):
        if not isinstance(background, Background):
            raise TypeError("Expected instance of Background class.")
        self.background = background

    def add_group(self, slides):
        if not all(isinstance(slide, Slide) for slide in slides):
            raise TypeError("All items in the group must be instances of Slide.")
        self.slides.append({"type": "group", "slides": slides})

    def _groups_for_parent(self, parent_title):
        groups = []
        for item in self.slides:
            if (
                isinstance(item, dict)
                and item.get("type") == "group"
                and item.get("parent_title") == parent_title
            ):
                groups.extend(item["slides"])
        return groups

    def _render_slide_item(self, item):
        if isinstance(item, dict) and item.get("type") == "group":
            group_html = "\n".join(slide.render() for slide in item["slides"])
            return f"<section>\n{group_html}\n</section>"

        if not isinstance(item, Slide):
            raise TypeError(f"Unexpected slide item: {item!r}")

        vertical_slides = self._groups_for_parent(item.title)
        if vertical_slides:
            vertical_html = "\n".join(slide.render() for slide in vertical_slides)
            background_html = item.background.generate_html() if item.background else ""
            return (
                f"<section{background_html}>\n{item.render()}\n{vertical_html}\n</section>"
            )

        return item.render()

    def generate_html(self):
        rendered = []
        grouped_parents = {
            item.get("parent_title")
            for item in self.slides
            if isinstance(item, dict) and item.get("type") == "group"
        }

        for item in self.slides:
            if (
                isinstance(item, dict)
                and item.get("type") == "group"
                and item.get("parent_title")
            ):
                continue

            if isinstance(item, Slide) and item.title in grouped_parents:
                rendered.append(self._render_slide_item(item))
            elif isinstance(item, Slide):
                rendered.append(item.render())
            else:
                rendered.append(self._render_slide_item(item))

        return wrap_in_html_template(
            self.title, self.theme, self.transition, "\n".join(rendered)
        )

    def _iter_slides(self):
        for item in self.slides:
            if isinstance(item, dict) and item.get("type") == "group":
                for slide in item["slides"]:
                    yield slide
            elif isinstance(item, Slide):
                yield item

    def save_to_file(self, filename="presentation.html", output_dir="presentations"):
        presentations_dir = Path(output_dir)
        presentations_dir.mkdir(parents=True, exist_ok=True)

        assets_dir = presentations_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        for slide in self._iter_slides():
            copy_assets_for_slide(slide, assets_dir, presentations_dir)
            for element in slide.elements:
                copy_element_assets(element, assets_dir, presentations_dir)

        revealjs_ref = files("pyreveal") / "revealjs"
        revealjs_dest = presentations_dir / "revealjs"

        with as_file(revealjs_ref) as revealjs_source:
            if not revealjs_dest.exists():
                shutil.copytree(revealjs_source, revealjs_dest)

        full_path = presentations_dir / filename
        full_path.write_text(self.generate_html(), encoding="utf-8")

        print(f"Presentation saved to: {full_path}")