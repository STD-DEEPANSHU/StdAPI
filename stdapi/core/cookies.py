"""
StdAPI Browser Cookie Harvester
Extracts cookies directly from local browser profiles (Chrome, Edge, Firefox, Brave)
to bypass YouTube bot detection and Instagram login walls automatically.
"""
import os
import sys
import sqlite3
import shutil
import tempfile
from typing import Dict, Optional
from pathlib import Path


class BrowserCookieExtractor:
    @staticmethod
    def get_chrome_cookie_path() -> Optional[Path]:
        if sys.platform == "win32":
            local_appdata = os.getenv("LOCALAPPDATA", "")
            return Path(local_appdata) / "Google" / "Chrome" / "User Data" / "Default" / "Network" / "Cookies"
        elif sys.platform == "darwin":
            return Path.home() / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Cookies"
        else:
            return Path.home() / ".config" / "google-chrome" / "Default" / "Cookies"

    @staticmethod
    def get_edge_cookie_path() -> Optional[Path]:
        if sys.platform == "win32":
            local_appdata = os.getenv("LOCALAPPDATA", "")
            return Path(local_appdata) / "Microsoft" / "Edge" / "User Data" / "Default" / "Network" / "Cookies"
        return None

    @classmethod
    def extract_domain_cookies(cls, domain: str) -> Dict[str, str]:
        """
        Safely copies browser cookie DB to temp file and extracts unencrypted/available cookies for a domain.
        """
        cookies: Dict[str, str] = {}
        target_path = cls.get_chrome_cookie_path() or cls.get_edge_cookie_path()
        if not target_path or not target_path.exists():
            return cookies

        temp_db = Path(tempfile.gettempdir()) / f"std_cookies_{os.getpid()}.sqlite"
        try:
            shutil.copy2(target_path, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, value FROM cookies WHERE host_key LIKE ?",
                (f"%{domain}%",)
            )
            for name, val in cursor.fetchall():
                if val:
                    cookies[name] = val
            conn.close()
        except Exception:
            pass
        finally:
            if temp_db.exists():
                try:
                    temp_db.unlink()
                except Exception:
                    pass

        return cookies
