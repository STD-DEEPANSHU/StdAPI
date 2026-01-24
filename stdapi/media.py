import requests
from typing import Optional

from .client import client, StdAPIError


def download(
    url: str,
    format: str = "mp4",
    output: Optional[str] = None,
) -> str:
    """
    Download media via StdAPI backend.

    Args:
        url (str): Media URL
        format (str): mp4 or mp3
        output (str, optional): Output filename

    Returns:
        str: Path to downloaded file
    """

    if format not in ("mp4", "mp3"):
        raise ValueError("format must be 'mp4' or 'mp3'")

    try:
        r = client.post(
            "/media/download",
            json={"url": url, "format": format},
            stream=True,
        )

        if not output:
            cd = r.headers.get("content-disposition")
            if cd and "filename=" in cd:
                output = cd.split("filename=")[-1].strip('"')
            else:
                output = f"stdapi_download.{format}"

        with open(output, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return output

    except Exception as e:
        raise StdAPIError(f"Media download failed: {e}")
