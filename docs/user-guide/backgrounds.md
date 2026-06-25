---
icon: lucide/paintbrush-vertical
---

# Backgrounds

Slide backgrounds map to reveal.js `data-background-*` attributes.

## Color

```python
from pyreveal import ColorBackground, Slide

slide = Slide(
    content="<h2>Colored slide</h2>",
    background=ColorBackground("#2d3436"),
)
```

## Image

```python
from pyreveal import ImageBackground, Slide

slide = Slide(
    content="<h2>Photo background</h2>",
    background=ImageBackground("photos/bg.jpg", size="cover"),
)
```

## Video

```python
from pyreveal import Slide, VideoBackground

slide = Slide(
    content="<h2>Video background</h2>",
    background=VideoBackground("assets/loop.mp4"),
)
```

## Iframe

```python
from pyreveal import IframeBackground, Slide

slide = Slide(
    content="<h2>Live page</h2>",
    background=IframeBackground("https://example.com"),
)
```

## Shared options

All background types accept optional `opacity`, `position`, `repeat`, `transition`, and `parallax` keyword arguments.

```python
ImageBackground("bg.jpg", size="cover", opacity=0.6, position="center")
```

## Presentation default

Apply a background to every slide that does not set its own:

```python
presentation.set_background(ColorBackground("#2d3436"))
```

## Factory helper

```python
from pyreveal import BackgroundFactory

bg = BackgroundFactory.create_background("color", "#1a1a2e")
bg = BackgroundFactory.create_background("image", "bg.jpg", size="cover")
bg = BackgroundFactory.create_background("video", "loop.mp4")
```