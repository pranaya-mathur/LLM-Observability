# rules/verdict_reducer.py

SEVERITY_ORDER = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}

def reduce_verdicts(verdicts):
    """
    Takes a list of RuleVerdict objects
    Returns the single most severe verdict
    """
    if not verdicts:
        return None

    return max(
        verdicts,
        key=lambda v: SEVERITY_ORDER.get(v.severity, 0)
    )
