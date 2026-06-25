---
icon: lucide/layout-grid
---

# Layout helpers (advanced)

Reveal.js layout classes are available through `Layout`, `Stack`, `HStack`, `VStack`, and `FitText`. Use these via `slide.element()` when the slide builder is not enough.

## Stack (overlapping layers)

```python
from pyreveal import Fragment, FragmentEffect, ImageElement, Presentation, Slide, Stack

slide = Slide()
slide.heading("Layers")
slide.element(
    Stack(children=[
        ImageElement("a.png", stretch=True),
        Fragment("Caption", effect=FragmentEffect.FADE_IN_THEN_OUT),
    ])
)
Presentation("Talk").add(slide)
```

## Horizontal and vertical stacks

```python
from pyreveal import Element, FitText, HStack, Slide, VStack

slide = Slide()
slide.element(
    HStack(children=[
        Element(tag="div", content="Left"),
        Element(tag="div", content="Right"),
    ])
)
slide.element(FitText("BIG TITLE"))
```

## Image modifiers

```python
ImageElement("chart.png", stretch=True, frame=True, lazy=True)
```

- `stretch`: `r-stretch` (fill slide height)
- `frame`: `r-frame` border styling
- `lazy`: `data-src` for deferred loading