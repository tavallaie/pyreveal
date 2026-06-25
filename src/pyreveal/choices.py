from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TypeVar

E = TypeVar("E", bound=Enum)


class Theme(str, Enum):
    BEIGE = "beige"
    BLACK = "black"
    BLACK_CONTRAST = "black-contrast"
    BLOOD = "blood"
    DRACULA = "dracula"
    LEAGUE = "league"
    MOON = "moon"
    NIGHT = "night"
    SERIF = "serif"
    SIMPLE = "simple"
    SKY = "sky"
    SOLARIZED = "solarized"
    WHITE = "white"
    WHITE_CONTRAST = "white-contrast"


class Transition(str, Enum):
    NONE = "none"
    SLIDE = "slide"
    FADE = "fade"
    CONVEX = "convex"
    CONCAVE = "concave"
    ZOOM = "zoom"


class Plugin(str, Enum):
    NOTES = "notes"
    HIGHLIGHT = "highlight"
    MARKDOWN = "markdown"
    MATH = "math"
    SEARCH = "search"
    ZOOM = "zoom"


class MathEngine(str, Enum):
    KATEX = "katex"
    MATHJAX2 = "mathjax2"
    MATHJAX3 = "mathjax3"
    MATHJAX4 = "mathjax4"


class BackgroundType(str, Enum):
    COLOR = "color"
    GRADIENT = "gradient"
    IMAGE = "image"
    VIDEO = "video"
    IFRAME = "iframe"


class BackgroundSize(str, Enum):
    COVER = "cover"
    CONTAIN = "contain"


class SlideVisibility(str, Enum):
    HIDDEN = "hidden"


class View(str, Enum):
    SLIDE = "slide"
    SCROLL = "scroll"
    PRINT = "print"


class SlideNumber(str, Enum):
    H_DOT_V = "h.v"
    H_SLASH_V = "h/v"
    C = "c"
    C_SLASH_T = "c/t"


class ScrollLayout(str, Enum):
    FULL = "full"
    COMPACT = "compact"


class ScrollSnap(str, Enum):
    PROXIMITY = "proximity"
    MANDATORY = "mandatory"


class KeyboardBinding(str, Enum):
    """Reveal.js API method names for custom keyboard shortcuts."""

    NEXT = "next"
    PREV = "prev"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    TOGGLE_PAUSE = "togglePause"
    TOGGLE_HELP = "toggleHelp"
    TOGGLE_OVERVIEW = "toggleOverview"
    TOGGLE_AUTO_SLIDE = "toggleAutoSlide"
    TOGGLE_JUMP_TO_SLIDE = "toggleJumpToSlide"
    PREV_FRAGMENT = "prevFragment"
    NEXT_FRAGMENT = "nextFragment"


@dataclass(frozen=True)
class CustomPlugin:
    """Third-party or custom reveal.js plugin script."""

    script: str
    init: str


class FragmentEffect(str, Enum):
    NONE = ""
    GROW = "grow"
    SHRINK = "shrink"
    FADE_OUT = "fade-out"
    FADE_RIGHT = "fade-right"
    FADE_UP = "fade-up"
    FADE_DOWN = "fade-down"
    FADE_LEFT = "fade-left"
    FADE_IN_THEN_OUT = "fade-in-then-out"
    FADE_IN_THEN_SEMI_OUT = "fade-in-then-semi-out"
    STRIKE = "strike"
    HIGHLIGHT_RED = "highlight-red"
    HIGHLIGHT_BLUE = "highlight-blue"
    HIGHLIGHT_GREEN = "highlight-green"
    HIGHLIGHT_CURRENT_RED = "highlight-current-red"
    HIGHLIGHT_CURRENT_BLUE = "highlight-current-blue"
    HIGHLIGHT_CURRENT_GREEN = "highlight-current-green"


def _format_choices(enum_cls: type[E]) -> str:
    return ", ".join(
        member.value or member.name.lower()
        for member in enum_cls
        if member.value != "" or member is getattr(enum_cls, "NONE", None)
    )


