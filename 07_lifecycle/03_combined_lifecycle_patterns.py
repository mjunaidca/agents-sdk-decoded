"""
03_combined_lifecycle_patterns.py

This example demonstrates advanced lifecycle patterns including:
- Combining RunHooks and AgentHooks for comprehensive monitoring
- Composite hooks pattern for complex scenarios
- Production-ready lifecycle management
- Multi-level observability and analytics
- Event correlation across global and agent-specific contexts

Key Concepts:
- Composite lifecycle monitoring
- Cross-layer event correlation  
- Production monitoring patterns
- Advanced analytics and insights
- Lifecycle orchestration and automation

Based on: https://openai.github.io/openai-agents-python/ref/lifecycle/
"""

import asyncio
import time
from typing import Any, Dict, List, Optional, Set, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
from collections import defaultdict

from agents import Agent, Runner, handoff, function_tool
from agents.lifecycle import RunHooks, AgentHooks


# ================================
# 1. Advanced Data Models
# ================================

class EventType(str, Enum):
    """Types of lifecycle events."""
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    HANDOFF = "handoff"
    ERROR = "error"
    PERFORMANCE_ALERT = "performance_alert"
    OPTIMIZATION_APPLIED = "optimization_applied"


class AlertLevel(str, Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class LifecycleEvent:
    """Unified lifecycle event structure."""
    event_id: str
    event_type: EventType
    timestamp: datetime
    agent_name: str
    context_id: str
    session_id: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)


@dataclass
class SystemAlert:
    """System alert for monitoring and operations."""
    alert_id: str
    level: AlertLevel
    title: str
    description: str
    timestamp: datetime
    agent_name: Optional[str] = None
    event_ids: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False


@dataclass
class AnalyticsReport:
    """Comprehensive analytics report."""
    report_id: str
    generated_at: datetime
    time_range: Dict[str, datetime]
    event_summary: Dict[str, int]
    agent_performance: Dict[str, Dict[str, float]]
    system_health: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]


# ================================
# 2. Event Bus and Storage
# ================================

class LifecycleEventBus:
    """Centralized event bus for lifecycle events."""

    def __init__(self):
        self.events: List[LifecycleEvent] = []
        self.subscribers: Dict[Union[EventType, str], List[Callable[[
            LifecycleEvent], None]]] = defaultdict(list)
        self.event_counter = 0

    def generate_event_id(self) -> str:
        """Generate unique event ID."""
        self.event_counter += 1
        return f"evt_{int(time.time())}_{self.event_counter}"

    def publish_event(self, event: LifecycleEvent) -> None:
        """Publish event to all subscribers."""
        self.events.append(event)

        # Notify subscribers
        for callback in self.subscribers[event.event_type]:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in event callback: {e}")

        # Also notify wildcard subscribers
        for callback in self.subscribers.get("*", []):
            try:
                callback(event)
            except Exception as e:
                print(f"Error in wildcard callback: {e}")

    def subscribe(self, event_type: Union[EventType, str], callback: Callable[[LifecycleEvent], None]) -> None:
        """Subscribe to events."""
        self.subscribers[event_type].append(callback)

    def get_events(self,
                   event_type: Optional[EventType] = None,
                   agent_name: Optional[str] = None,
                   since: Optional[datetime] = None,
                   limit: Optional[int] = None) -> List[LifecycleEvent]:
        """Query events with filters."""
        filtered_events = self.events

        if event_type:
            filtered_events = [
                e for e in filtered_events if e.event_type == event_type]

        if agent_name:
            filtered_events = [
                e for e in filtered_events if e.agent_name == agent_name]

        if since:
            filtered_events = [
                e for e in filtered_events if e.timestamp >= since]

        if limit:
            filtered_events = filtered_events[-limit:]

        return filtered_events


# ================================
# 3. Comprehensive RunHooks
# ================================

