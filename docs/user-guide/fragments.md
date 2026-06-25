---
icon: lucide/list-ordered
---

# Fragments and auto-animate

## Fragments

Fragments reveal content step-by-step during a slide:

```python
from pyreveal import FragmentEffect, Presentation, Slide

slide = Slide()
slide.heading = "Agenda"
slide.fragment("Introduction")
slide.fragment("Demo", effect=FragmentEffect.GROW)
slide.fragment("Q&A", effect=FragmentEffect.FADE_IN_THEN_OUT, index=2)

Presentation("Talk").add(slide)
```

### Fragment effects

Use the `FragmentEffect` enum. See [Choices](choices.md) for the full list.

```python
slide.fragment("Grow", effect=FragmentEffect.GROW)
slide.fragment("Fade up", effect=FragmentEffect.FADE_UP)
slide.fragment("Highlight", effect=FragmentEffect.HIGHLIGHT_RED)
```

Plain strings like `"grow"` still work, but the enum is preferred.

### Multiple fragments via kwargs

```python
Slide.make_title(
    "Agenda",
    fragments=[
        ("Introduction", {"effect": FragmentEffect.GROW}),
        "Summary",
    ],
)
```

## Auto-animate

Build matching slides with `Presentation.animate()`. Plain text is preferred:

```python
from pyreveal import Presentation, Theme

deck = (
    Presentation("Demo", theme=Theme.DRACULA)
    .animate(
        [
            {"title": "Before"},
            {"title": "After"},
        ],
        easing="ease-in-out",
    )
)
```

Each string value becomes a matched element with a `data-id`. HTML strings also work:

```python
deck.animate([
    {"title": "<h2>Before</h2>"},
    {"title": "<h2>After</h2>"},
])
```

### Advanced: AutoAnimate helper

For fine-grained control, use `AutoAnimate` directly:

```python
from pyreveal import AutoAnimate, Element, Presentation, Slide

anim = AutoAnimate(easing="ease-in-out")
slide = anim.slide(matches={"title": Element(tag="h2", content="Hello")})
Presentation("Talk").add(slide)
```

### Manual matching

```python
AutoAnimate.match("title", Element(tag="h2", content="Title"))
```