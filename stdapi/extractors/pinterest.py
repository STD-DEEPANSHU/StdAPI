import re
import yt_dlp
from .base import BaseExtractor, MediaResponse, StreamInfo

class PinterestExtractor(BaseExtractor):
    NAME = "Pinterest"
    VALID_URL = r"(?:https?:\/\/)?(?:www\.|pin\.)?pinterest\.(?:com|it|ca|co\.uk)\/pin\/.*"

    async def extract(self, url: str) -> MediaResponse:
        opts = {"quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            streams = [
                StreamInfo(url=f["url"], format=f.get("ext", "mp4"))
                for f in info.get("formats", []) if f.get("url")
            ]
            if not streams and info.get("url"):
                streams.append(StreamInfo(url=info["url"], format="mp4"))

            return MediaResponse(
                extractor=self.NAME,
                id=str(info.get("id", "pin")),
                title=info.get("title") or "Pinterest Pin",
                url=url,
                thumbnail=info.get("thumbnail"),
                author=info.get("uploader"),
                streams=streams
            )
