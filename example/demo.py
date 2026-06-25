"""
PyReveal demo — docs homepage title slide + feature tour.

    uv run python example/demo.py
    cd example/presentations && python3 -m http.server 8765
    open http://localhost:8765/demo.html
"""

import bootstrap  # noqa: F401

from pathlib import Path

from _common import OUTPUT_DIR, copy_assets, output

from pyreveal import (
    BackgroundType,
    Element,
    FitText,
    FragmentEffect,
    HStack,
    Plugin,
    Presentation,
    Slide,
    SlideVisibility,
    Stack,
    Theme,
    Transition,
)

# PyReveal docs homepage copy (docs/index.md)
DOCS_URL = "https://tavallaie.github.io/pyreveal"
GITHUB_URL = "https://github.com/tavallaie/pyreveal"
HERO_TITLE = "Presentations, written in Python"
HERO_TAGLINE = (
    "Build polished slides in code with titles, bullets, code, math, and speaker notes. "
    "Export one self-contained HTML file you can open offline or share anywhere."
)
HERO_NOTE = "No HTML required. Just Python."

# Remote demo assets (requires HTTP, not file://).
ARROW = "https://static.slid.es/reveal/arrow.png"
IMAGE_PLACEHOLDER = "https://static.slid.es/reveal/image-placeholder.png"
LIGHTBOX_IMAGE = "assets/image.jpg"
BG_VIDEO = "assets/clip.mp4"
LIGHTBOX_POSTER = "assets/poster.jpg"
LIGHTBOX_VIDEO = "assets/video.mp4"
GIF_BG = "http://i.giphy.com/90F8aUepslB84.gif"

_ANIMATE_EASING = "cubic-bezier(0.770, 0.000, 0.175, 1.000)"
_THEME_LINK = "document.querySelector('link[href*=\\'theme/\\']')"
_THREE_IMPORTMAP = """<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"
  }
}
</script>"""

_HOME_HERO_CSS = """
.reveal .slides section.demo-home-slide {
  background: transparent !important;
  padding: 0 !important;
}
.reveal .demo-home-slide-placeholder {
  opacity: 0;
  pointer-events: none;
}
#demo-home-fullpage {
  position: fixed;
  inset: 0;
  z-index: 5;
  display: flex;
  align-items: center;
  overflow: hidden;
  text-align: left;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.35s ease;
}
#demo-home-fullpage.is-active {
  opacity: 1;
  pointer-events: auto;
}
#demo-home-fullpage .demo-home-hero__bg {
  position: absolute;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  background: linear-gradient(160deg, #0c0d12 0%, #08090c 48%, #090a0f 100%);
}
#demo-home-fullpage .demo-home-hero__bg::before {
  content: "";
  position: absolute;
  inset: -20%;
  opacity: 0;
  background:
    repeating-linear-gradient(
      90deg,
      transparent 0,
      transparent 38px,
      rgba(200, 210, 224, 0.07) 39px,
      transparent 40px
    ),
    repeating-linear-gradient(
      0deg,
      transparent 0,
      transparent 38px,
      rgba(200, 210, 224, 0.07) 39px,
      transparent 40px
    );
  animation: demo-mesh-flow 28s linear infinite;
}
#demo-home-fullpage.no-hero-webgl .demo-home-hero__bg::before {
  opacity: 1;
}
#demo-home-fullpage.no-hero-webgl .demo-home-hero__canvas {
  opacity: 0;
  visibility: hidden;
}
@keyframes demo-mesh-flow {
  from { transform: translate3d(0, 0, 0) skewY(-2deg); }
  to { transform: translate3d(-40px, -24px, 0) skewY(-2deg); }
}
#demo-home-fullpage .demo-home-hero__canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}
#demo-home-fullpage .demo-home-hero__shade {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  backdrop-filter: blur(5px) saturate(1.05);
  -webkit-backdrop-filter: blur(5px) saturate(1.05);
  background:
    radial-gradient(ellipse 120% 90% at 50% 58%, transparent 42%, rgba(8, 9, 12, 0.12) 100%),
    linear-gradient(90deg, rgba(8, 9, 12, 0.2) 0%, rgba(8, 9, 12, 0.02) 38%, transparent 62%);
}
#demo-home-fullpage .demo-home-hero__content {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 72rem;
  margin: 0 auto;
  padding: 0 clamp(1.5rem, 5vw, 3rem);
}
body.demo-home-active .reveal .progress,
body.demo-home-active .reveal .controls {
  z-index: 10;
}
@media (prefers-reduced-motion: reduce) {
  #demo-home-fullpage .demo-home-hero__bg::before { animation: none; }
}
"""


