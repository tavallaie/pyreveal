---
icon: lucide/check-check
---

# Reveal.js feature support

PyReveal generates static reveal.js HTML. This page maps common [reveal.js features](https://revealjs.com/) to PyReveal APIs.

## Supported in Python

| reveal.js area | PyReveal API |
| -------------- | ------------ |
| Markup | `Slide.title()`, `text()`, `bullets()`, HTML blocks |
| Markdown | `Plugin.MARKDOWN`, `slide.markdown` |
| Backgrounds | `slide.bg()`, `Presentation.bg()` |
| Code | `Plugin.HIGHLIGHT`, `slide.code()` |
| Math | `Plugin.MATH`, `MathElement` |
| Fragments | `slide.fragment()`, `FragmentEffect` |
| Links / lightbox | `LinkElement(preview=True)`, `slide.image(preview=True)` |
| Layout | `Stack`, `HStack`, `VStack`, `FitText` |
| Slide visibility | `SlideVisibility.HIDDEN` |
| Themes / transitions | `Theme`, `Transition` enums |
| Vertical slides | `slide.vertical`, `Slide.section()` |
| Auto-animate | `Presentation.animate()`, `auto_animate` |
| Auto-slide | `auto_slide` on `Slide` |
| Speaker notes | `Plugin.NOTES`, `slide.note()` |
| Built-in plugins | `Plugin.NOTES`, `HIGHLIGHT`, `MARKDOWN`, `MATH`, `SEARCH`, `ZOOM` |
| Custom plugins | `CustomPlugin(script, init)` |

## Tier 1 helpers (typed shortcuts)

These wrap `configure()` with enums and fluent methods:

```python
from pyreveal import CustomPlugin, Plugin, Presentation, Slide, SlideNumber

deck = (
    Presentation("Talk")
    .navigation(hash=True, progress=True, overview=True)
    .deep_links(hash=True)
    .slide_numbers(SlideNumber.C_SLASH_T)
    .presentation_size(1280, 720)
    .preview_links(True)
    .scroll_view()
    .plugins(Plugin.NOTES, CustomPlugin("assets/extra.js", "RevealExtra"))
)

slide = Slide()
slide.id = "intro"
slide.image("photo.jpg", preview=True)
deck.add(slide)
```

| Method | reveal.js option |
| ------ | ---------------- |
| `navigation()` | `hash`, `controls`, `progress`, `touch`, `overview`, `keyboard`, `jumpToSlide` |
| `deep_links()` | `hash`, `respondToHashChanges`, `history` |
| `slide_numbers()` | `slideNumber`, `showSlideNumber` |
| `scroll_view()` | `view`, `scrollLayout`, `scrollSnap`, `scrollProgress`, `scrollActivationWidth` |
| `print_view()` | `view: "print"` |
| `presentation_size()` | `width`, `height`, `margin`, `minScale`, `maxScale` |
| `preview_links()` | `previewLinks` |

`configure(**options)` still accepts any reveal.js key not covered above.

## Deep links

Assign a slide id and enable hash URLs:

```python
slide = Slide()
slide.id = "agenda"
slide.title = "Agenda"

deck.deep_links(hash=True)
```

Open `deck.html#/agenda` in the browser to jump to that slide.

## Scroll view

```python
deck.scroll_view()
```

See [reveal.js scroll view](https://revealjs.com/scroll-view/) for behavior details.

## PDF export

PyReveal does not render PDF files. Export HTML, then open the print URL in Chromium:

```python
deck.save("output/talk.html", pdf_hint=True)
# PDF export URL: output/talk.html?print-pdf
```

Or build the URL manually:

```python
Presentation.pdf_print_url("output/talk.html")
```

Follow [reveal.js PDF export](https://revealjs.com/pdf-export/): open the `?print-pdf` URL, then print to PDF from the browser.

## Lightbox previews

```python
slide.image("thumb.jpg", preview=True)
slide.image("thumb.jpg", preview=True, preview_src="full.jpg")

from pyreveal import VideoElement

slide.element(VideoElement("clip.mp4", preview=True))
```

Link previews use `LinkElement(href, text, preview=True)` or `preview_links(True)` for all links.

## Custom plugins

```python
from pyreveal import CustomPlugin, Plugin, Presentation

deck.plugins(
    Plugin.HIGHLIGHT,
    CustomPlugin("revealjs/dist/plugin/notes.js", "RevealNotes"),
    CustomPlugin("assets/my-plugin.js", "RevealMyPlugin"),
)
```

- `script`: path relative to the saved HTML file
- `init`: global symbol passed to `Reveal.initialize({ plugins: [...] })`

Copy custom plugin files into the output folder when saving.

## Browser-only (not Python APIs)

These work in the exported deck but are not configured from Python beyond `configure()`:

- Overview mode, fullscreen, touch gestures (defaults on)
- PDF print layout runtime
- `Reveal.slide()` and other JS API methods
- `postMessage` integration

## Not supported

| Feature | Notes |
| ------- | ----- |
| React bindings | Use [reveal.js/react](https://revealjs.com/react/) separately |
| Multiplex | No first-class API; add custom JS if needed |
| Plugin authoring in Python | Register JS with `CustomPlugin` only |