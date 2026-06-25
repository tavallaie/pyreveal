---
icon: lucide/list-ordered
---

# Fragments and auto-animate

## Fragments

Fragments reveal content step-by-step during a slide. Use the `Fragment` element:

```python
from pyreveal import Fragment, PyReveal, Slide

slide = Slide(content="<h2>Agenda</h2>")
slide.add_element(Fragment("Introduction"))
slide.add_element(Fragment("Demo", effect="grow"))
slide.add_element(Fragment("Q&A", effect="fade-in-then-out", index=2))
presentation.add_slide(slide)
```

### Fragment effects

`grow`, `shrink`, `fade-out`, `fade-right`, `fade-up`, `fade-down`, `fade-left`, `fade-in-then-out`, `fade-in-then-semi-out`, `highlight-red`, `highlight-blue`, `highlight-green`, or empty for the default fade-in.

## Auto-animate

Use `AutoAnimate` to assign matching `data-id` values across consecutive slides:

```python
from pyreveal import AutoAnimate, Element, PyReveal

anim = AutoAnimate(easing="ease-in-out")
presentation.add_slide(
    anim.slide(matches={"title": Element(tag="h2", content="Hello")})
)
presentation.add_slide(
    anim.slide(matches={"title": Element(tag="h2", content="Hello World")})
)
```

### Sequence helper

Build a full animation chain in one call:

```python
presentation.add_auto_animate_sequence(
    [
        {"title": Element(tag="h2", content="Hello")},
        {"title": Element(tag="h2", content="Hello World")},
        {"title": "<h2>Goodbye</h2>", "badge": Element(tag="span", content="New")},
    ],
    easing="ease-in-out",
)
```

String values in a frame get `data-id` injected automatically (`AutoAnimate.html`).
Use the `_content` key for extra HTML that is not matched across slides.

### Manual matching

```python
AutoAnimate.match("title", Element(tag="h2", content="Title"))
```