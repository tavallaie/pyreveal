from __future__ import annotations

import json
from typing import Any

VALID_PLUGINS = frozenset(
    {"notes", "highlight", "markdown", "math", "search", "zoom"}
)

PLUGIN_GLOBALS = {
    "notes": "RevealNotes",
    "highlight": "RevealHighlight",
    "markdown": "RevealMarkdown",
    "search": "RevealSearch",
    "zoom": "RevealZoom",
}

MATH_ENGINES = {
    "katex": "RevealMath.KaTeX",
    "mathjax2": "RevealMath.MathJax2",
    "mathjax3": "RevealMath.MathJax3",
    "mathjax4": "RevealMath.MathJax4",
}


def build_initialize_options(
    transition: str, options: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Merge presentation transition with user-supplied Reveal.js options."""
    config: dict[str, Any] = {"transition": transition}
    if options:
        config.update(options)
    return config


def serialize_initialize_options(config: dict[str, Any]) -> str:
    """Serialize options for embedding in Reveal.initialize()."""
    return json.dumps(config, indent=12)


def plugin_script_tags(plugins: list[str]) -> str:
    """Return HTML script tags for enabled reveal.js plugins."""
    return "\n".join(
        f'    <script src="revealjs/dist/plugin/{name}.js"></script>'
        for name in plugins
    )


def plugin_initialize_list(
    plugins: list[str], *, math_engine: str = "katex"
) -> str:
    """Return the plugins array for Reveal.initialize()."""
    names: list[str] = []
    for name in plugins:
        if name == "math":
            names.append(MATH_ENGINES.get(math_engine, MATH_ENGINES["katex"]))
        else:
            names.append(PLUGIN_GLOBALS[name])
    return ", ".join(names)