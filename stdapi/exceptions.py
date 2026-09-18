class StdAPIError(Exception):
    """Base exception for all StdAPI errors."""
    pass

class ConnectionError(StdAPIError):
    """Raised when server connection fails or server is offline."""
    pass

class RateLimitError(StdAPIError):
    """Raised when rate limit is exceeded (HTTP 429)."""
    pass

class MediaExtractionError(StdAPIError):
    """Raised when media extraction fails."""
    pass
