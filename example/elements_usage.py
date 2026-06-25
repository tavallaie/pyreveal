"""Build slides from elements, styles, and Reveal.js configuration."""

from pyreveal import ImageElement, Presentation, Slide, Style, Theme, Transition

title_slide = Slide()
title_slide.title = "PyReveal Elements"

styled_slide = Slide()
styled_slide.heading("Styled image")
styled_slide.element(
    ImageElement(
        image_url="path/to/image.jpg",
        alt_text="Demo image",
        style=Style(width="400px", margin="0 auto"),
    )
)

vertical_parent = Slide()
vertical_parent.heading = "Vertical stack"
vertical_parent.vertical = [
    Slide.make_text("Point one"),
    Slide.make_text("Point two"),
]

(
    Presentation("Elements Demo", theme=Theme.WHITE, transition=Transition.FADE)
    .configure(hash=True, progress=True, controls=True, slideNumber=True)
    .add(title_slide, styled_slide, vertical_parent)
    .save("elements_presentation.html")
)