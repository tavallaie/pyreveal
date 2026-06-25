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

## Publish a release

Releases are automated by [`.github/workflows/release.yml`](https://github.com/tavallaie/pyreveal/blob/dev/.github/workflows/release.yml). Pushing a `v*` tag runs tests, publishes to PyPI, and creates a GitHub Release with generated notes.

### One-time PyPI setup

1. Create the [pyreveal](https://pypi.org/project/pyreveal/) project on PyPI (first release only).
2. On PyPI → **Publishing** → **Add a new trusted publisher**:
   - Owner: `tavallaie`
   - Repository: `pyreveal`
   - Workflow: `release.yml`
   - Environment: (leave blank unless you use a GitHub Environment)

No API tokens are stored in the repository; `uv publish` uses OIDC trusted publishing.

### Cut a release

1. Bump `version` in `pyproject.toml` and commit.
2. Tag and push:

```bash
git tag v0.7.0
git push origin v0.7.0
```

3. Watch the **Release** workflow on GitHub Actions.
4. Docs for the new version are deployed when the tag lands on `main` or `dev` (see [Documentation versioning](versioning.md)). After merging a release bump to `main`, push the tag from that commit.

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