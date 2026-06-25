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
from .content import BulletList, Content, Heading, Paragraph
from .core import PyReveal
from .choices import (
    BackgroundSize,
    BackgroundType,
    CustomPlugin,
    FragmentEffect,
    KeyboardBinding,
    MathEngine,
    Plugin,
    ScrollLayout,
    ScrollSnap,
    SlideNumber,
    SlideVisibility,
    Theme,
    Transition,
    View,
)
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
from .presentation import Presentation
from .slide import Slide
from .style import CSS, Style

__all__ = [
    "Presentation",
    "PyReveal",
    "Slide",
    "Theme",
    "Transition",
    "Plugin",
    "CustomPlugin",
    "MathEngine",
    "View",
    "SlideNumber",
    "ScrollLayout",
    "ScrollSnap",
    "BackgroundType",
    "BackgroundSize",
    "SlideVisibility",
    "FragmentEffect",
    "KeyboardBinding",
    "__version__",
    # Advanced / low-level (optional)
    "Content",
    "Heading",
    "Paragraph",
    "BulletList",
    "AutoAnimate",
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
]