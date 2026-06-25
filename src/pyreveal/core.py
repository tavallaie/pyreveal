import os
import shutil
from importlib.resources import as_file, files
from pathlib import Path

from .background import ImageBackground, VideoBackground
from .exceptions import (
    DuplicateSlideTitleError,
    EmptySlideContentError,
    InvalidThemeError,
    InvalidTransitionError,
    SlideGroupNotFoundError,
)
from .utils import generate_slides_html, wrap_in_html_template


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
        self.set_theme(theme)
        self.set_transition(transition)

    def add_slide(self, content, title=None, group=None, background=None):
        if not content.strip():
            raise EmptySlideContentError("Slide content cannot be empty.")

        if title and any(slide["title"] == title for slide in self.slides):
            raise DuplicateSlideTitleError(title)

        if group and not any(slide["title"] == group for slide in self.slides):
            raise SlideGroupNotFoundError(group)

        slide = {
            "title": title,
            "content": content,
            "group": group,
            "background": background,
        }
        self.slides.append(slide)

    def set_theme(self, theme):
        if theme not in self.VALID_THEMES:
            raise InvalidThemeError(
                f"'{theme}' is not a valid theme. Valid themes are: {', '.join(self.VALID_THEMES)}"
            )
        self.theme = theme

    def set_transition(self, transition):
        if transition not in self.VALID_TRANSITIONS:
            raise InvalidTransitionError(
                f"'{transition}' is not a valid transition. Valid transitions are: {', '.join(self.VALID_TRANSITIONS)}"
            )
        self.transition = transition

    def generate_html(self):
        slides_html = generate_slides_html(self.slides)
        return wrap_in_html_template(
            self.title, self.theme, self.transition, slides_html
        )

    def save_to_file(self, filename="presentation.html", output_dir="presentations"):
        presentations_dir = Path(output_dir)
        presentations_dir.mkdir(parents=True, exist_ok=True)

        assets_dir = presentations_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        for slide in self.slides:
            background = slide.get("background")
            if background and isinstance(background, ImageBackground):
                new_image_path = shutil.copy(background.image_url, assets_dir)
                slide["background"].image_url = os.path.relpath(
                    new_image_path, presentations_dir
                )
            elif background and isinstance(background, VideoBackground):
                new_video_path = shutil.copy(background.video_url, assets_dir)
                slide["background"].video_url = os.path.relpath(
                    new_video_path, presentations_dir
                )

        revealjs_ref = files("pyreveal") / "revealjs"
        revealjs_dest = presentations_dir / "revealjs"

        with as_file(revealjs_ref) as revealjs_source:
            if not revealjs_dest.exists():
                shutil.copytree(revealjs_source, revealjs_dest)

        full_path = presentations_dir / filename
        full_path.write_text(self.generate_html(), encoding="utf-8")

        print(f"Presentation saved to: {full_path}")