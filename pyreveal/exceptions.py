# exceptions.py


class InvalidThemeError(Exception):
    """Raised when an invalid theme is provided."""

    pass


class InvalidTransitionError(Exception):
    """Raised when an invalid transition type is provided."""

    pass


class EmptySlideContentError(Exception):
    """Raised when attempting to add a slide with empty content."""

    pass
