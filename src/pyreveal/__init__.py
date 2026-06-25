"""PyReveal — programmatic Reveal.js presentation generation."""

__version__ = "0.5.0"

from .background import (
    Background,
    BackgroundFactory,
    ColorBackground,
    IframeBackground,
    ImageBackground,
    VideoBackground,
)
from .core import PyReveal
from .element import (
    CodeElement,
    Element,
    Fragment,
    ImageElement,
    MarkdownElement,
    SpeakerNotes,
    VideoElement,
)
from .slide import Slide
from .style import CSS, Style

__all__ = [
    "PyReveal",
    "Slide",
    "Element",
    "Fragment",
    "SpeakerNotes",
    "ImageElement",
    "VideoElement",
    "CodeElement",
    "MarkdownElement",
    "Style",
    "CSS",
    "Background",
    "BackgroundFactory",
    "ColorBackground",
    "ImageBackground",
    "VideoBackground",
    "IframeBackground",
    "__version__",
]