import re
import yt_dlp
from .base import BaseExtractor, MediaResponse, StreamInfo

class TikTokExtractor(BaseExtractor):
    NAME = "TikTok"
    VALID_URL = r"(?:https?:\/\/)?(?:www\.|vt\.|vm\.)?tiktok\.com\/.*"

    async def extract(self, url: str) -> MediaResponse:
        opts = {
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            streams = []
            for f in info.get("formats", []):
                if f.get("url"):
                    streams.append(StreamInfo(
                        url=f["url"],
                        format=f.get("ext", "mp4"),
                        quality=f.get("format_note") or "HD No Watermark",
                        filesize=f.get("filesize"),
                        has_audio=True,
                        has_video=True,
                    ))

            return MediaResponse(
                extractor=self.NAME,
                id=str(info.get("id", "unknown")),
                title=info.get("title") or "TikTok Video",
                url=url,
                duration=info.get("duration"),
                thumbnail=info.get("thumbnail"),
                author=info.get("uploader"),
                streams=streams
            )
