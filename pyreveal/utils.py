# utils.py


def generate_slides_html(slides):
    """Generate the HTML representation for each slide."""
    return "\n".join([f"<section>{slide['content']}</section>" for slide in slides])


def wrap_in_html_template(title, theme, transition, slides_html):
    """Wrap the slides HTML in the full Reveal.js template."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="revealjs/dist/reveal.css">
        <link rel="stylesheet" href="revealjs/dist/theme/{theme}.css">
        <script src="revealjs/dist/reveal.js"></script>
        

    </head>
    <body>
        <div class="reveal">
            <div class="slides">
                {slides_html}
            </div>
        </div>
        <script>
            Reveal.initialize({{
                transition: '{transition}'
            }});
        </script>
    </body>
    </html>
    """
