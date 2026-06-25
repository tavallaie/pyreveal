"""PyReveal — programmatic Reveal.js presentation generation."""

__version__ = "0.3.0"

from .background import (
    Background,
    BackgroundFactory,
    ColorBackground,
    ImageBackground,
    VideoBackground,
)
from .core import PyReveal

__all__ = [
    "PyReveal",
    "Background",
    "BackgroundFactory",
    "ColorBackground",
    "ImageBackground",
    "VideoBackground",
    "__version__",
]