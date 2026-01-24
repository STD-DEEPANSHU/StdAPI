import os
import requests
from typing import Any, Dict, Optional


class STDAPIError(Exception):
    """Base exception for STDAPI SDK"""
    pass


class STDAPIClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 15,
    ):
        self.base_url = (
            base_url
            or os.getenv("STDAPI_BASE_URL")
            or "https://indiayzapi-e741f7bb1deb.herokuapp.com"
        ).rstrip("/")
        self.timeout = timeout

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            r = requests.get(
                f"{self.base_url}{path}",
                params=params,
                timeout=self.timeout,
            )
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            raise STDAPIError(
                "Failed to connect to STD API"
            ) from e


client = StdAPIClient()
