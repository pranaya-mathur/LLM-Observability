def agent_override_attempt(ctx):
    return (
        ctx.get("agent_action") == "continue"
        and ctx["verdict"].severity in ["high", "critical"]
    )


AGENT_RULES = [
    {
        "name": "agent_cannot_override_high_severity",
        "condition": agent_override_attempt,
        "action": "BLOCK"
    }
]
