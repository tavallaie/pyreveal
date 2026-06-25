import pytest

from pyreveal import PyReveal, Slide
from pyreveal.exceptions import InvalidThemeError


def test_generate_html_includes_title_and_slides():
    presentation = PyReveal(title="Test Deck", theme="white", transition="fade")
    presentation.add_slide(Slide(content="<h1>Hello</h1>"))

    html = presentation.generate_html()

    assert "<title>Test Deck</title>" in html
    assert "<h1>Hello</h1>" in html
    assert "revealjs/dist/theme/white.css" in html
    assert '"transition": "fade"' in html


def test_configure_options_in_initialize():
    presentation = PyReveal(transition="slide")
    presentation.configure(hash=True, progress=False, slideNumber="c/t")

    html = presentation.generate_html()

    assert '"hash": true' in html
    assert '"progress": false' in html
    assert '"slideNumber": "c/t"' in html


def test_configure_overrides_transition():
    presentation = PyReveal(transition="slide")
    presentation.configure(transition="zoom")

    html = presentation.generate_html()
    assert '"transition": "zoom"' in html


def test_invalid_theme_raises():
    presentation = PyReveal()
    with pytest.raises(InvalidThemeError):
        presentation.set_theme("not-a-theme")


def test_add_slide_object():
    presentation = PyReveal()
    presentation.add_slide(Slide(content="<p>Object slide</p>"))

    html = presentation.generate_html()
    assert "<p>Object slide</p>" in html


def test_vertical_slides_on_slide_object():
    presentation = PyReveal()
    parent = Slide(content="<h1>Intro</h1>")
    parent.add_vertical_slide(Slide(content="<p>Vertical 1</p>"))
    parent.add_vertical_slide(Slide(content="<p>Vertical 2</p>"))
    presentation.add_slide(parent)

    html = presentation.generate_html()
    assert "Vertical 1" in html
    assert "Vertical 2" in html


def test_add_group():
    presentation = PyReveal()
    presentation.add_group(
        [
            Slide(content="<h2>Stack</h2>"),
            Slide(content="<p>One</p>"),
        ]
    )

    html = presentation.generate_html()
    assert "<h2>Stack</h2>" in html
    assert "<p>One</p>" in html