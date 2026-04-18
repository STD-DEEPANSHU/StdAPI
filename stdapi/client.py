import os
import requests
from typing import Any, Dict, Optional
from .exceptions import StdAPIError


class StdAPIClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 15,
    ):
        self.base_url = (
            base_url
            or os.getenv("STDAPI_BASE_URL")
            or "https://api.stdapi.dev"
        ).rstrip("/")

        self.timeout = timeout

        self.headers = {
            "User-Agent": "StdDownloader/1.0",
            "Accept": "application/json",
        }

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            r = requests.get(
                f"{self.base_url}{path}",
                params=params,
                timeout=self.timeout,
                headers=self.headers,
            )

            if not r.ok:
                raise StdAPIError(
                    f"GET {path} failed | Status: {r.status_code} | Response: {r.text}"
                )

            return r.json()

        except ValueError:
            raise StdAPIError("Invalid JSON response from API")

        except requests.exceptions.RequestException as e:
            raise StdAPIError(f"Connection error: {str(e)}") from e

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ):
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
                    f"POST {path} failed | Status: {r.status_code} | Response: {r.text}"
                )

            return r.json() if not stream else r

        except ValueError:
            raise StdAPIError("Invalid JSON response from API")

        except requests.exceptions.RequestException as e:
            raise StdAPIError(f"Connection error: {str(e)}") from e


client = StdAPIClient()
