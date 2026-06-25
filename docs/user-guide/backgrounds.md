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

## Factory helper

```python
from pyreveal import BackgroundFactory

bg = BackgroundFactory.create_background("color", "#1a1a2e")
bg = BackgroundFactory.create_background("image", "bg.jpg", size="cover")
bg = BackgroundFactory.create_background("video", "loop.mp4")
```