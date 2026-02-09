# signals/domain/domain_mismatch.py

class DomainMismatchSignal:
    name = "domain_mismatch"

    def extract(self, prompt: str, response: str, metadata: dict):
        # 🔒 HARD GUARD
        if not response or not isinstance(response, str):
            return {
                "signal": self.name,
                "value": False,
                "confidence": 0.0,
                "explanation": "No response available for domain analysis"
            }

        response_l = response.lower()
        prompt_l = prompt.lower()

        biology_terms = ["mitochondria", "cell", "enzyme", "protein"]
        genai_terms = ["rag", "llm", "retrieval", "embedding", "vector"]

        biology_hits = any(t in response_l for t in biology_terms)
        genai_prompt = any(t in prompt_l for t in genai_terms)

        mismatch = biology_hits and genai_prompt

        return {
            "signal": self.name,
            "value": mismatch,
            "confidence": 0.9 if mismatch else 0.3,
            "explanation": (
                "Response belongs to biology domain while prompt context implies GenAI/RAG"
                if mismatch else
                "No strong domain conflict detected"
            )
        }
