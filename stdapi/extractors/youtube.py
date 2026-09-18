import re
import yt_dlp
from .base import BaseExtractor, MediaResponse, StreamInfo

class YouTubeExtractor(BaseExtractor):
    NAME = "YouTube"
    VALID_URL = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"

    async def extract(self, url: str) -> MediaResponse:
        match = re.search(self.VALID_URL, url)
        video_id = match.group(1) if match else "unknown"

        opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            streams = []
            for f in info.get("formats", []):
                if f.get("url"):
                    streams.append(StreamInfo(
                        url=f["url"],
                        format=f.get("ext", "mp4"),
                        quality=f.get("resolution") or f"{f.get('height')}p",
                        filesize=f.get("filesize") or f.get("filesize_approx"),
                        has_audio=f.get("acodec") != "none",
                        has_video=f.get("vcodec") != "none",
                    ))

            return MediaResponse(
                extractor=self.NAME,
                id=video_id,
                title=info.get("title") or "YouTube Video",
                url=url,
                duration=info.get("duration"),
                thumbnail=info.get("thumbnail"),
                author=info.get("uploader"),
                streams=streams,
                description=(info.get("description") or "")[:300]
            )
