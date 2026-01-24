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
        """
        StdAPI client configuration

        Args:
            base_url (str, optional): Override API base URL
            timeout (int): Request timeout in seconds
        """

        self.base_url = (
            base_url
            or os.getenv("STDAPI_BASE_URL")
            or "https://stdapi-backend.herokuapp.com"
        ).rstrip("/")

        self.timeout = timeout

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}{path}",
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise StdAPIError("Failed to connect to StdAPI backend") from e

    def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}{path}",
                json=json,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise StdAPIError("Failed to connect to StdAPI backend") from e


client = StdAPIClient()
