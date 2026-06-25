from __future__ import annotations

import re
from typing import Any

from .choices import (
    BackgroundSize,
    BackgroundType,
    SlideVisibility,
    Transition,
    coerce_background_size,
    coerce_background_type,
    coerce_fragment_effect,
    coerce_slide_visibility,
    coerce_transition,
)
from .background import (
    Background,
    ColorBackground,
    GradientBackground,
    IframeBackground,
    ImageBackground,
    VideoBackground,
)

_COLOR_RE = re.compile(
    r"^(#|rgb\(|rgba\(|hsl\(|hsla\(|[a-zA-Z]+$)"
)


def _looks_like_color(value: str) -> bool:
    return bool(_COLOR_RE.match(value.strip()))


def coerce_background(
    value: str | dict[str, Any] | Background | None = None,
    /,
    **kwargs: Any,
) -> Background:
    """Turn a plain string or dict into a :class:`Background`."""
    if isinstance(value, Background):
        return value

    spec: dict[str, Any] = dict(kwargs)
    if isinstance(value, dict):
        spec = {**value, **spec}
    elif isinstance(value, str):
        spec.setdefault("value", value)
    elif value is not None:
        raise TypeError(
            f"Expected str, dict, or Background, got {type(value).__name__}"
        )

    bg_type = spec.pop("type", None)
    raw = spec.pop("value", None)

    if bg_type is None:
        if "color" in spec:
            bg_type = "color"
        elif "gradient" in spec:
            bg_type = "gradient"
        elif "image" in spec:
            bg_type = "image"
        elif "video" in spec or "sources" in spec:
            bg_type = "video"
        elif "iframe" in spec:
            bg_type = "iframe"
        elif raw is not None:
            if _looks_like_color(raw):
                bg_type = "color"
            elif "gradient(" in raw:
                bg_type = "gradient"
            else:
                bg_type = "image"

    if bg_type is not None:
        bg_type = coerce_background_type(bg_type)

    if "size" in spec:
        spec["size"] = coerce_background_size(spec["size"])

    if bg_type == BackgroundType.COLOR.value:
        color = spec.pop("color", raw)
        return ColorBackground(color, **spec)
    if bg_type == BackgroundType.GRADIENT.value:
        gradient = spec.pop("gradient", raw)
        return GradientBackground(gradient, **spec)
    if bg_type == BackgroundType.IMAGE.value:
        image = spec.pop("image", raw)
        return ImageBackground(image, **spec)
    if bg_type == BackgroundType.VIDEO.value:
        video = spec.pop("video", raw)
        sources = spec.pop("sources", None)
        if sources is not None:
            return VideoBackground(sources=sources, **spec)
        return VideoBackground(video, **spec)
    if bg_type == BackgroundType.IFRAME.value:
        iframe = spec.pop("iframe", raw)
        return IframeBackground(iframe, **spec)

    raise ValueError(
        "Could not determine background type. Pass a color (#hex), image path, "
        "or a dict with type='color'|'image'|'gradient'|'video'|'iframe'."
    )


_SLIDE_FIELDS = frozenset({
    "content",
    "background",
    "slide_id",
    "transition",
    "state",
    "auto_slide",
    "auto_animate",
    "auto_animate_easing",
    "visibility",
    "notes",
    "markdown",
    "attributes",
})


def split_slide_kwargs(
    kwargs: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Split Slide constructor fields from fluent option kwargs."""
    ctor = {k: v for k, v in kwargs.items() if k in _SLIDE_FIELDS}
    options = {k: v for k, v in kwargs.items() if k not in _SLIDE_FIELDS}
    return ctor, options


def _coerce_fragment_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    if "effect" in kwargs:
        kwargs = {**kwargs, "effect": coerce_fragment_effect(kwargs["effect"])}
    return kwargs


def normalize_vertical_slides(
    slides: list[Any],
) -> list:
    from .slide import Slide

    normalized: list[Slide] = []
    for item in slides:
        if isinstance(item, Slide):
            normalized.append(item)
        elif isinstance(item, str):
            child = Slide()
            child.text(item)
            normalized.append(child)
        else:
            raise TypeError(
                "vertical slides must be Slide instances or plain text strings"
            )
    return normalized


def apply_slide_options(slide, **options: Any) -> None:
    """Apply fluent slide options from plain Python values."""
    opts = dict(options)

    bg = opts.pop("bg", None) or opts.pop("background", None)
    if bg is not None:
        slide.background = coerce_background(bg)

    note = opts.pop("note", None) or opts.pop("notes", None)
    if note is not None:
        slide.notes = note

    for fragment in opts.pop("fragments", ()) or ():
        if isinstance(fragment, str):
            slide.fragment(fragment)
        elif isinstance(fragment, tuple) and len(fragment) == 2:
            text, frag_kwargs = fragment
            slide.fragment(text, **_coerce_fragment_kwargs(frag_kwargs))
        elif isinstance(fragment, dict):
            data = dict(fragment)
            text = data.pop("text")
            slide.fragment(text, **_coerce_fragment_kwargs(data))
        else:
            raise TypeError(
                "fragments entries must be str, (str, dict), or dict with 'text'"
            )

    if "title" in opts:
        slide.title(opts.pop("title"))
    if "subtitle" in opts:
        slide.subtitle(opts.pop("subtitle"))
    if "heading" in opts:
        slide.heading(opts.pop("heading"))

    if "transition" in opts:
        slide.transition = coerce_transition(opts.pop("transition"))
    if "visibility" in opts:
        slide.visibility = coerce_slide_visibility(opts.pop("visibility"))

    for key in (
        "slide_id",
        "state",
        "auto_slide",
        "auto_animate",
        "auto_animate_easing",
        "markdown",
    ):
        if key in opts:
            setattr(slide, key, opts.pop(key))

    if opts:
        unknown = ", ".join(sorted(opts))
        raise TypeError(f"Unknown slide option(s): {unknown}")