import os
from typing import Optional
from .client import client, StdAPIError


def info(url: str):
    return client.get("/media/info", params={"url": url})


def download_link(url: str, format: str = "mp4"):
    if format not in ("mp4", "mp3"):
        raise ValueError("format must be 'mp4' or 'mp3'")

    return client.get("/media/download", params={
        "url": url,
        "format": format
    })


def download_file(
    url: str,
    format: str = "mp4",
    output: Optional[str] = None
) -> str:
    try:
        data = download_link(url, format)
        download_url = data.get("download_url")

        if not download_url:
            raise StdAPIError("No download URL returned from API")

        import requests

        r = requests.get(download_url, stream=True, timeout=30)

        if not r.ok:
            raise StdAPIError(
                "Failed to fetch file",
                status_code=r.status_code,
                response=r.text
            )

        # ✅ safe filename
        if not output:
            output = f"stdapi_download.{format}"

        output = os.path.basename(output)

        # ✅ write file safely
        with open(output, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return output

    except requests.exceptions.RequestException as e:
        raise StdAPIError(f"Network error: {e}") from e

    except OSError as e:
        raise StdAPIError(f"File write error: {e}") from e

    except StdAPIError:
        raise

    except Exception as e:
        raise StdAPIError(f"Unexpected error: {e}") from e
