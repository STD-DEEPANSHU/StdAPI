import os
import requests
from typing import Any, Dict, Optional
from .exceptions import StdAPIError


class StdAPIClient:
    def __init__(self, base_url: Optional[str] = None, timeout: int = 15):
        self.base_url = (
            base_url
            or os.getenv("STDAPI_BASE_URL")
            or "http://localhost:8000"
        ).rstrip("/")

        self.timeout = timeout

        self.headers = {
            "User-Agent": "StdAPI/1.0",
            "Accept": "application/json",
        }

    def get(self, path: str, params: Optional[Dict[str, Any]] = None):
        try:
            r = requests.get(
                f"{self.base_url}{path}",
                params=params,
                timeout=self.timeout,
                headers=self.headers,
            )

            if not r.ok:
                raise StdAPIError(
                    "GET request failed",
                    status_code=r.status_code,
                    response=r.text,
                )

            return r.json()

        except ValueError:
            raise StdAPIError("Invalid JSON response")

        except requests.exceptions.RequestException as e:
            raise StdAPIError(f"Connection error: {e}") from e

    def post(self, path: str, json=None, stream=False):
        try:
            r = requests.post(
                f"{self.base_url}{path}",
                json=json,
                timeout=self.timeout,
                headers=self.headers,
                stream=stream,
            )

            if not r.ok:
                raise StdAPIError(
                    "POST request failed",
                    status_code=r.status_code,
                    response=r.text,
                )

            return r if stream else r.json()

        except requests.exceptions.RequestException as e:
            raise StdAPIError(f"Connection error: {e}") from e


client = StdAPIClient()
