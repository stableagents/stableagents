"""
Diagnosis engine for self-healing capabilities.
"""
import time
import logging
import traceback
from typing import Dict, List, Any, Optional, Tuple, Callable
from .monitor import Issue, HealthMetric

class DiagnosisResult:
    """Results of diagnosing an issue."""
    
    def __init__(self, issue: Issue):
        self.issue = issue
        self.root_causes: List[str] = []
        self.confidence: float = 0.0  # 0.0 to 1.0
        self.diagnosis_time = time.time()
        self.resolution_suggestions: List[str] = []
        self.diagnosis_details: Dict[str, Any] = {}
        self.traced_components: List[str] = []
        
    def add_root_cause(self, cause: str, confidence: float = 0.5):
        """Add a potential root cause with confidence level."""
        self.root_causes.append(cause)
        # Update overall confidence as highest of all causes
        self.confidence = max(self.confidence, confidence)
        
    def add_resolution_suggestion(self, suggestion: str):
        """Add a suggestion for resolving the issue."""
        self.resolution_suggestions.append(suggestion)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary representation."""
        return {
            "issue_id": self.issue.id,
            "component": self.issue.component,
            "severity": self.issue.severity,
            "description": self.issue.description,
            "timestamp": self.issue.timestamp,
            "root_causes": self.root_causes,
            "confidence": self.confidence,
            "diagnosis_time": self.diagnosis_time,
            "resolution_suggestions": self.resolution_suggestions,
            "traced_components": self.traced_components
        }

class DiagnosticRule:
    """A rule for diagnosing specific types of issues."""
    
    def __init__(self, name: str, component_patterns: List[str], 
                 condition_fn: Callable[[Issue], bool], 
                 diagnose_fn: Callable[[Issue], Tuple[List[str], float]]):
        self.name = name
        self.component_patterns = component_patterns  # Components this rule applies to
        self.condition_fn = condition_fn  # Function to check if rule applies
        self.diagnose_fn = diagnose_fn  # Function to diagnose and return causes and confidence
        
    def applies_to(self, issue: Issue) -> bool:
        """Check if this rule applies to the given issue."""
        # Check component pattern match
        if not any(pattern in issue.component for pattern in self.component_patterns):
            return False
            
        # Check condition function
        return self.condition_fn(issue)
        
    def diagnose(self, issue: Issue) -> Tuple[List[str], float]:
        """Diagnose the issue and return potential causes and confidence."""
        return self.diagnose_fn(issue)

class DiagnosisEngine:
    """
    Engine for diagnosing issues and determining root causes.
    Uses rules and AI-assisted analysis to diagnose problems.
    """
    
    def __init__(self, agent=None):
        self.logger = logging.getLogger(__name__)
        self.rules: List[DiagnosticRule] = []
        self.diagnoses: Dict[str, DiagnosisResult] = {}  # Cache of diagnoses by issue id
        self.agent = agent  # Reference to StableAgents instance for AI-assisted diagnosis
        self.component_relationships: Dict[str, List[str]] = {}  # Component dependencies
        
    def register_rule(self, rule: DiagnosticRule):
        """Register a diagnostic rule with the engine."""
        self.rules.append(rule)
        
    def register_component_relationship(self, component: str, depends_on: List[str]):
        """Register component dependencies for tracing issues across components."""
        self.component_relationships[component] = depends_on
        
    def diagnose(self, issue: Issue) -> DiagnosisResult:
        """
        Diagnose an issue to determine root causes and suggest resolutions.
        
        Args:
            issue: The issue to diagnose
            
        Returns:
            A DiagnosisResult with root causes and suggestions
        """
        # Check if we've already diagnosed this issue
        if issue.id in self.diagnoses:
            return self.diagnoses[issue.id]
            
        # Create a new diagnosis result
        result = DiagnosisResult(issue)
        
        # Apply rules that match this issue
        applicable_rules = [rule for rule in self.rules if rule.applies_to(issue)]
        
        if applicable_rules:
            for rule in applicable_rules:
                try:
                    causes, confidence = rule.diagnose(issue)
                    for cause in causes:
                        result.add_root_cause(cause, confidence)
                except Exception as e:
                    self.logger.error(f"Error applying rule {rule.name}: {e}")
                    
        # If no rules applied or confidence is low, try AI-assisted diagnosis
        if not result.root_causes or result.confidence < 0.4:
            self._ai_assisted_diagnosis(issue, result)
            
        # Trace component dependencies to identify related issues
        traced_components = self._trace_component_dependencies(issue.component)
        result.traced_components = traced_components
        
        # Generate resolution suggestions
        self._generate_resolution_suggestions(result)
        
        # Cache the diagnosis
        self.diagnoses[issue.id] = result
        
        return result
        
    def _ai_assisted_diagnosis(self, issue: Issue, result: DiagnosisResult):
        """Use AI to assist in diagnosing complex issues."""
        if not self.agent:
            return
            
        try:
            # Format the issue for AI analysis
            issue_context = {
                "component": issue.component,
                "severity": issue.severity,
                "description": issue.description,
                "stack_trace": issue.stack_trace or "Not available",
                "metrics": [
                    {"name": m.name, "value": m.value, "healthy": m.healthy} 
                    for m in issue.metrics
                ]
            }
            
            # Create a diagnostic prompt
            prompt = f"""
            Please analyze this system issue and identify potential root causes:
            
            Component: {issue.component}
            Severity: {issue.severity}
            Description: {issue.description}
            
            Metrics: {str([f"{m.name}={m.value}" for m in issue.metrics])}
            
            Stack Trace: 
            {issue.stack_trace or 'Not available'}
            
            Based on this information, what are the most likely root causes?
            Format your response as a JSON object with the following structure:
            {{
                "root_causes": [
                    {{"cause": "description of cause", "confidence": 0.8, "explanation": "why you think this is a cause"}}
                ],
                "resolution_suggestions": [
                    "suggestion 1",
                    "suggestion 2"
                ]
            }}
            """
            
            # Send to AI for analysis
            ai_response = self.agent.generate_text(prompt)
            
            # Parse the response (simplified - in reality would need more robust parsing)
            # This is a placeholder for the actual AI integration
            if "root_causes" in ai_response:
                # Simple parsing assuming well-formatted response
                import json
                try:
                    analysis = json.loads(ai_response)
                    for cause_item in analysis.get("root_causes", []):
                        result.add_root_cause(
                            cause_item.get("cause", "Unknown cause"), 
                            cause_item.get("confidence", 0.5)
                        )
                    for suggestion in analysis.get("resolution_suggestions", []):
                        result.add_resolution_suggestion(suggestion)
                except json.JSONDecodeError:
                    self.logger.warning("Could not parse AI diagnosis response as JSON")
                    # Fallback: treat the whole response as a single cause
                    result.add_root_cause(f"AI diagnosis: {ai_response[:100]}...", 0.3)
        except Exception as e:
            self.logger.error(f"Error in AI-assisted diagnosis: {e}")
            result.diagnosis_details["ai_error"] = str(e)
            
    def _trace_component_dependencies(self, component: str, depth: int = 2) -> List[str]:
        """
        Trace component dependencies to find potentially related components.
        
        Args:
            component: The component to trace from
            depth: How many levels of dependencies to trace
            
        Returns:
            List of related component IDs
        """
        if depth <= 0:
            return []
            
        related_components = []
        
        # Get direct dependencies
        direct_deps = self.component_relationships.get(component, [])
        related_components.extend(direct_deps)
        
        # Recursively trace dependencies
        for dep in direct_deps:
            related_components.extend(
                self._trace_component_dependencies(dep, depth - 1)
            )
            
        # Get components that depend on this component
        for comp, deps in self.component_relationships.items():
            if component in deps and comp not in related_components:
                related_components.append(comp)
                
        return list(set(related_components))  # Remove duplicates
        
    def _generate_resolution_suggestions(self, result: DiagnosisResult):
        """Generate suggestions for resolving the issue based on diagnosis."""
        if not result.root_causes:
            result.add_resolution_suggestion("Collect more diagnostic information")
            return
            
        # Generate basic suggestions based on component and root causes
        component = result.issue.component
        
        # Example resolution strategies based on component type
        if "memory" in component.lower():
            result.add_resolution_suggestion("Check for memory leaks")
            result.add_resolution_suggestion("Increase memory allocation if consistently high")
            
        if "api" in component.lower() or "provider" in component.lower():
            result.add_resolution_suggestion("Verify API key validity")
            result.add_resolution_suggestion("Check for service outage or rate limits")
            
        if "model" in component.lower() or "local" in component.lower():
            result.add_resolution_suggestion("Verify model file exists and is accessible")
            result.add_resolution_suggestion("Check if model format is supported")
            
        # If we have a stack trace, suggest code-related fixes
        if result.issue.stack_trace:
            result.add_resolution_suggestion("Review stack trace for code-level issues")
            
        # If no specific suggestions, add general ones
        if not result.resolution_suggestions:
            result.add_resolution_suggestion("Restart the affected component")
            result.add_resolution_suggestion("Check logs for more detailed error information")
            result.add_resolution_suggestion("Update to the latest version of dependencies") 