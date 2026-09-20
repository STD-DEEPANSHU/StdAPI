from typing import Optional
from .client import StdAPIClient
from .results import Result

class ToolsModule:
    def __init__(self, client: StdAPIClient):
        self.client = client

    async def qr(self, text: str, box_size: int = 10, border: int = 2) -> Result:
        """Generate a QR code image data URL for any text or link."""
        return await self.client._request("POST", "/v1/tools/qrcode", json={"text": text, "box_size": box_size, "border": border})

    async def temp_mail(self) -> Result:
        """Generate a random active disposable email address."""
        return await self.client._request("GET", "/v1/tools/temp-mail")

    async def temp_mail_inbox(self, login: str, domain: str) -> Result:
        """Fetch incoming emails & OTPs for a given temp mail mailbox."""
        return await self.client._request("GET", "/v1/tools/temp-mail/inbox", params={"login": login, "domain": domain})

    async def ip(self, ip_address: Optional[str] = None) -> Result:
        """Lookup IP geolocation and details."""
        params = {"ip": ip_address} if ip_address else {}
        return await self.client._request("GET", "/v1/tools/ip-lookup", params=params)

    async def shorten(self, url: str) -> Result:
        """Shorten long URLs into clean tiny links."""
        return await self.client._request("GET", "/tools/shorten", params={"url": url})

    async def lyrics(self, song: str) -> Result:
        """Find song lyrics and cover art."""
        return await self.client._request("GET", "/tools/lyrics", params={"song": song})
