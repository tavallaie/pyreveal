# PyReveal

PyReveal is a Python library for building [Reveal.js](https://revealjs.com/) presentations programmatically. It bundles reveal.js 6.x and exports standalone HTML decks.

## Features

- Build slides with `Slide`, `Element`, and `Style` objects
- Themes, transitions, and backgrounds (color, image, video, iframe)
- Fragments, speaker notes, code blocks, and Markdown slides
- `enable_plugins()` for notes, highlight, markdown, math, search, and zoom
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
from pyreveal import PyReveal, Slide

presentation = PyReveal(title="My Presentation", theme="white", transition="slide")
presentation.configure(hash=True, progress=True, slideNumber="c/t")

intro = Slide(content="<h1>Welcome</h1>")
intro.add_vertical_slide(Slide(content="<p>Details</p>"))
presentation.add_slide(intro)

presentation.save_to_file("my_presentation.html")
```

See `example/basic_usage.py`, `example/elements_usage.py`, and `example/features_usage.py` for more.

## Slides and elements

```python
from pyreveal import ImageBackground, ImageElement, PyReveal, Slide, Style

presentation = PyReveal(title="Demo", theme="black")
slide = Slide(content="<h2>Hello</h2>", background=ImageBackground("bg.jpg"))
slide.add_element(
    ImageElement("chart.png", alt_text="Chart", style=Style(width="500px"))
)
presentation.add_slide(slide)
```

Vertical stacks can also be added with `add_group([slide1, slide2, ...])`.

## Reveal.js configuration

Pass any [reveal.js config](https://revealjs.com/config/) option via `configure()`:

```python
presentation.configure(
    hash=True,
    progress=True,
    slideNumber="h.v",
    view="scroll",  # scroll mode (reveal.js 5+)
)
```

Theme is selected with `set_theme()` (CSS). Transition defaults come from `set_transition()` but can be overridden in `configure(transition="fade")`.

## Auto-animate

```python
from pyreveal import AutoAnimate, Element

anim = AutoAnimate()
presentation.add_auto_animate_sequence(
    [
        {"title": Element(tag="h2", content="Hello")},
        {"title": Element(tag="h2", content="Hello World")},
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

MIT — see [LICENSE](./LICENSE).