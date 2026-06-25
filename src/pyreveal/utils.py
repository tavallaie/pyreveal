def generate_slides_html(slides):
    slides_html = []
    processed_titles = set()

    for slide in slides:
        if slide["title"] in processed_titles:
            continue

        background_html = (
            slide["background"].generate_html() if slide.get("background") else ""
        )

        if slide["group"]:
            group_slides = [s for s in slides if s["group"] == slide["group"]]
            vertical_slides_html = "\n".join(
                [
                    f"<section {sub_slide['background'].generate_html() if sub_slide.get('background') else ''}>{sub_slide['content']}</section>"
                    for sub_slide in group_slides
                ]
            )
            slides_html.append(
                f"<section {background_html}>\n{vertical_slides_html}\n</section>"
            )
            processed_titles.add(slide["group"])
        else:
            slides_html.append(
                f"<section {background_html}>{slide['content']}</section>"
            )

    return "\n".join(slides_html)


def wrap_in_html_template(title, theme, transition, slides_html):
    """Wrap slides HTML in a Reveal.js 6.x-compatible template."""
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
        Reveal.initialize({{
            transition: '{transition}'
        }});
    </script>
</body>
</html>
"""