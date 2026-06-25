"""PyReveal — programmatic Reveal.js presentation generation."""

__version__ = "0.7.0"

from .auto_animate import AutoAnimate
from .background import (
    Background,
    BackgroundFactory,
    ColorBackground,
    GradientBackground,
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
    LinkElement,
    MarkdownElement,
    MathElement,
    SpeakerNotes,
    VideoElement,
)
from .layouts import FitText, HStack, Layout, Stack, VStack
from .slide import Slide
from .style import CSS, Style

__all__ = [
    "AutoAnimate",
    "PyReveal",
    "Slide",
    "Element",
    "Fragment",
    "SpeakerNotes",
    "ImageElement",
    "VideoElement",
    "LinkElement",
    "MathElement",
    "CodeElement",
    "MarkdownElement",
    "Layout",
    "Stack",
    "HStack",
    "VStack",
    "FitText",
    "Style",
    "CSS",
    "Background",
    "BackgroundFactory",
    "ColorBackground",
    "GradientBackground",
    "ImageBackground",
    "VideoBackground",
    "IframeBackground",
    "__version__",
]