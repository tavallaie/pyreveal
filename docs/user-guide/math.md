---
icon: lucide/sigma
---

# Math

Enable the math plugin and add LaTeX via `slide.code()`-style elements or `MathElement`.

```python
from pyreveal import MathElement, MathEngine, Plugin, Presentation, Slide

deck = Presentation("Math")
deck.plugins(Plugin.MATH, math_engine=MathEngine.KATEX)

slide = Slide()
slide.heading("Equations")
slide.element(MathElement(r"E = mc^2"))
slide.element(MathElement(r"\int_0^1 x^2 dx", display=True))

deck.add(slide)
```

## Math engines

Use the `MathEngine` enum with `Plugin.MATH`:

| Member | Engine |
| ------ | ------ |
| `MathEngine.KATEX` | KaTeX (default) |
| `MathEngine.MATHJAX2` | MathJax 2 |
| `MathEngine.MATHJAX3` | MathJax 3 |
| `MathEngine.MATHJAX4` | MathJax 4 |

Inline math uses `\(...\)`; display math uses `\[...\]`, matching [reveal.js math](https://revealjs.com/math/).