class ComprehensiveRunHooks(RunHooks):
    """Advanced RunHooks with full observability and analytics."""

    def __init__(self, event_bus: LifecycleEventBus):
        self.event_bus = event_bus
        self.session_id = f"session_{int(time.time())}"
        self.alerts: List[SystemAlert] = []
        self.performance_thresholds = {
            "max_processing_time": 10.0,
            "max_tool_calls": 20,
            "max_handoffs": 5
        }
        self.session_metrics: Dict[str, Any] = {
            "total_agents": set(),
            "total_tools": set(),
            "start_time": datetime.now(),
            "handoff_count": 0,
            "error_count": 0
        }

    async def on_agent_start(self, context: Any, agent: Agent) -> None:
        """Track agent start with comprehensive monitoring."""
        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.AGENT_START,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id=str(id(context)),
            session_id=self.session_id,
            data={
                "agent_instructions_preview": agent.instructions[:100] + "..." if len(agent.instructions) > 100 else agent.instructions,
                "tools_available": [tool.name for tool in agent.tools] if agent.tools else [],
                "handoffs_available": len(getattr(agent, 'handoffs', [])) if hasattr(agent, 'handoffs') else 0
            },
            tags={"session", "agent_lifecycle"}
        )

        self.event_bus.publish_event(event)
        self.session_metrics["total_agents"].add(agent.name)

        print(
            f"🌟 [GLOBAL] Agent {agent.name} started in session {self.session_id}")

    async def on_agent_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Track agent completion with output analysis."""
        output_analysis = self._analyze_output(output)

        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.AGENT_END,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id=str(id(context)),
            session_id=self.session_id,
            data={
                "output_preview": str(output)[:200] + "..." if len(str(output)) > 200 else str(output),
                "output_analysis": output_analysis
            },
            metrics={
                "output_length": len(str(output)),
                "quality_score": output_analysis.get("quality_score", 0)
            },
            tags={"session", "agent_lifecycle", "completion"}
        )

        self.event_bus.publish_event(event)

        # Check for quality alerts
        if output_analysis.get("quality_score", 0) < 50:
            await self._create_alert(
                AlertLevel.WARNING,
                "Low Quality Output",
                f"Agent {agent.name} produced low quality output (score: {output_analysis.get('quality_score', 0)})",
                agent_name=agent.name,
                event_ids=[event.event_id]
            )

        print(
            f"🏁 [GLOBAL] Agent {agent.name} completed with quality score {output_analysis.get('quality_score', 0)}")

    async def on_handoff(self, context: Any, from_agent: Agent, to_agent: Agent) -> None:
        """Track handoffs with pattern analysis."""
        self.session_metrics["handoff_count"] += 1

        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.HANDOFF,
            timestamp=datetime.now(),
            agent_name=f"{from_agent.name}→{to_agent.name}",
            context_id=str(id(context)),
            session_id=self.session_id,
            data={
                "from_agent": from_agent.name,
                "to_agent": to_agent.name,
                "handoff_sequence": self.session_metrics["handoff_count"],
                "context_preserved": True  # Simplified assumption
            },
            metrics={
                "handoff_number": self.session_metrics["handoff_count"]
            },
            tags={"session", "handoff", "agent_transition"}
        )

        self.event_bus.publish_event(event)

        # Check for excessive handoffs
        if self.session_metrics["handoff_count"] > self.performance_thresholds["max_handoffs"]:
            await self._create_alert(
                AlertLevel.WARNING,
                "Excessive Handoffs",
                f"Session has {self.session_metrics['handoff_count']} handoffs, exceeding threshold of {self.performance_thresholds['max_handoffs']}",
                event_ids=[event.event_id]
            )

        print(
            f"🔄 [GLOBAL] Handoff #{self.session_metrics['handoff_count']}: {from_agent.name} → {to_agent.name}")

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Track tool usage with security monitoring."""
        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.TOOL_START,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id=str(id(context)),
            session_id=self.session_id,
            data={
                "tool_name": tool.name,
                "tool_description": getattr(tool, 'description', 'No description'),
                "agent_context": f"Agent {agent.name} using {tool.name}"
            },
            tags={"session", "tool_usage", "security"}
        )

        self.event_bus.publish_event(event)
        self.session_metrics["total_tools"].add(tool.name)

        # Security monitoring for sensitive tools
        sensitive_tools = ["delete", "remove", "admin", "system", "execute"]
        if any(keyword in tool.name.lower() for keyword in sensitive_tools):
            await self._create_alert(
                AlertLevel.WARNING,
                "Sensitive Tool Access",
                f"Agent {agent.name} accessing sensitive tool: {tool.name}",
                agent_name=agent.name,
                event_ids=[event.event_id]
            )

        print(f"🔧 [GLOBAL] Tool {tool.name} started by {agent.name}")

    async def on_tool_end(self, context: Any, agent: Agent, tool, result: str) -> None:
        """Track tool completion with result analysis."""
        result_analysis = self._analyze_tool_result(result)

        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.TOOL_END,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id=str(id(context)),
            session_id=self.session_id,
            data={
                "tool_name": tool.name,
                "result_preview": result[:100] + "..." if len(result) > 100 else result,
                "result_analysis": result_analysis
            },
            metrics={
                "result_length": len(result),
                "success_indicators": result_analysis.get("success_score", 0)
            },
            tags={"session", "tool_completion"}
        )

        self.event_bus.publish_event(event)

        print(f"✅ [GLOBAL] Tool {tool.name} completed by {agent.name}")

    def _analyze_output(self, output: Any) -> Dict[str, Any]:
        """Analyze agent output quality."""
        output_str = str(output)

        quality_indicators = {
            "length_appropriate": 50 <= len(output_str) <= 1000,
            "contains_helpful_language": any(word in output_str.lower() for word in ["help", "assist", "provide", "support"]),
            "professional_tone": any(word in output_str.lower() for word in ["please", "thank", "apologize"]),
            "addresses_query": "?" not in output_str or "answer" in output_str.lower()
        }

        quality_score = sum(quality_indicators.values()) * 25  # 0-100 scale

        return {
            "quality_score": quality_score,
            "indicators": quality_indicators,
            "word_count": len(output_str.split()),
            "character_count": len(output_str)
        }

    def _analyze_tool_result(self, result: str) -> Dict[str, Any]:
        """Analyze tool execution result."""
        success_indicators = {
            "contains_success_language": any(word in result.lower() for word in ["success", "completed", "done", "found"]),
            "contains_error_language": any(word in result.lower() for word in ["error", "failed", "exception", "invalid"]),
            "has_meaningful_content": len(result.strip()) > 10,
            "structured_response": any(char in result for char in ["{", "[", ":"])
        }

        success_score = 100
        if success_indicators["contains_error_language"]:
            success_score -= 50
        if not success_indicators["has_meaningful_content"]:
            success_score -= 30
        if success_indicators["contains_success_language"]:
            success_score += 10

        return {
            "success_score": max(0, success_score),
            "indicators": success_indicators,
            "result_type": "structured" if success_indicators["structured_response"] else "text"
        }

    async def _create_alert(self, level: AlertLevel, title: str, description: str,
                            agent_name: Optional[str] = None, event_ids: Optional[List[str]] = None) -> None:
        """Create system alert."""
        alert = SystemAlert(
            alert_id=f"alert_{int(time.time())}_{len(self.alerts)}",
            level=level,
            title=title,
            description=description,
            timestamp=datetime.now(),
            agent_name=agent_name,
            event_ids=event_ids or [],
            context={"session_id": self.session_id}
        )

        self.alerts.append(alert)
        print(f"🚨 [ALERT {level.value.upper()}] {title}: {description}")

    def generate_session_report(self) -> AnalyticsReport:
        """Generate comprehensive session analytics report."""
        current_time = datetime.now()
        session_duration = (
            current_time - self.session_metrics["start_time"]).total_seconds()

        # Get session events
        session_events = self.event_bus.get_events(
            since=self.session_metrics["start_time"])  # type: ignore

        # Event summary
        event_summary: Dict[str, int] = {}
        for event in session_events:
            event_summary[event.event_type.value] = event_summary.get(
                event.event_type.value, 0) + 1

        # Agent performance summary
        agent_performance = {}
        for agent_name in self.session_metrics["total_agents"]:
            agent_events = [
                e for e in session_events if e.agent_name == agent_name]
            agent_performance[agent_name] = {
                "total_events": len(agent_events),
                "avg_quality_score": sum(e.metrics.get("quality_score", 0) for e in agent_events) / len(agent_events) if agent_events else 0
            }

        # System health
        system_health = {
            "session_duration_seconds": session_duration,
            "total_agents_used": len(self.session_metrics["total_agents"]),
            "total_tools_used": len(self.session_metrics["total_tools"]),
            "handoff_count": self.session_metrics["handoff_count"],
            "alert_count": len(self.alerts),
            "events_per_minute": (len(session_events) / session_duration * 60) if session_duration > 0 else 0
        }

        # Generate insights
        insights = []
        if self.session_metrics["handoff_count"] > 3:
            insights.append(
                f"High handoff activity ({self.session_metrics['handoff_count']} handoffs) may indicate complex user journey")
        if len(self.alerts) > 0:
            insights.append(
                f"{len(self.alerts)} alerts generated during session - review for optimization opportunities")
        if len(self.session_metrics["total_tools"]) > 10:
            insights.append(
                f"Extensive tool usage ({len(self.session_metrics['total_tools'])} tools) - consider workflow optimization")

        # Generate recommendations
        recommendations = []
        if self.session_metrics["handoff_count"] > self.performance_thresholds["max_handoffs"]:
            recommendations.append(
                "Consider optimizing agent routing to reduce handoffs")
        if len([a for a in self.alerts if a.level == AlertLevel.WARNING]) > 2:
            recommendations.append(
                "Multiple warnings detected - review agent performance and configuration")

        return AnalyticsReport(
            report_id=f"report_{self.session_id}",
            generated_at=current_time,
            time_range={
                "start": self.session_metrics["start_time"],
                "end": current_time
            },
            event_summary=event_summary,
            agent_performance=agent_performance,
            system_health=system_health,
            insights=insights,
            recommendations=recommendations
        )


