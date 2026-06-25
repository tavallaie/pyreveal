# PyReveal reveal.js parity plan

PyReveal owns **build a great deck in Python, export portable HTML**. It does not chase full reveal.js parity (no React bindings, no runtime JS API wrappers).

## Shipped

Typed helpers, docs, and tests for high-value reveal.js options.

| Item | API / docs | Status |
| ---- | ---------- | ------ |
| Navigation helpers | `navigation()`, `deep_links()` | done |
| Slide numbers | `slide_numbers(SlideNumber)` | done |
| Scroll / print view | `scroll_view()`, `print_view()` | done |
| Presentation size | `presentation_size()` | done |
| Link lightbox | `preview_links()`, `slide.image(preview=True)` | done |
| Custom plugins | `CustomPlugin` | done |
| Deep links | `slide.id` alias | done |
| PDF hint on save | `pdf_print_url()`, `save(pdf_hint=True)` | done |
| Deck auto-slide | `auto_slide()`, `auto_progression()` | done |
| Parallax backgrounds | `parallax_background()`, per-slide `parallax` | done |
| Keyboard bindings | `keyboard_bindings()`, `KeyboardBinding` | done |
| Auto-animate ergonomics | `AutoAnimate.text()`, `animate()` coercion | done |
| Search plugin docs | `docs/user-guide/search.md` | done |
| PDF export guide | `docs/user-guide/pdf-export.md` | done |
| Unified demo | `example/demo.py` | done |
| Parity matrix | `docs/user-guide/reveal-features.md` | done |

Tests:

- `tests/test_presentation_helpers.py` — navigation, scroll view, slide numbers, plugins, PDF URL
- `tests/test_deck_authoring.py` — auto-slide, auto-animate, search plugin
- `tests/test_reveal_config.py` — parallax, keyboard bindings, auto-progression alias

---

## Backlog

Implement when there is explicit demand.

| Item | Notes | Effort |
| ---- | ----- | ------ |
| **Multiplex** | Live presenter + audience sync. Needs `multiplex` plugin, secret/hash config, and often a socket server. Document as `CustomPlugin` recipe first. | high |
| **Linked slide previews** | Extend beyond `LinkElement(preview=True)` to slide-preview patterns from reveal docs. | medium |
| **CLI** | `pyreveal build deck.py` to run a script and emit HTML. | medium |
| **Deck builder sugar** | `deck.title_slide()`, `deck.code_slide()` on top of `Slide` factories. | low |
| **Runtime Reveal API** | `Reveal.slide()`, events, `postMessage` — browser-only after export. | skip |
| **React bindings** | Use [reveal.js/react](https://revealjs.com/react/) separately. | skip |
| **Python plugin authoring** | Plugins are JS; register paths via `CustomPlugin` only. | skip |

### Backlog acceptance (when started)

- Multiplex: example deck + doc page, or explicit “not supported” with custom-plugin pointer
- CLI: entry point in `pyproject.toml`, documented in quickstart
- No new Python wrappers around browser-only reveal APIs