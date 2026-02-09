def static_fallback(verdict: dict) -> str:
    return (
        "⚠️ This response was withheld due to reliability concerns.\n\n"
        "The system detected potential hallucination or missing grounding.\n"
        "Please consult a verified source or rephrase your query."
    )
