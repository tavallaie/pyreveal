---
icon: lucide/book-open
---

# API reference

## Overview

| Class | Role |
| ----- | ---- |
| `Presentation` | Deck container: theme, plugins, backgrounds, export |
| `Slide` | One slide: content, fragments, backgrounds, vertical children |
| `PyReveal` | Alias for `Presentation` |

**Workflow:** build `Slide()` objects → `Presentation.add(slide)` → `save()`

## Package exports

```python
from pyreveal import (
    # Core
    Presentation, PyReveal, Slide,
    # Typed choices
    Theme, Transition, Plugin, MathEngine,
    BackgroundType, BackgroundSize, SlideVisibility, FragmentEffect,
    # Advanced (optional)
    Element, Fragment, CodeElement, ImageElement, MathElement, MarkdownElement,
    SpeakerNotes, VideoElement, LinkElement,
    AutoAnimate, Background, BackgroundFactory,
    ColorBackground, GradientBackground, ImageBackground, VideoBackground, IframeBackground,
    Content, Heading, Paragraph, BulletList,
    Layout, Stack, HStack, VStack, FitText,
    Style, CSS,
)
```

---

## Typed choices

See [Choices](../user-guide/choices.md) for full enum tables and examples.

| Enum | Used for |
| ---- | -------- |
| `Theme` | `Presentation(theme=…)`, `set_theme()` |
| `Transition` | `Presentation(transition=…)`, slide `transition` |
| `Plugin` | `plugins()`, `enable_plugins()` |
| `MathEngine` | `plugins(…, math_engine=…)` |
| `BackgroundType` | `bg(type=…)` |
| `BackgroundSize` | `bg(size=…)` |
| `SlideVisibility` | slide `visibility` |
| `FragmentEffect` | `fragment(…, effect=…)` |
| `View` | `scroll_view()`, `print_view()` |
| `SlideNumber` | `slide_numbers()` |
| `ScrollLayout` / `ScrollSnap` | `scroll_view()` |
| `CustomPlugin` | `plugins()` / `enable_plugins()` |

Plain strings still work (`theme="dracula"`); enums are preferred.

---

## Presentation

### Constructor

```python
Presentation(title="Untitled Presentation", *, theme=Theme.BLACK, transition=Transition.SLIDE)
```

`Presentation.Theme`, `.Transition`, `.Plugin`, and `.MathEngine` are aliases of the module-level enums.

### Configuration

| Method | Description |
| ------ | ----------- |
| `configure(**options)` | Pass options to `Reveal.initialize()` |
| `navigation(…)` | Hash, controls, progress, touch, overview, keyboard |
| `deep_links(…)` | Hash URLs and slide deep linking |
| `slide_numbers(format, …)` | Slide number display format |
| `scroll_view(…)` | Enable scroll view layout |
| `print_view()` | Enable print/PDF layout |
| `presentation_size(width, height, …)` | Base slide dimensions |
| `preview_links(enabled=True)` | Global link lightbox previews |
| `auto_slide(interval_ms, *, stoppable=True, loop=False)` | Deck-wide auto-advance |
| `set_theme(theme)` | Set CSS theme (`Theme` or string) |
| `set_transition(transition)` | Set default transition (`Transition` or string) |
| `plugins(*plugins, math_engine=MathEngine.KATEX)` | Enable built-in and `CustomPlugin` scripts |
| `enable_plugins(…)` | Alias for `plugins()` |
| `bg(value, **kwargs)` | Default deck background |
| `set_background(…)` | Alias for `bg()` |
| `stylesheet(path)` / `add_stylesheet(path)` | Link extra CSS file |
| `css(css)` / `add_inline_css(css)` | Embed inline CSS |

### Slides

| Method | Description |
| ------ | ----------- |
| `add(*slides)` | Add pre-built `Slide` objects (fluent return) |
| `slide(slide)` | Alias for `add()` |
| `add_slide(slide)` | Add slide (no return) |
| `section(parent, *children)` | Add parent; append extra vertical children |
| `add_group(slides)` | Vertical stack from a list (legacy) |
| `animate(frames, *, easing, content_key="_content")` | Auto-animate sequence |

### Export

| Method | Description |
| ------ | ----------- |
| `html()` / `generate_html()` | Build HTML string |
| `save_to_string()` | Alias for `html()` |
| `save(path, *, copy_revealjs=True, quiet=False, pdf_hint=False)` | Write HTML; creates parent dirs when `path` includes a folder |
| `save_to_file(filename, output_dir="presentations", …)` | Write to a named output folder |
| `pdf_print_url(path)` (static) | Build `?print-pdf` URL for browser PDF export |

### `bg()` shorthand

| Input | Result |
| ----- | ------ |
| `"#222"` | Color background |
| `"bg.jpg"` | Image background |
| `{"type": BackgroundType.VIDEO, "video": "…"}` | Typed dict |
| `ColorBackground(…)` | Background subclass |

Shared kwargs: `opacity`, `position`, `repeat`, `size`, `transition`, `parallax`, plus type-specific keys (`image`, `gradient`, `sources`, `iframe`, `interactive`, …).

---

## Slide

### Constructor

```python
Slide(*blocks, **options)
```

