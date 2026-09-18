import re
import yt_dlp
from .base import BaseExtractor, MediaResponse, StreamInfo

class InstagramExtractor(BaseExtractor):
    NAME = "Instagram"
    VALID_URL = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel|tv)\/([A-Za-z0-9_-]+)"

    async def extract(self, url: str) -> MediaResponse:
        match = re.search(self.VALID_URL, url)
        post_id = match.group(1) if match else "unknown"

        opts = {
            "quiet": True,
            "no_warnings": True,
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if "entries" in info and info["entries"]:
                info = info["entries"][0]

            streams = []
            formats = info.get("formats", [])
            for f in formats:
                if f.get("url"):
                    streams.append(StreamInfo(
                        url=f["url"],
                        format="mp4" if f.get("ext") == "mp4" else f.get("ext", "mp4"),
                        quality=f.get("format_note") or f"{f.get('height', 'HD')}p",
                        filesize=f.get("filesize"),
                        has_audio=f.get("acodec") != "none",
                        has_video=f.get("vcodec") != "none",
                    ))

            if not streams and info.get("url"):
                streams.append(StreamInfo(url=info["url"], format="mp4"))

            return MediaResponse(
                extractor=self.NAME,
                id=post_id,
                title=info.get("title") or f"Instagram Post by @{info.get('uploader', 'user')}",
                url=url,
                duration=info.get("duration"),
                thumbnail=info.get("thumbnail"),
                author=info.get("uploader") or info.get("channel"),
                streams=streams,
                description=info.get("description")
            )
