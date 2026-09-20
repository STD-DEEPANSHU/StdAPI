"""
StdAPI 2.0 — Universal Industrial Engine & Developer Suite
"""
import asyncio
from typing import Optional
from .extractors.registry import find_extractor
from .core.stealth import StealthSession
from .core.ffmpeg import FFmpegPipeline
from .core.cookies import BrowserCookieExtractor
from .core.cache import MediaCache
from .extractors.base import MediaResponse, StreamInfo


class StdEngine:
    """
    High-level local embedded engine.
    Usage:
        import asyncio
        from stdapi import StdEngine

        async def main():
            engine = StdEngine()
            media = await engine.extract("https://www.instagram.com/reel/xyz")
            print(media.best_video_url)

        asyncio.run(main())
    """
    def __init__(self, use_cache: bool = True):
        self.cache = MediaCache() if use_cache else None

    async def extract(self, url: str) -> MediaResponse:
        if self.cache:
            cached = self.cache.get(url)
            if cached:
                # Return cached MediaResponse
                streams = [StreamInfo(**s) for s in cached.get("streams", [])]
                cached["streams"] = streams
                return MediaResponse(**cached)

        extractor = find_extractor(url)
        if not extractor:
            raise ValueError(f"Unsupported media URL: {url}")

        result = await extractor.extract(url)

        if self.cache:
            self.cache.set(url, result.to_dict())

        return result


# Core Remote SDK
from .client import StdAPIClient
from .media import MediaModule
from .tools import ToolsModule
from .ai import AIModule
from .results import Result
from .exceptions import StdAPIError, ConnectionError, RateLimitError

_default_client = StdAPIClient()
media = MediaModule(_default_client)
tools = ToolsModule(_default_client)
ai = AIModule(_default_client)

__all__ = [
    "StdEngine",
    "StdAPIClient",
    "MediaModule",
    "ToolsModule",
    "AIModule",
    "Result",
    "StdAPIError",
    "ConnectionError",
    "RateLimitError",
    "media",
    "tools",
    "ai",
    "find_extractor",
    "StealthSession",
    "FFmpegPipeline",
    "BrowserCookieExtractor",
    "MediaResponse",
    "StreamInfo",
]

