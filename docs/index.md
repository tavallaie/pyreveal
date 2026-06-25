# PyReveal

PyReveal is a Python library for building [Reveal.js](https://revealjs.com/) presentations programmatically. It bundles reveal.js 6.x and writes self-contained HTML decks you can open locally or host anywhere.

## Why PyReveal?

- **Object-oriented API** — compose decks with `Slide`, `Element`, and `Style`
- **Reveal.js 6** — themes, transitions, scroll view, and more via `configure()`
- **Standalone output** — `save_to_file()` copies reveal.js assets into the output folder

## Quick example

```python
from pyreveal import PyReveal, Slide

presentation = PyReveal(title="Hello", theme="white", transition="fade")
presentation.configure(hash=True, progress=True)

intro = Slide(content="<h1>Welcome</h1>")
intro.add_vertical_slide(Slide(content="<p>Details</p>"))
presentation.add_slide(intro)

presentation.save_to_file("deck.html")
```

## Documentation versions

This site is versioned with [mike](https://github.com/squidfunk/mike) and [Zensical](https://zensical.org/). Use the version selector in the header to switch between releases.

## Next steps

- [Installation](getting-started/installation.md)
- [Quick start](getting-started/quickstart.md)
- [Slides](user-guide/slides.md)