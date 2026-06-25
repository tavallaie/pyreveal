---
icon: lucide/zap
---

# Quick start

## How it works

1. **Build slides** with `Slide()` for title, bullets, code, fragments, backgrounds
2. **Build the deck** with `Presentation` for theme, plugins, default background
3. **Add slides** with `deck.add(slide, …)` and **export** with `deck.save("deck.html")`

`PyReveal` is a backward-compatible alias for `Presentation`.

## 1. Create slides

Each slide is a `Slide()` object. Set content with methods or assignment:

```python
from pyreveal import Slide

intro = Slide()
intro.title = "Welcome to PyReveal"
intro.subtitle("Build decks in Python")

agenda = Slide()
agenda.heading("Agenda")
agenda.bullets(["Introduction", "Demo", "Q&A"])
```

## 2. Vertical slides (reorderable list)

Vertical children live on `slide.vertical` as a **list** you can reorder:

```python
first = Slide.make_text("First vertical slide")
second = Slide.make_text("Second vertical slide")

intro.vertical = [first, second]
intro.vertical = [second, first]  # swap order
```

You can also assign plain strings; they become text slides automatically:

```python
intro.vertical = ["Point A", "Point B"]
```

Or build a section in one call:

```python
section = Slide.section("Agenda", "Topic 1", "Topic 2")
```

## 3. Add slides to the deck

```python
from pyreveal import Plugin, Presentation, Slide, Theme, Transition

intro = Slide()
intro.title = "Welcome"
intro.subtitle("Build decks in Python")
intro.vertical = [
    Slide.make_text("First point"),
    Slide.make_text("Second point"),
]

photo = Slide()
photo.heading("Photo background")
photo.bg("path/to/image.jpg")

deck = (
    Presentation("My Presentation", theme=Theme.BLACK, transition=Transition.SLIDE)
    .configure(hash=True, progress=True, slideNumber="c/t")
    .plugins(Plugin.NOTES)
    .add(intro, agenda, photo)
    .save("my_presentation.html")
)
```

Open `presentations/my_presentation.html` in a browser. The output folder also contains copied `revealjs/` assets.

## Typed choices

Prefer enums over raw strings for themes, transitions, plugins, and effects:

```python
from pyreveal import Plugin, Theme, Transition

Presentation("Talk", theme=Theme.DRACULA, transition=Transition.FADE)
    .plugins(Plugin.NOTES, Plugin.HIGHLIGHT)
```

See [Choices](../user-guide/choices.md) for the full list.

## HTML escape hatch

You do not need HTML for normal slides. When needed:

```python
custom = Slide("<h1>Custom</h1><p>markup</p>")
```

Plain strings without tags become paragraphs: `Slide("Just text")`.

## Explore the documentation

| Topic | Guide |
| ----- | ----- |
| Install | [Installation](installation.md) |
| Slides & vertical stacks | [Slides](../user-guide/slides.md) |
| Typed enums | [Choices](../user-guide/choices.md) |
| Backgrounds | [Backgrounds](../user-guide/backgrounds.md) |
| Fragments & auto-animate | [Fragments](../user-guide/fragments.md) |
| Plugins, code, math | [Plugins](../user-guide/plugins.md) · [Math](../user-guide/math.md) |
| Reveal.js parity | [Feature support](../user-guide/reveal-features.md) |
| Themes & Reveal.js config | [Configuration](../user-guide/configuration.md) |
| Layouts & elements (advanced) | [Layouts](../user-guide/layouts.md) · [Elements](../user-guide/elements.md) |
| Full API | [API reference](../reference/api.md) |

## Examples in the repository

- `example/basic_usage.py`: slides, vertical stacks, backgrounds
- `example/features_usage.py`: fragments, plugins, code, auto-animate
- `example/elements_usage.py`: low-level elements and styles

## Versioning

Documentation is versioned with [mike](https://github.com/squidfunk/mike). Use the version selector in the header to switch between releases. See [Documentation versioning](../development/versioning.md) for publishing.

## Next steps

- [Slides](../user-guide/slides.md): full slide API
- [Fragments](../user-guide/fragments.md): stepped reveals and auto-animate
- [Plugins](../user-guide/plugins.md): notes, highlight, markdown, math