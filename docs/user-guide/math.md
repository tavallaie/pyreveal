---
icon: lucide/sigma
---

# Math

Enable the math plugin and add LaTeX via `MathElement` or raw slide content.

```python
from pyreveal import MathElement, PyReveal, Slide

presentation = PyReveal()
presentation.enable_plugins("math", math_engine="katex")
# math_engine: katex, mathjax2, mathjax3, mathjax4

slide = Slide(content="<h2>Equations</h2>")
slide.add_element(MathElement(r"E = mc^2"))
slide.add_element(MathElement(r"\int_0^1 x^2 dx", display=True))
presentation.add_slide(slide)
```

Inline math uses `\(...\)`; display math uses `\[...\]`, matching [reveal.js math](https://revealjs.com/math/).