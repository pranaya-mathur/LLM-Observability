# enforcement/actions.py
from enum import Enum

class EnforcementAction(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    FALLBACK = "fallback"
    BLOCK = "block"
