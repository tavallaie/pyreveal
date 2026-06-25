# Contributing

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

Generate embedded PyReveal demos, then preview:

```bash
uv sync --group docs
uv run python scripts/build_docs_demo.py
uv run zensical serve
```

Build a static site:

```bash
uv run python scripts/build_docs_demo.py
uv run zensical build --clean
```

See [Documentation versioning](versioning.md) for publishing versioned docs to GitHub Pages.