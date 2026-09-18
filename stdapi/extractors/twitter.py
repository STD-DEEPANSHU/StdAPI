import re
import yt_dlp
from .base import BaseExtractor, MediaResponse, StreamInfo

class TwitterExtractor(BaseExtractor):
    NAME = "Twitter/X"
    VALID_URL = r"(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)\/[a-zA-Z0-9_]+\/status\/([0-9]+)"

    async def extract(self, url: str) -> MediaResponse:
        opts = {"quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            streams = [
                StreamInfo(url=f["url"], format=f.get("ext", "mp4"), quality=f.get("format_note"))
                for f in info.get("formats", []) if f.get("url")
            ]
            return MediaResponse(
                extractor=self.NAME,
                id=str(info.get("id", "tweet")),
                title=info.get("title") or f"Post by @{info.get('uploader', 'x')}",
                url=url,
                thumbnail=info.get("thumbnail"),
                author=info.get("uploader"),
                streams=streams
            )
