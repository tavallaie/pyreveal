from pathlib import Path

import pytest

from pyreveal import (
    FitText,
    GradientBackground,
    HStack,
    IframeBackground,
    ImageElement,
    Layout,
    LinkElement,
    MathElement,
    PyReveal,
    Slide,
    Stack,
    VideoBackground,
)
from pyreveal.helpers import is_remote_asset


def test_gradient_background():
    bg = GradientBackground("linear-gradient(to bottom, #111, #222)")
    html = bg.generate_html()
    assert "data-background-gradient=" in html


def test_iframe_background_interactive():
    bg = IframeBackground("https://example.com", interactive=True, preload=True)
    html = bg.generate_html()
    assert 'data-background-iframe="https://example.com"' in html
    assert "data-background-interactive" in html
    assert "data-preload" in html


def test_video_background_multiple_sources():
    bg = VideoBackground(sources=["a.mp4", "a.webm"], preload=True)
    html = bg.generate_html()
    assert 'data-background-video="a.mp4,a.webm"' in html
    assert "data-preload" in html


def test_slide_visibility_and_id():
    slide = Slide(
        content="<p>Hidden</p>",
        slide_id="secret",
        visibility="hidden",
    )
    html = slide.render()
    assert 'id="secret"' in html
    assert 'data-visibility="hidden"' in html


def test_layout_stack():
    layout = Stack(
        children=[
            ImageElement("a.png", stretch=True),
            ImageElement("b.png", stretch=True),
        ]
    )
    html = layout.generate_html()
    assert 'class="r-stack"' in html
    assert "r-stretch" in html


def test_hstack_and_fit_text():
    row = HStack(children=[FitText("BIG")])
    html = row.generate_html()
    assert "r-hstack" in html
    assert "r-fit-text" in html


def test_math_and_link_elements():
    math = MathElement(r"E = mc^2", display=True)
    link = LinkElement("#/2", "Go to slide 2", preview=True)
    assert math.generate_html().startswith("\\[")
    assert 'data-preview-link="#/2"' in link.generate_html()


def test_lazy_image():
    img = ImageElement("https://cdn.example.com/pic.png", lazy=True)
    html = img.generate_html()
    assert 'data-src="https://cdn.example.com/pic.png"' in html
    assert ' src="' not in html


def test_is_remote_asset():
    assert is_remote_asset("https://x.com/a.png")
    assert not is_remote_asset("local.png")


def test_enable_math_katex_engine():
    presentation = PyReveal()
    presentation.enable_plugins("math", math_engine="katex")
    html = presentation.generate_html()
    assert "RevealMath.KaTeX" in html


def test_extra_css_and_inline():
    presentation = PyReveal()
    presentation.add_stylesheet("custom.css")
    presentation.add_inline_css(".brand { color: gold; }")
    html = presentation.generate_html()
    assert 'href="custom.css"' in html
    assert ".brand { color: gold; }" in html


def test_remote_image_not_copied(tmp_path):
    presentation = PyReveal()
    slide = Slide(content="<h2>Remote</h2>")
    slide.add_element(ImageElement("https://example.com/logo.png"))
    presentation.add_slide(slide)
    presentation.save_to_file(
        "deck.html", output_dir=str(tmp_path), copy_revealjs=False, quiet=True
    )
    html = (tmp_path / "deck.html").read_text()
    assert 'src="https://example.com/logo.png"' in html
    assert list((tmp_path / "assets").iterdir()) == []


def test_local_image_copied(tmp_path):
    asset = tmp_path / "photo.png"
    asset.write_bytes(b"png")
    presentation = PyReveal()
    slide = Slide(content="<h2>Local</h2>")
    slide.add_element(ImageElement(str(asset)))
    presentation.add_slide(slide)
    presentation.save_to_file(
        "deck.html", output_dir=str(tmp_path), copy_revealjs=False, quiet=True
    )
    html = (tmp_path / "deck.html").read_text()
    assert "assets/photo.png" in html
    assert (tmp_path / "assets" / "photo.png").exists()


def test_invalid_math_engine():
    presentation = PyReveal()
    with pytest.raises(ValueError, match="MathEngine"):
        presentation.enable_plugins("math", math_engine="not-real")