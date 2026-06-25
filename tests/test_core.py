import pytest

from pyreveal import PyReveal
from pyreveal.exceptions import EmptySlideContentError, InvalidThemeError


def test_generate_html_includes_title_and_slides():
    presentation = PyReveal(title="Test Deck", theme="white", transition="fade")
    presentation.add_slide("<h1>Hello</h1>")

    html = presentation.generate_html()

    assert "<title>Test Deck</title>" in html
    assert "<h1>Hello</h1>" in html
    assert "revealjs/dist/theme/white.css" in html
    assert "transition: 'fade'" in html


def test_empty_slide_raises():
    presentation = PyReveal()
    with pytest.raises(EmptySlideContentError):
        presentation.add_slide("   ")


def test_invalid_theme_raises():
    presentation = PyReveal()
    with pytest.raises(InvalidThemeError):
        presentation.set_theme("not-a-theme")