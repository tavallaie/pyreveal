import pytest

from pyreveal import (
    BackgroundType,
    FragmentEffect,
    MathEngine,
    Plugin,
    Presentation,
    Slide,
    SlideVisibility,
    Theme,
    Transition,
)
from pyreveal.exceptions import InvalidThemeError, InvalidTransitionError


def test_presentation_accepts_theme_and_transition_enums():
    deck = Presentation(
        "Choices",
        theme=Theme.DRACULA,
        transition=Transition.FADE,
    )
    html = deck.html()
    assert "dracula.css" in html
    assert '"transition": "fade"' in html


def test_plugins_and_math_engine_enums():
    deck = Presentation("Plugins").plugins(Plugin.NOTES, Plugin.MATH, math_engine=MathEngine.KATEX)
    html = deck.html()
    assert "RevealNotes" in html
    assert "RevealMath.KaTeX" in html


def test_invalid_theme_still_raises():
    with pytest.raises(InvalidThemeError):
        Presentation("Bad").set_theme("not-a-theme")


def test_invalid_transition_still_raises():
    with pytest.raises(InvalidTransitionError):
        Presentation("Bad").set_transition("warp")


def test_slide_visibility_enum():
    slide = Slide(visibility=SlideVisibility.HIDDEN)
    assert 'data-visibility="hidden"' in slide.render()


def test_background_type_enum_in_dict():
    slide = Slide()
    slide.bg(type=BackgroundType.IMAGE, image="bg.jpg", size="cover")
    html = slide.render()
    assert 'data-background="bg.jpg"' in html


def test_fragment_effect_enum_on_slide():
    slide = Slide()
    slide.title = "Demo"
    slide.fragment("Point", effect=FragmentEffect.FADE_UP)
    assert "fragment fade-up" in slide.render()


def test_string_choices_still_work():
    deck = Presentation("Legacy", theme="white", transition="slide")
    deck.plugins("notes")
    assert "white.css" in deck.html()