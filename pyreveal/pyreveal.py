import os
import shutil
import pkg_resources

from .exceptions import (
    InvalidThemeError,
    InvalidTransitionError,
    EmptySlideContentError,
    DuplicateSlideTitleError,
    SlideGroupNotFoundError,
)
from .utils import generate_slides_html, wrap_in_html_template
from .background import ImageBackground, VideoBackground, Background
from .element import ImageElement, VideoElement
from .helpers import copy_element_assets, copy_assets_for_slide
from .slide import Slide


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
        self.background = None

    def add_slide(self, slide):
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

    def set_background(self, background):
        if not isinstance(background, Background):
            raise TypeError("Expected instance of Background class.")
        self.background = background

    def add_group(self, slides):
        """
        Add a group of slides (vertical slides) to the presentation.
        """
        if not all(isinstance(slide, Slide) for slide in slides):
            raise TypeError("All items in the group must be instances of Slide.")

        group = {"type": "group", "slides": slides}
        self.slides.append(group)

    def generate_html(self):
        slides_html = []
        for item in self.slides:
            if item["type"] == "group":
                group_html = "\n".join([slide.render() for slide in item["slides"]])
                slides_html.append(f"<section>\n{group_html}\n</section>")
            else:
                slides_html.append(item.render())

        return wrap_in_html_template(
            self.title, self.theme, self.transition, "\n".join(slides_html)
        )

    def save_to_file(self, filename="presentation.html"):
        # Ensure the presentations directory exists
        presentations_dir = "presentations"
        if not os.path.exists(presentations_dir):
            os.makedirs(presentations_dir)
        # Ensure the assets directory exists inside presentations
        assets_dir = os.path.join(presentations_dir, "assets")
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        # Copy assets (background images, videos, etc.) to the assets directory and update slide references

        for slide in self.slides:
            background = slide.background
            if background and isinstance(background, ImageBackground):
                # Copy the image and update the slide's image URL
                new_image_path = shutil.copy(background.image_url, assets_dir)
                slide.background.image_url = os.path.relpath(
                    new_image_path, presentations_dir
                )
            elif background and isinstance(background, VideoBackground):
                # Copy the video and update the slide's video URL
                new_video_path = shutil.copy(background.video_url, assets_dir)
                slide.background.video_url = os.path.relpath(
                    new_video_path, presentations_dir
                )
            # Copy element assets (images, videos, etc.) to the assets directory and update element references
            for element in slide.elements:
                copy_element_assets(element, assets_dir, presentations_dir)

        # Locate the Reveal.js assets bundled with your package
        revealjs_source = pkg_resources.resource_filename("pyreveal", "revealjs")

        # Construct the full path to save the file
        full_path = os.path.join(presentations_dir, filename)

        # Copy the Reveal.js assets to the presentations directory
        revealjs_dest = os.path.join(presentations_dir, "revealjs")
        if not os.path.exists(revealjs_dest):
            shutil.copytree(revealjs_source, revealjs_dest)

        with open(full_path, "w") as f:
            html = self.generate_html()
            print(html)
            f.write(html)

        print(f"Presentation saved to: {full_path}")
