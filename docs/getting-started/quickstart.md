# Quick start

This guide uses the canonical **Slide-based API**. See [Slides](../user-guide/slides.md) for vertical stacks, groups, and backgrounds.

```python
from pyreveal import PyReveal, Slide

presentation = PyReveal(
    title="My Presentation",
    theme="black",
    transition="slide",
)

presentation.configure(hash=True, progress=True, slideNumber="c/t")

intro = Slide(content="<h1>Welcome to PyReveal</h1>")
intro.add_vertical_slide(Slide(content="<p>First vertical slide</p>"))
intro.add_vertical_slide(Slide(content="<p>Second vertical slide</p>"))
presentation.add_slide(intro)

presentation.add_slide(Slide(content="<h2>Another horizontal slide</h2>"))

presentation.save_to_file("my_presentation.html")
```

Open `presentations/my_presentation.html` in a browser. The `presentations/` folder also contains copied `revealjs/` assets.

## Examples in the repository

- `example/basic_usage.py` — slides and vertical stacks
- `example/elements_usage.py` — `ImageElement`, `Style`, and `add_group()`