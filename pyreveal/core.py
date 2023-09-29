# pyreveal.py
import os
import shutil
import pkg_resources

from .exceptions import (
    InvalidThemeError,
    InvalidTransitionError,
    EmptySlideContentError,
)
from .utils import generate_slides_html, wrap_in_html_template


class PyReveal:
    VALID_THEMES = [
        "black",
        "white",
        "league",
        "sky",
        "beige",
        "simple",
        "serif",
        "night",
        "moon",
        "solarized",
    ]
    VALID_TRANSITIONS = ["slide", "fade", "convex", "concave", "zoom"]

    def __init__(
        self, title="Untitled Presentation", theme="black", transition="slide"
    ):
        self.title = title
        self.slides = []
        self.set_theme(theme)
        self.set_transition(transition)

    def add_slide(self, content, title=None):
        if not content.strip():
            raise EmptySlideContentError("Slide content cannot be empty.")
        slide = {"title": title, "content": content}
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

    def save_to_file(self, filename="presentation.html"):
        # Ensure the presentations directory exists
        presentations_dir = "presentations"
        if not os.path.exists(presentations_dir):
            os.makedirs(presentations_dir)

        # Locate the Reveal.js assets bundled with your package
        revealjs_source = pkg_resources.resource_filename("pyreveal", "revealjs")

        # Construct the full path to save the file
        full_path = os.path.join(presentations_dir, filename)

        # Copy the Reveal.js assets to the presentations directory
        revealjs_dest = os.path.join(presentations_dir, "revealjs")
        if not os.path.exists(revealjs_dest):
            shutil.copytree(revealjs_source, revealjs_dest)

        with open(full_path, "w") as f:
            f.write(self.generate_html())

        print(f"Presentation saved to: {full_path}")
