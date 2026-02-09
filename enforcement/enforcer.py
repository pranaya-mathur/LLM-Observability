# enforcement/enforcer.py
from enforcement.verdict_adapter import VerdictAdapter
from enforcement.actions import EnforcementAction

class ActionEnforcer:

    def enforce(self, rule_verdict, llm_response: str):
        action = VerdictAdapter.resolve_action(rule_verdict)

        if action == EnforcementAction.ALLOW:
            return {
                "action": "allow",
                "final_response": llm_response,
                "verdict": rule_verdict,
            }

        if action == EnforcementAction.WARN:
            return {
                "action": "warn",
                "final_response": (
                    "Warning: Response may be unreliable.\n\n"
                    + llm_response
                ),
                "verdict": rule_verdict,
            }

        if action == EnforcementAction.FALLBACK:
            return {
                "action": "fallback",
                "final_response": (
                    "Safe fallback activated due to reliability issues."
                ),
                "verdict": rule_verdict,
            }

        if action == EnforcementAction.BLOCK:
            return {
                "action": "block",
                "final_response": (
                    "Response blocked due to high-risk semantic hallucination."
                ),
                "verdict": rule_verdict,
            }

        return {
            "action": "allow",
            "final_response": llm_response,
            "verdict": rule_verdict,
        }
