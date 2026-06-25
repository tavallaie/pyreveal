from pyreveal.config import (
    build_initialize_options,
    plugin_initialize_list,
    plugin_script_tags,
    serialize_initialize_options,
    sort_plugins,
)


def test_build_initialize_options_merges_transition():
    config = build_initialize_options("fade", {"hash": True})
    assert config == {"transition": "fade", "hash": True}


def test_build_initialize_options_user_overrides_transition():
    config = build_initialize_options("slide", {"transition": "zoom"})
    assert config["transition"] == "zoom"


def test_serialize_initialize_options_json():
    serialized = serialize_initialize_options({"hash": True, "progress": False})
    assert '"hash": true' in serialized
    assert '"progress": false' in serialized


def test_plugin_script_tags():
    tags = plugin_script_tags(["notes", "highlight"])
    assert "plugin/notes.js" in tags
    assert "plugin/highlight.js" in tags


def test_sort_plugins_puts_markdown_before_highlight():
    ordered = sort_plugins(["highlight", "markdown", "notes", "zoom"])
    assert ordered.index("markdown") < ordered.index("highlight")
    assert ordered[0] == "zoom"


def test_plugin_initialize_list():
    names = plugin_initialize_list(["notes", "zoom"])
    assert names == "RevealZoom, RevealNotes"


def test_plugin_initialize_list_math_engine():
    names = plugin_initialize_list(["math"], math_engine="mathjax4")
    assert names == "RevealMath.MathJax4"


def test_wrap_in_html_template_plugins_inside_initialize_object():
    from pyreveal import Plugin, Presentation, Slide

    html = (
        Presentation("T")
        .plugins(Plugin.NOTES, Plugin.HIGHLIGHT)
        .add(Slide.make_text("hi"))
        .html()
    )
    assert "},\n            plugins:" not in html
    assert "plugins: [RevealNotes, RevealHighlight]" in html
    assert "Reveal.initialize({" in html
    assert "});" in html