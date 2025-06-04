"""
Self-healing controller that integrates monitoring, diagnosis, and recovery.
"""
import os
import json
import time
import logging
import threading
from typing import Dict, List, Any, Optional, Callable

from .monitor import SystemMonitor, Issue, HealthMetric
from .diagnosis import DiagnosisEngine, DiagnosisResult, DiagnosticRule
from .recovery import RecoveryEngine, RecoveryAction, RecoveryPlan

class SelfHealingController:
    """
    Central controller for self-healing capabilities.
    Integrates monitoring, diagnosis, and recovery components.
    """
    
    def __init__(self, agent=None):
        self.logger = logging.getLogger(__name__)
        self.agent = agent
        
        # Create component instances
        self.monitor = SystemMonitor()
        self.diagnosis_engine = DiagnosisEngine(agent=self.agent)
        self.recovery_engine = RecoveryEngine(
            agent=self.agent,
            monitor=self.monitor,
            diagnosis_engine=self.diagnosis_engine
        )
        
        # Configuration
        self.config: Dict[str, Any] = {
            "monitoring_interval": 10.0,  # seconds
            "auto_recovery": False,
            "min_severity_for_recovery": "high",
            "risk_threshold": "medium",
            "learning_enabled": True,
            "telemetry_enabled": False,
            "telemetry_path": None
        }
        
        # State tracking
        self.is_active = False
        self.learning_data: Dict[str, Any] = {
            "issue_patterns": {},
            "successful_recoveries": [],
            "failed_recoveries": []
        }
        
        # Initialize standard health check components
        self._initialize_standard_components()
        
    def _initialize_standard_components(self):
        """Initialize standard monitoring components and recovery actions."""
        # Register standard diagnostic rules
        self._register_standard_diagnostic_rules()
        
        # Register standard recovery actions
        self._register_standard_recovery_actions()
        
    def _register_standard_diagnostic_rules(self):
        """Register standard diagnostic rules."""
        # API Provider connectivity rule
        api_rule = DiagnosticRule(
            name="api_connectivity",
            component_patterns=["provider", "api"],
            condition_fn=lambda issue: "api" in issue.component.lower() or "provider" in issue.component.lower(),
            diagnose_fn=lambda issue: (
                ["API connectivity issue or invalid credentials"],
                0.7 if "api key" in issue.description.lower() or "connection" in issue.description.lower() else 0.3
            )
        )
        self.diagnosis_engine.register_rule(api_rule)
        
        # Local model rule
        model_rule = DiagnosticRule(
            name="local_model_issues",
            component_patterns=["model", "local"],
            condition_fn=lambda issue: "model" in issue.component.lower() or "local" in issue.component.lower(),
            diagnose_fn=lambda issue: (
                ["Local model file not found or inaccessible" if "not found" in issue.description.lower() 
                 else "Incompatible model format or corruption"],
                0.8 if "not found" in issue.description.lower() else 0.6
            )
        )
        self.diagnosis_engine.register_rule(model_rule)
        
        # Memory usage rule
        memory_rule = DiagnosticRule(
            name="memory_issues",
            component_patterns=["memory"],
            condition_fn=lambda issue: "memory" in issue.component.lower(),
            diagnose_fn=lambda issue: (
                ["Memory leak detected" if any(m.name == "growth_rate" and m.value > 0.1 for m in issue.metrics)
                 else "Memory usage exceeding threshold"],
                0.7
            )
        )
        self.diagnosis_engine.register_rule(memory_rule)
        
    def _register_standard_recovery_actions(self):
        """Register standard recovery actions."""
        # Logging diagnostics action
        self.recovery_engine.register_action(RecoveryAction(
            action_id="log_diagnostics",
            name="Log Diagnostics",
            description="Log detailed diagnostics about the issue",
            action_fn=self._action_log_diagnostics,
            risk_level="low"
        ))
        
        # Verify recovery action
        self.recovery_engine.register_action(RecoveryAction(
            action_id="verify_recovery",
            name="Verify Recovery",
            description="Verify that the issue has been resolved",
            action_fn=self._action_verify_recovery,
            risk_level="low"
        ))
        
        # Garbage collection action
        self.recovery_engine.register_action(RecoveryAction(
            action_id="gc_collect",
            name="Run Garbage Collection",
            description="Force Python garbage collection to free memory",
            action_fn=self._action_gc_collect,
            risk_level="low"
        ))
        
        # Retry API call action
        self.recovery_engine.register_action(RecoveryAction(
            action_id="retry_api_call",
            name="Retry API Call",
            description="Retry the failed API call with exponential backoff",
            action_fn=self._action_retry_api_call,
            risk_level="low"
        ))
        
        # Reset API provider action
        self.recovery_engine.register_action(RecoveryAction(
            action_id="reset_api_provider",
            name="Reset API Provider",
            description="Reset the API provider connection and configuration",
            action_fn=self._action_reset_api_provider,
            risk_level="medium"
        ))
        
        # Reload model action
        self.recovery_engine.register_action(RecoveryAction(
            action_id="reload_model",
            name="Reload Model",
            description="Reload the model from disk",
            action_fn=self._action_reload_model,
            risk_level="medium"
        ))
        
        # Switch to fallback model action
        self.recovery_engine.register_action(RecoveryAction(
            action_id="switch_to_fallback_model",
            name="Switch to Fallback Model",
            description="Switch to a fallback model when primary model fails",
            action_fn=self._action_switch_to_fallback_model,
            risk_level="medium"
        ))
        
        # Restart component action
        self.recovery_engine.register_action(RecoveryAction(
            action_id="restart_component",
            name="Restart Component",
            description="Restart the affected component",
            action_fn=self._action_restart_component,
            risk_level="high"
        ))
        
    # Recovery action implementations
    def _action_log_diagnostics(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Log detailed diagnostics about the issue."""
        try:
            self.logger.info(f"DIAGNOSTICS for issue {issue.id}:")
            self.logger.info(f"  Component: {issue.component}")
            self.logger.info(f"  Severity: {issue.severity}")
            self.logger.info(f"  Description: {issue.description}")
            self.logger.info(f"  Root causes: {diagnosis.root_causes}")
            self.logger.info(f"  Confidence: {diagnosis.confidence}")
            
            if issue.stack_trace:
                self.logger.info(f"  Stack trace: {issue.stack_trace[:500]}...")
                
            self.logger.info(f"  Metrics: {[(m.name, m.value) for m in issue.metrics]}")
            
            return True
        except Exception as e:
            self.logger.error(f"Error logging diagnostics: {e}")
            return False
            
    def _action_verify_recovery(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Verify that the issue has been resolved."""
        try:
            # Check if the issue still exists in active issues
            active_issues = self.monitor.get_active_issues()
            issue_ids = [i.id for i in active_issues]
            
            if issue.id not in issue_ids:
                self.logger.info(f"Issue {issue.id} appears to be resolved")
                return True
                
            # Check the component health
            component_id = issue.component
            metrics = self.monitor.check_component(component_id)
            
            # If metrics are now healthy, consider resolved
            all_healthy = all(m.healthy for m in metrics)
            
            if all_healthy:
                self.logger.info(f"Component {component_id} now reports healthy metrics")
                return True
            else:
                self.logger.warning(f"Component {component_id} still reports unhealthy metrics")
                return False
        except Exception as e:
            self.logger.error(f"Error verifying recovery: {e}")
            return False
            
    def _action_gc_collect(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Force Python garbage collection to free memory."""
        try:
            import gc
            self.logger.info("Running garbage collection")
            collected = gc.collect()
            self.logger.info(f"Garbage collection freed {collected} objects")
            return True
        except Exception as e:
            self.logger.error(f"Error running garbage collection: {e}")
            return False
            
    def _action_retry_api_call(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Retry the failed API call with exponential backoff."""
        if not self.agent:
            return False
            
        try:
            # Extract provider name from component if possible
            component = issue.component
            provider = None
            
            if "provider." in component:
                provider = component.split("provider.")[1].split(".")[0]
                
            if not provider and hasattr(self.agent, "get_active_ai_provider"):
                provider = self.agent.get_active_ai_provider()
                
            if not provider:
                self.logger.warning("Could not determine provider for retry")
                return False
                
            self.logger.info(f"Attempting to retry API call for provider {provider}")
            
            # Simple test call to check if API is working
            try:
                if hasattr(self.agent, "generate_text"):
                    # Use a very simple prompt as a test
                    test_result = self.agent.generate_text("test", max_tokens=5)
                    success = bool(test_result and len(test_result) > 0)
                    
                    if success:
                        self.logger.info("API call retry successful")
                        return True
                    else:
                        self.logger.warning("API call retry returned empty result")
                        return False
            except Exception as inner_e:
                self.logger.warning(f"API call retry failed: {inner_e}")
                return False
        except Exception as e:
            self.logger.error(f"Error retrying API call: {e}")
            return False
            
    def _action_reset_api_provider(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Reset the API provider connection and configuration."""
        if not self.agent:
            return False
            
        try:
            # Extract provider from component if possible
            component = issue.component
            provider = None
            
            if "provider." in component:
                provider = component.split("provider.")[1].split(".")[0]
                
            if not provider and hasattr(self.agent, "get_active_ai_provider"):
                provider = self.agent.get_active_ai_provider()
                
            if not provider:
                self.logger.warning("Could not determine provider to reset")
                return False
                
            self.logger.info(f"Resetting provider {provider}")
            
            # Re-initialize the provider if possible
            if hasattr(self.agent, "ai_manager") and hasattr(self.agent.ai_manager, "get_provider"):
                # Clear provider instance
                if provider in self.agent.ai_manager.provider_instances:
                    del self.agent.ai_manager.provider_instances[provider]
                    
                # Get a fresh provider instance
                new_provider = self.agent.ai_manager.get_provider(provider)
                return new_provider is not None
            
            return False
        except Exception as e:
            self.logger.error(f"Error resetting API provider: {e}")
            return False
            
    def _action_reload_model(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Reload the model from disk."""
        if not self.agent:
            return False
            
        try:
            self.logger.info("Attempting to reload local model")
            
            if hasattr(self.agent, "set_local_model"):
                # If we have a model path from the issue metrics, use it
                model_path = None
                for metric in issue.metrics:
                    if metric.name == "model_path" and metric.value:
                        model_path = metric.value
                        break
                        
                # Reload the model
                result = self.agent.set_local_model(model_path)
                
                if result:
                    self.logger.info("Local model reloaded successfully")
                    return True
                else:
                    self.logger.warning("Failed to reload local model")
                    return False
            
            return False
        except Exception as e:
            self.logger.error(f"Error reloading model: {e}")
            return False
            
    def _action_switch_to_fallback_model(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Switch to a fallback model when primary model fails."""
        if not self.agent:
            return False
            
        try:
            self.logger.info("Attempting to switch to fallback model")
            
            # Try to find a fallback model
            fallback_path = os.path.join(
                os.path.expanduser("~"), 
                ".stableagents", 
                "models", 
                "fallback"
            )
            
            if not os.path.exists(fallback_path):
                self.logger.warning(f"No fallback model found at {fallback_path}")
                
                # Try to use any model in the models directory
                models_dir = os.path.join(os.path.expanduser("~"), ".stableagents", "models")
                
                if os.path.exists(models_dir):
                    for dirpath, dirnames, filenames in os.walk(models_dir):
                        for filename in filenames:
                            if filename.endswith(".gguf"):
                                fallback_path = os.path.join(dirpath, filename)
                                self.logger.info(f"Found alternative model at {fallback_path}")
                                break
                                
            if os.path.exists(fallback_path) and hasattr(self.agent, "set_local_model"):
                result = self.agent.set_local_model(fallback_path)
                
                if result:
                    self.logger.info(f"Switched to fallback model: {fallback_path}")
                    return True
                else:
                    self.logger.warning(f"Failed to switch to fallback model: {fallback_path}")
                    return False
            
            # If no local model available, try switching to a remote provider
            if hasattr(self.agent, "set_active_ai_provider"):
                # Check if we have any API keys
                if hasattr(self.agent, "list_ai_providers"):
                    providers = self.agent.list_ai_providers()
                    
                    for provider in providers:
                        if provider.get("has_key", False) and not provider.get("is_active", False):
                            # Try to switch to this provider
                            self.logger.info(f"Attempting to switch to remote provider: {provider['name']}")
                            
                            if self.agent.set_active_ai_provider(provider["name"]):
                                self.logger.info(f"Switched to remote provider: {provider['name']}")
                                return True
            
            self.logger.warning("No fallback model or remote provider available")
            return False
        except Exception as e:
            self.logger.error(f"Error switching to fallback model: {e}")
            return False
            
    def _action_restart_component(self, issue: Issue, diagnosis: DiagnosisResult) -> bool:
        """Restart the affected component."""
        if not self.agent:
            return False
            
        try:
            component = issue.component
            self.logger.info(f"Attempting to restart component: {component}")
            
            # Handle specific component types
            if "provider" in component.lower():
                return self._action_reset_api_provider(issue, diagnosis)
                
            if "model" in component.lower() or "local" in component.lower():
                return self._action_reload_model(issue, diagnosis)
                
            # General restart logic for other components
            if hasattr(self.agent, "reset"):
                self.logger.info("Performing general agent reset")
                self.agent.reset()
                return True
                
            return False
        except Exception as e:
            self.logger.error(f"Error restarting component: {e}")
            return False
            
    # Main controller methods
    def start(self, auto_recovery: bool = False):
        """Start the self-healing system."""
        if self.is_active:
            return
            
        # Start monitoring
        self.monitor.start_monitoring(self.config["monitoring_interval"])
        
        # Enable auto-recovery if configured
        if auto_recovery or self.config["auto_recovery"]:
            self.recovery_engine.enable_auto_recovery(
                min_severity=self.config["min_severity_for_recovery"],
                risk_threshold=self.config["risk_threshold"]
            )
            
        self.is_active = True
        self.logger.info("Self-healing system started")
        
    def stop(self):
        """Stop the self-healing system."""
        if not self.is_active:
            return
            
        # Stop monitoring
        self.monitor.stop_monitoring()
        
        # Disable auto-recovery
        self.recovery_engine.disable_auto_recovery()
        
        self.is_active = False
        self.logger.info("Self-healing system stopped")
        
    def set_config(self, config: Dict[str, Any]):
        """Update the self-healing configuration."""
        self.config.update(config)
        
        # Apply changes if already active
        if self.is_active:
            self.stop()
            self.start()
            
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the self-healing system."""
        status = {
            "is_active": self.is_active,
            "config": self.config,
            "health": self.monitor.get_system_health() if self.is_active else {"status": "inactive"},
            "recovery_stats": self.recovery_engine.get_recovery_statistics(),
            "active_issues": len(self.monitor.get_active_issues()) if self.is_active else 0
        }
        
        return status
        
    def register_component(self, component_id: str, check_function: Callable, 
                           thresholds: Dict[str, Any] = None,
                           depends_on: List[str] = None):
        """
        Register a component for health monitoring.
        
        Args:
            component_id: Unique identifier for the component
            check_function: Function that returns health metrics for the component
            thresholds: Dictionary of threshold values for metrics
            depends_on: List of component IDs this component depends on
        """
        self.monitor.register_component(component_id, check_function, thresholds)
        
        if depends_on:
            self.diagnosis_engine.register_component_relationship(component_id, depends_on)
            
    def handle_issue(self, issue: Issue, auto_recover: bool = False) -> Optional[RecoveryPlan]:
        """
        Handle an issue manually.
        
        Args:
            issue: The issue to handle
            auto_recover: Whether to automatically execute recovery actions
            
        Returns:
            The recovery plan if auto_recover is True, otherwise None
        """
        # Diagnose the issue
        diagnosis = self.diagnosis_engine.diagnose(issue)
        
        # Create a recovery plan
        plan = self.recovery_engine.create_plan(issue, diagnosis)
        
        if auto_recover:
            # Execute the plan
            self.recovery_engine.execute_plan(plan)
            
        return plan
        
    def learn_from_history(self):
        """Learn from past issues and recoveries to improve future responses."""
        if not self.config["learning_enabled"]:
            return
            
        # Analyze recovery history
        history = self.recovery_engine.recovery_history
        
        # Skip if not enough data
        if len(history) < 5:
            return
            
        self.logger.info("Learning from recovery history")
        
        # Identify successful and failed recovery patterns
        successful = [plan for plan in history if plan.success]
        failed = [plan for plan in history if not plan.success]
        
        # Store patterns for future use
        self.learning_data["successful_recoveries"] = [
            {
                "component": plan.issue.component,
                "description_pattern": plan.issue.description[:50],
                "actions": [action.name for action, _ in plan.executed_actions]
            }
            for plan in successful[:10]  # Store the 10 most recent
        ]
        
        self.learning_data["failed_recoveries"] = [
            {
                "component": plan.issue.component,
                "description_pattern": plan.issue.description[:50],
                "actions": [action.name for action, _ in plan.executed_actions]
            }
            for plan in failed[:10]  # Store the 10 most recent
        ]
        
        # Update success rates for actions
        for action_id, action in self.recovery_engine.actions.items():
            self.logger.info(f"Action {action.name}: {action.success_rate:.2f} success rate ({action.success_count}/{action.attempt_count})")
            
        # Save learning data if telemetry is enabled
        if self.config["telemetry_enabled"] and self.config["telemetry_path"]:
            try:
                with open(self.config["telemetry_path"], "w") as f:
                    json.dump(self.learning_data, f, indent=2)
            except Exception as e:
                self.logger.error(f"Error saving learning data: {e}")
                
    def get_health_report(self) -> Dict[str, Any]:
        """Get a detailed health report of the system."""
        if not self.is_active:
            return {"status": "inactive"}
            
        # Get system health
        health = self.monitor.get_system_health()
        
        # Get component metrics
        component_health = {}
        for component_id in self.monitor.components:
            metrics = self.monitor.check_component(component_id)
            component_health[component_id] = {
                "healthy": all(m.healthy for m in metrics),
                "metrics": [
                    {"name": m.name, "value": m.value, "healthy": m.healthy}
                    for m in metrics
                ],
                "last_check": self.monitor.components[component_id]["last_check"]
            }
            
        # Get active issues
        active_issues = [
            {
                "id": issue.id,
                "component": issue.component,
                "severity": issue.severity,
                "description": issue.description,
                "timestamp": issue.timestamp
            }
            for issue in self.monitor.get_active_issues()
        ]
        
        # Get recovery plans for active issues
        recovery_plans = {}
        for issue_id, plan in self.recovery_engine.recovery_plans.items():
            if plan.completed:
                recovery_plans[issue_id] = {
                    "success": plan.success,
                    "actions_executed": len(plan.executed_actions),
                    "completed_time": plan.completed_time
                }
        
        return {
            "timestamp": time.time(),
            "status": health["status"],
            "components": component_health,
            "active_issues": active_issues,
            "recovery_plans": recovery_plans,
            "auto_recovery": self.recovery_engine.auto_recovery_enabled,
            "monitoring_interval": self.config["monitoring_interval"]
        } 