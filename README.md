# ⚡ StdAPI

<p align="center">
  <strong>The Unified Developer & Bot Engine</strong><br>
  <em>Asynchronous Python SDK & CLI for Media, AI, Search, and Automation.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/stdapi/"><img src="https://img.shields.io/pypi/v/stdapi?style=for-the-badge&color=blue" alt="PyPI"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdAPI/stargazers"><img src="https://img.shields.io/github/stars/STD-DEEPANSHU/StdAPI?style=for-the-badge&color=gold" alt="Stars"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdAPI/network/members"><img src="https://img.shields.io/github/forks/STD-DEEPANSHU/StdAPI?style=for-the-badge&color=orange" alt="Forks"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdAPI/blob/main/LICENSE"><img src="https://img.shields.io/github/license/STD-DEEPANSHU/StdAPI?style=for-the-badge&color=green" alt="License"></a>
</p>

---

## 🚀 Why StdAPI?

Building Telegram bots, automation scripts, or microservices usually means juggling 10 different libraries and APIs. 

**StdAPI gives you everything under one standard, asynchronous interface:**
- 🎬 **Media Downloader:** YouTube, Instagram Reels, TikTok, Twitter/X, Pinterest, Facebook.
- 🤖 **AI Chat:** Free multi-model intelligence (`gpt-4o-mini`, `gemini`, `deepseek`).
- 🔍 **Knowledge & Search:** Instant web search and Wikipedia extracts.
- 🛠 **Developer Tools:** Lyrics finder, QR generator, URL shortener, IP info.
- ⚡ **Bot-Ready:** Auto in-memory buffers (`BytesIO`) for zero-disk Telegram (Pyrogram/Telethon) and Discord uploads.

---

## 📦 Installation

```bash
pip install -U stdapi
```

---

## ⚡ 10-Second Quickstart

```python
import asyncio
from stdapi import StdAPI

async def main():
    async with StdAPI() as api:
        # 1. Download Instagram Reel or YouTube Video
        media = await api.media.download("https://www.instagram.com/reel/Cxxxxxx/", format="mp4")
        print(f"Title: {media.title}")
        print(f"Direct Stream: {media.download_url}")

        # 2. Free AI Chat
        ai_res = await api.ai.chat("Explain recursion in 2 sentences")
        print(f"AI: {ai_res.response}")

        # 3. Wikipedia Summary
        wiki = await api.search.wiki("Artificial Intelligence")
        print(f"Wiki: {wiki.extract}")

asyncio.run(main())
```

---

## 🤖 1-Minute Telegram Bot Recipe (Pyrogram)

Send downloaded videos or photos directly to users without saving files to disk:

```python
from pyrogram import Client, filters
from stdapi import StdAPI

bot = Client("std_bot", api_id=12345, api_hash="xyz", bot_token="TOKEN")
api = StdAPI()

@bot.on_message(filters.regex(r"https?://.*"))
async def handle_download(client, message):
    url = message.text
    status = await message.reply_text("⚡ Extracting media with StdAPI...")
    
    # Directly download into memory buffer
    video_buffer = await api.media.get_buffer(url, format="mp4")
    
    await message.reply_video(video_buffer, caption="Downloaded via @StdAPI")
    await status.delete()

bot.run()
```

---

## 💻 Terminal CLI Usage

StdAPI comes with a lightning-fast CLI out of the box:

```bash
# Extract media link
stdapi media "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Ask AI
stdapi ai "Write a python regex for email validation"

# Search Web & Wikipedia
stdapi search "Quantum Computing" --wiki

# Developer Tools
stdapi tools --lyrics "Shape of You"
stdapi tools --shorten "https://very-long-url.com/something"
```

---

## 📂 Modules & Methods

| Module | Method | Description |
| :--- | :--- | :--- |
| `api.media` | `info(url)` | Extract title, duration, author, thumbnail |
| `api.media` | `download(url, format="mp4")` | Get direct stream link (mp4 or mp3) |
| `api.media` | `get_buffer(url, format="mp4")` | Direct in-memory `BytesIO` for bots |
| `api.ai` | `chat(prompt, model="gpt-4o-mini")` | Multi-model chat completions |
| `api.search` | `web(query, limit=5)` | Instant web search results |
| `api.search` | `wiki(topic)` | Wikipedia summary and thumbnail |
| `api.tools` | `lyrics(song)` | Full song lyrics and cover art |
| `api.tools` | `qr(text)` | Generate QR code image URL |
| `api.tools` | `shorten(url)` | Shorten long URLs |
| `api.tools` | `ip(ip_address)` | IP Geolocation & ISP details |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to check [issues page](https://github.com/STD-DEEPANSHU/StdAPI/issues).

---

## 📝 License

Distributed under the Apache-2.0 License. See `LICENSE` for more information.

Built with ❤️ by [STD-DEEPANSHU](https://github.com/STD-DEEPANSHU).
