# PyReveal

PyReveal is a Python library for building [Reveal.js](https://revealjs.com/) presentations programmatically. It bundles reveal.js 6.x and exports standalone HTML decks.

## Features

- **Two-class API:** build `Slide` objects, add them to `Presentation`
- **No HTML required:** `title`, `text`, `bullets`, `code`, `image`, fragments, notes
- **Typed choices:** `Theme`, `Transition`, `Plugin`, `FragmentEffect`, and more
- **Reorderable vertical slides:** `slide.vertical = [child_a, child_b]`
- Themes, transitions, backgrounds (color, image, video, iframe, gradient)
- Plugins: notes, highlight, markdown, math (KaTeX/MathJax), search, zoom
- `configure()` for Reveal.js options (hash URLs, progress bar, scroll view, etc.)
- Export self-contained HTML with bundled reveal.js assets

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

After cloning, initialize the reveal.js submodule:

```bash
git submodule update --init --recursive
```

## Installation

```bash
pip install pyreveal
```

Or with uv:

```bash
uv add pyreveal
```

For local development:

```bash
uv sync --dev
```

## Quick start

```python
from pyreveal import Plugin, Presentation, Slide, Theme, Transition

intro = Slide()
intro.title = "Welcome"
intro.subtitle("Build decks in Python")
intro.vertical = [
    Slide.make_text("First point"),
    Slide.make_text("Second point"),
]

(
    Presentation("My Presentation", theme=Theme.WHITE, transition=Transition.SLIDE)
    .configure(hash=True, progress=True, slideNumber="c/t")
    .plugins(Plugin.NOTES)
    .add(intro)
    .save("my_presentation.html")
)
```

Define slides with `Slide()`, add them with `Presentation.add()`. `PyReveal` is an alias for `Presentation`.

## Slides

```python
from pyreveal import BackgroundSize, FragmentEffect, Presentation, Slide, Theme

welcome = Slide()
welcome.title = "Agenda"
welcome.fragment("Introduction", effect=FragmentEffect.GROW)
welcome.bullets(["One", "Two", "Three"])

chart = Slide()
chart.heading("Chart")
chart.image("chart.png")
chart.bg("bg.jpg", size=BackgroundSize.COVER)

Presentation("Demo", theme=Theme.BLACK).add(welcome, chart)
```

Backgrounds accept color strings (`"#222"`), image paths, or dicts. No extra classes needed.

## Auto-animate

```python
Presentation("Demo").animate(
    [
        {"title": "Before"},
        {"title": "After"},
    ]
)
```

## Documentation

Versioned documentation is published with [Zensical](https://zensical.org/) and [mike](https://github.com/squidfunk/mike):

**https://tavallaie.github.io/pyreveal/**

Preview locally:

```bash
uv sync --group docs
uv run zensical serve
```

See `docs/development/versioning.md` for publishing new doc versions.

## Development

```bash
uv sync --dev
uv run pytest
uv build
```

## Links

- Documentation: https://tavallaie.github.io/pyreveal/
- Issues: https://github.com/tavallaie/pyreveal/issues
- Source: https://github.com/tavallaie/pyreveal

## License

MIT. See [LICENSE](./LICENSE).