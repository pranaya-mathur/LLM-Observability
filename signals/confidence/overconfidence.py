# signals/overconfidence.py

class OverconfidenceSignal:
    name = "overconfidence"

    def extract(self, prompt: str, response: str, metadata: dict):
        if not response or not isinstance(response, str):
            return {
                "signal": self.name,
                "value": False,
                "confidence": 0.0,
                "explanation": "No response available to assess confidence"
            }

        absolute_terms = ["always", "definitely", "guaranteed", "never"]
        overconfident = any(t in response.lower() for t in absolute_terms)

        return {
            "signal": self.name,
            "value": overconfident,
            "confidence": 0.7 if overconfident else 0.3,
            "explanation": (
                "Response shows absolute certainty without qualifiers"
                if overconfident else
                "Response includes uncertainty or hedging"
            )
        }
