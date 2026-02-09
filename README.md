# LLM Observability - Control Tower Edition

## Overview

Production-grade LLM observability system with **policy-driven enforcement**. Detects hallucinations, missing grounding, and other LLM failures, then applies configurable policies for blocking or warning.

### Key Features

- 🎯 **Policy-Driven**: All enforcement decisions driven by YAML configuration
- 🚨 **Failure Detection**: Detects fabricated concepts, missing grounding, domain mismatches
- ⚖️ **Severity Mapping**: CRITICAL → BLOCK, HIGH → WARN, MEDIUM/LOW → LOG
- 🏗️ **Enterprise Architecture**: Separation of detection, policy, and enforcement
- 🔄 **Deterministic**: Same input = same output (no heuristics)

## Architecture

```
LLM Response → Signals → Control Tower → Policy Engine → Enforcement
                  ↓            ↓              ↓              ↓
              Detection    Evaluation    Severity       Action
                                        Mapping
```

### Control Tower vs Legacy Mode

| Aspect | Legacy (run_ollama.py) | Control Tower (run_control_tower.py) |
|--------|------------------------|---------------------------------------|
| Decision Logic | Hardcoded rules | YAML policy config |
| Severity | Heuristic-based | Policy-defined |
| Action | Verdict reduction | Direct from policy |
| Maintainability | Code changes needed | Config changes only |
| Auditability | Limited | Full policy trail |

## Prerequisites

- Python 3.10+
- Ollama running locally
  ```bash
  ollama run phi3
  ```

## Installation

```bash
# Clone repository
git clone https://github.com/pranaya-mathur/LLM-Observability.git
cd LLM-Observability

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Control Tower Mode (Recommended)

```bash
python -m examples.run_control_tower
```

**Sample Output:**
```
[POLICY DECISION]
  Failure Class: fabricated_concept
  Severity: CRITICAL
  Action: BLOCK
  Confidence: 0.80
  Reason: Hallucinated terms/concepts pose safety risk
  Block: True

❌ RESPONSE BLOCKED
Reason: Hallucinated terms/concepts pose safety risk
Severity: CRITICAL
```

### Legacy Mode

```bash
python -m examples.run_ollama
```

## Configuration

Edit `config/policy.yaml` to customize enforcement policies:

```yaml
failure_policies:
  fabricated_concept:
    severity: "critical"  # critical, high, medium, low
    action: "block"       # block, warn, log, allow
    reason: "Hallucinated terms/concepts pose safety risk"
  
  missing_grounding:
    severity: "high"
    action: "warn"
    reason: "Unverified claims require user awareness"
```

### Policy Modification

**No code changes needed!** Just edit YAML:

1. Change severity level → Changes enforcement action automatically
2. Modify thresholds → Adjusts confidence requirements
3. Add new failure classes → System picks them up immediately

## Project Structure

```
LLM-Observability/
├── config/
│   ├── policy.yaml          # 🎯 Policy configuration (EDIT THIS)
│   └── policy_loader.py     # YAML loader
├── contracts/
│   ├── failure_classes.py   # Failure taxonomy
│   └── severity_levels.py   # Severity & action enums
├── enforcement/
│   └── control_tower.py     # Policy-driven enforcement
├── signals/
│   └── runner.py            # Signal detection
├── examples/
│   ├── run_control_tower.py # 🆕 New policy-driven example
│   └── run_ollama.py        # Legacy example
└── core/
    └── interceptor.py       # LLM call interceptor
```

## Example Use Cases

### 1. Block Hallucinations

**Scenario**: LLM invents "RAG = Ruthenium-Arsenic Growth"

**Policy**:
```yaml
fabricated_concept:
  severity: "critical"
  action: "block"
```

**Result**: Response blocked entirely ❌

### 2. Warn on Missing Sources

**Scenario**: LLM makes claims without citations

**Policy**:
```yaml
missing_grounding:
  severity: "high"
  action: "warn"
```

**Result**: Response delivered with warning ⚠️

### 3. Log Tone Issues

**Scenario**: Response is too casual

**Policy**:
```yaml
tone_issue:
  severity: "low"
  action: "log"
```

**Result**: Response allowed, logged for analysis ℹ️

## Production Readiness

### ✅ What's Production-Ready

- Policy-driven architecture
- Type-safe enums and contracts
- Separation of concerns
- Configuration-based enforcement
- Deterministic decisions

### 🚧 What Needs Work

- [ ] Structured logging (replace print statements)
- [ ] Metrics collection and monitoring
- [ ] Database persistence for audit trail
- [ ] Advanced signal detection (current signals are basic)
- [ ] API wrapper for easy integration

## Contributing

To add new failure classes:

1. Add to `contracts/failure_classes.py`
2. Add signal detector in `signals/`
3. Configure policy in `config/policy.yaml`

No changes needed in enforcement logic!

## License

MIT License

## Acknowledgments

Built with production MLOps principles for enterprise LLM governance.
