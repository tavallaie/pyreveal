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

Preview docs locally:

```bash
uv run zensical serve
```

Build a static site:

```bash
uv run zensical build --clean
```

See [Documentation versioning](versioning.md) for publishing versioned docs to GitHub Pages.