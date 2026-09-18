from typing import Optional
from .client import StdAPIClient
from .results import Result

class AIModule:
    def __init__(self, client: StdAPIClient):
        self.client = client

    async def chat(
        self,
        prompt: str,
        model: str = "gpt-4o-mini",
        system_prompt: Optional[str] = None
    ) -> Result:
        """
        Query AI models (gpt-4o-mini, gpt-4o, gemini, deepseek).
        """
        payload = {"prompt": prompt, "model": model}
        if system_prompt:
            payload["system_prompt"] = system_prompt
        return await self.client._request("POST", "/ai/chat", json=payload)
