# signals/missing_grounding.py

class MissingGroundingSignal:
    name = "missing_grounding"

    def extract(self, prompt: str, response: str, metadata: dict):
        if not response or not isinstance(response, str):
            return {
                "signal": self.name,
                "value": False,
                "confidence": 0.0,
                "explanation": "No response available to check grounding"
            }

        grounding_terms = ["source", "document", "retrieved", "context", "according to"]
        grounded = any(t in response.lower() for t in grounding_terms)

        return {
            "signal": self.name,
            "value": not grounded,
            "confidence": 0.6 if not grounded else 0.3,
            "explanation": (
                "Response lacks grounding indicators"
                if not grounded else
                "Response contains grounding indicators"
            )
        }
