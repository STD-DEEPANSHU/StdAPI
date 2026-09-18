import os
import aiohttp
import asyncio
from typing import Optional, Dict, Any
from .exceptions import StdAPIError, ConnectionError, RateLimitError
from .results import Result

DEFAULT_BASE_URL = "https://stdapi-bef2d35099cb.herokuapp.com"


class StdAPIClient:
    """
    Core Async Client for StdAPI.
    """
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 25,
        session: Optional[aiohttp.ClientSession] = None
    ):
        self.base_url = (
            base_url
            or os.getenv("STDAPI_BASE_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._custom_session = session
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get_session(self) -> aiohttp.ClientSession:
        if self._custom_session and not self._custom_session.closed:
            return self._custom_session
        if self._session is None or self._session.closed:
            headers = {
                "User-Agent": "StdAPI-Python-SDK/1.0.1",
                "Accept": "application/json"
            }
            self._session = aiohttp.ClientSession(headers=headers, timeout=self.timeout)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> Result:
        session = await self.get_session()
        url = f"{self.base_url}/{path.lstrip('/')}"

        try:
            async with session.request(method, url, params=params, json=json) as resp:
                if resp.status == 429:
                    raise RateLimitError("Rate limit reached on StdAPI server.")
                
                try:
                    data = await resp.json(content_type=None)
                except Exception:
                    text = await resp.text()
                    raise StdAPIError(f"Server returned non-JSON response ({resp.status}): {text[:150]}")

                if not resp.ok:
                    detail = data.get("detail") if isinstance(data, dict) else str(data)
                    raise StdAPIError(f"StdAPI Error [{resp.status}]: {detail}")

                return Result(data)

        except aiohttp.ClientConnectorError as e:
            raise ConnectionError(f"Could not connect to StdAPI server at {self.base_url}: {e}")
        except asyncio.TimeoutError:
            raise StdAPIError(f"Request timed out for endpoint {path}")
