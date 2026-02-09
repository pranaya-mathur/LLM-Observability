# rules/llm_rules.py

class HighConfidenceDomainMismatchRule:
    name = "semantic_hallucination_domain_mismatch"
    severity = "high"
    action = "BLOCK"

    def evaluate(self, signals):
        signal = signals.get("domain_mismatch")

        if (
            signal
            and signal["value"] is True
            and signal["confidence"] >= 0.8
        ):
            return {
                "rule": self.name,
                "severity": self.severity,
                "action": self.action,
                "explanation": "High confidence domain mismatch detected"
            }

        return None
