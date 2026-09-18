"""
StdAPI Python SDK v1.0.1
Unified API client for Media, AI, Search, and Tools.
"""

from typing import Optional
import aiohttp
from .client import StdAPIClient
from .media import MediaModule
from .ai import AIModule
from .search import SearchModule
from .tools import ToolsModule
from .results import Result
from .exceptions import StdAPIError, ConnectionError, RateLimitError, MediaExtractionError

class StdAPI:
    """
    Main entry point for StdAPI.
    
    Usage:
        import asyncio
        from stdapi import StdAPI

        async def main():
            api = StdAPI()
            # Media
            media = await api.media.download("https://instagram.com/reel/...")
            print(media.download_url)

            # AI
            res = await api.ai.chat("Explain Python generators")
            print(res.response)

            # Search
            wiki = await api.search.wiki("Elon Musk")
            print(wiki.extract)

        asyncio.run(main())
    """
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 25,
        session: Optional[aiohttp.ClientSession] = None
    ):
        self.client = StdAPIClient(base_url=base_url, timeout=timeout, session=session)
        self.media = MediaModule(self.client)
        self.ai = AIModule(self.client)
        self.search = SearchModule(self.client)
        self.tools = ToolsModule(self.client)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()

    async def close(self):
        await self.client.close()


__all__ = [
    "StdAPI",
    "StdAPIClient",
    "Result",
    "StdAPIError",
    "ConnectionError",
    "RateLimitError",
    "MediaExtractionError",
]
