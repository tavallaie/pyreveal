"""Canonical PyReveal usage with Slide objects."""

from pyreveal import ImageBackground, PyReveal, Slide

presentation = PyReveal(title="My Presentation", theme="black", transition="slide")
presentation.configure(hash=True, progress=True, slideNumber="c/t")

intro = Slide(content="<h1>Welcome to PyReveal</h1>", title="intro")
intro.add_vertical_slide(Slide(content="<p>First vertical slide</p>"))
intro.add_vertical_slide(Slide(content="<p>Second vertical slide</p>"))
presentation.add_slide(intro)

presentation.add_slide(Slide(content="<h2>Another horizontal slide</h2>"))

bg = ImageBackground(image_url="path/to/image.jpg")
presentation.add_slide(
    Slide(content="<h2>Slide with background</h2>", background=bg)
)

presentation.save_to_file("my_presentation.html")