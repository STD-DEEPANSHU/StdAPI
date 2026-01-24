import os
import requests
from typing import Any, Dict, Optional


class StdAPIError(Exception):
    """Base exception for StdAPI"""
    pass


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
            )
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            raise StdAPIError("Failed to connect to StdAPI backend") from e

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
                stream=stream,
            )
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            raise StdAPIError("Failed to connect to StdAPI backend") from e


client = StdAPIClient()
