from pyreveal import (
    CustomPlugin,
    Presentation,
    Plugin,
    Slide,
    SlideNumber,
    View,
)
from pyreveal.config import pdf_print_query


def test_navigation_and_deep_links_helpers():
    deck = (
        Presentation("Nav")
        .navigation(hash=True, progress=True, overview=True)
        .deep_links(hash=True, respond_to_hash_changes=True)
    )
    html = deck.html()
    assert '"hash": true' in html
    assert '"progress": true' in html
    assert '"overview": true' in html
    assert '"respondToHashChanges": true' in html


def test_scroll_view_helper():
    deck = Presentation("Scroll").scroll_view()
    html = deck.html()
    assert '"view": "scroll"' in html
    assert '"scrollLayout": "full"' in html
    assert '"scrollSnap": "mandatory"' in html


def test_slide_numbers_helper():
    deck = Presentation("Numbers").slide_numbers(SlideNumber.C_SLASH_T)
    html = deck.html()
    assert '"slideNumber": "c/t"' in html


def test_presentation_size_and_preview_links():
    deck = (
        Presentation("Size")
        .presentation_size(1280, 720)
        .preview_links(True)
    )
    html = deck.html()
    assert '"width": 1280' in html
    assert '"height": 720' in html
    assert '"previewLinks": true' in html


def test_custom_plugin_paths():
    custom = CustomPlugin("assets/extra.js", "RevealExtra")
    deck = Presentation("Custom").enable_plugins(Plugin.NOTES, custom)
    html = deck.html()
    assert 'src="assets/extra.js"' in html
    assert "RevealExtra" in html
    assert "RevealNotes" in html


def test_slide_id_alias_and_image_lightbox():
    slide = Slide()
    slide.id = "intro"
    slide.image("photo.jpg", preview=True)
    html = slide.render()
    assert 'id="intro"' in html
    assert 'data-preview-image="photo.jpg"' in html


def test_video_lightbox():
    from pyreveal import VideoElement

    slide = Slide()
    slide.element(VideoElement("clip.mp4", preview=True))
    html = slide.render()
    assert 'data-preview-video="clip.mp4"' in html


def test_pdf_print_url_and_query():
    assert Presentation.pdf_print_url("output/talk.html") == "output/talk.html?print-pdf"
    assert pdf_print_query() == "?print-pdf"


def test_print_view_helper():
    deck = Presentation("Print").print_view()
    assert '"view": "print"' in deck.html()