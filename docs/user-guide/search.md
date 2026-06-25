---
icon: lucide/search
---

# In-deck search

PyReveal bundles reveal.js search but does not enable it by default. Add `Plugin.SEARCH` when building the deck.

## Enable search

```python
from pyreveal import Plugin, Presentation, Slide

deck = (
    Presentation("Talk")
    .plugins(Plugin.SEARCH)
)

slide = Slide()
slide.title = "Agenda"
slide.text("Topics we will cover today.")
deck.add(slide).save("talk.html")
```

The exported HTML loads `revealjs/dist/plugin/search.js` and registers `RevealSearch` in `Reveal.initialize()`.

## Using search in the browser

Open the saved HTML in a browser. The reveal.js search plugin adds a search box in the top-right corner of the deck.

1. Click the search field (or use the keyboard shortcut from [reveal.js search](https://revealjs.com/search/)).
2. Type a query and press Enter.
3. The deck jumps to the next slide that contains the text and highlights the match.

Search runs entirely in the browser on the exported HTML. No Python API is involved at runtime.

## Tips

- Use distinctive slide titles and headings so queries are easy to find.
- Combine with `slide.id` and `deep_links()` when you want hash URLs as well as full-text search.
- Search indexes visible slide text; speaker notes are not searched.

## Related

- [Plugins](plugins.md) — all bundled plugins
- [Configuration](configuration.md) — `plugins()` and `configure()`