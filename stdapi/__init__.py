from .wikipedia import search as wikipedia_search
from .quote import random as random_quote
from .media import download as media_download

__all__ = [
    "wikipedia_search",
    "random_quote",
    "media_download",
]

__version__ = "0.1.0"
