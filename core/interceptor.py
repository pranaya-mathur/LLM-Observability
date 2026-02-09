# core/interceptor.py

import httpx
from signals.runner import run_signals
from rules.engine import evaluate_rules
from enforcement.verdict_adapter import VerdictAdapter
from enforcement.actions import EnforcementAction


class OllamaInterceptor:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    async def call(self, model: str, prompt: str):
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(180.0)) as client:
                response = await client.post(url, json=payload)

            if response.status_code != 200:
                print(f"[Interceptor] Ollama HTTP {response.status_code}")
                return None

            data = response.json()
            text = data.get("message", {}).get("content")

            if not text:
                print("[Interceptor] Empty response from LLM")
                return None

        except httpx.ReadTimeout:
            print("[Interceptor] LLM call timed out")
            return None

        except Exception as e:
            print(f"[Interceptor] LLM call failed: {e}")
            return None

        # ---------------- SAFETY PIPELINE ---------------- #

        signals = run_signals(
            prompt=prompt,
            response=text,
            metadata={}
        )

        verdicts = evaluate_rules(signals)

        for verdict in verdicts:
            action = VerdictAdapter.resolve_action(verdict)
            if action == EnforcementAction.BLOCK:
                 print(
                     f"[Interceptor] BLOCKED | "
                     f"[Interceptor] BLOCKED | "
                     f"severity={verdict.severity}"
                 )

            return None

        return text
