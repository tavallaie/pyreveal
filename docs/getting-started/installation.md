---
icon: lucide/download
---

# Installation

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Install from PyPI

```bash
pip install pyreveal
```

Or with uv:

```bash
uv add pyreveal
```

## Install from source

Clone the repository and initialize the reveal.js submodule:

```bash
git clone https://github.com/tavallaie/pyreveal.git
cd pyreveal
git submodule update --init --recursive
uv sync --dev
```

reveal.js 6.x ships pre-built `dist/` files in the submodule, so you do not need Node.js to use PyReveal.

## Verify the install

```bash
uv run python -c "from pyreveal import Presentation, Slide, Theme; print(Theme.DRACULA.value)"
```

## Next step

[Quick start](quickstart.md) to build your first deck.