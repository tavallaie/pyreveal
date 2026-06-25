"""PyReveal feature showcase: plugins, fragments, notes, code, and backgrounds."""

from pyreveal import (
    CodeElement,
    ColorBackground,
    Fragment,
    ImageBackground,
    PyReveal,
    Slide,
)

presentation = PyReveal(title="Feature Demo", theme="dracula", transition="fade")
presentation.configure(hash=True, progress=True, slideNumber="c/t")
presentation.enable_plugins("notes", "highlight", "markdown")
presentation.set_background(ColorBackground("#1a1a2e", opacity=0.9))

intro = Slide(
    content="<h1>PyReveal 0.5</h1>",
    notes="Welcome the audience and outline the talk.",
    auto_animate=True,
)
intro.add_element(Fragment("Build decks in Python", effect="grow"))
intro.add_element(Fragment("Export portable HTML", index=1))
presentation.add_slide(intro)

code_slide = Slide(content="<h2>Code</h2>")
code_slide.add_element(
    CodeElement(
        "from pyreveal import PyReveal, Slide\n\n"
        "deck = PyReveal(title='Hello')\n"
        "deck.add_slide(Slide(content='<h1>Hi</h1>'))",
        language="python",
        line_numbers=True,
    )
)
presentation.add_slide(code_slide)

presentation.add_slide(
    Slide(
        content="<h2>Markdown slide</h2>",
        markdown="## Agenda\n\n- Slides\n- Fragments\n- Plugins",
        background=ImageBackground("path/to/bg.jpg", size="cover", position="center"),
    )
)

presentation.save_to_file("feature_demo.html")