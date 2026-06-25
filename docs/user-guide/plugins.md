---
icon: lucide/plug
---

# Plugins

PyReveal bundles reveal.js plugins but does not enable them by default. Call `plugins()` (or `enable_plugins()`) on the presentation.

```python
from pyreveal import Plugin, Presentation, Slide, Theme

deck = (
    Presentation("Talk", theme=Theme.DRACULA)
    .plugins(Plugin.NOTES, Plugin.HIGHLIGHT, Plugin.MARKDOWN)
)

slide = Slide()
slide.title = "Hello"
deck.add(slide)
```

## Supported plugins

Use the `Plugin` enum:

| Member | Purpose |
| ------ | ------- |
| `Plugin.NOTES` | Speaker view (`s` key) and `<aside class="notes">` |
| `Plugin.HIGHLIGHT` | Syntax-highlighted code via `slide.code()` |
| `Plugin.MARKDOWN` | Markdown slides (`slide.markdown = "…"`) |
| `Plugin.MATH` | LaTeX math rendering |
| `Plugin.SEARCH` | In-deck search |
| `Plugin.ZOOM` | Alt+click zoom |

Enable only what you need; each plugin adds scripts to the output HTML.

## Custom plugins

```python
from pyreveal import CustomPlugin, Plugin, Presentation

deck.plugins(
    Plugin.HIGHLIGHT,
    CustomPlugin("assets/extra.js", "RevealExtra"),
)
```

- `script`: path relative to the saved HTML file
- `init`: plugin global for `Reveal.initialize({ plugins: [...] })`

Copy custom `.js` files into the output folder when saving.

## Speaker notes

```python
slide = Slide()
slide.title = "Topic"
slide.note("Mention the 2026 roadmap.")
```

Requires `Plugin.NOTES`.

## Code blocks

```python
slide = Slide()
slide.heading("Example")
slide.code("print('hello')", language="python", line_numbers=True)
```

Requires `Plugin.HIGHLIGHT`.

## Markdown slides

```python
slide = Slide()
slide.markdown = "## Title\n\n- Point one\n- Point two"
```

Requires `Plugin.MARKDOWN`.

## Math

```python
from pyreveal import MathEngine, Plugin

deck.plugins(Plugin.MATH, math_engine=MathEngine.KATEX)
```

See [Math](math.md) for `MathElement` details.

## Search

```python
deck.plugins(Plugin.SEARCH)
```

Adds an in-deck search box. See [Search](search.md) for usage in the browser.

## Advanced: low-level elements

You can still use `CodeElement`, `MarkdownElement`, and `SpeakerNotes` directly via `slide.element()`. The slide builder methods above are preferred.