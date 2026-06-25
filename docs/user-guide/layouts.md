---
icon: lucide/layout-grid
---

# Layout helpers

Reveal.js layout classes are available through `Layout`, `Stack`, `HStack`, `VStack`, and `FitText`.

## Stack (overlapping layers)

```python
from pyreveal import Fragment, ImageElement, Stack

slide = Slide(content="<h2>Layers</h2>")
slide.add_element(
    Stack(children=[
        ImageElement("a.png", stretch=True),
        Fragment("Caption", effect="fade-in-then-out"),
    ])
)
```

## Horizontal and vertical stacks

```python
from pyreveal import Element, FitText, HStack, VStack

slide.add_element(
    HStack(children=[
        Element(tag="div", content="<p>Left</p>"),
        Element(tag="div", content="<p>Right</p>"),
    ])
)

slide.add_element(FitText("BIG TITLE"))
```

## Image modifiers

```python
ImageElement("chart.png", stretch=True, frame=True, lazy=True)
```

- `stretch` — `r-stretch` (fill slide height)
- `frame` — `r-frame` border styling
- `lazy` — `data-src` for deferred loading