def _arrow(
    href: str,
    *,
    rotate: bool = False,
    navigate_down: bool = False,
) -> str:
    transform = " transform: rotate(180deg)" if rotate else ""
    link_class = ' class="navigate-down"' if navigate_down else ""
    return (
        f'<a href="{href}"{link_class}>'
        f'<img class="r-frame" style="background: rgba(255, 255, 255, 0.1);{transform}" '
        f'width="178" height="238" data-src="{ARROW}" alt="Arrow" />'
        f"</a>"
    )


def _hero_button_styles() -> tuple[str, str]:
    btn = (
        "display: inline-block; padding: 0.55em 1.15em; border-radius: 4px; "
        "color: #fff; text-decoration: none; font-size: 0.9rem; "
        "backdrop-filter: blur(6px);"
    )
    btn_primary = (
        f"{btn} background: linear-gradient(35deg, rgba(176, 186, 198, 0.55), "
        "rgba(220, 226, 235, 0.35)); border: 1px solid rgba(220, 226, 235, 0.25);"
    )
    btn_secondary = f"{btn} background: rgba(255, 255, 255, 0.14);"
    return btn_primary, btn_secondary


def _hero_buttons_html() -> str:
    btn_primary, btn_secondary = _hero_button_styles()
    return (
        '<p style="display: flex; flex-wrap: wrap; gap: 0.75rem; margin: 0;">'
        f'<a href="{DOCS_URL}/getting-started/quickstart/" style="{btn_primary}">'
        "Get started</a>"
        f'<a href="{DOCS_URL}/reference/api/" style="{btn_secondary}">'
        "API reference</a>"
        "</p>"
    )


def _home_hero_slide() -> Slide:
    """Docs landing page hero (overrides/home.html + docs/index.md + Three.js mesh)."""
    slide = Slide(attributes={"class": "demo-home-slide"})
    slide.add(
        '<div class="demo-home-hero">'
        '<div class="demo-home-hero__bg" aria-hidden="true">'
        '<canvas id="demo-hero-canvas" class="demo-home-hero__canvas"></canvas>'
        '<div class="demo-home-hero__shade" aria-hidden="true"></div>'
        "</div>"
        '<div class="demo-home-hero__content">'
        '<p style="margin: 0 0 1rem; font-size: 0.95rem; letter-spacing: 0.08em; '
        'text-transform: uppercase; color: rgba(255, 255, 255, 0.72);">PyReveal</p>'
        f'<h1 style="font-size: clamp(1.75rem, 4.5vw, 2.75rem); letter-spacing: -0.04em; '
        f"line-height: 1.15; margin: 0 0 0.75rem; color: #fff; font-weight: 600; "
        f'text-shadow: 0 1px 24px rgba(0, 0, 0, 0.45);">{HERO_TITLE}</h1>'
        f'<p style="font-size: clamp(1rem, 2vw, 1.125rem); line-height: 1.55; '
        f"margin: 0 0 0.75rem; color: #fff; "
        f'text-shadow: 0 1px 16px rgba(0, 0, 0, 0.4);">{HERO_TAGLINE}</p>'
        f'<p style="margin: 0 0 1.25rem; color: rgba(255, 255, 255, 0.82);">'
        f"<small><em>{HERO_NOTE}</em></small></p>"
        f"{_hero_buttons_html()}"
        "</div>"
        "</div>"
        '<div class="demo-home-slide-placeholder" aria-hidden="true"></div>'
    )
    return slide


