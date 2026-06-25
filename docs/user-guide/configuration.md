---
icon: lucide/sliders-horizontal
---

# Reveal.js configuration

Use `configure()` to pass any option to `Reveal.initialize()`. See the [reveal.js config reference](https://revealjs.com/config/) for all keys.

PyReveal also provides typed helpers for common options. See [Reveal.js feature support](reveal-features.md).

## Quick setup

```python
from pyreveal import Presentation, Slide, SlideNumber, Theme, Transition

deck = (
    Presentation("Talk", theme=Theme.WHITE, transition=Transition.SLIDE)
    .navigation(hash=True, progress=True)
    .deep_links(hash=True)
    .slide_numbers(SlideNumber.H_DOT_V)
    .presentation_size(1280, 720)
)

slide = Slide()
slide.id = "intro"
slide.title = "Hello"
deck.add(slide)
```

## Helper methods

| Method | Purpose |
| ------ | ------- |
| `navigation()` | Controls, progress, touch, overview, keyboard |
| `deep_links()` | Hash URLs and slide deep linking |
| `slide_numbers()` | Slide number format |
| `scroll_view()` | Scrollable deck layout |
| `print_view()` | Print-optimized layout |
| `presentation_size()` | Base width/height and scale bounds |
| `preview_links()` | Global link lightbox previews |
| `configure(**options)` | Any other reveal.js option |

### Scroll view

```python
deck.scroll_view()
```

### Raw configure passthrough

```python
deck.configure(hash=True, progress=True, slideNumber="h.v", controls=True)
```

## Theme and transition

Use typed enums. See [Choices](choices.md):

| Setting | How to set |
| ------- | ---------- |
| Theme | `Presentation(theme=Theme.DRACULA)` or `set_theme(Theme.DRACULA)` |
| Transition | `Presentation(transition=Transition.FADE)` or `set_transition(Transition.FADE)` |

`configure(transition="zoom")` overrides the presentation default at render time.

## Export

```python
# Simple: creates parent directories
deck.save("output/talk/deck.html")

# Show PDF export URL after save
deck.save("output/talk/deck.html", pdf_hint=True)

# Build the print URL manually
Presentation.pdf_print_url("output/talk/deck.html")
# -> output/talk/deck.html?print-pdf

# Legacy: fixed output folder name
deck.save_to_file("deck.html", output_dir="build/my-talk")

# HTML string only
html = deck.html()
```

Open the `?print-pdf` URL in Chromium and print to PDF. See [reveal.js PDF export](https://revealjs.com/pdf-export/).

`save()` copies reveal.js assets into the output folder by default.

## Extra CSS

```python
deck.stylesheet("custom.css")
deck.css("section { font-size: 28px; }")
```