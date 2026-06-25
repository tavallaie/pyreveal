import pytest

from pyreveal import AutoAnimate, Element, PyReveal


def test_match_sets_data_id():
    element = Element(tag="h2", content="Hello")
    AutoAnimate.match("title", element)
    assert element.data_id == "title"
    assert 'data-id="title"' in element.generate_html()


def test_html_injects_data_id():
    markup = AutoAnimate.html("title", "<h2>Hello</h2>")
    assert 'data-id="title"' in markup
    assert "<h2" in markup
    assert "Hello</h2>" in markup


def test_html_rejects_existing_data_id():
    with pytest.raises(ValueError, match="already contains data-id"):
        AutoAnimate.html("title", '<h2 data-id="x">Hello</h2>')


def test_slide_with_matches():
    helper = AutoAnimate(easing="ease-in-out")
    slide = helper.slide(
        matches={
            "title": Element(tag="h2", content="Hello"),
            "body": Element(tag="p", content="World"),
        }
    )
    html = slide.render()
    assert "data-auto-animate" in html
    assert 'data-auto-animate-easing="ease-in-out"' in html
    assert 'data-id="title"' in html
    assert 'data-id="body"' in html


def test_sequence_assigns_shared_keys():
    helper = AutoAnimate()
    slides = helper.sequence(
        [
            {"title": Element(tag="h2", content="Hello")},
            {"title": Element(tag="h2", content="Hello World")},
            {
                "title": Element(tag="h2", content="Goodbye"),
                "badge": Element(tag="span", content="New"),
            },
        ]
    )
    assert len(slides) == 3
    assert all(s.auto_animate for s in slides)
    assert slides[0].elements[0].data_id == "title"
    assert slides[1].elements[0].data_id == "title"
    assert slides[2].elements[1].data_id == "badge"


def test_sequence_with_html_string_values():
    helper = AutoAnimate()
    slides = helper.sequence(
        [
            {"title": "<h2>One</h2>"},
            {"title": "<h2>Two</h2>"},
        ]
    )
    html = slides[0].render() + slides[1].render()
    assert html.count('data-id="title"') == 2
    assert "One</h2>" in html
    assert "Two</h2>" in html


def test_sequence_with_content_key():
    helper = AutoAnimate()
    slides = helper.sequence(
        [
            {"_content": "<p>Intro</p>", "title": Element(tag="h2", content="A")},
            {"title": Element(tag="h2", content="B")},
        ]
    )
    assert "<p>Intro</p>" in slides[0].render()


def test_add_auto_animate_sequence_on_presentation():
    presentation = PyReveal()
    presentation.add_auto_animate_sequence(
        [
            {"title": Element(tag="h2", content="Start")},
            {"title": Element(tag="h2", content="End")},
        ],
        easing="ease-in-out",
    )
    html = presentation.generate_html()
    assert html.count("<section data-auto-animate") == 2
    assert html.count('data-id="title"') == 2
    assert 'data-auto-animate-easing="ease-in-out"' in html


def test_match_key_mismatch_raises():
    helper = AutoAnimate()
    element = Element(tag="h2", content="Hi", data_id="other")
    with pytest.raises(ValueError, match="does not match key"):
        helper.slide(matches={"title": element})