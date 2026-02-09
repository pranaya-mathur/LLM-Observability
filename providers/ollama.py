import httpx

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    async def generate(self, model, prompt, stream=False):
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": stream
                }
            )
        r.raise_for_status()
        return r.json()["response"]