# ================================
# 4. Enhanced AgentHooks with Integration
# ================================

class IntegratedAgentHooks(AgentHooks):
    """AgentHooks that integrate with the global event bus."""

    def __init__(self, agent_name: str, event_bus: LifecycleEventBus):
        self.agent_name = agent_name
        self.event_bus = event_bus
        self.agent_metrics = {
            "activations": 0,
            "total_processing_time": 0.0,
            "tools_used": [],
            "handoffs_received": 0,
            "performance_scores": []
        }
        self.optimization_applied = False

    async def on_start(self, context: Any, agent: Agent) -> None:
        """Agent-specific start monitoring with global coordination."""
        start_time = time.time()
        self.agent_metrics["activations"] += 1

        # Create agent-specific event
        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.AGENT_START,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id=str(id(context)),
            data={
                "activation_number": self.agent_metrics["activations"],
                "agent_specific_context": "Agent-level monitoring active",
                "previous_performance": self._get_performance_summary()
            },
            metrics={
                "activation_count": self.agent_metrics["activations"]
            },
            tags={"agent_specific", "performance_tracking"}
        )

        self.event_bus.publish_event(event)

        # Apply learned optimizations
        if self.agent_metrics["activations"] > 5 and not self.optimization_applied:
            await self._apply_optimizations(agent)

        print(
            f"🤖 [AGENT {agent.name}] Activation #{self.agent_metrics['activations']} with performance tracking")

    async def on_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Agent-specific completion monitoring."""
        # Calculate performance score
        performance_score = self._calculate_performance_score(output)
        self.agent_metrics["performance_scores"].append(performance_score)

        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.AGENT_END,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id=str(id(context)),
            data={
                "completion_context": "Agent-specific completion tracking",
                "performance_trend": self._analyze_performance_trend()
            },
            metrics={
                "performance_score": performance_score,
                "average_performance": sum(self.agent_metrics["performance_scores"]) / len(self.agent_metrics["performance_scores"])
            },
            tags={"agent_specific", "performance_analysis"}
        )

        self.event_bus.publish_event(event)

        print(
            f"✅ [AGENT {agent.name}] Completed with performance score {performance_score:.2f}")

    async def on_handoff(self, context: Any, agent: Agent, source: Agent) -> None:
        """Track handoffs from agent perspective."""
        self.agent_metrics["handoffs_received"] += 1

        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.HANDOFF,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id=str(id(context)),
            data={
                "handoff_from": source.name,
                "agent_readiness": self._assess_readiness(),
                "handoff_context": f"Receiving control from {source.name}"
            },
            metrics={
                "handoffs_received": self.agent_metrics["handoffs_received"]
            },
            tags={"agent_specific", "handoff_received"}
        )

        self.event_bus.publish_event(event)

        print(
            f"🔄 [AGENT {agent.name}] Handoff received from {source.name} (total: {self.agent_metrics['handoffs_received']})")

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Track tool usage from agent perspective."""
        self.agent_metrics["tools_used"].append({
            "tool_name": tool.name,
            "timestamp": datetime.now(),
            "activation": self.agent_metrics["activations"]
        })

        # Agent-specific tool optimization
        tool_frequency = len(
            [t for t in self.agent_metrics["tools_used"] if t["tool_name"] == tool.name])

        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.TOOL_START,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id=str(id(context)),
            data={
                "tool_name": tool.name,
                "tool_frequency": tool_frequency,
                "tool_efficiency": self._calculate_tool_efficiency(tool.name)
            },
            metrics={
                "tool_frequency": tool_frequency,
                "total_tools_used": len(self.agent_metrics["tools_used"])
            },
            tags={"agent_specific", "tool_efficiency"}
        )

        self.event_bus.publish_event(event)

        print(
            f"🔧 [AGENT {agent.name}] Tool {tool.name} usage #{tool_frequency}")

    async def on_tool_end(self, context: Any, agent: Agent, tool, result: str) -> None:
        """Complete tool tracking from agent perspective."""
        # Update tool usage with result
        for tool_usage in reversed(self.agent_metrics["tools_used"]):
            if tool_usage["tool_name"] == tool.name and "result_length" not in tool_usage:
                tool_usage["result_length"] = len(result)
                tool_usage["completed_at"] = datetime.now()
                break

        print(
            f"✅ [AGENT {agent.name}] Tool {tool.name} completed successfully")

    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get current performance summary."""
        if not self.agent_metrics["performance_scores"]:
            return {"status": "no_data"}

        return {
            "average_score": sum(self.agent_metrics["performance_scores"]) / len(self.agent_metrics["performance_scores"]),
            "score_count": len(self.agent_metrics["performance_scores"]),
            "trend": self._analyze_performance_trend()
        }

    def _calculate_performance_score(self, output: Any) -> float:
        """Calculate performance score for this completion."""
        base_score = 50.0
        output_str = str(output)

        # Output quality factors
        if 50 <= len(output_str) <= 500:
            base_score += 20
        if any(word in output_str.lower() for word in ["help", "assist", "provide"]):
            base_score += 15
        if len(output_str.split()) > 10:  # Substantial response
            base_score += 10

        # Agent-specific factors
        if self.agent_metrics["activations"] > 1:
            # Improvement over time
            if self.agent_metrics["performance_scores"]:
                recent_avg = sum(self.agent_metrics["performance_scores"][-3:]) / min(
                    3, len(self.agent_metrics["performance_scores"]))
                if base_score > recent_avg:
                    base_score += 5  # Improvement bonus

        return min(100, max(0, base_score))

    def _analyze_performance_trend(self) -> str:
        """Analyze performance trend over recent activations."""
        if len(self.agent_metrics["performance_scores"]) < 3:
            return "insufficient_data"

        recent_scores = self.agent_metrics["performance_scores"][-5:]
        if len(recent_scores) < 3:
            return "insufficient_data"

        # Simple trend analysis
        first_half_avg = sum(
            recent_scores[:len(recent_scores)//2]) / (len(recent_scores)//2)
        second_half_avg = sum(recent_scores[len(
            recent_scores)//2:]) / (len(recent_scores) - len(recent_scores)//2)

        if second_half_avg > first_half_avg + 5:
            return "improving"
        elif second_half_avg < first_half_avg - 5:
            return "declining"
        else:
            return "stable"

    def _assess_readiness(self) -> Dict[str, Any]:
        """Assess agent readiness for handoff."""
        return {
            "activation_count": self.agent_metrics["activations"],
            "recent_performance": self.agent_metrics["performance_scores"][-1] if self.agent_metrics["performance_scores"] else None,
            "tools_available": len(set(t["tool_name"] for t in self.agent_metrics["tools_used"])),
            "readiness_score": min(100, self.agent_metrics["activations"] * 10 + 50)
        }

    def _calculate_tool_efficiency(self, tool_name: str) -> float:
        """Calculate efficiency for specific tool."""
        tool_usages = [t for t in self.agent_metrics["tools_used"]
                       if t["tool_name"] == tool_name]
        if not tool_usages:
            return 0.0

        completed_usages = [t for t in tool_usages if "result_length" in t]
        if not completed_usages:
            return 50.0  # Neutral score for incomplete data

        # Simple efficiency calculation based on result length
        avg_result_length = sum(t["result_length"]
                                for t in completed_usages) / len(completed_usages)
        efficiency = min(100, max(0, avg_result_length / 10)
                         )  # Normalize to 0-100

        return efficiency

    async def _apply_optimizations(self, agent: Agent) -> None:
        """Apply learned optimizations to agent."""
        self.optimization_applied = True

        # Create optimization event
        event = LifecycleEvent(
            event_id=self.event_bus.generate_event_id(),
            event_type=EventType.OPTIMIZATION_APPLIED,
            timestamp=datetime.now(),
            agent_name=agent.name,
            context_id="optimization_context",
            data={
                "optimization_type": "performance_improvement",
                "trigger": f"after_{self.agent_metrics['activations']}_activations",
                "performance_summary": self._get_performance_summary()
            },
            tags={"optimization", "agent_improvement"}
        )

        self.event_bus.publish_event(event)

        print(
            f"🎯 [AGENT {agent.name}] Applied performance optimizations after {self.agent_metrics['activations']} activations")


# ================================
# 5. Demo Tools and Agents
# ================================

@function_tool
def analyze_data(dataset: str) -> str:
    """Analyze a dataset and return insights."""
    return f"Data analysis complete for {dataset}: Found 5 key trends, 3 anomalies, and 2 optimization opportunities"


@function_tool
def generate_report(data: str) -> str:
    """Generate a comprehensive report based on data."""
    return f"Report generated based on {data}: Executive summary, detailed findings, and actionable recommendations included"


@function_tool
def send_notification(message: str) -> str:
    """Send notification to stakeholders."""
    return f"Notification sent: '{message}' delivered to all stakeholders successfully"


def create_analytics_agent(event_bus: LifecycleEventBus) -> Agent:
    """Create analytics agent with integrated hooks."""
    agent = Agent(
        name="AnalyticsAgent",
        instructions="You are an analytics agent that processes data and generates insights. Focus on accuracy and actionable recommendations.",
        tools=[analyze_data, generate_report]
    )

    # Attach integrated hooks
    agent.hooks = IntegratedAgentHooks("AnalyticsAgent", event_bus)
    return agent


def create_reporting_agent(event_bus: LifecycleEventBus) -> Agent:
    """Create reporting agent with integrated hooks."""
    agent = Agent(
        name="ReportingAgent",
        instructions="You are a reporting specialist. Create clear, professional reports and communicate findings effectively.",
        tools=[generate_report, send_notification]
    )

    # Attach integrated hooks
    agent.hooks = IntegratedAgentHooks("ReportingAgent", event_bus)
    return agent


def create_coordinator_agent(event_bus: LifecycleEventBus) -> Agent:
    """Create coordinator agent with integrated hooks."""
    agent = Agent(
        name="CoordinatorAgent",
        instructions="You are a coordinator that manages workflows and ensures smooth operations between different agents.",
        tools=[send_notification]
    )

    # Attach integrated hooks
    agent.hooks = IntegratedAgentHooks("CoordinatorAgent", event_bus)
    return agent


# ================================
# 6. Demo Functions
# ================================

async def demo_integrated_lifecycle_monitoring():
    """Demonstrate integrated RunHooks and AgentHooks."""
    print("=== Integrated Lifecycle Monitoring Demo ===")

    # Create event bus and hooks
    event_bus = LifecycleEventBus()
    run_hooks = ComprehensiveRunHooks(event_bus)

    # Create agents with integrated hooks
    analytics_agent = create_analytics_agent(event_bus)
    reporting_agent = create_reporting_agent(event_bus)

    # Set up handoffs
    analytics_agent.handoffs = [
        handoff(reporting_agent, tool_name_override="generate_detailed_report")
    ]

    # Subscribe to events for real-time monitoring
    def event_monitor(event: LifecycleEvent):
        print(
            f"📡 [EVENT MONITOR] {event.event_type.value}: {event.agent_name} at {event.timestamp.strftime('%H:%M:%S')}")

    event_bus.subscribe("*", event_monitor)

    # Run workflow with comprehensive monitoring
    result = await Runner.run(
        analytics_agent,
        input="Analyze sales data from Q4 and create a comprehensive report for stakeholders",
        hooks=run_hooks
    )

    print(f"\nFinal Result: {result.final_output}")

    # Generate and display session report
    session_report = run_hooks.generate_session_report()
    print(f"\n📊 Session Analytics Report:")
    print(f"  Report ID: {session_report.report_id}")
    print(
        f"  Duration: {session_report.system_health['session_duration_seconds']:.2f}s")
    print(f"  Events: {session_report.event_summary}")
    print(f"  Agents: {list(session_report.agent_performance.keys())}")
    print(f"  Insights: {session_report.insights}")
    print(f"  Recommendations: {session_report.recommendations}")


async def demo_event_correlation_analysis():
    """Demonstrate event correlation and pattern analysis."""
    print("\n=== Event Correlation Analysis Demo ===")

    # Create event bus and monitoring
    event_bus = LifecycleEventBus()
    run_hooks = ComprehensiveRunHooks(event_bus)

    # Create multiple agents for complex workflow
    analytics_agent = create_analytics_agent(event_bus)
    reporting_agent = create_reporting_agent(event_bus)
    coordinator_agent = create_coordinator_agent(event_bus)

    # Set up complex handoff chain
    analytics_agent.handoffs = [
        handoff(reporting_agent, tool_name_override="create_detailed_report"),
        handoff(coordinator_agent, tool_name_override="coordinate_workflow")
    ]
    reporting_agent.handoffs = [
        handoff(coordinator_agent, tool_name_override="coordinate_final_steps")
    ]

    # Track event patterns
    event_patterns = []

    def pattern_analyzer(event: LifecycleEvent):
        event_patterns.append({
            "type": event.event_type.value,
            "agent": event.agent_name,
            "timestamp": event.timestamp,
            "tags": list(event.tags)
        })

    event_bus.subscribe("*", pattern_analyzer)

    # Run multiple scenarios
    scenarios = [
        "Analyze customer satisfaction data and prepare executive briefing",
        "Process quarterly financial results and notify board members",
        "Generate market analysis report for upcoming product launch"
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario[:50]}... ---")

        result = await Runner.run(
            analytics_agent,
            input=scenario,
            hooks=run_hooks
        )

        # Add delay between scenarios
        await asyncio.sleep(1)

    # Analyze patterns
    print(f"\n🔍 Event Pattern Analysis:")

    # Event frequency by type
    event_types = {}
    for pattern in event_patterns:
        event_type = pattern["type"]
        event_types[event_type] = event_types.get(event_type, 0) + 1

    print(f"  Event Frequency: {event_types}")

    # Agent activity
    agent_activity = {}
    for pattern in event_patterns:
        agent = pattern["agent"]
        agent_activity[agent] = agent_activity.get(agent, 0) + 1

    print(f"  Agent Activity: {agent_activity}")

    # Handoff patterns
    handoff_patterns = [p for p in event_patterns if p["type"] == "handoff"]
    print(f"  Handoff Count: {len(handoff_patterns)}")

    # Generate final session report
    final_report = run_hooks.generate_session_report()
    print(f"\n📈 Final Session Report:")
    print(f"  Total Events: {len(event_patterns)}")
    print(f"  System Health: {final_report.system_health}")
    print(f"  Alerts Generated: {len(run_hooks.alerts)}")


async def demo_production_monitoring_patterns():
    """Demonstrate production-ready monitoring patterns."""
    print("\n=== Production Monitoring Patterns Demo ===")

    # Create event bus with production monitoring
    event_bus = LifecycleEventBus()
    run_hooks = ComprehensiveRunHooks(event_bus)

    # Set stricter production thresholds
    run_hooks.performance_thresholds = {
        "max_processing_time": 5.0,
        "max_tool_calls": 10,
        "max_handoffs": 3
    }

    # Create production agents
    analytics_agent = create_analytics_agent(event_bus)
    reporting_agent = create_reporting_agent(event_bus)
    coordinator_agent = create_coordinator_agent(event_bus)

    # Set up production handoff chain
    analytics_agent.handoffs = [
        handoff(reporting_agent, tool_name_override="generate_production_report"),
        handoff(coordinator_agent,
                tool_name_override="coordinate_production_workflow")
    ]
    reporting_agent.handoffs = [
        handoff(coordinator_agent, tool_name_override="finalize_production_output")
    ]

    # Production monitoring subscriptions
    critical_events = []
    performance_events = []

    def critical_event_handler(event: LifecycleEvent):
        if "error" in event.tags or "critical" in event.tags:
            critical_events.append(event)
            print(
                f"🚨 [CRITICAL] {event.event_type.value} in {event.agent_name}")

    def performance_handler(event: LifecycleEvent):
        if event.event_type in [EventType.AGENT_END, EventType.TOOL_END]:
            performance_events.append(event)

    event_bus.subscribe("*", critical_event_handler)
    event_bus.subscribe("*", performance_handler)

    # Simulate production workload
    production_requests = [
        "Generate urgent financial analysis for board meeting tomorrow",
        "Process critical customer escalation data and prepare response strategy",
        "Analyze system performance metrics and create optimization recommendations",
        "Handle emergency data breach analysis and notification requirements"
    ]

    for i, request in enumerate(production_requests, 1):
        print(f"\n--- Production Request {i} ---")

        try:
            result = await Runner.run(
                analytics_agent,
                input=request,
                hooks=run_hooks
            )

            print(f"✅ Production request completed successfully")

        except Exception as e:
            print(f"❌ Production request failed: {e}")

            # Create error event
            error_event = LifecycleEvent(
                event_id=event_bus.generate_event_id(),
                event_type=EventType.ERROR,
                timestamp=datetime.now(),
                agent_name="system",
                context_id="error_context",
                data={"error": str(e), "request": request},
                tags={"error", "production", "critical"}
            )
            event_bus.publish_event(error_event)

        # Brief pause between requests
        await asyncio.sleep(0.5)

    # Production monitoring summary
    print(f"\n📊 Production Monitoring Summary:")
    print(f"  Total Requests Processed: {len(production_requests)}")
    print(f"  Critical Events: {len(critical_events)}")
    print(f"  Performance Events: {len(performance_events)}")
    print(f"  System Alerts: {len(run_hooks.alerts)}")

    # Alert breakdown
    alert_levels = {}
    for alert in run_hooks.alerts:
        alert_levels[alert.level.value] = alert_levels.get(
            alert.level.value, 0) + 1

    print(f"  Alert Breakdown: {alert_levels}")

    # Performance metrics
    if performance_events:
        avg_quality = sum(e.metrics.get("quality_score", 0)
                          for e in performance_events) / len(performance_events)
        print(f"  Average Quality Score: {avg_quality:.2f}")

    # Generate production report
    production_report = run_hooks.generate_session_report()
    print(f"\n📋 Production Report Generated: {production_report.report_id}")
    print(f"  Recommendations: {production_report.recommendations}")


# ================================
# 7. Main Demo Function
# ================================

async def main():
    """Run all combined lifecycle pattern demonstrations."""
    print("🌐 OpenAI Agents SDK - Combined Lifecycle Patterns")
    print("=" * 60)

    # Run all demonstrations
    await demo_integrated_lifecycle_monitoring()
    await demo_event_correlation_analysis()
    await demo_production_monitoring_patterns()

    print("\n" + "=" * 60)
    print("✅ Combined lifecycle patterns demonstration complete!")
    print("\nKey Takeaways:")
    print("1. RunHooks and AgentHooks can work together for comprehensive monitoring")
    print("2. Event buses enable real-time correlation and pattern analysis")
    print("3. Production monitoring requires stricter thresholds and alerting")
    print("4. Lifecycle events provide valuable insights for optimization")
    print("5. Combined patterns enable enterprise-grade observability")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())


# ================================
# 8. Production Implementation Notes
# ================================

"""
Combined Lifecycle Production Patterns:

1. **Event-Driven Architecture**:
   - Centralized event bus for all lifecycle events
   - Real-time event correlation and pattern analysis
   - Event sourcing for audit trails and replay capability
   - Stream processing for high-volume environments

2. **Multi-Level Monitoring**:
   - Global (RunHooks) for system-wide monitoring
   - Agent-specific (AgentHooks) for individual optimization
   - Cross-layer correlation for comprehensive insights
   - Hierarchical alerting based on event severity

3. **Production Observability**:
   - Real-time dashboards for operational visibility
   - Automated alerting for anomaly detection
   - Performance trending and capacity planning
   - SLA monitoring and compliance reporting

4. **Advanced Analytics**:
   - Machine learning for pattern recognition
   - Predictive analytics for proactive optimization
   - User journey analysis across agent handoffs
   - Business intelligence integration

5. **Operational Excellence**:
   - Automated incident response workflows
   - Chaos engineering for resilience testing
   - Blue-green deployments with monitoring
   - Continuous optimization based on lifecycle data

6. **Scalability Considerations**:
   - Event sampling for high-volume systems
   - Distributed monitoring across clusters
   - Efficient data storage and retrieval
   - Load balancing of monitoring components
"""
