"""Define slides with Slide(), then add them to the deck."""

from pyreveal import Presentation, Slide, Theme, Transition

intro = Slide()
intro.title = "Welcome to PyReveal"
intro.subtitle("Build decks in Python")
intro.vertical = [
    Slide.make_text("First vertical slide"),
    Slide.make_text("Second vertical slide"),
]

another = Slide()
another.heading = "Another horizontal slide"

photo = Slide()
photo.heading("Photo background")
photo.bg("path/to/image.jpg")

deck = (
    Presentation("My Presentation", theme=Theme.BLACK, transition=Transition.SLIDE)
    .configure(hash=True, progress=True, slideNumber="c/t")
    .add(intro, another, photo)
    .save("my_presentation.html")
)