from pyreveal import FragmentEffect, Presentation, Slide


def test_instance_slide_builder():
    welcome = Slide()
    welcome.title("Welcome")
    welcome.subtitle = "PyReveal"
    welcome.fragment("Point one", effect=FragmentEffect.GROW)
    welcome.note("Say hello")

    agenda = Slide()
    agenda.heading("Agenda")
    agenda.bullets(["One", "Two", "Three"])

    code = Slide()
    code.heading("Demo")
    code.code("print('hi')", language="python")

    section = Slide()
    section.heading("Section")
    section.vertical = [Slide.make_text("Vertical detail")]

    deck = (
        Presentation("Fluent Deck", theme="white", transition="fade")
        .configure(hash=True, progress=True)
        .plugins("notes", "highlight")
        .bg("#111111")
        .add(welcome, agenda, code, section)
    )

    html = deck.html()
    assert "<title>Fluent Deck</title>" in html
    assert "<h1>Welcome</h1>" in html
    assert "<p>PyReveal</p>" in html
    assert "Point one" in html
    assert "<li>One</li>" in html
    assert "language-python" in html
    assert "print" in html and "hi" in html
    assert "Vertical detail" in html
    assert "RevealNotes" in html


def test_title_assignment_and_method():
    slide = Slide()
    slide.title = "Hello"
    assert "<h1>Hello</h1>" in slide.content

    slide2 = Slide()
    slide2.title("World", subtitle="Subtitle")
    assert "<h1>World</h1>" in slide2.content
    assert "<p>Subtitle</p>" in slide2.content


def test_slide_factories_still_work():
    slide = Slide.make_title("Hello", subtitle="World", bg="#333")
    assert "<h1>Hello</h1>" in slide.content
    assert slide.background is not None


def test_bg_accepts_color_string_and_image_dict():
    default_bg = Slide()
    default_bg.heading("Default background")

    custom_bg = Slide()
    custom_bg.heading("Custom background")
    custom_bg.bg(image="bg.jpg", size="cover")

    html = Presentation("BG").bg("#222").add(default_bg, custom_bg).html()
    assert 'data-background-color="#222"' in html
    assert 'data-background="bg.jpg"' in html


def test_fragments_via_slide_kwargs():
    slide = Slide.make_title(
        "Agenda",
        fragments=[("Intro", {"effect": FragmentEffect.GROW}), "Outro"],
    )
    html = Presentation("Frags").add(slide).html()
    assert "Intro" in html
    assert "fragment grow" in html
    assert "Outro" in html


def test_pyreveal_is_presentation_alias():
    from pyreveal import PyReveal

    assert PyReveal is Presentation


def test_save_path_with_directory(tmp_path):
    slide = Slide()
    slide.text("Done")
    Presentation("Save test").add(slide).save(
        tmp_path / "talk" / "deck.html", quiet=True
    )
    assert (tmp_path / "talk" / "deck.html").exists()


def test_vertical_array_can_be_reordered():
    first = Slide.make_text("First")
    second = Slide.make_text("Second")

    intro = Slide()
    intro.title = "Main"
    intro.vertical = [first, second]
    intro.vertical = [second, first]

    html = Presentation("Nested").add(intro).html()
    assert html.index("Second") < html.index("First")


def test_vertical_assignment_from_plain_text():
    intro = Slide()
    intro.title = "Section"
    intro.vertical = ["Point A", "Point B"]

    html = Presentation("Nested").add(intro).html()
    assert "Point A" in html
    assert "Point B" in html


def test_slide_accepts_html_positional_and_content_kwarg():
    slide = Slide("<h1>Hello</h1>")
    assert "<h1>Hello</h1>" in slide.content

    slide2 = Slide(content="<p>Hi</p>")
    assert "<p>Hi</p>" in slide2.content

    slide3 = Slide()
    slide3.content = "<h2>Custom</h2>"
    assert "<h2>Custom</h2>" in slide3.content


def test_plain_text_string_becomes_paragraph():
    slide = Slide("Just text")
    assert "<p>Just text</p>" in slide.content


def test_animate_accepts_plain_text():
    deck = Presentation("Anim").animate(
        [{"title": "Before"}, {"title": "After"}]
    )
    html = deck.html()
    assert "Before" in html
    assert "After" in html
    assert 'data-id="title"' in html


def test_save_recopies_incomplete_revealjs(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    stale = output_dir / "revealjs"
    stale.mkdir()
    (stale / "README.md").write_text("incomplete copy")

    Presentation("T").add(Slide.make_text("hi")).save_to_file(
        "deck.html",
        output_dir=str(output_dir),
        copy_revealjs=True,
        quiet=True,
    )

    assert (output_dir / "revealjs" / "dist" / "reveal.js").is_file()