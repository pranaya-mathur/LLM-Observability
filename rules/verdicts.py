from dataclasses import dataclass
from typing import List


@dataclass
class RuleVerdict:
    failure_type: str
    severity: str
    recommended_action: str
    triggered_by: List[str]
