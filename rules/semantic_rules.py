# rules/semantic_rules.py

from rules.base import BaseRule
from rules.verdicts import RuleVerdict


class HighRiskSemanticHallucinationRule(BaseRule):
    name = "high_risk_semantic_hallucination"

    def evaluate(self, signals: dict):
        """
        signals: dict[str, signal_dict]
        """

        domain = signals.get("domain_mismatch")
        grounding = signals.get("missing_grounding")
        confidence = signals.get("overconfidence")

        if not domain or not grounding or not confidence:
            return None

        if (
            domain.get("value") is True
            and grounding.get("value") is True
            and confidence.get("value") is True
        ):
            return RuleVerdict(
                failure_type="semantic_hallucination",
                severity="high",
                recommended_action="block_or_fallback",
                triggered_by=[
                    "domain_mismatch",
                    "missing_grounding",
                    "overconfidence",
                ],
            )

        return None


class FabricatedConceptRule(BaseRule):
    name = "fabricated_concept"

    def evaluate(self, signals: dict):
        fabricated = signals.get("fabricated_concept")
        confidence = signals.get("overconfidence")

        if not fabricated or not confidence:
            return None

        if fabricated.get("value") and confidence.get("value"):
            return RuleVerdict(
                failure_type="concept_fabrication",
                severity="critical",
                recommended_action="hard_block",
                triggered_by=[
                    "fabricated_concept",
                    "overconfidence",
                ],
            )

        return None
