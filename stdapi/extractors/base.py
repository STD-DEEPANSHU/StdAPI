"""
StdAPI Extractor Plugin Base (yt-dlp pattern)
Every platform inherits from BaseExtractor for standardized schema and error recovery.
"""
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class StreamInfo:
    url: str
    format: str  # "mp4", "mp3", "m4a", "webm"
    quality: Optional[str] = None  # "1080p", "720p", "320kbps"
    filesize: Optional[int] = None
    has_audio: bool = True
    has_video: bool = True


@dataclass
class MediaResponse:
    extractor: str
    id: str
    title: str
    url: str
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    author: Optional[str] = None
    streams: List[StreamInfo] = field(default_factory=list)
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def best_video_url(self) -> Optional[str]:
        for s in reversed(self.streams):
            if s.has_video and s.has_audio:
                return s.url
        return self.streams[0].url if self.streams else None

    @property
    def best_audio_url(self) -> Optional[str]:
        for s in self.streams:
            if s.format in ("mp3", "m4a") or (s.has_audio and not s.has_video):
                return s.url
        return self.best_video_url


class BaseExtractor(ABC):
    NAME: str = "Generic"
    VALID_URL: str = r""

    @classmethod
    def matches(cls, url: str) -> bool:
        return bool(re.search(cls.VALID_URL, url, re.IGNORECASE))

    @abstractmethod
    async def extract(self, url: str) -> MediaResponse:
        """Extract media streams and metadata from the given URL."""
        pass
