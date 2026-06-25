---
icon: lucide/presentation
---

# PyReveal

PyReveal is a Python library for building [Reveal.js](https://revealjs.com/) presentations programmatically. It bundles reveal.js 6.x and exports self-contained HTML you can open locally or host anywhere.

## Key features

- **Slide API** — compose decks with `Slide`, `Element`, and `Style`
- **Reveal.js 6** — themes, transitions, plugins, fragments, and `configure()`
- **Portable output** — `save_to_file()` copies reveal.js assets into the output folder

## Quick start

```python
from pyreveal import PyReveal, Slide

presentation = PyReveal(title="Hello", theme="white", transition="fade")
presentation.configure(hash=True, progress=True)

intro = Slide(content="<h1>Welcome</h1>")
intro.add_vertical_slide(Slide(content="<p>Details</p>"))
presentation.add_slide(intro)

presentation.save_to_file("deck.html")
```

## Next steps

- [Installation](getting-started/installation.md)
- [Quick start](getting-started/quickstart.md)
- [Slides](user-guide/slides.md)
- [Fragments](user-guide/fragments.md)
- [Plugins](user-guide/plugins.md)
- [Configuration](user-guide/configuration.md)
- [API reference](reference/api.md)

## Versioning

Documentation is versioned with [mike](https://github.com/squidfunk/mike). Use the version selector in the header to switch between releases.