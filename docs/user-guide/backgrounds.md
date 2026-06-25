---
icon: lucide/paintbrush-vertical
---

# Backgrounds

Slide backgrounds map to reveal.js `data-background-*` attributes. You do not need background classes for typical use; pass plain values to `bg()`.

## Plain values (preferred)

```python
from pyreveal import BackgroundSize, BackgroundType, Presentation, Slide

# Color string
slide = Slide()
slide.title = "Colored"
slide.bg("#2d3436")

# Image path
slide.bg("photos/bg.jpg")

# Image with options
slide.bg(image="bg.jpg", size=BackgroundSize.COVER, opacity=0.6)

# Explicit type via enum
slide.bg(type=BackgroundType.GRADIENT, gradient="linear-gradient(to bottom, #283b95, #17b2c3)")

# Video
slide.bg(type=BackgroundType.VIDEO, video="assets/loop.mp4")

# Iframe
slide.bg(
    type=BackgroundType.IFRAME,
    iframe="https://example.com",
    interactive=True,
)
```

## Deck default background

Apply a background to every slide that does not set its own:

```python
deck = Presentation("Talk")
deck.bg("#1a1a2e", opacity=0.9)
# or
deck.bg("default-bg.jpg")
```

## Shared options

All background types accept optional `opacity`, `position`, `repeat`, `transition`, and `parallax`.

```python
slide.bg(image="bg.jpg", size=BackgroundSize.COVER, opacity=0.6, position="center")
slide.bg(image="bg.jpg", parallax="2")  # per-slide parallax multiplier
```

## Deck-wide parallax background

For a single large background that scrolls as you move through the deck, use `Presentation.parallax_background()`:

```python
deck = Presentation("Talk")
deck.parallax_background(
    "assets/parallax.jpg",
    size="2100px 900px",
    horizontal=200,
    vertical=50,
)
```

This maps to reveal.js `parallaxBackground*` config options. See [reveal.js parallax backgrounds](https://revealjs.com/backgrounds/#parallax-background).

## Video with multiple formats

```python
slide.bg(
    type=BackgroundType.VIDEO,
    sources=["clip.mp4", "clip.webm"],
    preload=True,
)
```

## Advanced: background classes

For fine-grained control, background classes remain available:

```python
from pyreveal import ColorBackground, GradientBackground, ImageBackground

slide.bg(ColorBackground("#2d3436"))
slide.bg(ImageBackground("bg.jpg", size="cover"))
```

## Factory helper

```python
from pyreveal import BackgroundFactory, BackgroundType

bg = BackgroundFactory.create_background(BackgroundType.COLOR, "#1a1a2e")
bg = BackgroundFactory.create_background(BackgroundType.IMAGE, "bg.jpg", size="cover")
```