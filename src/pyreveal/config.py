import json
from typing import Any


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