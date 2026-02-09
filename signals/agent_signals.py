def agent_step_exhaustion(ctx):
    return {
        "signal": "agent_step_exhaustion",
        "value": ctx["agent_step"] > ctx["agent_max_steps"],
        "confidence": 1.0,
        "explanation": "Agent exceeded maximum allowed steps"
    }
