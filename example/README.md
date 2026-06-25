# Examples

| File | Purpose |
| ---- | ------- |
| `demo.py` | Full feature tour deck |
| `bootstrap.py` | Adds `example/` to `sys.path` when run from repo root |
| `_common.py` | Output paths and asset copying |
| `assets/` | Local images, video, and Three.js hero module |

Build the demo (output goes to `presentations/`, gitignored):

```bash
uv run python example/demo.py
cd example/presentations && python3 -m http.server 8765
```

`presentations/revealjs/` is copied from `src/pyreveal/revealjs/` on save — do not commit it.