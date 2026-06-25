from __future__ import annotations

from html import escape

from .config import (
    plugin_initialize_list,
    plugin_script_tags,
    serialize_initialize_options,
)


def wrap_in_html_template(
    title: str,
    theme: str,
    slides_html: str,
    initialize_options: dict,
    plugins: list[str] | None = None,
    *,
    math_engine: str = "katex",
    extra_css: list[str] | None = None,
    inline_css: str | None = None,
) -> str:
    """Wrap slides HTML in a Reveal.js 6.x-compatible template."""
    plugins = plugins or []
    config_js = serialize_initialize_options(initialize_options)
    plugin_scripts = plugin_script_tags(plugins) if plugins else ""
    highlight_css = (
        '\n    <link rel="stylesheet" href="revealjs/dist/plugin/highlight/monokai.css">'
        if "highlight" in plugins
        else ""
    )
    extra_css_links = "".join(
        f'\n    <link rel="stylesheet" href="{escape(path)}">'
        for path in (extra_css or [])
    )
    inline_style = (
        f"\n    <style>\n{inline_css}\n    </style>" if inline_css else ""
    )
    plugin_init = (
        f",\n            plugins: [{plugin_initialize_list(plugins, math_engine=math_engine)}]"
        if plugins
        else ""
    )
    plugin_block = f"\n{plugin_scripts}" if plugin_scripts else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="revealjs/dist/reset.css">
    <link rel="stylesheet" href="revealjs/dist/reveal.css">
    <link rel="stylesheet" href="revealjs/dist/theme/{theme}.css">{highlight_css}{extra_css_links}{inline_style}
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {slides_html}
        </div>
    </div>
    <script src="revealjs/dist/reveal.js"></script>{plugin_block}
    <script>
        Reveal.initialize({config_js}{plugin_init});
    </script>
</body>
</html>
"""