from .config import serialize_initialize_options


def wrap_in_html_template(title, theme, slides_html, initialize_options):
    """Wrap slides HTML in a Reveal.js 6.x-compatible template."""
    config_js = serialize_initialize_options(initialize_options)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="revealjs/dist/reset.css">
    <link rel="stylesheet" href="revealjs/dist/reveal.css">
    <link rel="stylesheet" href="revealjs/dist/theme/{theme}.css">
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {slides_html}
        </div>
    </div>
    <script src="revealjs/dist/reveal.js"></script>
    <script>
        Reveal.initialize({config_js});
    </script>
</body>
</html>
"""