def coerce_choice(
    enum_cls: type[E],
    value: E | str | None,
    *,
    default: E | None = None,
    label: str | None = None,
) -> str:
    """Normalize an enum member or string to its reveal.js value."""
    name = label or enum_cls.__name__
    if value is None:
        if default is not None:
            return default.value
        raise TypeError(f"{name} is required")
    if isinstance(value, enum_cls):
        return value.value
    if isinstance(value, str):
        try:
            return enum_cls(value).value
        except ValueError:
            pass
        key = value.upper().replace("-", "_")
        if key in enum_cls.__members__:
            return enum_cls[key].value
        raise ValueError(
            f"Unknown {name} {value!r}. Choose from: {_format_choices(enum_cls)}"
        )
    raise TypeError(
        f"{name} must be {enum_cls.__name__} or str, got {type(value).__name__}"
    )


def coerce_theme(value: Theme | str) -> str:
    return coerce_choice(Theme, value)


def coerce_transition(value: Transition | str) -> str:
    return coerce_choice(Transition, value)


def coerce_plugin(value: Plugin | str) -> str:
    return coerce_choice(Plugin, value)


def coerce_math_engine(value: MathEngine | str) -> str:
    return coerce_choice(MathEngine, value)


def coerce_background_type(value: BackgroundType | str) -> str:
    return coerce_choice(BackgroundType, value)


def coerce_background_size(value: BackgroundSize | str) -> str:
    if isinstance(value, BackgroundSize):
        return value.value
    if value in {s.value for s in BackgroundSize}:
        return value
    return value


def coerce_slide_visibility(value: SlideVisibility | str) -> str:
    return coerce_choice(SlideVisibility, value)


def coerce_fragment_effect(effect: FragmentEffect | str | None = None) -> str:
    return coerce_choice(FragmentEffect, effect, default=FragmentEffect.NONE)


def coerce_view(value: View | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, View):
        return None if value is View.SLIDE else value.value
    if isinstance(value, str):
        try:
            return coerce_view(View(value))
        except ValueError:
            pass
        key = value.upper()
        if key in View.__members__:
            return coerce_view(View[key])
        raise ValueError(
            f"Unknown View {value!r}. Choose from: {_format_choices(View)}"
        )
    raise TypeError(f"View must be View or str, got {type(value).__name__}")


def coerce_keyboard_bindings(
    bindings: dict[int | str, KeyboardBinding | str | None],
) -> dict[int, str | None]:
    """Normalize a key-code map for reveal.js ``keyboard`` config."""
    result: dict[int, str | None] = {}
    for key, action in bindings.items():
        if isinstance(key, str):
            try:
                key_code = int(key)
            except ValueError as exc:
                raise ValueError(
                    f"Keyboard binding key must be a key code integer, got {key!r}"
                ) from exc
        elif isinstance(key, int):
            key_code = key
        else:
            raise TypeError(
                f"Keyboard binding keys must be int or str, got {type(key).__name__}"
            )

        if action is None:
            result[key_code] = None
        elif isinstance(action, KeyboardBinding):
            result[key_code] = action.value
        elif isinstance(action, str):
            try:
                result[key_code] = KeyboardBinding(action).value
            except ValueError as exc:
                valid = _format_choices(KeyboardBinding)
                raise ValueError(
                    f"Unknown keyboard action {action!r}. Choose from: {valid}"
                ) from exc
        else:
            raise TypeError(
                "Keyboard binding values must be KeyboardBinding, str, or None, "
                f"got {type(action).__name__}"
            )
    return result


def coerce_slide_number(value: bool | SlideNumber | str) -> bool | str:
    if isinstance(value, bool):
        return value
    if isinstance(value, SlideNumber):
        return value.value
    if isinstance(value, str):
        if value in {member.value for member in SlideNumber}:
            return value
        try:
            return SlideNumber(value).value
        except ValueError as exc:
            raise ValueError(
                f"Unknown SlideNumber {value!r}. "
                f"Choose from: {', '.join(member.value for member in SlideNumber)}"
            ) from exc
    raise TypeError(
        f"SlideNumber must be bool, SlideNumber, or str, got {type(value).__name__}"
    )