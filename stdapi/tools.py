from typing import Optional
from .client import StdAPIClient
from .results import Result

class ToolsModule:
    def __init__(self, client: StdAPIClient):
        self.client = client

    async def qr(self, text: str) -> Result:
        """Generate a QR code image URL for any text or link."""
        return await self.client._request("GET", "/tools/qr", params={"text": text})

    async def shorten(self, url: str) -> Result:
        """Shorten long URLs into clean tiny links."""
        return await self.client._request("GET", "/tools/shorten", params={"url": url})

    async def ip(self, ip_address: Optional[str] = None) -> Result:
        """Lookup IP geolocation and details."""
        params = {"ip": ip_address} if ip_address else {}
        return await self.client._request("GET", "/tools/ip", params=params)

    async def lyrics(self, song: str) -> Result:
        """Find song lyrics and cover art."""
        return await self.client._request("GET", "/tools/lyrics", params={"song": song})