def build() -> Presentation:
    # ── Title (docs homepage) ────────────────────────────────────────────────
    title = _home_hero_slide()

    hello = Slide.make_heading("Hello There")
    hello.text(
        "PyReveal enables you to create beautiful interactive slide decks using Python, "
        "powered by reveal.js under the hood. Go beyond the usual reveal.js toolkit with "
        "PyReveal-only extras like Three.js — this presentation shows you what it can do."
    )

    # ── Vertical slides ──────────────────────────────────────────────────────
    vertical_main = Slide()
    vertical_main.heading("Vertical Slides")
    vertical_main.text("Slides can be nested inside of each other.")
    vertical_main.add("<p>Use the <em>Space</em> key to navigate through all slides.</p>")
    vertical_main.add("<br />", _arrow("#/2/1", navigate_down=True))

    basement1 = Slide.make_heading("Basement Level 1")
    basement1.text(
        "Nested slides are useful for adding additional detail underneath a high level "
        "horizontal slide."
    )

    basement2 = Slide.make_heading("Basement Level 2")
    basement2.id = "basement-2"
    basement2.text("That's it, time to go back up.")
    basement2.add("<br />", _arrow("#/2", rotate=True))

    vertical = Slide.section(vertical_main, basement1, basement2)

    hidden = Slide(visibility=SlideVisibility.HIDDEN)
    hidden.heading("Hidden Slides")
    hidden.text(
        "This slide is visible in the source, but hidden when the presentation is viewed. "
        "You can show all hidden slides by setting the `showHiddenSlides` config option "
        "to `true`."
    )

    # ── Pretty code (auto-animate) ───────────────────────────────────────────
    pretty_code = Slide(
        auto_animate=True,
        content=(
            '<h2 data-id="code-title">Pretty Code</h2>'
            '<pre data-id="code-animation"><code class="hljs python" '
            'data-trim data-line-numbers>\n'
            "from pyreveal import Presentation, Slide\n\n"
            "deck = Presentation(\"My Talk\")\n"
            "slide = Slide()\n"
            "slide.title = \"Hello\"\n"
            "slide.code(\"print('Hello')\", language=\"python\")\n\n"
            "deck.add(slide).save(\"deck.html\")\n"
            "</code></pre>"
            "<p>Code syntax highlighting courtesy of "
            '<a href="https://highlightjs.org/usage/">highlight.js</a>.</p>'
        ),
    )

    animated_code = Slide(
        auto_animate=True,
        content=(
            '<h2 data-id="code-title">With Animations</h2>'
            '<pre data-id="code-animation"><code class="hljs python" '
            'data-trim data-line-numbers="|4,8-11|17|22-24">'
            '<script type="text/template">\n'
            "from pyreveal import Plugin, Presentation, Slide, Theme\n\n"
            "intro = Slide()\n"
            "intro.title = \"Welcome\"\n"
            "intro.bullets([\"One\", \"Two\", \"Three\"])\n\n"
            "photo = Slide()\n"
            "photo.heading(\"Photo slide\")\n"
            "photo.bg(\"path/to/image.jpg\")\n\n"
            "deck = (\n"
            "    Presentation(\"My Talk\", theme=Theme.BLACK)\n"
            "    .plugins(Plugin.HIGHLIGHT, Plugin.NOTES)\n"
            "    .add(intro, photo)\n"
            "    .save(\"deck.html\")\n"
            ")\n"
            "</script></code></pre>"
        ),
    )

    # ── Point of view & touch ────────────────────────────────────────────────
    overview = Slide.make_heading("Point of View")
    overview.add("<p>Press <strong>ESC</strong> to enter the slide overview.</p>")
    overview.add(
        "<p>Hold down the <strong>alt</strong> key (<strong>ctrl</strong> in Linux) and "
        "click on any element to zoom towards it using "
        '<a href="http://lab.hakim.se/zoom-js">zoom.js</a>. '
        "Click again to zoom back out.</p>"
    )
    overview.text("(NOTE: Use ctrl + click in Linux.)")

    touch = Slide.make_heading("Touch Optimized")
    touch.text(
        "Presentations look great on touch devices, like mobile phones and tablets. "
        "Simply swipe through your slides."
    )

    # ── Auto-animate boxes ───────────────────────────────────────────────────
    box_style = (
        "background: #999; width: 50px; height: 50px; "
        "margin: 10px; border-radius: 5px"
    )

    def _box(data_id: str, style: str, *, delay: str | None = None) -> Element:
        attrs: dict[str, str] = {"style": style}
        if delay is not None:
            attrs["data-auto-animate-delay"] = delay
        el = Element(tag="div", attributes=attrs)
        el.set_data_id(data_id)
        return el

    animate_intro = Slide(auto_animate=True, auto_animate_easing=_ANIMATE_EASING)
    animate_intro.heading("Auto-Animate")
    animate_intro.add(
        "<p>Automatically animate matching elements across slides with "
        f'<a href="{DOCS_URL}/user-guide/fragments/">Auto-Animate</a>.</p>'
    )
    animate_intro.element(
        HStack(
            children=[
                _box("box1", box_style),
                _box("box2", box_style),
                _box("box3", box_style),
            ],
            attributes={"class": "justify-center"},
        )
    )

    animate_colors = Slide(auto_animate=True, auto_animate_easing=_ANIMATE_EASING)
    animate_colors.element(
        HStack(
            children=[
                _box(
                    "box1",
                    "background: cyan; width: 150px; height: 100px; margin: 10px",
                    delay="0",
                ),
                _box(
                    "box2",
                    "background: magenta; width: 150px; height: 100px; margin: 10px",
                    delay="0.1",
                ),
                _box(
                    "box3",
                    "background: yellow; width: 150px; height: 100px; margin: 10px",
                    delay="0.2",
                ),
            ],
            attributes={"class": "justify-center"},
        )
    )
    animate_colors.element(
        Element(
            tag="h2",
            content="Auto-Animate",
            attributes={"style": "margin-top: 20px"},
        )
    )

    animate_stack = Slide(auto_animate=True, auto_animate_easing=_ANIMATE_EASING)
    _circle = "border-radius: 50%"
    animate_stack.element(
        Stack(
            children=[
                _box(
                    "box1",
                    f"background: cyan; width: 300px; height: 300px; {_circle}",
                ),
                _box(
                    "box2",
                    f"background: magenta; width: 200px; height: 200px; {_circle}",
                ),
                _box(
                    "box3",
                    f"background: yellow; width: 100px; height: 100px; {_circle}",
                ),
            ]
        )
    )
    animate_stack.element(
        Element(
            tag="h2",
            content="Auto-Animate",
            attributes={"style": "margin-top: 20px"},
        )
    )

    # ── Markdown ─────────────────────────────────────────────────────────────
    markdown = Slide.from_markdown(
        "## Markdown Support\n\n"
        "Write content using inline or external Markdown.\n"
        "Instructions and more info available in the "
        f"[docs]({DOCS_URL}/user-guide/plugins/).\n\n"
        "```python []\n"
        "from pyreveal import Slide\n\n"
        "slide = Slide.from_markdown(\n"
        '    "## Markdown Support\\n\\n"\n'
        '    "- **Bold** and `code` work too"\n'
        ")\n"
        "```"
    )

    # ── Lightbox ─────────────────────────────────────────────────────────────
    lightbox = Slide()
    lightbox.heading("Lightbox")
    lightbox.add(
        "Turn any element into a "
        f'<a href="{DOCS_URL}/user-guide/reveal-features/#lightbox-previews">lightbox</a> using '
        "<strong>data‑preview‑image</strong> & <strong>data‑preview‑video</strong>."
    )
    lightbox.add(
        '<div class="r-hstack" style="gap: 2rem;">'
        "<div>"
        '<pre style="font-size: 12px; width: 100%"><code class="python" data-trim>'
        'slide.image("assets/image.jpg", preview=True)'
        "</code></pre>"
        f'<img src="{LIGHTBOX_IMAGE}" height="100" data-preview-image>'
        "</div>"
        "<div>"
        '<pre style="font-size: 12px; width: 100%"><code class="python" data-trim>'
        'slide.image("assets/poster.jpg", preview=True,\n'
        '            preview_src="assets/video.mp4")'
        "</code></pre>"
        f'<img src="{LIGHTBOX_POSTER}" height="100" '
        f'data-preview-video="{LIGHTBOX_VIDEO}">'
        "</div>"
        "</div>"
    )

    fit_text = Slide()
    fit_text.add(
        "<p>Use <code>FitText</code> to auto-size text: "
        '<code>slide.element(FitText("FIT TEXT"))</code></p>'
    )
    fit_text.element(FitText("FIT TEXT"))

    # ── Fragments (vertical) ─────────────────────────────────────────────────
    fragments = Slide(slide_id="fragments")
    fragments.heading("Fragments")
    fragments.text("Hit the next arrow...")
    fragments.fragment("... to step through ...")
    fragments.add(
        '<p><span class="fragment">... a</span> '
        '<span class="fragment">fragmented</span> '
        '<span class="fragment">slide.</span></p>'
    )
    fragments.note(
        "This slide has fragments which are also stepped through in the notes window."
    )

    fragment_styles = Slide()
    fragment_styles.heading("Fragment Styles")
    fragment_styles.text("There's different types of fragments, like:")
    fragment_styles.fragment("grow", effect=FragmentEffect.GROW)
    fragment_styles.fragment("shrink", effect=FragmentEffect.SHRINK)
    fragment_styles.fragment("fade-out", effect=FragmentEffect.FADE_OUT)
    fragment_styles.add(
        '<p>'
        '<span style="display: inline-block" class="fragment fade-right">fade-right, </span>'
        '<span style="display: inline-block" class="fragment fade-up">up, </span>'
        '<span style="display: inline-block" class="fragment fade-down">down, </span>'
        '<span style="display: inline-block" class="fragment fade-left">left</span>'
        "</p>"
    )
    fragment_styles.fragment("fade-in-then-out", effect=FragmentEffect.FADE_IN_THEN_OUT)
    fragment_styles.fragment(
        "fade-in-then-semi-out", effect=FragmentEffect.FADE_IN_THEN_SEMI_OUT
    )
    fragment_styles.add(
        "<p>Highlight "
        '<span class="fragment highlight-red">red</span> '
        '<span class="fragment highlight-blue">blue</span> '
        '<span class="fragment highlight-green">green</span>'
        "</p>"
    )

    fragments_section = Slide.section(fragments, fragment_styles)

    # ── Transitions & themes ─────────────────────────────────────────────────
    transitions = Slide(slide_id="transitions")
    transitions.heading("Transition Styles")
    transitions.add(
        "<p>You can select from different transitions, like: <br />"
        '<a href="?transition=none#/transitions">None</a> - '
        '<a href="?transition=fade#/transitions">Fade</a> - '
        '<a href="?transition=slide#/transitions">Slide</a> - '
        '<a href="?transition=convex#/transitions">Convex</a> - '
        '<a href="?transition=concave#/transitions">Concave</a> - '
        '<a href="?transition=zoom#/transitions">Zoom</a>'
        "</p>"
    )

    themes = Slide(slide_id="themes")
    themes.heading("Themes")
    themes.add(
        "<p>PyReveal comes with a few themes built in: <br />"
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/black.css'); return false;\">Black (default)</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/white.css'); return false;\">White</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/league.css'); return false;\">League</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/sky.css'); return false;\">Sky</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/beige.css'); return false;\">Beige</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/simple.css'); return false;\">Simple</a>"
        "<br />"
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/serif.css'); return false;\">Serif</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/blood.css'); return false;\">Blood</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/night.css'); return false;\">Night</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/moon.css'); return false;\">Moon</a> - "
        f'<a href="#/themes" onclick="{_THEME_LINK}.setAttribute(\'href\','
        f"'revealjs/dist/theme/solarized.css'); return false;\">Solarized</a>"
        "</p>"
    )

    # ── Backgrounds (vertical) ───────────────────────────────────────────────
    _code_on_light = (
        "background: rgba(255, 255, 255, 0.92); color: #1a1a1a; padding: 0.75em; "
        "border-radius: 4px; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);"
    )
    _code_on_light_inner = "color: #1a1a1a; background: transparent;"

    bg_color = Slide()
    bg_color.bg("#dddddd")
    bg_color.heading("Slide Backgrounds")
    bg_color.add(
        '<p style="color: #1a1a1a;">Call <code style="color: #1a1a1a; '
        'background: rgba(255, 255, 255, 0.7);">slide.bg()</code> to change the '
        "background color. All CSS color formats are supported.</p>"
    )
    bg_color.add(
        f'<pre style="{_code_on_light}"><code class="hljs python" '
        f'style="{_code_on_light_inner}">slide.bg("#dddddd")'
        "</code></pre>"
    )
    bg_color.add("<br />", _arrow("#", navigate_down=True))

    bg_gradient = Slide()
    bg_gradient.bg(
        gradient="linear-gradient(to bottom, #283b95, #17b2c3)",
        type=BackgroundType.GRADIENT,
    )
    bg_gradient.heading("Gradient Backgrounds")
    bg_gradient.add(
        '<pre><code class="hljs python wrap">slide.bg(\n'
        '\tgradient="linear-gradient(to bottom, #ddd, #191919)"\n'
        ")</code></pre>"
    )

    bg_image = Slide()
    bg_image.bg(IMAGE_PLACEHOLDER)
    bg_image.heading("Image Backgrounds")
    bg_image.add(
        '<pre><code class="hljs python">slide.bg("image.png")</code></pre>'
    )

    bg_tiled = Slide()
    bg_tiled.bg(IMAGE_PLACEHOLDER, repeat="repeat", size="100px")
    bg_tiled.heading("Tiled Backgrounds")
    bg_tiled.add(
        '<pre><code class="hljs python" style="word-wrap: break-word;">'
        'slide.bg("image.png", repeat="repeat", size="100px")</code></pre>'
    )

    _code_on_dark = "color: #fff; background: transparent; word-wrap: break-word;"

    bg_video = Slide()
    bg_video.bg(type=BackgroundType.VIDEO, video=BG_VIDEO, color="#000000")
    bg_video.add(
        '<div style="background-color: rgba(0, 0, 0, 0.9); color: #fff; padding: 20px">'
        '<h2 style="color: #fff;">Video Backgrounds</h2>'
        '<pre style="background: transparent; color: #fff; margin: 0;">'
        f'<code class="hljs python" style="{_code_on_dark}">'
        'slide.bg(type=BackgroundType.VIDEO,\n'
        '         video="assets/clip.mp4", color="#000")</code></pre>'
        "</div>"
    )

    bg_gif = Slide()
    bg_gif.bg(GIF_BG)
    bg_gif.heading("... and GIFs!")

    backgrounds = Slide.section(
        bg_color, bg_gradient, bg_image, bg_tiled, bg_video, bg_gif
    )

    # ── Background transitions ─────────────────────────────────────────────────
    bg_trans1 = Slide(transition=Transition.SLIDE)
    bg_trans1.bg("#4d7e65", transition="zoom")
    bg_trans1.heading("Background Transitions")
    bg_trans1.text(
        "Different background transitions are available via the backgroundTransition "
        'option. This one\'s called "zoom".'
    )
    bg_trans1.add(
        '<pre><code class="hljs python">'
        'deck.configure(backgroundTransition="zoom")</code></pre>'
    )

    bg_trans2 = Slide(transition=Transition.SLIDE)
    bg_trans2.bg("#b5533c", transition="zoom")
    bg_trans2.heading("Background Transitions")
    bg_trans2.text("You can override background transitions per-slide.")
    bg_trans2.add(
        '<pre><code class="hljs python" style="word-wrap: break-word;">'
        'slide.bg("#b5533c", transition="zoom")</code></pre>'
    )

    # ── Iframe background ────────────────────────────────────────────────────
    iframe_bg = Slide()
    iframe_bg.bg(type=BackgroundType.IFRAME, iframe="https://techbend.dev", interactive=True)
    iframe_bg.add(
        '<div style="'
        "position: absolute; width: 40%; right: 0; "
        "box-shadow: 0 1px 4px rgba(0, 0, 0, 0.5), 0 5px 25px rgba(0, 0, 0, 0.2); "
        "background-color: rgba(0, 0, 0, 0.9); color: #fff; padding: 20px; "
        'font-size: 20px; text-align: left;">'
        "<h2>Iframe Backgrounds</h2>"
        "<p>Since PyReveal exports to the web, you can easily embed other web content. "
        "Try interacting with the page in the background.</p>"
        "</div>"
    )

    # ── Lists, table, quotes ─────────────────────────────────────────────────
    ul_slide = Slide.make_bullets(
        ["No order here", "Or here", "Or here", "Or here"],
        title="Marvelous List",
    )

    ol_slide = Slide.make_bullets(
        ["One is smaller than...", "Two is smaller than...", "Three!"],
        title="Fantastic Ordered List",
        ordered=True,
    )

    table = Slide()
    table.heading("Tabular Tables")
    table.add(
        "<table><thead><tr>"
        "<th>Item</th><th>Value</th><th>Quantity</th>"
        "</tr></thead><tbody>"
        "<tr><td>Apples</td><td>$1</td><td>7</td></tr>"
        "<tr><td>Lemonade</td><td>$2</td><td>18</td></tr>"
        "<tr><td>Bread</td><td>$3</td><td>2</td></tr>"
        "</tbody></table>"
    )

    quotes = Slide()
    quotes.heading("Clever Quotes")
    quotes.add(
        "<p>These guys come in two forms, inline: "
        '<q cite="http://searchservervirtualization.techtarget.com/'
        'definition/Our-Favorite-Technology-Quotations">'
        "The nice thing about standards is that there are so many to choose from</q> "
        "and block:</p>"
        '<blockquote cite="http://searchservervirtualization.techtarget.com/'
        'definition/Our-Favorite-Technology-Quotations">'
        "&ldquo;For years there has been a theory that millions of monkeys typing at "
        "random on millions of typewriters would reproduce the entire works of "
        "Shakespeare. The Internet has proven this theory to be untrue.&rdquo;"
        "</blockquote>"
    )

    links = Slide.make_heading("Intergalactic Interconnections")
    links.add(
        '<p>You can link between slides internally, '
        '<a href="#/basement-2">like this</a>.</p>'
    )

    # ── Speaker view, PDF, state ───────────────────────────────────────────────
    speaker = Slide.make_heading("Speaker View")
    speaker.add(
        f"<p>There's a <a href=\"{DOCS_URL}/user-guide/plugins/\">speaker view</a>. "
        "It includes a timer, preview of the upcoming slide as well as your speaker notes."
        "</p>"
    )
    speaker.add("<p>Press the <em>S</em> key to try it out.</p>")
    speaker.note(
        "Oh hey, these are some notes. They'll be hidden in your presentation, but you "
        "can see them if you open the speaker notes window (hit 's' on your keyboard)."
    )

    pdf = Slide.make_heading("Export to PDF")
    pdf.add(
        f"<p>Presentations can be <a href=\"{DOCS_URL}/user-guide/pdf-export/\">exported "
        "to PDF</a>, here's an example:</p>"
    )
    pdf.add(
        '<iframe data-src="https://www.slideshare.net/slideshow/embed_code/42840540" '
        'width="445" height="355" frameborder="0" marginwidth="0" marginheight="0" '
        'scrolling="no" style="border: 3px solid #666; margin-bottom: 5px; max-width: 100%" '
        "allowfullscreen></iframe>"
    )

    global_state = Slide.make_heading("Global State")
    global_state.add(
        "<p>Set <code>state=\"something\"</code> on a <code>Slide</code> and "
        '<code>"something"</code> will be added as a class to the document element '
        "when the slide is open. This lets you apply broader style changes, like "
        "switching the page background.</p>"
    )

    state_events = Slide(state="customevent")
    state_events.heading("State Events")
    state_events.add(
        "<p>In Python, attach a state name when building the slide. PyReveal exports "
        "slides that fire a matching event in the browser when opened.</p>"
    )
    state_events.add(
        '<pre><code class="hljs python" data-trim style="font-size: 18px;">'
        'slide = Slide(state="customevent")\n'
        'slide.heading("State Events")\n'
        "</code></pre>"
    )

    pause = Slide.make_heading("Take a Moment")
    pause.text(
        "Press B or . on your keyboard to pause the presentation. This is helpful when "
        "you're on stage and want to take distracting slides off the screen."
    )

    end = Slide(attributes={"style": "text-align: left"})
    end.add(
        "<h1>THE END</h1>"
        f"{_hero_buttons_html()}"
        "<p>"
        f'<a href="{GITHUB_URL}">'
        "Source code on GitHub</a>"
        "</p>"
    )

    deck = Presentation(
        "PyReveal",
        theme=Theme.BLACK,
        transition=Transition.SLIDE,
    )

    deck.add(
        title,
        hello,
        vertical,
        hidden,
        pretty_code,
        animated_code,
        overview,
        animate_intro,
        animate_colors,
        animate_stack,
        touch,
        markdown,
        lightbox,
        fit_text,
        fragments_section,
        transitions,
        themes,
        backgrounds,
        bg_trans1,
        bg_trans2,
        iframe_bg,
        ul_slide,
        ol_slide,
        table,
        quotes,
        links,
        speaker,
        pdf,
        global_state,
        state_events,
        pause,
        end,
    )

    (
        deck.configure(center=True, backgroundTransition="zoom")
        .navigation(hash=True, controls=True, progress=True)
        .css(_HOME_HERO_CSS)
        .extra_head(_THREE_IMPORTMAP)
        .script("assets/home-hero.mjs")
        .plugins(
            Plugin.ZOOM,
            Plugin.NOTES,
            Plugin.SEARCH,
            Plugin.MARKDOWN,
            Plugin.HIGHLIGHT,
        )
    )

    return deck


def _write_index(target_html: Path) -> None:
    index = target_html.parent / "index.html"
    index.write_text(
        "<!DOCTYPE html><html><head>"
        '<meta charset="utf-8">'
        '<meta http-equiv="refresh" content="0;url=demo.html">'
        "</head><body>"
        '<p><a href="demo.html">Open PyReveal demo</a></p>'
        "</body></html>",
        encoding="utf-8",
    )


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = output("demo.html")
    build().save(path, pdf_hint=True)
    _write_index(path)

    print()
    copy_assets(path.parent)

    print("Serve locally (Three.js mesh + remote assets need HTTP):")
    print(f"  cd {path.parent.resolve()}")
    print("  python3 -m http.server 8765")
    print("  open http://localhost:8765/demo.html")