---
icon: lucide/puzzle
---

# Elements and styles (advanced)

For most slides, use the `Slide()` builder (`title`, `text`, `code`, `image`, `fragment`, etc.). This page covers low-level `Element` subclasses when you need extra control.

## When to use elements

| Need | Prefer |
| ---- | ------ |
| Title, text, bullets | `slide.title`, `slide.text`, `slide.bullets` |
| Code | `slide.code()` |
| Image | `slide.image()` |
| Fragment | `slide.fragment()` |
| Custom HTML structure | `Element`, `Stack`, `HStack`, … |

## Image elements

```python
from pyreveal import ImageElement, Presentation, Slide, Style

slide = Slide()
slide.heading("Chart")
slide.element(
    ImageElement(
        image_url="assets/chart.png",
        alt_text="Sales chart",
        style=Style(width="480px", margin="0 auto"),
    )
)
Presentation("Talk").add(slide).save("deck.html")
```

When you call `save()`, image paths referenced by elements are copied into the output `assets/` directory.

## Video elements

```python
from pyreveal import Slide, VideoElement

slide = Slide()
slide.heading("Demo")
slide.element(VideoElement(video_url="assets/demo.mp4"))
```

## Code and fragments via elements

```python
from pyreveal import CodeElement, Fragment, FragmentEffect

slide.element(CodeElement("print(1)", language="python", line_numbers=True))
slide.element(Fragment("Step one", effect=FragmentEffect.GROW))
```

Requires `Plugin.HIGHLIGHT` for code blocks.

## Generic elements

`Element` supports arbitrary tags, attributes, nested children, `data_id` for auto-animate, and inline CSS via `Style`.

See [Layouts](layouts.md) for `Stack`, `HStack`, `VStack`, and `FitText`.