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
| Auto-slide / auto-progression | `auto_slide()`, `auto_progression()`, `Slide(auto_slide=…)` |
| Parallax backgrounds | `parallax_background()`, `slide.bg(…, parallax=…)` |
| Custom keyboard bindings | `keyboard_bindings()`, `KeyboardBinding` |
| Speaker notes | `Plugin.NOTES`, `slide.note()` |
| Built-in plugins | `Plugin.NOTES`, `HIGHLIGHT`, `MARKDOWN`, `MATH`, `SEARCH`, `ZOOM` |
| Custom plugins | `CustomPlugin(script, init)` |

## Fluent helpers

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
| `auto_slide(ms)` / `auto_progression(ms)` | `autoSlide`, `autoSlideStoppable`, `loop` |
| `parallax_background(image, …)` | `parallaxBackgroundImage`, `parallaxBackgroundSize`, `parallaxBackgroundHorizontal`, `parallaxBackgroundVertical`, … |
| `keyboard_bindings(bindings, …)` | `keyboard`, `keyboardCondition` |

`configure(**options)` still accepts any reveal.js key not covered above.

## Guides for common workflows

| Topic | PyReveal API / doc |
| ----- | ------------------ |
| Deck auto-slide / auto-progression | `auto_slide()`, `auto_progression()` |
| Per-slide auto-slide | `Slide(auto_slide=…)` / `data-autoslide` |
| Parallax background | `parallax_background(image, *, size, horizontal, vertical, …)` |
| Keyboard bindings | `keyboard_bindings({key_code: action, …})`, `KeyboardBinding` |
| Auto-animate | `animate()`, `AutoAnimate.text()` — see [Fragments](fragments.md) |
| In-deck search | `Plugin.SEARCH` — see [Search](search.md) |
| PDF export | `save(pdf_hint=True)`, `pdf_print_url()` — see [PDF export](pdf-export.md) |

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

PyReveal does not render PDF files. Export HTML, then open the print URL in Chromium. See the [PDF export guide](pdf-export.md).

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