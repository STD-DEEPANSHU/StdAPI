from typing import Optional
from io import BytesIO
from .client import StdAPIClient
from .results import Result

class MediaModule:
    def __init__(self, client: StdAPIClient):
        self.client = client

    async def info(self, url: str) -> Result:
        """Extract metadata (title, thumbnail, duration, uploader) from media URL."""
        return await self.client._request("GET", "/media/info", params={"url": url})

    async def download(self, url: str, format: str = "mp4") -> Result:
        """Get direct high-speed download link for video (mp4) or audio (mp3)."""
        if format not in ("mp4", "mp3"):
            raise ValueError("format must be 'mp4' or 'mp3'")
        return await self.client._request("GET", "/media/download", params={"url": url, "format_type": format})

    async def get_buffer(self, url: str, format: str = "mp4") -> BytesIO:
        """
        Download media directly into an in-memory BytesIO buffer (Zero disk I/O).
        Perfect for Telegram/Discord bot replies.
        """
        data = await self.download(url, format)
        download_url = data.download_url
        session = await self.client.get_session()
        async with session.get(download_url) as resp:
            content = await resp.read()
            buf = BytesIO(content)
            buf.name = f"media_{data.get('title', 'file')[:20]}.{format}"
            return buf
