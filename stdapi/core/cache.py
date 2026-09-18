"""
StdAPI Persistent SQLite Cache
Stores extracted media links and metadata with automatic TTL expiration.
"""
import time
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any

CACHE_DB_PATH = Path.home() / ".stdapi" / "cache.sqlite"


class MediaCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds
        CACHE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(CACHE_DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS media_cache (
                    url_hash TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    timestamp REAL NOT NULL
                )
            """)
            conn.commit()

    def get(self, url: str) -> Optional[Dict[str, Any]]:
        now = time.time()
        with sqlite3.connect(CACHE_DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT data, timestamp FROM media_cache WHERE url_hash = ?", (url,))
            row = cur.fetchone()
            if row:
                data_str, timestamp = row
                if now - timestamp < self.ttl:
                    return json.loads(data_str)
                else:
                    cur.execute("DELETE FROM media_cache WHERE url_hash = ?", (url,))
                    conn.commit()
        return None

    def set(self, url: str, data: Dict[str, Any]):
        now = time.time()
        with sqlite3.connect(CACHE_DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO media_cache (url_hash, data, timestamp) VALUES (?, ?, ?)",
                (url, json.dumps(data), now)
            )
            conn.commit()
