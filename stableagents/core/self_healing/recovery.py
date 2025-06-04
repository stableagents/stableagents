"""
Recovery engine for self-healing capabilities.
"""
import os
import time
import json
import logging
import threading
import traceback
from typing import Dict, List, Any, Optional, Callable, Tuple
from .monitor import Issue
from .diagnosis import DiagnosisResult

class RecoveryAction:
    """Represents a potential recovery action for an issue."""
    
    def __init__(self, action_id: str, name: str, description: str, 
                 action_fn: Callable[[Issue, DiagnosisResult], bool],
                 risk_level: str = "medium"):
        self.action_id = action_id
        self.name = name
        self.description = description
        self.action_fn = action_fn  # Function that executes the recovery action
        self.risk_level = risk_level  # "low", "medium", "high"
        self.prerequisites: List[str] = []  # List of action IDs that must run first
        self.success_rate: float = 0.0  # Success rate based on history (0.0 to 1.0)
        self.attempt_count: int = 0
        self.success_count: int = 0
        
    def execute(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Execute the recovery action."""
        self.attempt_count += 1
        success = False
        
        try:
            success = self.action_fn(issue, diagnosis)
        except Exception:
            success = False
            
        if success:
            self.success_count += 1
            
        # Update success rate
        self.success_rate = self.success_count / self.attempt_count if self.attempt_count > 0 else 0.0
        
        return success
        
    def add_prerequisite(self, action_id: str):
        """Add a prerequisite action that must be completed before this one."""
        if action_id not in self.prerequisites:
            self.prerequisites.append(action_id)

class RecoveryPlan:
    """A plan for recovering from an issue."""
    
    def __init__(self, issue: Issue, diagnosis: DiagnosisResult):
        self.issue = issue
        self.diagnosis = diagnosis
        self.actions: List[RecoveryAction] = []
        self.executed_actions: List[Tuple[RecoveryAction, bool]] = []  # (action, success)
        self.created_time = time.time()
        self.completed = False
        self.success = False
        self.completed_time: Optional[float] = None
        self.notes: List[str] = []
        
    def add_action(self, action: RecoveryAction):
        """Add an action to the recovery plan."""
        self.actions.append(action)
        
    def add_note(self, note: str):
        """Add a note to the recovery plan."""
        self.notes.append(note)
        
    def execute(self) -> bool:
        """Execute all recovery actions in the plan."""
        if self.completed:
            return self.success
            
        # Track which actions have been executed
        executed_action_ids = {action.action_id for action, _ in self.executed_actions}
        
        # Loop until all actions are executed
        while len(self.executed_actions) < len(self.actions):
            # Find an action that can be executed (all prerequisites are met)
            next_action = None
            for action in self.actions:
                if action.action_id in executed_action_ids:
                    continue  # Already executed
                    
                # Check if all prerequisites are met
                prereqs_met = all(prereq in executed_action_ids for prereq in action.prerequisites)
                if prereqs_met:
                    next_action = action
                    break
                    
            if not next_action:
                # No actions can be executed - possible circular dependency
                self.add_note("Recovery plan has circular dependency or unmet prerequisites")
                self.completed = True
                self.success = False
                self.completed_time = time.time()
                return False
                
            # Execute the action
            success = next_action.execute(self.issue, self.diagnosis)
            self.executed_actions.append((next_action, success))
            executed_action_ids.add(next_action.action_id)
            
            # If a critical action fails, stop the plan
            if not success and next_action.risk_level == "high":
                self.add_note(f"Critical action {next_action.name} failed, stopping recovery plan")
                self.completed = True
                self.success = False
                self.completed_time = time.time()
                return False
                
        # All actions executed
        self.completed = True
        self.success = all(success for _, success in self.executed_actions)
        self.completed_time = time.time()
        return self.success
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary representation."""
        return {
            "issue_id": self.issue.id,
            "diagnosis_confidence": self.diagnosis.confidence,
            "actions": [
                {
                    "name": action.name,
                    "success": success,
                    "risk_level": action.risk_level
                }
                for action, success in self.executed_actions
            ],
            "created_time": self.created_time,
            "completed": self.completed,
            "success": self.success,
            "completed_time": self.completed_time,
            "notes": self.notes
        }

class RecoveryEngine:
    """
    Engine for executing recovery actions to resolve issues.
    """
    
    def __init__(self, agent=None, monitor=None, diagnosis_engine=None):
        self.logger = logging.getLogger(__name__)
        self.agent = agent  # Reference to StableAgents instance
        self.monitor = monitor  # Reference to SystemMonitor
        self.diagnosis_engine = diagnosis_engine  # Reference to DiagnosisEngine
        self.actions: Dict[str, RecoveryAction] = {}  # Available recovery actions
        self.recovery_plans: Dict[str, RecoveryPlan] = {}  # Plans by issue ID
        self.recovery_history: List[RecoveryPlan] = []  # History of executed plans
        self.auto_recovery_enabled = False
        self.recovery_thread = None
        self.recovery_active = False
        self.risk_threshold = "medium"  # Maximum risk level for automatic recovery
        
    def register_action(self, action: RecoveryAction):
        """Register a recovery action with the engine."""
        self.actions[action.action_id] = action
        
    def create_plan(self, issue: Issue, diagnosis: Optional[DiagnosisResult] = None) -> RecoveryPlan:
        """
        Create a recovery plan for an issue.
        
        Args:
            issue: The issue to recover from
            diagnosis: Optional diagnosis result for the issue
            
        Returns:
            A recovery plan with appropriate actions
        """
        # Get diagnosis if not provided
        if not diagnosis and self.diagnosis_engine:
            diagnosis = self.diagnosis_engine.diagnose(issue)
        elif not diagnosis:
            # Create a minimal diagnosis with no root causes
            from .diagnosis import DiagnosisResult
            diagnosis = DiagnosisResult(issue)
            diagnosis.add_resolution_suggestion("Restart affected component")
            
        # Create a new plan
        plan = RecoveryPlan(issue, diagnosis)
        
        # Add appropriate actions based on component, severity, and diagnosis
        component = issue.component
        severity = issue.severity
        
        # Example logic for choosing recovery actions
        if "memory" in component.lower():
            # For memory issues
            if "leak" in str(diagnosis.root_causes).lower():
                if "gc_collect" in self.actions:
                    plan.add_action(self.actions["gc_collect"])
                    
        if "provider" in component.lower() or "api" in component.lower():
            # For API provider issues
            if "retry_api_call" in self.actions:
                plan.add_action(self.actions["retry_api_call"])
                
            if severity == "high" and "reset_api_provider" in self.actions:
                plan.add_action(self.actions["reset_api_provider"])
                
        if "model" in component.lower() or "local" in component.lower():
            # For model issues
            if "reload_model" in self.actions:
                plan.add_action(self.actions["reload_model"])
                
            if severity == "high" and "switch_to_fallback_model" in self.actions:
                plan.add_action(self.actions["switch_to_fallback_model"])
                
        # For any component, restart is often a good fallback
        if "restart_component" in self.actions:
            if not plan.actions or severity in ["high", "critical"]:
                plan.add_action(self.actions["restart_component"])
                
        # Add generic recovery actions for any issue type
        if "log_diagnostics" in self.actions:
            plan.add_action(self.actions["log_diagnostics"])
            
        # Always try to verify recovery last
        if "verify_recovery" in self.actions:
            plan.add_action(self.actions["verify_recovery"])
            
        # Cache the plan
        self.recovery_plans[issue.id] = plan
        
        return plan
        
    def execute_plan(self, plan: RecoveryPlan) -> bool:
        """Execute a recovery plan."""
        self.logger.info(f"Executing recovery plan for issue {plan.issue.id}")
        
        success = plan.execute()
        
        if success:
            self.logger.info(f"Recovery plan for issue {plan.issue.id} completed successfully")
            
            # Mark the issue as resolved if we have a monitor
            if self.monitor:
                resolution = f"Automatic recovery completed at {time.time()}"
                self.monitor.resolve_issue(plan.issue.id, resolution)
        else:
            self.logger.warning(f"Recovery plan for issue {plan.issue.id} failed")
            
        # Add to history
        self.recovery_history.append(plan)
        
        return success
        
    def recover_from_issue(self, issue: Issue) -> bool:
        """Create and execute a recovery plan for an issue."""
        plan = self.create_plan(issue)
        return self.execute_plan(plan)
        
    def enable_auto_recovery(self, min_severity: str = "medium", risk_threshold: str = "medium"):
        """
        Enable automatic recovery for issues above the given severity.
        
        Args:
            min_severity: Minimum severity for automatic recovery ("low", "medium", "high", "critical")
            risk_threshold: Maximum risk level for automatic recovery ("low", "medium", "high")
        """
        if self.auto_recovery_enabled:
            return
            
        if not self.monitor:
            self.logger.error("Cannot enable auto-recovery without a SystemMonitor")
            return
            
        self.auto_recovery_enabled = True
        self.risk_threshold = risk_threshold
        
        # Register a callback for new issues
        self.monitor.register_callback("issue_detected", 
                                      lambda issue: self._handle_new_issue(issue, min_severity))
        
        # Start recovery thread
        self.recovery_active = True
        self.recovery_thread = threading.Thread(
            target=self._recovery_loop,
            daemon=True
        )
        self.recovery_thread.start()
        
        self.logger.info(f"Automatic recovery enabled for issues with min severity: {min_severity}")
        
    def disable_auto_recovery(self):
        """Disable automatic recovery."""
        self.auto_recovery_enabled = False
        self.recovery_active = False
        
        if self.recovery_thread:
            self.recovery_thread.join(timeout=2.0)
            self.recovery_thread = None
            
        self.logger.info("Automatic recovery disabled")
        
    def _handle_new_issue(self, issue: Issue, min_severity: str):
        """Handle a new issue for potential auto-recovery."""
        if not self.auto_recovery_enabled:
            return
            
        # Check severity threshold
        severity_levels = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        issue_level = severity_levels.get(issue.severity, 0)
        min_level = severity_levels.get(min_severity, 1)
        
        if issue_level < min_level:
            return  # Not severe enough
            
        # Queue for recovery
        self.logger.info(f"Auto-recovery queued for issue {issue.id}")
        
        # Create a plan but don't execute yet (will be done by recovery thread)
        self.create_plan(issue)
        
    def _recovery_loop(self):
        """Background thread for executing recovery plans."""
        while self.recovery_active:
            try:
                # Find issues that need recovery
                if self.monitor:
                    active_issues = self.monitor.get_active_issues()
                    
                    for issue in active_issues:
                        # Skip if we already have a completed plan for this issue
                        if (issue.id in self.recovery_plans and 
                            self.recovery_plans[issue.id].completed):
                            continue
                            
                        # Create a plan if needed
                        if issue.id not in self.recovery_plans:
                            self.create_plan(issue)
                            
                        # Execute the plan if it's not too risky
                        plan = self.recovery_plans[issue.id]
                        
                        # Check if plan has any high-risk actions
                        if self.risk_threshold != "high":
                            high_risk = any(a.risk_level == "high" for a in plan.actions)
                            if high_risk and self.risk_threshold == "low":
                                continue  # Skip high-risk plan
                                
                            medium_risk = any(a.risk_level == "medium" for a in plan.actions)
                            if medium_risk and self.risk_threshold == "low":
                                continue  # Skip medium-risk plan
                                
                        # Execute the plan
                        self.execute_plan(plan)
                
                # Sleep before checking again
                time.sleep(10)
            except Exception as e:
                self.logger.error(f"Error in recovery loop: {e}")
                traceback.print_exc()
                time.sleep(30)  # Longer delay after error
                
    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get statistics about recovery actions and success rates."""
        total_plans = len(self.recovery_history)
        successful_plans = sum(1 for plan in self.recovery_history if plan.success)
        success_rate = successful_plans / total_plans if total_plans > 0 else 0
        
        action_stats = {}
        for action_id, action in self.actions.items():
            action_stats[action_id] = {
                "name": action.name,
                "attempts": action.attempt_count,
                "successes": action.success_count,
                "success_rate": action.success_rate,
                "risk_level": action.risk_level
            }
            
        return {
            "total_plans": total_plans,
            "successful_plans": successful_plans,
            "success_rate": success_rate,
            "actions": action_stats,
            "auto_recovery_enabled": self.auto_recovery_enabled,
            "risk_threshold": self.risk_threshold
        } 