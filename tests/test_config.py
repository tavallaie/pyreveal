from pyreveal.config import build_initialize_options, serialize_initialize_options


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