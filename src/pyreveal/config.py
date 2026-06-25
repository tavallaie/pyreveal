from __future__ import annotations

import json
from html import escape
from typing import Any

from .choices import CustomPlugin, MathEngine, Plugin

VALID_PLUGINS = frozenset(plugin.value for plugin in Plugin)

PLUGIN_GLOBALS = {
    Plugin.NOTES.value: "RevealNotes",
    Plugin.HIGHLIGHT.value: "RevealHighlight",
    Plugin.MARKDOWN.value: "RevealMarkdown",
    Plugin.SEARCH.value: "RevealSearch",
    Plugin.ZOOM.value: "RevealZoom",
}

MATH_ENGINES = {
    MathEngine.KATEX.value: "RevealMath.KaTeX",
    MathEngine.MATHJAX2.value: "RevealMath.MathJax2",
    MathEngine.MATHJAX3.value: "RevealMath.MathJax3",
    MathEngine.MATHJAX4.value: "RevealMath.MathJax4",
}

# reveal.js expects markdown before highlight in script + init order.
PLUGIN_LOAD_ORDER = [
    Plugin.ZOOM.value,
    Plugin.NOTES.value,
    Plugin.SEARCH.value,
    Plugin.MARKDOWN.value,
    Plugin.HIGHLIGHT.value,
    Plugin.MATH.value,
]


def sort_plugins(plugins: list[str]) -> list[str]:
    order = {name: index for index, name in enumerate(PLUGIN_LOAD_ORDER)}
    return sorted(plugins, key=lambda name: order.get(name, len(PLUGIN_LOAD_ORDER)))


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


def plugin_script_tags(
    plugins: list[str],
    custom_plugins: list[CustomPlugin] | None = None,
) -> str:
    """Return HTML script tags for enabled reveal.js plugins."""
    tags = [
        f'    <script src="revealjs/dist/plugin/{name}.js"></script>'
        for name in sort_plugins(plugins)
    ]
    for plugin in custom_plugins or []:
        tags.append(f'    <script src="{escape(plugin.script)}"></script>')
    return "\n".join(tags)


def plugin_initialize_list(
    plugins: list[str],
    *,
    math_engine: str = MathEngine.KATEX.value,
    custom_plugins: list[CustomPlugin] | None = None,
) -> str:
    """Return the plugins array for Reveal.initialize()."""
    names: list[str] = []
    for name in sort_plugins(plugins):
        if name == Plugin.MATH.value:
            names.append(MATH_ENGINES.get(math_engine, MATH_ENGINES[MathEngine.KATEX.value]))
        else:
            names.append(PLUGIN_GLOBALS[name])
    for plugin in custom_plugins or []:
        names.append(plugin.init)
    return ", ".join(names)


def pdf_print_query(path: str | None = None) -> str:
    """Return the ``?print-pdf`` query string for reveal.js PDF export."""
    return "?print-pdf" if not path else f"{path}?print-pdf"