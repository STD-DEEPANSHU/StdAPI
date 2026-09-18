from .client import StdAPIClient
from .results import Result

class SearchModule:
    def __init__(self, client: StdAPIClient):
        self.client = client

    async def web(self, query: str, limit: int = 5) -> Result:
        """Search the web for queries and get instant snippets."""
        return await self.client._request("GET", "/search/web", params={"q": query, "limit": limit})

    async def wiki(self, topic: str, lang: str = "en") -> Result:
        """Get Wikipedia summary, thumbnail, and link."""
        return await self.client._request("GET", "/search/wiki", params={"q": topic, "lang": lang})
