from .exceptions import (
    InvalidThemeError,
    InvalidTransitionError,
    EmptySlideContentError,
    SlideGroupNotFoundError,
    DuplicateSlideTitleError,
)


def validate_theme(theme):
    valid_themes = [
        "beige",
        "black",
        "black-contrast",
        "blood",
        "dracula",
        "league",
        "moon",
        "night",
        "serif",
        "simple",
        "sky",
        "solarized",
        "white",
        "white-contrast",
    ]
    if theme not in valid_themes:
        raise InvalidThemeError(
            f"'{theme}' is not a valid theme. Valid themes are: {', '.join(valid_themes)}"
        )


def validate_transition(transition):
    valid_transitions = ["none", "slide", "fade", "convex", "concave", "zoom"]
    if transition not in valid_transitions:
        raise InvalidTransitionError(
            f"'{transition}' is not a valid transition. Valid transitions are: {', '.join(valid_transitions)}"
        )


def validate_slide_content(content):
    if not content.strip():
        raise EmptySlideContentError("Slide content cannot be empty.")
