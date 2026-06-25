---
icon: lucide/plug
---

# Plugins

PyReveal bundles reveal.js plugins but does not enable them by default. Call `enable_plugins()` to load them in the generated HTML.

```python
from pyreveal import PyReveal, Slide

presentation = PyReveal(title="Talk")
presentation.enable_plugins("notes", "highlight", "markdown", "math", "search", "zoom")
presentation.add_slide(Slide(content="<h1>Hello</h1>"))
```

## Supported plugins

| Plugin | Purpose |
| ------ | ------- |
| `notes` | Speaker view (`s` key) and `<aside class="notes">` |
| `highlight` | Syntax-highlighted code via `CodeElement` |
| `markdown` | Markdown slides and `MarkdownElement` |
| `math` | LaTeX math rendering |
| `search` | In-deck search |
| `zoom` | Alt+click zoom |

Enable only what you need — each plugin adds scripts to the output HTML.

## Speaker notes

Set notes on a slide or use `SpeakerNotes`:

```python
from pyreveal import Slide, SpeakerNotes

slide = Slide(content="<h2>Topic</h2>", notes="Mention the 2026 roadmap.")
# or
slide.add_element(SpeakerNotes("Extra detail for the presenter."))
```

Requires the `notes` plugin.

## Code blocks

```python
from pyreveal import CodeElement, Slide

slide = Slide(content="<h2>Example</h2>")
slide.add_element(
    CodeElement("print('hello')", language="python", line_numbers=True)
)
```

Requires the `highlight` plugin.

## Markdown slides

```python
slide = Slide(markdown="## Title\n\n- Point one\n- Point two")
```

Requires the `markdown` plugin.