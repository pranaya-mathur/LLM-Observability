# signals/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any


class SignalResult(dict):
    """
    {
      signal: str,
      value: bool | int | float | str,
      confidence: float,
      explanation: str
    }
    """


class BaseSignal(ABC):
    name: str

    @abstractmethod
    def extract(
        self,
        *,
        prompt: str,
        response: str,
        metadata: Dict[str, Any]
    ) -> SignalResult:
        pass
