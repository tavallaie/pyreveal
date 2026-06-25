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

Matching `data-id` values animate between consecutive slides:

```python
slide_a = Slide(content="<h2 data-id=\"title\">Hello</h2>", auto_animate=True)
slide_b = Slide(
    content="<h2 data-id=\"title\">Hello World</h2>",
    auto_animate=True,
    auto_animate_easing="ease-in-out",
)
```

Set `data_id` on `Element` instances for finer control:

```python
from pyreveal import Element

slide.add_element(Element(tag="h2", content="Title", data_id="title"))
```