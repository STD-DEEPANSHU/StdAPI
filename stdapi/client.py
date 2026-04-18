import os
import requests
from typing import Any, Dict, Optional
from .exceptions import StdAPIError


class StdAPIClient:
    def __init__(self, base_url: Optional[str] = None, timeout: int = 15):
        self.base_url = (
            base_url
            or os.getenv("STDAPI_BASE_URL")
            or "https://stdapi-bef2d35099cb.herokuapp.com"  # ✅ production default
        ).rstrip("/")

        self.timeout = timeout

        self.session = requests.Session()  # ✅ performance boost

        self.headers = {
            "User-Agent": "StdAPI/1.0",
            "Accept": "application/json",
        }

    def _handle_response(self, r, path: str):
        if not r.ok:
            raise StdAPIError(
                f"{r.request.method} {path} failed",
                status_code=r.status_code,
                response=r.text,
            )

        try:
            return r.json()
        except ValueError:
            raise StdAPIError("Invalid JSON response")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        try:
            r = self.session.get(
                f"{self.base_url}{path}",
                params=params,
                timeout=self.timeout,
                headers=self.headers,
            )
            return self._handle_response(r, path)

        except requests.exceptions.RequestException as e:
            raise StdAPIError(f"Connection error: {e}") from e

    def post(self, path: str, json=None, stream=False):
        try:
            r = self.session.post(
                f"{self.base_url}{path}",
                json=json,
                timeout=self.timeout,
                headers=self.headers,
                stream=stream,
            )

            if stream:
                if not r.ok:
                    raise StdAPIError(
                        f"POST {path} failed",
                        status_code=r.status_code,
                        response=r.text,
                    )
                return r

            return self._handle_response(r, path)

        except requests.exceptions.RequestException as e:
            raise StdAPIError(f"Connection error: {e}") from e


client = StdAPIClient()
