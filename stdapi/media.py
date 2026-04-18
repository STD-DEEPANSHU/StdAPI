import os
from typing import Optional
from .client import client, StdAPIError


def info(url: str):
    return client.get("/media/info", params={"url": url})


def download_link(url: str, format: str = "mp4"):
    return client.get("/media/download", params={
        "url": url,
        "format": format
    })


def download_file(url: str, format: str = "mp4", output: Optional[str] = None):
    try:
        data = download_link(url, format)
        download_url = data.get("download_url")

        if not download_url:
            raise StdAPIError("No download URL returned")

        import requests

        r = requests.get(download_url, stream=True)

        if not output:
            output = f"stdapi_download.{format}"

        with open(output, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

        return output

    except Exception as e:
        raise StdAPIError(f"Download failed: {e}") from e
