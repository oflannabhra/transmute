"""Custom exceptions for transmute."""


class TransmuteError(Exception):
    """Base exception for transmute errors."""


class FormatNotFoundError(TransmuteError):
    """Raised when a format handler cannot be found."""


class ParseError(TransmuteError):
    """Raised when a CSV cannot be parsed."""


class CardNotFoundError(TransmuteError):
    """Raised when a card cannot be found via Scryfall."""


class ScryfallAPIError(TransmuteError):
    """Raised when Scryfall API returns an error."""


class RateLimitError(ScryfallAPIError):
    """Raised when Scryfall rate limit is exceeded."""
