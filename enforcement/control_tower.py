"""Control Tower - Policy-driven enforcement engine.

Centralized decision system that maps detected failures to enforcement actions
based on configured policies. Replaces heuristic-based enforcement with
deterministic policy execution.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from config.policy_loader import get_policy_loader
from contracts.failure_classes import FailureClass
from contracts.severity_levels import SeverityLevel, EnforcementAction


@dataclass
class EnforcementDecision:
    """Decision made by control tower for enforcement."""
    
    action: EnforcementAction
    severity: SeverityLevel
    failure_class: str
    confidence: float
    reason: str
    message: str
    should_block: bool


class ControlTower:
    """Policy-driven enforcement decision engine.
    
    Makes deterministic enforcement decisions based on:
    1. Detected failure class
    2. Detection confidence
    3. Configured policy rules
    4. Severity thresholds
    """
    
    def __init__(self):
        """Initialize control tower with policy configuration."""
        self.policy = get_policy_loader()
    
    def evaluate(
        self, 
        signals: List[Dict[str, Any]]
    ) -> Optional[EnforcementDecision]:
        """Evaluate signals and make enforcement decision.
        
        Args:
            signals: List of signal dictionaries from detection layer
            
        Returns:
            EnforcementDecision if action needed, None if all clear
        """
        # Process signals by severity (critical first)
        decisions = []
        
        for signal in signals:
            decision = self._evaluate_signal(signal)
            if decision:
                decisions.append(decision)
        
        # Return highest severity decision
        if not decisions:
            return None
        
        # Sort by severity priority
        severity_order = [
            SeverityLevel.CRITICAL,
            SeverityLevel.HIGH,
            SeverityLevel.MEDIUM,
            SeverityLevel.LOW,
            SeverityLevel.INFO,
        ]
        
        decisions.sort(
            key=lambda d: severity_order.index(d.severity)
        )
        
        return decisions[0]  # Return most severe
    
    def _evaluate_signal(self, signal: Dict[str, Any]) -> Optional[EnforcementDecision]:
        """Evaluate a single signal against policy.
        
        Args:
            signal: Signal dictionary with detection results
            
        Returns:
            EnforcementDecision if action needed, None otherwise
        """
        signal_name = signal.get("signal")
        if not signal_name:
            return None
        
        # Check if signal indicates a failure
        is_failure = signal.get("value", False)
        if not is_failure:
            return None
        
        # Get confidence score
        confidence = signal.get("confidence", 0.0)
        
        # Check if confidence meets threshold for enforcement
        if not self.policy.should_enforce(signal_name, confidence):
            return None
        
        # Get policy-defined severity and action
        severity = self.policy.get_severity(signal_name)
        action = self.policy.get_action(signal_name)
        reason = self.policy.get_reason(signal_name)
        
        # Generate user-facing message
        message_template = self.policy.get_message_template(action)
        message = message_template.format(reason=reason)
        
        return EnforcementDecision(
            action=action,
            severity=severity,
            failure_class=signal_name,
            confidence=confidence,
            reason=reason,
            message=message,
            should_block=(action == EnforcementAction.BLOCK)
        )
    
    def enforce(
        self, 
        decision: Optional[EnforcementDecision],
        llm_response: str
    ) -> Dict[str, Any]:
        """Apply enforcement decision to LLM response.
        
        Args:
            decision: Enforcement decision from evaluate()
            llm_response: Original LLM response text
            
        Returns:
            Dictionary with action taken and final response
        """
        if decision is None:
            # No issues detected - allow response
            return {
                "action": EnforcementAction.ALLOW,
                "final_response": llm_response,
                "message": "",
                "blocked": False,
            }
        
        if decision.should_block:
            # Block response entirely
            return {
                "action": decision.action,
                "final_response": None,
                "message": decision.message,
                "blocked": True,
                "reason": decision.reason,
                "severity": decision.severity.value,
            }
        
        elif decision.action == EnforcementAction.WARN:
            # Return response with warning
            final_response = f"{decision.message}\n\n{llm_response}"
            return {
                "action": decision.action,
                "final_response": final_response,
                "message": decision.message,
                "blocked": False,
                "severity": decision.severity.value,
            }
        
        else:  # LOG or ALLOW
            # Pass through, log for monitoring
            return {
                "action": decision.action,
                "final_response": llm_response,
                "message": decision.message,
                "blocked": False,
                "severity": decision.severity.value,
            }
