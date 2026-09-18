from io import BytesIO
from typing import Any, Dict

class Result(dict):
    """
    A smart dictionary that supports dot notation access (e.g. res.title)
    and helper conversions.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in list(self.items()):
            if isinstance(value, dict):
                self[key] = Result(value)
            elif isinstance(value, list):
                self[key] = [Result(v) if isinstance(v, dict) else v for v in value]

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'Result' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'Result' object has no attribute '{name}'")
