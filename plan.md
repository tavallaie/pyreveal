# PyReveal reveal.js parity plan

PyReveal owns **build a great deck in Python, export portable HTML**. It does not chase full reveal.js parity (no React bindings, no runtime JS API wrappers).

## Tier 1 (done)

Typed helpers and docs for high-value reveal.js options.

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
| Parity matrix | `docs/user-guide/reveal-features.md` | done |

Tests: `tests/test_tier1_features.py`

---

## Tier 2 (implement now)

Core deck-authoring gaps: kiosk auto-slide, safer auto-animate, search docs, PDF export guide.

### 2.1 Deck-level auto-slide

**Goal:** Kiosk-style decks that advance on a timer without per-slide `data-autoslide`.

**API**

```python
deck.auto_slide(5000)                          # every 5s
deck.auto_slide(3000, loop=True)               # loop deck
deck.auto_slide(4000, stoppable=False)         # ignore user input
deck.auto_slide(False)                           # disable globally
```

Maps to reveal.js: `autoSlide`, `autoSlideStoppable`, `loop`.

Per-slide `Slide(auto_slide=…)` / `data-autoslide` remains for overrides.

**Files**

- `src/pyreveal/presentation.py` — `auto_slide()` helper
- `docs/user-guide/configuration.md` — helper table + example
- `docs/user-guide/reveal-features.md` — Tier 2 helpers section
- `docs/reference/api.md` — method row
- `tests/test_tier2_features.py` — config serialization tests

**Acceptance**

- `deck.auto_slide(5000).html()` contains `"autoSlide": 5000`
- `loop=True` and `stoppable=False` appear in initialize options
- `auto_slide(False)` sets `"autoSlide": false`

### 2.2 Auto-animate ergonomics

**Goal:** Fewer `data-id` mistakes when building matched slides by hand.

**API / docs**

- `AutoAnimate.text(key, text, *, tag=None)` — matched element from plain text
- Expand `docs/user-guide/fragments.md` with key-to-tag table and multi-element example
- Document that `Presentation.animate()` coerces plain strings and dicts with `text` key

**Files**

- `src/pyreveal/auto_animate.py` — `AutoAnimate.text()` static method
- `docs/user-guide/fragments.md`
- `docs/reference/api.md`
- `tests/test_tier2_features.py` — `AutoAnimate.text` + plain-text `animate()` coverage

**Acceptance**

- `AutoAnimate.text("title", "Hello")` renders with `data-id="title"`
- Existing `animate([{"title": "A"}, {"title": "B"}])` tests still pass

### 2.3 Search plugin examples

**Goal:** `Plugin.SEARCH` is usable without reading reveal.js source.

**Docs**

- New `docs/user-guide/search.md`: enable plugin, Ctrl+Shift+F (reveal default), search box behavior
- Section in `docs/user-guide/plugins.md` linking to search guide
- Nav entry in `zensical.toml`

**Files**

- `docs/user-guide/search.md`
- `docs/user-guide/plugins.md`
- `zensical.toml`

**Acceptance**

- Example deck snippet shows `.plugins(Plugin.SEARCH)`
- Parity matrix lists search under Tier 2 docs

### 2.4 PDF export guide

**Goal:** Standalone walkthrough for `?print-pdf` workflow (PyReveal does not render PDFs).

**Docs**

- New `docs/user-guide/pdf-export.md`: save deck, open print URL, Chromium print settings, fragments/notes caveats
- Trim duplicate prose in `reveal-features.md`; link to guide
- `configuration.md` export section links to guide

**Files**

- `docs/user-guide/pdf-export.md`
- `docs/user-guide/reveal-features.md`
- `docs/user-guide/configuration.md`
- `zensical.toml`

**Acceptance**

- Guide documents `save(pdf_hint=True)` and `Presentation.pdf_print_url()`
- Links to [reveal.js PDF export](https://revealjs.com/pdf-export/)

### 2.5 Example update

- `example/features_usage.py` — optional comment or small block showing `auto_slide` / `Plugin.SEARCH` (keep example runnable)

---

## Tier 3 (defer)

Narrow audience or different product layer. Implement only when there is explicit demand.

| Item | Notes | Effort |
| ---- | ----- | ------ |
| **Multiplex** | Live presenter + audience sync. Needs `multiplex` plugin, secret/hash config, and often a socket server. Document as `CustomPlugin` recipe first. | high |
| **Linked slide previews** | Extend beyond `LinkElement(preview=True)` to slide-preview patterns from reveal docs. | medium |
| **CLI** | `pyreveal build deck.py` to run a script and emit HTML. | medium |
| **Deck builder sugar** | `deck.title_slide()`, `deck.code_slide()` on top of `Slide` factories. | low |
| **Runtime Reveal API** | `Reveal.slide()`, events, `postMessage` — browser-only after export. | skip |
| **React bindings** | Use [reveal.js/react](https://revealjs.com/react/) separately. | skip |
| **Python plugin authoring** | Plugins are JS; register paths via `CustomPlugin` only. | skip |

### Tier 3 acceptance (when started)

- Multiplex: example deck + doc page, or explicit “not supported” with custom-plugin pointer
- CLI: entry point in `pyproject.toml`, documented in quickstart
- No new Python wrappers around browser-only reveal APIs

---

## Roadmap order

1. ~~Tier 1~~ (shipped in 0.7.0)
2. **Tier 2** (this milestone)
3. Ship 0.7.x patch or 0.8.0 with Tier 2
4. Tier 3 items as issues, not blockers