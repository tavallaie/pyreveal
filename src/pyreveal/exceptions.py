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