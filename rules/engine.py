# rules/engine.py

from rules.semantic_rules import (
    HighRiskSemanticHallucinationRule,
    FabricatedConceptRule
)
from rules.llm_rules import HighConfidenceDomainMismatchRule


ALL_RULES = [
    FabricatedConceptRule(),                 # highest severity first
    HighRiskSemanticHallucinationRule(),
    HighConfidenceDomainMismatchRule()
]


def _normalize_signals(signals_list):
    """
    Convert list of signal dicts to dict keyed by signal name
    """
    normalized = {}
    for s in signals_list:
        name = s.get("signal")
        if name:
            normalized[name] = s
    return normalized


def evaluate_rules(signals):
    """
    signals: list[dict]  ← from run_signals
    """
    verdicts = []

    signals_dict = _normalize_signals(signals)

    for rule in ALL_RULES:
        verdict = rule.evaluate(signals_dict)
        if verdict:
            verdicts.append(verdict)

    return verdicts
