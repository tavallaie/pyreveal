from pyreveal import KeyboardBinding, Presentation, Slide


def test_auto_progression_alias():
    deck = Presentation("Prog").auto_progression(4000, loop=True)
    html = deck.html()
    assert '"autoSlide": 4000' in html
    assert '"loop": true' in html


def test_parallax_background():
    deck = Presentation("Para").parallax_background(
        "parallax.jpg",
        size="2100px 900px",
        repeat="no-repeat",
        position="top left",
        horizontal=200,
        vertical=50,
    )
    html = deck.html()
    assert '"parallaxBackgroundImage": "parallax.jpg"' in html
    assert '"parallaxBackgroundSize": "2100px 900px"' in html
    assert '"parallaxBackgroundRepeat": "no-repeat"' in html
    assert '"parallaxBackgroundPosition": "top left"' in html
    assert '"parallaxBackgroundHorizontal": 200' in html
    assert '"parallaxBackgroundVertical": 50' in html


def test_keyboard_bindings_enum_and_disable():
    deck = Presentation("Keys").keyboard_bindings(
        {13: KeyboardBinding.NEXT, 32: None},
        condition="focused",
    )
    html = deck.html()
    assert '"13": "next"' in html
    assert '"32": null' in html
    assert '"keyboardCondition": "focused"' in html


def test_keyboard_bindings_string_action():
    deck = Presentation("Keys").keyboard_bindings({66: "togglePause"})
    html = deck.html()
    assert '"66": "togglePause"' in html


def test_slide_background_parallax():
    slide = Slide()
    slide.bg(image="bg.jpg", parallax="2")
    html = slide.render()
    assert 'data-background-parallax="2"' in html