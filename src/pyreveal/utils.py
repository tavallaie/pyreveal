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
    custom_plugins: list | None = None,
    math_engine: str = "katex",
    extra_css: list[str] | None = None,
    inline_css: str | None = None,
    extra_head: str | None = None,
    extra_scripts: list[str] | None = None,
    inline_js: str | None = None,
) -> str:
    """Wrap slides HTML in a Reveal.js 6.x-compatible template."""
    plugins = plugins or []
    config_js = serialize_initialize_options(initialize_options)
    plugin_scripts = (
        plugin_script_tags(plugins, custom_plugins)
        if plugins or custom_plugins
        else ""
    )
    highlight_css = (
        '\n    <link rel="stylesheet" href="revealjs/dist/plugin/highlight/zenburn.css">'
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
    head_extra = f"\n    {extra_head}" if extra_head else ""
    script_tags = "".join(
        f'\n    <script type="module" src="{escape(path)}"></script>'
        for path in (extra_scripts or [])
    )
    inline_script = f"\n    <script>\n{inline_js}\n    </script>" if inline_js else ""
    plugin_list = (
        plugin_initialize_list(
            plugins, math_engine=math_engine, custom_plugins=custom_plugins
        )
        if plugins or custom_plugins
        else ""
    )
    if plugin_list:
        config_js = config_js.rstrip()
        if config_js.endswith("}"):
            config_js = (
                config_js[:-1]
                + f",\n            plugins: [{plugin_list}]\n        }}"
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
    <link rel="stylesheet" href="revealjs/dist/theme/{theme}.css">{highlight_css}{extra_css_links}{inline_style}{head_extra}
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {slides_html}
        </div>
    </div>
    <script src="revealjs/dist/reveal.js"></script>{plugin_block}
    <script>
        Reveal.initialize({config_js});
    </script>{inline_script}{script_tags}
</body>
</html>
"""