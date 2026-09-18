# ⚡ StdAPI 2.0 — The Industrial Media & Dev Engine

<p align="center">
  <strong>Universal Stealth Extractor • In-Process FFmpeg Pipeline • Model Context Protocol (MCP) Server</strong><br>
  <em>The developer tool engineered for daily automation, bot builders, and AI-driven workflows.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/stdapi/"><img src="https://img.shields.io/pypi/v/stdapi?style=for-the-badge&color=blue" alt="PyPI"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdAPI/stargazers"><img src="https://img.shields.io/github/stars/STD-DEEPANSHU/StdAPI?style=for-the-badge&color=gold" alt="Stars"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdAPI/network/members"><img src="https://img.shields.io/github/forks/STD-DEEPANSHU/StdAPI?style=for-the-badge&color=orange" alt="Forks"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdAPI/blob/main/LICENSE"><img src="https://img.shields.io/github/license/STD-DEEPANSHU/StdAPI?style=for-the-badge&color=green" alt="License"></a>
</p>

---

## ⚡ What Makes StdAPI 2.0 Different?

Unlike brittle API wrappers that break within days, **StdAPI is a self-contained, local-first engine**:

1. 🛡️ **Stealth Network Engine (`core.stealth`):** Real Chrome/Safari TLS/JA3 fingerprint emulation + automated local browser cookie harvesting (Chrome, Edge, Firefox) to bypass Cloudflare, YouTube bot blocks, and Instagram login walls.
2. 🎬 **Plugin Architecture (`extractors/`):** Clean, modular `yt-dlp` inspired plugins for Instagram Reels, YouTube, TikTok (No-Watermark), Twitter/X, and Pinterest.
3. 🎞️ **In-Process FFmpeg Pipeline (`core.ffmpeg`):** Lossless stream muxing (combines 1080p/4K video with audio), 320kbps MP3 transcoding, video trimming, and ID3 album art tagging.
4. 🤖 **Native Model Context Protocol (MCP):** Connects directly with **Claude Desktop**, **Cursor IDE**, and AI Coding Assistants.
5. 💻 **Interactive Hacker TUI:** Beautiful terminal dashboard powered by Rich.

---

## 📦 Installation

```bash
pip install -U stdapi
```

---

## 🚀 3-Line Python Quickstart

```python
import asyncio
from stdapi import StdEngine

async def main():
    engine = StdEngine()
    
    # Extract any video (Instagram, YouTube, TikTok, etc.)
    media = await engine.extract("https://www.instagram.com/reel/Cxxxxxx/")
    print(f"Title: {media.title}")
    print(f"Direct Stream: {media.best_video_url}")

asyncio.run(main())
```

---

## 🤖 Model Context Protocol (MCP) Setup for Claude / Cursor

StdAPI includes an open-standard MCP server. To give **Claude Desktop** or **Cursor** superpowers to download and process media autonomously, add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "stdapi": {
      "command": "stdapi",
      "args": ["mcp"]
    }
  }
}
```

---

## 💻 Terminal CLI & TUI

```bash
# Launch interactive diagnostics dashboard
stdapi tui

# Extract direct stream URL
stdapi extract "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Convert video to 320k MP3 using FFmpeg
stdapi convert input_video.mp4 output_song.mp3

# Start MCP stdio server
stdapi mcp
```

---

## 🏗️ Architecture

```
stdapi/
├── core/
│   ├── stealth.py      # TLS & browser fingerprint spoofing
│   ├── cookies.py      # Local browser cookie harvester
│   ├── ffmpeg.py       # Stream muxing & audio transcoding
│   └── cache.py        # SQLite persistent cache
├── extractors/
│   ├── base.py         # BaseExtractor dataclass & regex
│   ├── instagram.py    # Instagram Reels, Posts & Carousels
│   ├── youtube.py      # YouTube adaptive streams
│   ├── tiktok.py       # TikTok watermark-free streams
│   ├── twitter.py      # Twitter/X video extractor
│   └── pinterest.py    # Pinterest HD media
├── mcp/
│   └── server.py       # Model Context Protocol stdio server
└── ui/
    ├── tui.py          # Rich interactive dashboard
    └── cli.py          # Unified CLI interface
```

---

## 📄 License
Licensed under Apache-2.0. Developed by [STD-DEEPANSHU](https://github.com/STD-DEEPANSHU).
