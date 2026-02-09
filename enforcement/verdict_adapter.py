# enforcement/verdict_adapter.py
from enforcement.actions import EnforcementAction

class VerdictAdapter:

    SEVERITY_ACTION_MAP = {
        "low": EnforcementAction.WARN,
        "medium": EnforcementAction.FALLBACK,
        "high": EnforcementAction.BLOCK,
        "critical": EnforcementAction.BLOCK,
    }

    @classmethod
    def resolve_action(cls, rule_verdict):
        severity = getattr(rule_verdict, "severity", "low")
        return cls.SEVERITY_ACTION_MAP.get(
            severity,
            EnforcementAction.ALLOW
        )
