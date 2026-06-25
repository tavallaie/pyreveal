---
icon: lucide/puzzle
---

# Elements and styles

Slides can include structured HTML via `Element` subclasses and optional `Style` objects.

## Image elements

```python
from pyreveal import ImageElement, PyReveal, Slide, Style

slide = Slide(content="<h2>Chart</h2>")
slide.add_element(
    ImageElement(
        image_url="assets/chart.png",
        alt_text="Sales chart",
        style=Style(width="480px", margin="0 auto"),
    )
)
presentation.add_slide(slide)
```

When you call `save_to_file()`, image paths referenced by elements are copied into the output `assets/` directory.

## Video elements

```python
from pyreveal import Slide, VideoElement

slide = Slide(content="<h2>Demo</h2>")
slide.add_element(VideoElement(video_url="assets/demo.mp4"))
```

## Fragments

```python
from pyreveal import Fragment

slide.add_element(Fragment("Step one", effect="grow"))
```

See [Fragments](fragments.md) for effects and auto-animate.

## Code blocks

```python
from pyreveal import CodeElement

slide.add_element(CodeElement("print(1)", language="python", line_numbers=True))
```

Requires `presentation.enable_plugins("highlight")`.

## Generic elements

`Element` supports arbitrary tags, attributes, nested children, `data_id` for auto-animate, and inline CSS via `Style`.