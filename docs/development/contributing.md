---
icon: lucide/heart-handshake
---

# Contributing

PyReveal favors a small public API: build `Slide()` objects, add them to `Presentation`, export with `save()`. Prefer plain strings and typed enums (`Theme`, `Plugin`, …) over low-level HTML and element classes unless you need fine-grained control.

## Development setup

```bash
git clone https://github.com/tavallaie/pyreveal.git
cd pyreveal
git submodule update --init --recursive
uv sync --dev --group docs
```

## Run tests

```bash
uv run pytest
```

## Build the package

```bash
uv build
```

## Documentation

Preview docs locally:

```bash
uv sync --group docs
uv run zensical serve
```

Build a static site:

```bash
uv run zensical build --clean
```

See [Documentation versioning](versioning.md) for publishing versioned docs to GitHub Pages.