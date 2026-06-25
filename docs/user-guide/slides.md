---
icon: lucide/layers
---

# Slides

A `Slide` holds HTML content, an optional background, child elements, and optional vertical slides.

## Basic slide

```python
from pyreveal import PyReveal, Slide

presentation = PyReveal()
presentation.add_slide(Slide(content="<h1>Title</h1><p>Body</p>"))
```

## Vertical slides

Nest slides under a horizontal slide with `add_vertical_slide()`:

```python
parent = Slide(content="<h1>Section</h1>")
parent.add_vertical_slide(Slide(content="<p>Point A</p>"))
parent.add_vertical_slide(Slide(content="<p>Point B</p>"))
presentation.add_slide(parent)
```

## Vertical groups

Use `add_group()` when you want a vertical stack without a separate parent slide object:

```python
presentation.add_group([
    Slide(content="<h2>Agenda</h2>"),
    Slide(content="<p>Topic 1</p>"),
    Slide(content="<p>Topic 2</p>"),
])
```

