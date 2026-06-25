---
icon: lucide/git-branch
---

# Documentation versioning

PyReveal documentation uses [Zensical](https://zensical.org/) with [mike](https://github.com/squidfunk/mike) for versioned deployments on GitHub Pages, following the [Zensical versioning guide](https://zensical.org/docs/setup/versioning/).

## How it works

- Each release is published under `https://tavallaie.github.io/pyreveal/<version>/`
- The `latest` alias points to the current release
- The site root redirects to `latest`
- A version selector appears in the documentation header

Configuration lives in `zensical.toml`:

```toml
[project.extra.version]
provider = "mike"
```

## Local preview

Serve the current working tree (single version):

```bash
uv sync --group docs
uv run zensical serve
```

Preview all deployed versions after a local mike deploy:

```bash
uv run mike serve
```

## Publish a new version manually

Use the **major.minor** version (for example `0.4` for package version `0.4.0`):

```bash
uv sync --group docs
git fetch origin gh-pages --depth=1 || true

uv run mike deploy --push --update-aliases 0.4 latest
uv run mike set-default --push latest
```

## CI deployment

Pushes to `main` and `dev` run `.github/workflows/docs.yml`, which:

1. Reads the package version from `pyproject.toml`
2. Deploys docs with `mike deploy`
3. Updates the `latest` alias and default redirect

## First-time setup

If the `gh-pages` branch does not exist yet, the first workflow run creates it. Enable GitHub Pages for the repository:

**Settings → Pages → Deploy from branch → `gh-pages` → `/ (root)`**