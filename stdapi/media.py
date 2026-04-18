import os
import requests
from typing import Optional

from .client import client, StdAPIError


def download(
    url: str,
    format: str = "mp4",
    output: Optional[str] = None,
) -> str:

    if format not in ("mp4", "mp3"):
        raise ValueError("format must be 'mp4' or 'mp3'")

    try:
        r = client.post(
            "/media/download",
            json={"url": url, "format": format},
            stream=True,
        )

        # ✅ Validate content type
        content_type = r.headers.get("content-type", "")
        if "application/json" in content_type:
            raise StdAPIError("API returned JSON instead of media file")

        # ✅ Safe filename
        if not output:
            cd = r.headers.get("content-disposition", "")
            if "filename=" in cd:
                filename = cd.split("filename=")[-1].strip('"')
                output = os.path.basename(filename)
            else:
                output = f"stdapi_download.{format}"

        # ✅ Write file
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
