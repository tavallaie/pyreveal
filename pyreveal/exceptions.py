# exceptions.py


class PyRevealException(Exception):
    """Base exception for the PyReveal library."""

    pass


class InvalidThemeError(PyRevealException):
    """Raised when an invalid theme is provided."""

    def __init__(self, theme, valid_themes):
        super().__init__(
            f"'{theme}' is not a valid theme. Valid themes are: {', '.join(valid_themes)}"
        )


class InvalidTransitionError(PyRevealException):
    """Raised when an invalid transition is provided."""

    def __init__(self, transition, valid_transitions):
        super().__init__(
            f"'{transition}' is not a valid transition. Valid transitions are: {', '.join(valid_transitions)}"
        )


class EmptySlideContentError(PyRevealException):
    """Raised when a slide with empty content is added."""

    def __init__(self):
        super().__init__("Slide content cannot be empty.")


class DuplicateSlideTitleError(PyRevealException):
    """Raised when a slide with a duplicate title is added."""

    def __init__(self, title):
        super().__init__(f"A slide with the title '{title}' already exists.")


class SlideGroupNotFoundError(PyRevealException):
    """Raised when a slide references a group that doesn't exist."""

    def __init__(self, group):
        super().__init__(f"No slide with the title '{group}' found for grouping.")


class InvalidBackgroundTypeError(PyRevealException):
    """Raised when an invalid background type is provided."""

    def __init__(self, bg_type):
        super().__init__(f"Unsupported background type: {bg_type}")


class InvalidElementError(PyRevealException):
    """Raised when an invalid element is provided or used."""

    def __init__(self, element):
        super().__init__(f"Invalid or unsupported element: {element}")


class InvalidCSSPropertyError(PyRevealException):
    """Raised when an invalid CSS property or value is used."""

    def __init__(self, property_name, value):
        super().__init__(f"Invalid value '{value}' for CSS property '{property_name}'.")


# You can continue to add more specific exceptions as needed.
