# Examples

| File | Purpose |
| ---- | ------- |
| `demo.py` | Full feature tour deck |
| `bootstrap.py` | Adds `example/` to `sys.path` when run from repo root |
| `_common.py` | Output paths and asset copying |

Demo media lives in `docs/demo/assets/` (committed). Local runs copy assets into `example/presentations/` when needed.

```bash
uv run python example/demo.py
cd example/presentations && python3 -m http.server 8765
```

For the documentation home page:

```bash
uv run python example/demo.py --docs
# or: uv run python scripts/build_docs_demo.py
```

`presentations/revealjs/` and `docs/demo/revealjs/` are copied from `src/pyreveal/revealjs` on save — do not commit them.