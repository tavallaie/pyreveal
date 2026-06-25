"""PyReveal — programmatic Reveal.js presentation generation."""

__version__ = "0.4.0"

from .background import (
    Background,
    BackgroundFactory,
    ColorBackground,
    ImageBackground,
    VideoBackground,
)
from .core import PyReveal
from .element import Element, ImageElement, VideoElement
from .slide import Slide
from .style import CSS, Style

__all__ = [
    "PyReveal",
    "Slide",
    "Element",
    "ImageElement",
    "VideoElement",
    "Style",
    "CSS",
    "Background",
    "BackgroundFactory",
    "ColorBackground",
    "ImageBackground",
    "VideoBackground",
    "__version__",
]