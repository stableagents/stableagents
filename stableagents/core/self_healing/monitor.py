"""
System monitoring for self-healing capabilities.
"""
import time
import logging
import threading
import traceback
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass

@dataclass
class HealthMetric:
    """A single health metric for the system."""
    name: str
    value: Any
    timestamp: float
    healthy: bool = True
    details: Optional[str] = None

@dataclass
class Issue:
    """Represents a detected issue in the system."""
    id: str
    component: str
    severity: str  # "low", "medium", "high", "critical"
    description: str
    timestamp: float
    metrics: List[HealthMetric]
    stack_trace: Optional[str] = None
    resolved: bool = False
    resolution_timestamp: Optional[float] = None
    resolution_description: Optional[str] = None

class SystemMonitor:
    """
    Monitors the health and behavior of the StableAgents system.
    Detects anomalies, errors, and performance issues.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.health_metrics: Dict[str, HealthMetric] = {}
        self.issues: List[Issue] = []
        self.components: Dict[str, Dict[str, Any]] = {}
        self.thresholds: Dict[str, Dict[str, Any]] = {}
        self.monitoring_active = False
        self.monitoring_thread = None
        self.callbacks: Dict[str, List[Callable]] = {
            "issue_detected": [],
            "issue_resolved": [],
            "health_changed": []
        }
        
    def start_monitoring(self, interval: float = 5.0):
        """Start continuous monitoring in the background."""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitoring_thread.start()
        self.logger.info("System monitoring started")
        
    def stop_monitoring(self):
        """Stop the monitoring thread."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
            self.monitoring_thread = None
        self.logger.info("System monitoring stopped")
        
    def _monitoring_loop(self, interval: float):
        """Background loop that periodically checks system health."""
        while self.monitoring_active:
            try:
                self.check_all_components()
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                # Don't want to crash the monitoring thread
                time.sleep(max(1.0, interval / 2))
                
    def register_component(self, component_id: str, check_function: Callable, 
                           thresholds: Dict[str, Any] = None):
        """
        Register a component to be monitored.
        
        Args:
            component_id: Unique identifier for the component
            check_function: Function that returns health metrics for the component
            thresholds: Dictionary of threshold values for metrics
        """
        self.components[component_id] = {
            "check_function": check_function,
            "last_check": 0,
        }
        
        if thresholds:
            self.thresholds[component_id] = thresholds
            
        self.logger.debug(f"Registered component for monitoring: {component_id}")
        
    def register_callback(self, event_type: str, callback: Callable):
        """Register a callback function for monitoring events."""
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
            
    def check_component(self, component_id: str) -> List[HealthMetric]:
        """
        Check the health of a specific component.
        
        Args:
            component_id: The component to check
            
        Returns:
            List of health metrics for the component
        """
        if component_id not in self.components:
            self.logger.warning(f"Unknown component: {component_id}")
            return []
            
        component = self.components[component_id]
        
        try:
            # Call the check function for this component
            metrics = component["check_function"]()
            component["last_check"] = time.time()
            
            # Update stored metrics
            for metric in metrics:
                self.health_metrics[f"{component_id}.{metric.name}"] = metric
                
            # Check for issues based on thresholds
            self._evaluate_thresholds(component_id, metrics)
            
            return metrics
        except Exception as e:
            # If the check itself fails, that's an issue
            self.logger.error(f"Error checking component {component_id}: {e}")
            stack_trace = traceback.format_exc()
            
            # Create an issue for the failed check
            issue = Issue(
                id=f"check_failure_{component_id}_{time.time()}",
                component=component_id,
                severity="high",
                description=f"Health check failed: {str(e)}",
                timestamp=time.time(),
                metrics=[],
                stack_trace=stack_trace
            )
            
            self._add_issue(issue)
            return []
            
    def check_all_components(self) -> Dict[str, List[HealthMetric]]:
        """Check all registered components and return their metrics."""
        results = {}
        for component_id in self.components:
            metrics = self.check_component(component_id)
            results[component_id] = metrics
        return results
        
    def _evaluate_thresholds(self, component_id: str, metrics: List[HealthMetric]):
        """
        Compare metrics against thresholds and create issues when exceeded.
        
        Args:
            component_id: The component being checked
            metrics: List of metrics to evaluate
        """
        if component_id not in self.thresholds:
            return
            
        thresholds = self.thresholds[component_id]
        
        for metric in metrics:
            metric_key = metric.name
            
            if metric_key in thresholds:
                threshold = thresholds[metric_key]
                
                # Check if threshold is exceeded
                if isinstance(metric.value, (int, float)):
                    if "min" in threshold and metric.value < threshold["min"]:
                        self._create_threshold_issue(component_id, metric, threshold, "below minimum")
                    elif "max" in threshold and metric.value > threshold["max"]:
                        self._create_threshold_issue(component_id, metric, threshold, "above maximum")
                elif isinstance(metric.value, bool) and not metric.value:
                    # Boolean check failed
                    self._create_threshold_issue(component_id, metric, threshold, "check failed")
                    
    def _create_threshold_issue(self, component_id: str, metric: HealthMetric, 
                                threshold: Dict[str, Any], violation_type: str):
        """Create an issue for a threshold violation."""
        severity = threshold.get("severity", "medium")
        
        issue = Issue(
            id=f"threshold_{component_id}_{metric.name}_{time.time()}",
            component=component_id,
            severity=severity,
            description=f"Metric {metric.name} {violation_type}: value={metric.value}",
            timestamp=time.time(),
            metrics=[metric]
        )
        
        self._add_issue(issue)
        
    def _add_issue(self, issue: Issue):
        """Add a new issue and trigger callbacks."""
        # Check if this issue already exists (to avoid duplicates)
        for existing in self.issues:
            if (existing.component == issue.component and 
                existing.description == issue.description and
                not existing.resolved):
                # Update the existing issue instead of creating a new one
                existing.timestamp = issue.timestamp
                existing.metrics = issue.metrics
                return
                
        # Add the new issue
        self.issues.append(issue)
        self.logger.warning(f"Issue detected: {issue.severity} - {issue.description}")
        
        # Trigger callbacks
        for callback in self.callbacks.get("issue_detected", []):
            try:
                callback(issue)
            except Exception as e:
                self.logger.error(f"Error in issue_detected callback: {e}")
                
    def resolve_issue(self, issue_id: str, resolution_description: str = None):
        """Mark an issue as resolved."""
        for issue in self.issues:
            if issue.id == issue_id and not issue.resolved:
                issue.resolved = True
                issue.resolution_timestamp = time.time()
                issue.resolution_description = resolution_description
                
                self.logger.info(f"Issue resolved: {issue.description}")
                
                # Trigger callbacks
                for callback in self.callbacks.get("issue_resolved", []):
                    try:
                        callback(issue)
                    except Exception as e:
                        self.logger.error(f"Error in issue_resolved callback: {e}")
                        
                return True
                
        return False
        
    def get_active_issues(self, component_id: str = None, min_severity: str = None) -> List[Issue]:
        """Get all unresolved issues, optionally filtered by component and severity."""
        active_issues = [issue for issue in self.issues if not issue.resolved]
        
        if component_id:
            active_issues = [i for i in active_issues if i.component == component_id]
            
        if min_severity:
            severity_levels = {"low": 0, "medium": 1, "high": 2, "critical": 3}
            min_level = severity_levels.get(min_severity, 0)
            active_issues = [i for i in active_issues if severity_levels.get(i.severity, 0) >= min_level]
            
        return active_issues
        
    def get_system_health(self) -> Dict[str, Any]:
        """Get an overview of system health."""
        active_issues = self.get_active_issues()
        critical_issues = [i for i in active_issues if i.severity == "critical"]
        high_issues = [i for i in active_issues if i.severity == "high"]
        
        # Determine overall health status
        if critical_issues:
            status = "critical"
        elif high_issues:
            status = "degraded"
        elif active_issues:
            status = "warning"
        else:
            status = "healthy"
            
        return {
            "status": status,
            "active_issues": len(active_issues),
            "critical_issues": len(critical_issues),
            "high_issues": len(high_issues),
            "components": len(self.components),
            "metrics": len(self.health_metrics),
            "last_check": max([comp.get("last_check", 0) for comp in self.components.values()], default=0)
        } 