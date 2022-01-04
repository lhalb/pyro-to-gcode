# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class ValueTooSmallError(Error):
    """Raised when the input value is way too small"""
    pass


class ValueNearlyTooLargeError(Error):
    """Raised, when the input is critical"""
    pass


class ValueTooLargeError(Error):
    """Raised when the input value is probably too large"""
    pass