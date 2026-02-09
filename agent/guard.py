# agent/guard.py

from agent.context import AgentContext


class AgentGuard:
    def check(self, ctx: AgentContext) -> dict:
        if ctx.is_exhausted():
            ctx.blocked = True
            ctx.block_reason = "agent_step_exhaustion"
            return {
                "blocked": True,
                "reason": ctx.block_reason
            }

        return {"blocked": False}
