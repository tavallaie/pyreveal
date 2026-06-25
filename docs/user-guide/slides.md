---
icon: lucide/layers
---

# Slides

Build each slide with `Slide()`, then pass it to `Presentation.add()`.

## Instance builder

```python
from pyreveal import FragmentEffect, Presentation, Slide

welcome = Slide()
welcome.title = "Welcome"          # assignment
welcome.subtitle("PyReveal")       # or welcome.subtitle = "PyReveal"

agenda = Slide()
agenda.heading("Agenda")
agenda.bullets(["One", "Two", "Three"])

demo = Slide()
demo.heading("Demo")
demo.code("print('hi')", language="python")

deck = Presentation("Talk").add(welcome, agenda, demo)
```

| Method / assignment | Purpose |
| ------------------- | ------- |
| `title` / `title("…")` | Main title (`<h1>`) |
| `subtitle` / `subtitle = "…"` | Subtitle paragraph |
| `heading` / `heading = "…"` | Section heading (`<h2>`) |
| `text("…")` | Add paragraph(s) |
| `bullets([...])` | Bullet or numbered list |
| `code("…", language="python")` | Code block |
| `image("…", caption="…")` | Image |
| `markdown = "…"` | Markdown body |
| `fragment("…", effect=FragmentEffect.GROW)` | Stepped reveal |
| `note("…")` | Speaker notes |
| `bg("#222")` / `bg("photo.jpg")` | Background |

## Fluent options before adding

```python
slide = Slide()
slide.title = "Agenda"
slide.fragment("Introduction", effect=FragmentEffect.GROW)
slide.fragment("Demo", index=1)
slide.note("Walk through each point.")
slide.bg("#222")

deck.add(slide)
```

Or pass options to a one-shot factory:

```python
Slide.make_title(
    "Agenda",
    fragments=[("Introduction", {"effect": FragmentEffect.GROW}), "Outro"],
    note="Speaker note",
    bg="#222",
)
```

## Vertical slides (reorderable list)

Vertical children live on `slide.vertical` as a **list**. Assign, append, or reorder:

```python
first = Slide.make_text("Point A")
second = Slide.make_text("Point B")

intro = Slide()
intro.title = "Section"
intro.vertical = [first, second]

# Reorder
intro.vertical = [second, first]

# Or assign plain strings (converted to text slides)
intro.vertical = ["Point A", "Point B"]
```

Build a section in one expression:

```python
section = Slide.section("Agenda", "Topic 1", "Topic 2")
deck.add(section)
```

## Adding slides to the deck

```python
deck = Presentation("Talk")
deck.add(slide_one)
deck.add(slide_two, slide_three)   # multiple at once
deck.slide(another_slide)          # alias for add()
```

`Presentation` handles deck-level settings (theme, plugins, default background). `Slide` owns slide content.

## One-shot factories

Optional shortcuts when you prefer a single expression:

| Factory | Purpose |
| ------- | ------- |
| `Slide.make_title(text, *, subtitle)` | Title slide |
| `Slide.make_heading(text)` | Heading slide |
| `Slide.make_text(*paragraphs)` | Text slide(s) |
| `Slide.make_bullets(items, *, title)` | Bullet list |
| `Slide.make_code(source, *, language)` | Code slide |
| `Slide.make_image(src, *, caption)` | Image slide |
| `Slide.from_markdown(source)` | Markdown slide |
| `Slide.section(main, *children)` | Section with vertical children |

## HTML escape hatch

You do not need HTML for normal slides. When needed:

```python
custom = Slide("<h1>Custom</h1><p>markup</p>")
custom = Slide(content="<h2>Also works</h2>")
```

Plain strings without tags become paragraphs: `Slide("Just text")` → `<p>Just text</p>`.