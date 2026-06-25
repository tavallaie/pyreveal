"""Build slides step by step, compose the deck, export."""

from pyreveal import FragmentEffect, Plugin, Presentation, Slide, Theme, Transition

# Optional: kiosk auto-slide and in-deck search
# deck.auto_slide(8000, loop=True)
# deck.plugins(Plugin.SEARCH)

welcome = Slide()
welcome.title("PyReveal")
welcome.fragment("Build decks in Python", effect=FragmentEffect.GROW)
welcome.fragment("Export portable HTML", index=1)
welcome.note("Welcome the audience and outline the talk.")

code = Slide()
code.heading("Code")
code.code(
    "from pyreveal import Presentation, Slide\n\n"
    "welcome = Slide()\n"
    "welcome.title = 'Hi'\n"
    "Presentation('Hello').add(welcome).save('deck.html')",
    language="python",
    line_numbers=True,
)

agenda = Slide()
agenda.markdown = "## Agenda\n\n- Slides\n- Fragments\n- Plugins"
agenda.bg(image="path/to/bg.jpg", size="cover", position="center")

deck = (
    Presentation("Feature Demo", theme=Theme.DRACULA, transition=Transition.FADE)
    .configure(hash=True, progress=True, slideNumber="c/t")
    .plugins(Plugin.NOTES, Plugin.HIGHLIGHT, Plugin.MARKDOWN)
    .bg("#1a1a2e", opacity=0.9)
    .add(welcome, code)
    .animate(
        [
            {"title": "Before"},
            {"title": "After"},
        ],
        easing="ease-in-out",
    )
    .add(agenda)
    .save("feature_demo.html")
)