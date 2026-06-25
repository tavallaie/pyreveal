import pytest

from pyreveal import (
    CodeElement,
    Element,
    Fragment,
    ImageElement,
    MarkdownElement,
    SpeakerNotes,
    Style,
    VideoElement,
)


def test_fragment_basic():
    frag = Fragment("Step one")
    html = frag.generate_html()
    assert 'class="fragment"' in html
    assert "Step one" in html


def test_fragment_with_effect_and_index():
    frag = Fragment("Grow", effect="grow", index=2)
    html = frag.generate_html()
    assert 'class="fragment grow"' in html
    assert 'data-fragment-index="2"' in html


def test_fragment_invalid_effect():
    with pytest.raises(ValueError):
        Fragment("bad", effect="not-real")


def test_speaker_notes():
    notes = SpeakerNotes("Remember to mention the roadmap.")
    assert '<aside class="notes">' in notes.generate_html()


def test_code_element_with_language():
    code = CodeElement("print('hi')", language="python", line_numbers=True)
    html = code.generate_html()
    assert 'class="language-python"' in html
    assert "data-line-numbers" in html
    assert "print(" in html and "hi" in html


def test_markdown_element():
    md = MarkdownElement("## Hello\n\nWorld")
    html = md.generate_html()
    assert "data-markdown" in html
    assert "## Hello" in html


def test_element_data_id():
    el = Element(tag="p", content="text", data_id="title")
    assert 'data-id="title"' in el.generate_html()


def test_video_element_without_data_id():
    video = VideoElement("clip.mp4")
    html = video.generate_html()
    assert "data-id" not in html
    assert 'src="clip.mp4"' in html


def test_image_element_with_style():
    img = ImageElement("pic.png", alt_text="Pic", style=Style(width="100px"))
    html = img.generate_html()
    assert 'alt="Pic"' in html
    assert "width: 100px" in html