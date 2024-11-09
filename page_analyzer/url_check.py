import validators
from urllib.parse import urlparse

MAX_URL_LEN = 255
ERROR_INVALID_URL = "Некорректный URL"
ERROR_TOO_LONG_URL = "Слишком длинный URL"


class InvalidURLError(Exception):
    """Raised when the URL is invalid."""
    pass


class URLTooLongError(Exception):
    """Raised when the URL exceeds the maximum allowed length."""
    pass


def validate_url(url: str) -> None:
    """Validates URL correctness and length.

    Raises:
        InvalidURLError: If the URL is invalid.
        URLTooLongError: If the URL length exceeds the maximum allowed length.
    """
    if not validators.url(url):
        raise InvalidURLError(ERROR_INVALID_URL)
    elif len(url) > MAX_URL_LEN:
        raise URLTooLongError(ERROR_TOO_LONG_URL)


def normalize_url(url: str) -> str:
    """Converts URL to standard form."""
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
