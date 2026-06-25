---
icon: lucide/list-checks
---

# Typed choices

PyReveal uses Python enums for common string options. Your editor can autocomplete them, and invalid values raise a clear error listing valid choices.

Plain strings still work (`theme="dracula"`), but enums are preferred.

## Import

```python
from pyreveal import (
    BackgroundSize,
    BackgroundType,
    CustomPlugin,
    FragmentEffect,
    MathEngine,
    Plugin,
    ScrollLayout,
    ScrollSnap,
    SlideNumber,
    KeyboardBinding,
    SlideVisibility,
    Theme,
    Transition,
    View,
)
```

## Theme

Deck CSS theme: `Presentation(theme=…)` and `set_theme()`.

```python
Presentation("Talk", theme=Theme.DRACULA)
```

| Member | Value |
| ------ | ----- |
| `BEIGE` | `beige` |
| `BLACK` | `black` |
| `BLACK_CONTRAST` | `black-contrast` |
| `BLOOD` | `blood` |
| `DRACULA` | `dracula` |
| `LEAGUE` | `league` |
| `MOON` | `moon` |
| `NIGHT` | `night` |
| `SERIF` | `serif` |
| `SIMPLE` | `simple` |
| `SKY` | `sky` |
| `SOLARIZED` | `solarized` |
| `WHITE` | `white` |
| `WHITE_CONTRAST` | `white-contrast` |

## Transition

Slide transition: `Presentation(transition=…)`, `set_transition()`, or per-slide `transition`.

```python
Presentation("Talk", transition=Transition.FADE)
```

`NONE`, `SLIDE`, `FADE`, `CONVEX`, `CONCAVE`, `ZOOM`

## Plugin

Reveal.js plugins: `plugins()` / `enable_plugins()`.

```python
deck.plugins(Plugin.NOTES, Plugin.HIGHLIGHT, Plugin.MATH)
```

| Member | Purpose |
| ------ | ------- |
| `NOTES` | Speaker view |
| `HIGHLIGHT` | Syntax-highlighted code |
| `MARKDOWN` | Markdown slides |
| `MATH` | LaTeX math |
| `SEARCH` | In-deck search |
| `ZOOM` | Alt+click zoom |

## MathEngine

Math renderer when `Plugin.MATH` is enabled.

```python
deck.plugins(Plugin.MATH, math_engine=MathEngine.KATEX)
```

`KATEX`, `MATHJAX2`, `MATHJAX3`, `MATHJAX4`

## BackgroundType

Explicit background kind in `bg()` dicts.

```python
slide.bg(type=BackgroundType.IMAGE, image="bg.jpg", size=BackgroundSize.COVER)
```

`COLOR`, `GRADIENT`, `IMAGE`, `VIDEO`, `IFRAME`

## BackgroundSize

Common image background sizes. Custom strings (e.g. `"100px"`) still work.

`COVER`, `CONTAIN`

## SlideVisibility

Per-slide visibility attribute.

```python
Slide(visibility=SlideVisibility.HIDDEN)
```

## View

Presentation layout mode for `configure(view=…)` and helpers like `scroll_view()`.

| Member | Value | Meaning |
| ------ | ----- | ------- |
| `SLIDE` | `slide` | Default slide mode (no `view` key emitted) |
| `SCROLL` | `scroll` | Scrollable page layout |
| `PRINT` | `print` | Print/PDF layout |

```python
deck.scroll_view()  # preferred over configure(view=View.SCROLL)
deck.print_view()
```

## SlideNumber

Slide number format for `slide_numbers()`.

| Member | Value |
| ------ | ----- |
| `H_DOT_V` | `h.v` |
| `H_SLASH_V` | `h/v` |
| `C` | `c` |
| `C_SLASH_T` | `c/t` |

```python
deck.slide_numbers(SlideNumber.C_SLASH_T)
deck.slide_numbers(False)  # hide numbers
```

## ScrollLayout / ScrollSnap

Used by `scroll_view()`.

`ScrollLayout`: `FULL`, `COMPACT`

`ScrollSnap`: `PROXIMITY`, `MANDATORY` (or pass `snap=False`)

## CustomPlugin

Register third-party plugin scripts:

```python
CustomPlugin("assets/my-plugin.js", "RevealMyPlugin")
```

## KeyboardBinding

Reveal.js API actions for `keyboard_bindings()`. Pass `None` to disable a key.

```python
from pyreveal import KeyboardBinding, Presentation

deck.keyboard_bindings({13: KeyboardBinding.NEXT, 32: None})
```

`NEXT`, `PREV`, `LEFT`, `RIGHT`, `UP`, `DOWN`, `TOGGLE_PAUSE`, `TOGGLE_HELP`, `TOGGLE_OVERVIEW`, `TOGGLE_AUTO_SLIDE`, `TOGGLE_JUMP_TO_SLIDE`, `PREV_FRAGMENT`, `NEXT_FRAGMENT`

## FragmentEffect

Fragment animation: `slide.fragment(…, effect=…)`.

```python
slide.fragment("Demo", effect=FragmentEffect.GROW)
slide.fragment("Highlight", effect=FragmentEffect.FADE_UP)
```

| Member | Animation |
| ------ | --------- |
| `NONE` | Default fade-in |
| `GROW` / `SHRINK` | Scale |
| `FADE_OUT` | Fade out |
| `FADE_UP` / `DOWN` / `LEFT` / `RIGHT` | Directional |
| `FADE_IN_THEN_OUT` | Fade in then out |
| `FADE_IN_THEN_SEMI_OUT` | Fade in then semi-out |
| `STRIKE` | Strikethrough |
| `HIGHLIGHT_RED` / `BLUE` / `GREEN` | Color highlight |
| `HIGHLIGHT_CURRENT_*` | Highlight current step |