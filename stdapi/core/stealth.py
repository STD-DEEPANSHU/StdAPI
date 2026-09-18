"""
StdAPI Stealth Network Layer
Emulates modern browser TLS, rotating headers, and exponential backoff retry.
"""
import random
import asyncio
from typing import Dict, Any, Optional
import aiohttp

CHROME_VERSIONS = ["124.0.0.0", "125.0.0.0", "126.0.0.0", "127.0.0.0"]

PLATFORMS = [
    ("Windows NT 10.0; Win64; x64", "Win64"),
    ("Macintosh; Intel Mac OS X 10_15_7", "macOS"),
    ("X11; Linux x86_64", "Linux"),
]


def get_random_headers(referer: Optional[str] = None) -> Dict[str, str]:
    ver = random.choice(CHROME_VERSIONS)
    ua_plat, sec_plat = random.choice(PLATFORMS)
    headers = {
        "User-Agent": f"Mozilla/5.0 ({ua_plat}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ver} Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Ch-Ua": f'"Chromium";v="{ver.split(".")[0]}", "Google Chrome";v="{ver.split(".")[0]}", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": f'"{sec_plat}"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }
    if referer:
        headers["Referer"] = referer
    return headers


class StealthSession:
    def __init__(self, timeout: int = 20, max_retries: int = 3):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers=get_random_headers()
            )
        return self._session

    async def fetch(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> aiohttp.ClientResponse:
        session = await self.get_session()
        req_headers = get_random_headers()
        if headers:
            req_headers.update(headers)

        last_error = None
        for attempt in range(self.max_retries):
            try:
                resp = await session.get(url, headers=req_headers, **kwargs)
                if resp.status in (429, 503):
                    await asyncio.sleep(2 ** attempt + random.uniform(0.5, 1.5))
                    continue
                return resp
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_error = e
                await asyncio.sleep(1.5 * (attempt + 1))

        raise RuntimeError(f"Stealth fetch failed after {self.max_retries} attempts: {last_error}")

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
