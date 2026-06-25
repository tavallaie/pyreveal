import pytest

from pyreveal import PyReveal, Slide
from pyreveal.exceptions import EmptySlideContentError, InvalidThemeError


def test_generate_html_includes_title_and_slides():
    presentation = PyReveal(title="Test Deck", theme="white", transition="fade")
    presentation.add_slide(content="<h1>Hello</h1>")

    html = presentation.generate_html()

    assert "<title>Test Deck</title>" in html
    assert "<h1>Hello</h1>" in html
    assert "revealjs/dist/theme/white.css" in html
    assert "transition: 'fade'" in html


def test_empty_slide_raises():
    presentation = PyReveal()
    with pytest.raises(EmptySlideContentError):
        presentation.add_slide(content="   ")


def test_invalid_theme_raises():
    presentation = PyReveal()
    with pytest.raises(InvalidThemeError):
        presentation.set_theme("not-a-theme")


def test_add_slide_object():
    presentation = PyReveal()
    presentation.add_slide(Slide(content="<p>Object slide</p>"))

    html = presentation.generate_html()
    assert "<p>Object slide</p>" in html


def test_legacy_vertical_slides():
    presentation = PyReveal()
    presentation.add_slide(content="Intro", title="Intro")
    presentation.add_slide(content="Vertical 1", group="Intro")
    presentation.add_slide(content="Vertical 2", group="Intro")

    html = presentation.generate_html()
    assert "Vertical 1" in html
    assert "Vertical 2" in html