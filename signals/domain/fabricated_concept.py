# signals/fabricated_concept.py

class FabricatedConceptSignal:
    name = "fabricated_concept"

    def extract(self, prompt: str, response: str, metadata: dict):
        if not response or not isinstance(response, str):
            return {
                "signal": self.name,
                "value": False,
                "confidence": 0.0,
                "explanation": "No response available to check fabricated concepts"
            }

        if "(" in response and ")" in response:
            return {
                "signal": self.name,
                "value": True,
                "confidence": 0.8,
                "explanation": "Suspicious acronym expansion detected"
            }

        return {
            "signal": self.name,
            "value": False,
            "confidence": 0.2,
            "explanation": "No fabricated concept pattern detected"
        }
