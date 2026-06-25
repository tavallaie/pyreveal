from pyreveal import AutoAnimate, Plugin, Presentation, Slide


def test_auto_slide_interval():
    deck = Presentation("Kiosk").auto_slide(5000)
    html = deck.html()
    assert '"autoSlide": 5000' in html


def test_auto_slide_loop_and_not_stoppable():
    deck = Presentation("Loop").auto_slide(3000, loop=True, stoppable=False)
    html = deck.html()
    assert '"autoSlide": 3000' in html
    assert '"loop": true' in html
    assert '"autoSlideStoppable": false' in html


def test_auto_slide_disable():
    deck = Presentation("Off").auto_slide(False)
    html = deck.html()
    assert '"autoSlide": false' in html


def test_auto_slide_zero_uses_per_slide_only():
    slide = Slide("Timed", auto_slide=2000)
    deck = Presentation("Mixed").auto_slide(0).add(slide)
    html = deck.html()
    assert '"autoSlide": 0' in html
    assert 'data-autoslide="2000"' in html


def test_auto_animate_text_helper():
    element = AutoAnimate.text("title", "Hello")
    assert element.data_id == "title"
    assert 'data-id="title"' in element.generate_html()
    assert "Hello" in element.generate_html()


def test_auto_animate_text_custom_tag():
    element = AutoAnimate.text("badge", "New", tag="span")
    html = element.generate_html()
    assert "<span" in html
    assert 'data-id="badge"' in html


def test_animate_plain_text_frames():
    deck = Presentation("Anim").animate(
        [
            {"title": "Before", "count": "1"},
            {"title": "After", "count": "2"},
        ]
    )
    html = deck.html()
    assert html.count('data-id="title"') == 2
    assert html.count('data-id="count"') == 2
    assert "Before" in html
    assert "After" in html


def test_search_plugin_in_html():
    deck = Presentation("Search").plugins(Plugin.SEARCH)
    html = deck.html()
    assert 'plugin/search.js' in html
    assert "RevealSearch" in html