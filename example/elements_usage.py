"""Build slides from elements, styles, and Reveal.js configuration."""

from pyreveal import ImageElement, PyReveal, Slide, Style

presentation = PyReveal(title="Elements Demo", theme="white", transition="fade")
presentation.configure(
    hash=True,
    progress=True,
    controls=True,
    slideNumber=True,
)

title_slide = Slide(content="<h1>PyReveal Elements</h1>")
presentation.add_slide(title_slide)

styled_slide = Slide(content="<h2>Styled image</h2>")
image = ImageElement(
    image_url="path/to/image.jpg",
    alt_text="Demo image",
    style=Style(width="400px", margin="0 auto"),
)
styled_slide.add_element(image)
presentation.add_slide(styled_slide)

presentation.add_group(
    [
        Slide(content="<h2>Vertical stack</h2>"),
        Slide(content="<p>Point one</p>"),
        Slide(content="<p>Point two</p>"),
    ]
)

presentation.save_to_file("elements_presentation.html")