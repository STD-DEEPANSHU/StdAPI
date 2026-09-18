"""
StdAPI In-Process FFmpeg Controller
High-speed stream muxing (merging video + audio), format transcoding,
MP3 320kbps conversion, and ID3 metadata tagging.
"""
import shutil
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class FFmpegPipeline:
    @staticmethod
    def is_available() -> bool:
        return shutil.which("ffmpeg") is not None

    @classmethod
    async def mux_streams(
        cls,
        video_path: str,
        audio_path: str,
        output_path: str
    ) -> bool:
        """
        Merge separated high-res video (1080p/4K) and audio stream into a single MP4 container.
        """
        if not cls.is_available():
            raise EnvironmentError("FFmpeg is not installed on the system PATH.")

        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-strict", "experimental",
            str(output_path)
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        await proc.communicate()
        return proc.returncode == 0

    @classmethod
    async def convert_to_audio(
        cls,
        input_file: str,
        output_file: str,
        bitrate: str = "320k",
        title: Optional[str] = None,
        artist: Optional[str] = None
    ) -> bool:
        """
        Convert any video/audio stream to high-bitrate MP3 with optional ID3 metadata.
        """
        if not cls.is_available():
            raise EnvironmentError("FFmpeg is not installed on the system PATH.")

        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_file),
            "-vn",
            "-b:a", bitrate,
        ]
        if title:
            cmd.extend(["-metadata", f"title={title}"])
        if artist:
            cmd.extend(["-metadata", f"artist={artist}"])

        cmd.append(str(output_file))

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        await proc.communicate()
        return proc.returncode == 0

    @classmethod
    async def trim_video(
        cls,
        input_file: str,
        output_file: str,
        start_seconds: int,
        duration_seconds: int
    ) -> bool:
        """
        Trim video without re-encoding (Lossless fast cut).
        """
        if not cls.is_available():
            raise EnvironmentError("FFmpeg is not installed on the system PATH.")

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_seconds),
            "-i", str(input_file),
            "-t", str(duration_seconds),
            "-c", "copy",
            str(output_file)
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        await proc.communicate()
        return proc.returncode == 0
