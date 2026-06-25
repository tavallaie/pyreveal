---
icon: lucide/book-open
---

# API reference

## PyReveal

| Method | Description |
| ------ | ----------- |
| `PyReveal(title, theme, transition)` | Create a presentation |
| `add_slide(slide)` | Add a `Slide` |
| `add_group(slides)` | Add a vertical stack |
| `configure(**options)` | Pass options to `Reveal.initialize()` |
| `enable_plugins(*names)` | Enable reveal.js plugins |
| `set_theme(theme)` | Set CSS theme |
| `set_transition(transition)` | Set default transition |
| `set_background(background)` | Default background for slides without one |
| `generate_html()` | Build HTML string |
| `save_to_string()` | Alias for `generate_html()` |
| `save_to_file(filename, output_dir)` | Write HTML and copy assets |

## Slide

| Parameter / method | Description |
| ------------------ | ----------- |
| `content` | HTML body |
| `markdown` | Markdown body (requires markdown plugin) |
| `background` | `Background` instance |
| `notes` | Speaker notes text |
| `transition`, `state`, `auto_slide` | Per-slide reveal.js attributes |
| `auto_animate`, `auto_animate_easing` | Auto-animate between slides |
| `add_element(element)` | Add an `Element` |
| `add_vertical_slide(slide)` | Nest a vertical slide |

## Elements

| Class | Purpose |
| ----- | ------- |
| `Element` | Generic HTML element |
| `Fragment` | Stepped reveal (`.fragment`) |
| `SpeakerNotes` | `<aside class="notes">` |
| `ImageElement` | `<img>` with optional `Style` |
| `VideoElement` | `<video>` |
| `CodeElement` | Syntax-highlighted `<pre><code>` |
| `MarkdownElement` | Inline Markdown block |

## Backgrounds

| Class | reveal.js attribute |
| ----- | ------------------- |
| `ColorBackground` | `data-background-color` |
| `ImageBackground` | `data-background` |
| `VideoBackground` | `data-background-video` |
| `IframeBackground` | `data-background-iframe` |

All backgrounds support optional `opacity`, `position`, `repeat`, `transition`, and `parallax`.

Use `BackgroundFactory.create_background(type, value, **kwargs)` as a shortcut.