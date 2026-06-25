from pyreveal import (
    ColorBackground,
    Fragment,
    ImageBackground,
    PyReveal,
    Slide,
)


def test_enable_plugins_in_html():
    presentation = PyReveal()
    presentation.enable_plugins("notes", "highlight", "markdown")
    presentation.add_slide(Slide(content="<p>Hi</p>"))

    html = presentation.generate_html()

    assert "revealjs/dist/plugin/notes.js" in html
    assert "revealjs/dist/plugin/highlight.js" in html
    assert "revealjs/dist/plugin/markdown.js" in html
    assert "plugin/highlight/monokai.css" in html
    assert "RevealNotes" in html
    assert "RevealHighlight" in html
    assert "RevealMarkdown" in html


def test_enable_plugins_invalid_name():
    presentation = PyReveal()
    try:
        presentation.enable_plugins("not-a-plugin")
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_save_to_string():
    presentation = PyReveal(title="String Deck")
    presentation.add_slide(Slide(content="<p>inline</p>"))
    html = presentation.save_to_string()
    assert "<title>String Deck</title>" in html
    assert "<p>inline</p>" in html


def test_presentation_default_background():
    presentation = PyReveal()
    presentation.set_background(ColorBackground("#abcdef"))
    presentation.add_slide(Slide(content="<p>No explicit bg</p>"))

    html = presentation.generate_html()
    assert 'data-background-color="#abcdef"' in html


def test_slide_auto_animate_and_notes():
    slide = Slide(
        content="<h2>Anim</h2>",
        auto_animate=True,
        auto_animate_easing="ease-in-out",
        notes="Say hello",
        transition="fade",
        state="alert",
    )
    html = slide.render()
    assert "data-auto-animate" in html
    assert 'data-auto-animate-easing="ease-in-out"' in html
    assert '<aside class="notes">Say hello</aside>' in html
    assert 'data-transition="fade"' in html
    assert 'data-state="alert"' in html


def test_slide_markdown_mode():
    slide = Slide(markdown="## Title\n\nBody")
    html = slide.render()
    assert "data-markdown" in html
    assert "## Title" in html
    assert "<script type=\"text/template\">" in html


def test_fragments_on_slide():
    presentation = PyReveal()
    slide = Slide(content="<h2>Steps</h2>")
    slide.add_element(Fragment("One"))
    slide.add_element(Fragment("Two", effect="grow"))
    presentation.add_slide(slide)

    html = presentation.generate_html()
    assert 'class="fragment"' in html
    assert 'class="fragment grow"' in html


def test_vertical_slides_with_default_background():
    presentation = PyReveal()
    presentation.set_background(ImageBackground("default.jpg"))
    parent = Slide(content="<h1>Main</h1>")
    parent.add_vertical_slide(Slide(content="<p>Sub</p>"))
    presentation.add_slide(parent)

    html = presentation.generate_html()
    assert 'data-background="default.jpg"' in html
    assert "<h1>Main</h1>" in html
    assert "<p>Sub</p>" in html