| Positional / keyword | Behavior |
| -------------------- | -------- |
| `Slide("plain text")` | Paragraph |
| `Slide("<h1>HTML</h1>")` | Raw HTML escape hatch |
| `Slide(content="…")` | Same as a single string block |

Constructor fields (`**kwargs`):

| Field | Type | Description |
| ----- | ---- | ----------- |
| `transition` | `Transition \| str` | Per-slide transition |
| `visibility` | `SlideVisibility \| str` | e.g. `SlideVisibility.HIDDEN` |
| `slide_id` | `str` | `id` attribute |
| `state` | `str` | `data-state` |
| `auto_slide` | `int` | `data-autoslide` (ms) |
| `auto_animate` | `bool` | Enable auto-animate on this slide |
| `auto_animate_easing` | `str` | Easing for auto-animate |
| `notes` / `note` | `str` | Speaker notes |
| `markdown` | `str` | Markdown body |
| `bg` / `background` | any | Background shorthand |
| `fragments` | `list` | Initial fragments (see below) |
| `attributes` | `dict` | Extra HTML attributes |

Fluent options (`bg`, `note`, `fragments`, `title`, `subtitle`, `heading`, …) also work on factories and `Slide.section()`.

### Instance builder

| Method / assignment | Description |
| ------------------- | ----------- |
| `title("…")` / `title = "…"` | Main title (`<h1>`); getter when called with no args |
| `subtitle("…")` / `subtitle = "…"` | Subtitle paragraph |
| `heading("…")` / `heading = "…"` | Section heading (`<h2>` by default) |
| `text(*paragraphs)` | Append paragraph(s) |
| `bullets(items, *, ordered=False)` | Bullet list; getter when called with no args |
| `code(source, *, language="python", line_numbers=False)` | Code block (needs `Plugin.HIGHLIGHT`) |
| `id` (property) | Slide DOM id for hash deep links (alias for `slide_id`) |
| `image(src, *, caption, alt, stretch=False, preview=False)` | Image with optional lightbox preview |
| `markdown = "…"` | Markdown body (needs `Plugin.MARKDOWN`) |
| `fragment(text, *, effect=FragmentEffect.NONE, index=None)` | Stepped reveal |
| `note(text)` | Speaker notes (needs `Plugin.NOTES`) |
| `bg(value, **kwargs)` / `set_background(…)` | Per-slide background |
| `vertical` (property) | List of vertical child slides; assign to reorder |
| `add(*content)` | Append content blocks |
| `element(el)` / `add_element(el)` | Add an `Element` subclass |
| `add_vertical_slide(slide \| str)` | Append one vertical child |

### Factories

| Class method | Purpose |
| ------------ | ------- |
| `Slide.make_title(text, *, subtitle, level=1, **options)` | Title slide |
| `Slide.make_heading(text, *, level=2, **options)` | Heading slide |
| `Slide.make_text(*paragraphs, **options)` | Text slide(s) |
| `Slide.make_bullets(items, *, title, ordered=False, **options)` | Bullet list |
| `Slide.make_code(code, *, title, language, line_numbers, **options)` | Code slide |
| `Slide.make_image(src, *, title, caption, alt, stretch, **options)` | Image slide |
| `Slide.from_markdown(markdown, **options)` | Markdown slide |
| `Slide.section(main, *children, **options)` | Horizontal slide with vertical children |

`main` and `children` accept `Slide` instances or plain strings (converted to text slides).

### `fragments` option format

```python
Slide.make_title(
    "Agenda",
    fragments=[
        "Plain fragment",
        ("Grow", {"effect": FragmentEffect.GROW}),
        {"text": "Dict form", "index": 2},
    ],
)
```

### Rendering

| Method | Description |
| ------ | ----------- |
| `content` (property) | Combined HTML of content blocks |
| `generate_html(**kwargs)` | Full `<section>` HTML |
| `render(default_background=…)` | Render with deck default background |

---

## Auto-animate

```python
deck.animate(
    [
        {"title": "Before", "body": "First"},
        {"title": "After", "body": "Second"},
    ],
    easing="ease-in-out",
    content_key="_content",  # optional extra body key
)
```

Each dict key becomes a matched element with a stable `data-id`. Plain strings are preferred; HTML strings also work.

Advanced: `AutoAnimate(easing=…).sequence(frames)`, `AutoAnimate.text("id", "text")`, or `AutoAnimate.match("id", element)`.

---

## Advanced types

Optional for fine-grained control. See [Elements](../user-guide/elements.md) and [Layouts](../user-guide/layouts.md).

| Type | Purpose |
| ---- | ------- |
| `Element` | Arbitrary HTML tag, attributes, children, `Style` |
| `Fragment` | Low-level fragment with `FragmentEffect` |
| `CodeElement`, `ImageElement`, `VideoElement`, `LinkElement` | Typed media |
| `MathElement` | LaTeX (needs `Plugin.MATH`) |
| `MarkdownElement` | Markdown block |
| `SpeakerNotes` | Notes element |
| `Stack`, `HStack`, `VStack`, `FitText` | Reveal.js layout helpers |
| `Background` subclasses | `ColorBackground`, `ImageBackground`, … |
| `BackgroundFactory.create_background(type, …)` | Programmatic background creation |
| `Style`, `CSS` | Inline and stylesheet helpers |