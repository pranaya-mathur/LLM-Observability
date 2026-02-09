from abc import ABC, abstractmethod
from typing import List, Dict
from rules.verdicts import RuleVerdict


class BaseRule(ABC):
    name: str

    @abstractmethod
    def evaluate(self, signals: List[Dict]) -> RuleVerdict | None:
        """
        Return RuleVerdict if rule fires, else None
        """
        pass
