from pyreveal.config import (
    build_initialize_options,
    plugin_initialize_list,
    plugin_script_tags,
    serialize_initialize_options,
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


def test_plugin_initialize_list():
    names = plugin_initialize_list(["notes", "zoom"])
    assert names == "RevealNotes, RevealZoom"


def test_plugin_initialize_list_math_engine():
    names = plugin_initialize_list(["math"], math_engine="mathjax4")
    assert names == "RevealMath.MathJax4"