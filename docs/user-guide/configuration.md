# Reveal.js configuration

Use `configure()` to pass options to `Reveal.initialize()` in the generated HTML. See the [reveal.js config reference](https://revealjs.com/config/) for all keys.

```python
presentation = PyReveal(theme="white", transition="slide")
presentation.configure(
    hash=True,
    progress=True,
    slideNumber="h.v",
    controls=True,
    view="scroll",
)
```

## Theme vs transition

| Setting | How to set | Notes |
| -------- | ----------- | ----- |
| Theme | `set_theme("dracula")` | Loads `revealjs/dist/theme/<name>.css` |
| Transition | `set_transition("fade")` or `configure(transition="fade")` | `configure()` wins at render time |

## Supported themes

`beige`, `black`, `black-contrast`, `blood`, `dracula`, `league`, `moon`, `night`, `serif`, `simple`, `sky`, `solarized`, `white`, `white-contrast`

## Supported transitions

`none`, `slide`, `fade`, `convex`, `concave`, `zoom`

## Output directory

```python
presentation.save_to_file("deck.html", output_dir="build/my-talk")
```