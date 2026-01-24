import requests
from typing import Optional

from .client import client
from .exceptions import StdAPIError


def download(
    url: str,
    format: str = "mp4",
    output: Optional[str] = None
) -> str:
    """
    Download media using StdAPI backend.

    Args:
        url (str): Media URL
        format (str): mp4 or mp3
        output (str, optional): Output filename

    Returns:
        str: Path to downloaded file
    """

    if format not in ("mp4", "mp3"):
        raise ValueError("format must be 'mp4' or 'mp3'")

    params = {
        "url": url,
        "format": format
    }

    download_url = f"{client.base_url}/media/download"

    try:
        with requests.get(
            download_url,
            params=params,
            stream=True,
            timeout=client.timeout
        ) as response:

            response.raise_for_status()

            # auto filename
            if not output:
                content_disposition = response.headers.get("content-disposition")
                if content_disposition and "filename=" in content_disposition:
                    output = content_disposition.split("filename=")[-1].strip('"')
                else:
                    output = f"stdapi_download.{format}"

            with open(output, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            return output

    except Exception as e:
        raise StdAPIError(f"Media download failed: {e}")
