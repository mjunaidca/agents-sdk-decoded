"""
04_production_lifecycle_patterns.py

This example demonstrates production-ready lifecycle patterns for enterprise deployment:
- Enterprise-grade monitoring and alerting
- SLA tracking and compliance reporting
- Performance optimization and capacity planning
- Multi-tenant lifecycle management
- Integration with external monitoring systems

Key Concepts:
- Production observability patterns
- Enterprise monitoring integration
- SLA compliance and reporting
- Automated optimization workflows
- Multi-tenant lifecycle isolation

Based on: https://openai.github.io/openai-agents-python/ref/lifecycle/
"""

import asyncio
import time
import json
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from agents import Agent, Runner, handoff, function_tool
from agents.lifecycle import RunHooks, AgentHooks


# ================================
# 1. Production Data Models
# ================================

class SeverityLevel(str, Enum):
    """Production severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MetricType(str, Enum):
    """Types of production metrics."""
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    AVAILABILITY = "availability"
    RESOURCE_USAGE = "resource_usage"
    QUALITY_SCORE = "quality_score"


@dataclass
class ProductionMetric:
    """Production metric with SLA tracking."""
    metric_id: str
    metric_type: MetricType
    value: float
    threshold: float
    timestamp: datetime
    tenant_id: Optional[str] = None
    agent_name: Optional[str] = None
    is_sla_violation: bool = False
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SLATarget:
    """Service Level Agreement target definition."""
    name: str
    metric_type: MetricType
    target_value: float
    threshold_operator: str  # "<=", ">=", "==", "!=", "<", ">"
    time_window_minutes: int = 60
    violation_threshold_percent: float = 95.0
    enabled: bool = True


@dataclass
class ProductionAlert:
    """Production alert with escalation."""
    alert_id: str
    severity: SeverityLevel
    title: str
    description: str
    timestamp: datetime
    tenant_id: Optional[str] = None
    agent_name: Optional[str] = None
    metric_values: Dict[str, float] = field(default_factory=dict)
    escalated: bool = False
    resolved: bool = False
    resolution_time: Optional[datetime] = None


# ================================
# 2. Production Monitoring System
# ================================

class ProductionMonitoringSystem:
    """Centralized production monitoring and alerting system."""

    def __init__(self):
        self.metrics: List[ProductionMetric] = []
        self.alerts: List[ProductionAlert] = []
        self.sla_targets: List[SLATarget] = []
        self.alert_counter = 0
        self.metric_counter = 0

        # Default SLA targets
        self._initialize_default_slas()

    def _initialize_default_slas(self):
        """Initialize default SLA targets for production."""
        self.sla_targets = [
            SLATarget(
                name="Response Time SLA",
                metric_type=MetricType.LATENCY,
                target_value=2.0,  # 2 seconds
                threshold_operator="<=",
                time_window_minutes=60
            ),
            SLATarget(
                name="Error Rate SLA",
                metric_type=MetricType.ERROR_RATE,
                target_value=1.0,  # 1%
                threshold_operator="<=",
                time_window_minutes=60
            ),
            SLATarget(
                name="Availability SLA",
                metric_type=MetricType.AVAILABILITY,
                target_value=99.9,  # 99.9%
                threshold_operator=">=",
                time_window_minutes=60
            ),
            SLATarget(
                name="Quality Score SLA",
                metric_type=MetricType.QUALITY_SCORE,
                target_value=80.0,  # 80/100
                threshold_operator=">=",
                time_window_minutes=60
            )
        ]

    def record_metric(self, metric_type: MetricType, value: float,
                      agent_name: Optional[str] = None,
                      tenant_id: Optional[str] = None,
                      context: Optional[Dict[str, Any]] = None) -> ProductionMetric:
        """Record a production metric with SLA checking."""
        self.metric_counter += 1

        # Find applicable SLA target
        sla_target = self._find_sla_target(metric_type)

        # Check for SLA violation
        is_violation = False
        threshold = 0.0
        if sla_target:
            threshold = sla_target.target_value
            is_violation = self._check_sla_violation(value, sla_target)

        metric = ProductionMetric(
            metric_id=f"metric_{int(time.time())}_{self.metric_counter}",
            metric_type=metric_type,
            value=value,
            threshold=threshold,
            timestamp=datetime.now(),
            tenant_id=tenant_id,
            agent_name=agent_name,
            is_sla_violation=is_violation,
            context=context or {}
        )

        self.metrics.append(metric)

        # Create alert if SLA violation
        if is_violation and sla_target:
            self._create_sla_violation_alert(metric, sla_target)

        return metric

    def _find_sla_target(self, metric_type: MetricType) -> Optional[SLATarget]:
        """Find applicable SLA target for metric type."""
        for target in self.sla_targets:
            if target.metric_type == metric_type and target.enabled:
                return target
        return None

    def _check_sla_violation(self, value: float, sla_target: SLATarget) -> bool:
        """Check if metric value violates SLA target."""
        operator = sla_target.threshold_operator
        threshold = sla_target.target_value

        if operator == "<=":
            return value > threshold
        elif operator == ">=":
            return value < threshold
        elif operator == "==":
            return value != threshold
        elif operator == "!=":
            return value == threshold
        elif operator == "<":
            return value >= threshold
        elif operator == ">":
            return value <= threshold
        else:
            return False

    def _create_sla_violation_alert(self, metric: ProductionMetric, sla_target: SLATarget):
        """Create alert for SLA violation."""
        self.alert_counter += 1

        # Determine severity based on how much threshold is exceeded
        severity = self._calculate_alert_severity(metric, sla_target)

        alert = ProductionAlert(
            alert_id=f"alert_{int(time.time())}_{self.alert_counter}",
            severity=severity,
            title=f"SLA Violation: {sla_target.name}",
            description=f"{metric.metric_type.value} value {metric.value} violates SLA target {sla_target.target_value}",
            timestamp=datetime.now(),
            tenant_id=metric.tenant_id,
            agent_name=metric.agent_name,
            metric_values={metric.metric_type.value: metric.value}
        )

        self.alerts.append(alert)

        print(f"🚨 [SLA VIOLATION {severity.value.upper()}] {alert.title}")
        print(
            f"   Agent: {metric.agent_name}, Value: {metric.value}, Threshold: {sla_target.target_value}")

    def _calculate_alert_severity(self, metric: ProductionMetric, sla_target: SLATarget) -> SeverityLevel:
        """Calculate alert severity based on SLA violation magnitude."""
        value = metric.value
        threshold = sla_target.target_value

        # Calculate percentage over/under threshold
        if sla_target.threshold_operator in ["<=", "<"]:
            # For upper bounds (latency, error rate)
            excess_percent = ((value - threshold) / threshold) * 100
        else:
            # For lower bounds (availability, quality)
            excess_percent = ((threshold - value) / threshold) * 100

        if excess_percent >= 50:
            return SeverityLevel.CRITICAL
        elif excess_percent >= 25:
            return SeverityLevel.HIGH
        elif excess_percent >= 10:
            return SeverityLevel.MEDIUM
        else:
            return SeverityLevel.LOW

    def get_sla_compliance_report(self, time_window_hours: int = 24,
                                  tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Generate SLA compliance report."""
        since = datetime.now() - timedelta(hours=time_window_hours)

        # Filter metrics
        filtered_metrics = [
            m for m in self.metrics
            if m.timestamp >= since and (tenant_id is None or m.tenant_id == tenant_id)
        ]

        compliance_report = {
            "report_generated_at": datetime.now().isoformat(),
            "time_window_hours": time_window_hours,
            "tenant_id": tenant_id,
            "total_metrics": len(filtered_metrics),
            "sla_targets": {},
            "overall_compliance": {}
        }

        # Calculate compliance for each SLA target
        for sla_target in self.sla_targets:
            if not sla_target.enabled:
                continue

            target_metrics = [
                m for m in filtered_metrics
                if m.metric_type == sla_target.metric_type
            ]

            if not target_metrics:
                continue

            violations = [m for m in target_metrics if m.is_sla_violation]
            violation_rate = (len(violations) / len(target_metrics)) * 100
            compliance_rate = 100 - violation_rate

            compliance_report["sla_targets"][sla_target.name] = {
                "metric_type": sla_target.metric_type.value,
                "target_value": sla_target.target_value,
                "total_measurements": len(target_metrics),
                "violations": len(violations),
                "violation_rate_percent": violation_rate,
                "compliance_rate_percent": compliance_rate,
                "meets_sla": compliance_rate >= sla_target.violation_threshold_percent
            }

        # Overall compliance
        all_sla_met = all(
            target_data["meets_sla"]
            for target_data in compliance_report["sla_targets"].values()
        )

        compliance_report["overall_compliance"] = {
            "all_slas_met": all_sla_met,
            "total_alerts": len([a for a in self.alerts if a.timestamp >= since]),
            "critical_alerts": len([a for a in self.alerts if a.timestamp >= since and a.severity == SeverityLevel.CRITICAL])
        }

        return compliance_report

    def get_performance_trends(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get performance trends over time window."""
        since = datetime.now() - timedelta(hours=time_window_hours)

        filtered_metrics = [m for m in self.metrics if m.timestamp >= since]

        trends = {}

        for metric_type in MetricType:
            type_metrics = [
                m for m in filtered_metrics if m.metric_type == metric_type]

            if not type_metrics:
                continue

            values = [m.value for m in type_metrics]

            trends[metric_type.value] = {
                "count": len(values),
                "average": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "latest": values[-1] if values else 0,
                "trend": self._calculate_trend(values)
            }

        return {
            "time_window_hours": time_window_hours,
            "trends": trends,
            "generated_at": datetime.now().isoformat()
        }

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from values."""
        if len(values) < 2:
            return "insufficient_data"

        # Simple trend calculation - compare first and second half
        mid = len(values) // 2
        first_half_avg = sum(values[:mid]) / mid if mid > 0 else 0
        second_half_avg = sum(values[mid:]) / (len(values) - mid)

        change_percent = ((second_half_avg - first_half_avg) /
                          first_half_avg * 100) if first_half_avg > 0 else 0

        if change_percent > 5:
            return "increasing"
        elif change_percent < -5:
            return "decreasing"
        else:
            return "stable"


# ================================
# 3. Production RunHooks
# ================================

class ProductionRunHooks(RunHooks):
    """Production-ready RunHooks with comprehensive monitoring."""

    def __init__(self, monitoring_system: ProductionMonitoringSystem, tenant_id: Optional[str] = None):
        self.monitoring_system = monitoring_system
        self.tenant_id = tenant_id
        self.session_id = f"session_{int(time.time())}"
        self.session_start = datetime.now()
        self.agent_timings: Dict[str, float] = {}
        self.total_tools_used = 0
        self.total_handoffs = 0

    async def on_agent_start(self, context: Any, agent: Agent) -> None:
        """Track agent start with production metrics."""
        self.agent_timings[agent.name] = time.time()

        # Record availability metric
        self.monitoring_system.record_metric(
            MetricType.AVAILABILITY,
            100.0,  # Agent started successfully
            agent_name=agent.name,
            tenant_id=self.tenant_id,
            context={"session_id": self.session_id, "event": "agent_start"}
        )

        print(
            f"📊 [PRODUCTION] Agent {agent.name} started - tracking metrics for tenant {self.tenant_id}")

    async def on_agent_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Track agent completion with detailed production metrics."""
        end_time = time.time()
        start_time = self.agent_timings.get(agent.name, end_time)
        latency = end_time - start_time

        # Record latency metric
        self.monitoring_system.record_metric(
            MetricType.LATENCY,
            latency,
            agent_name=agent.name,
            tenant_id=self.tenant_id,
            context={"session_id": self.session_id,
                     "event": "agent_completion"}
        )

        # Assess and record quality score
        quality_score = self._assess_output_quality(output)
        self.monitoring_system.record_metric(
            MetricType.QUALITY_SCORE,
            quality_score,
            agent_name=agent.name,
            tenant_id=self.tenant_id,
            context={"session_id": self.session_id,
                     "output_length": len(str(output))}
        )

        print(
            f"📊 [PRODUCTION] Agent {agent.name} completed - Latency: {latency:.3f}s, Quality: {quality_score:.1f}")

    async def on_handoff(self, context: Any, from_agent: Agent, to_agent: Agent) -> None:
        """Track handoff performance metrics."""
        self.total_handoffs += 1

        # Record handoff as throughput metric
        self.monitoring_system.record_metric(
            MetricType.THROUGHPUT,
            self.total_handoffs,
            agent_name=f"{from_agent.name}→{to_agent.name}",
            tenant_id=self.tenant_id,
            context={"session_id": self.session_id,
                     "handoff_count": self.total_handoffs}
        )

        print(
            f"📊 [PRODUCTION] Handoff #{self.total_handoffs}: {from_agent.name} → {to_agent.name}")

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Track tool usage metrics."""
        self.total_tools_used += 1

        print(
            f"📊 [PRODUCTION] Tool {tool.name} started by {agent.name} (total tools: {self.total_tools_used})")

    async def on_tool_end(self, context: Any, agent: Agent, tool, result: str) -> None:
        """Track tool completion metrics."""
        # Assess tool success rate
        success_rate = 95.0 if "error" not in result.lower() else 5.0

        # Record as inverted error rate (100 - error_rate)
        error_rate = 100.0 - success_rate
        self.monitoring_system.record_metric(
            MetricType.ERROR_RATE,
            error_rate,
            agent_name=agent.name,
            tenant_id=self.tenant_id,
            context={
                "session_id": self.session_id,
                "tool_name": tool.name,
                "result_length": len(result)
            }
        )

        print(
            f"📊 [PRODUCTION] Tool {tool.name} completed - Success rate: {success_rate:.1f}%")

    def _assess_output_quality(self, output: Any) -> float:
        """Assess output quality for production metrics."""
        output_str = str(output)
        quality_score = 50.0  # Base score

        # Length factor
        if 50 <= len(output_str) <= 1000:
            quality_score += 20
        elif len(output_str) > 1000:
            quality_score += 10

        # Content quality indicators
        helpful_words = ["help", "assist", "provide",
                         "support", "recommend", "suggest"]
        if any(word in output_str.lower() for word in helpful_words):
            quality_score += 15

        # Professional tone
        professional_words = ["please", "thank", "appreciate", "understand"]
        if any(word in output_str.lower() for word in professional_words):
            quality_score += 10

        # Completeness indicator
        if "?" not in output_str or any(word in output_str.lower() for word in ["answer", "solution", "resolve"]):
            quality_score += 5

        return min(100.0, max(0.0, quality_score))

    def get_session_summary(self) -> Dict[str, Any]:
        """Get production session summary."""
        session_duration = (
            datetime.now() - self.session_start).total_seconds()

        return {
            "session_id": self.session_id,
            "tenant_id": self.tenant_id,
            "duration_seconds": session_duration,
            "agents_used": list(self.agent_timings.keys()),
            "total_tools_used": self.total_tools_used,
            "total_handoffs": self.total_handoffs,
            "avg_agent_latency": sum(
                time.time() - start_time
                for start_time in self.agent_timings.values()
            ) / len(self.agent_timings) if self.agent_timings else 0,
            "session_throughput": (self.total_tools_used + self.total_handoffs) / session_duration if session_duration > 0 else 0
        }


# ================================
# 4. Production AgentHooks
# ================================

class ProductionAgentHooks(AgentHooks):
    """Production-ready AgentHooks with detailed agent monitoring."""

    def __init__(self, agent_name: str, monitoring_system: ProductionMonitoringSystem, tenant_id: Optional[str] = None):
        self.agent_name = agent_name
        self.monitoring_system = monitoring_system
        self.tenant_id = tenant_id
        self.activation_count = 0
        self.tool_usage_count = 0
        self.average_latency = 0.0
        self.performance_scores: List[float] = []

    async def on_start(self, context: Any, agent: Agent) -> None:
        """Track agent-specific start metrics."""
        self.activation_count += 1

        # Record resource usage metric (simplified)
        # Simulated resource usage
        resource_usage = min(100.0, self.activation_count * 5)
        self.monitoring_system.record_metric(
            MetricType.RESOURCE_USAGE,
            resource_usage,
            agent_name=agent.name,
            tenant_id=self.tenant_id,
            context={"activation_count": self.activation_count}
        )

        print(
            f"🤖 [AGENT {agent.name}] Activation #{self.activation_count} - Resource usage: {resource_usage:.1f}%")

    async def on_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Track agent-specific completion metrics."""
        # Calculate agent-specific quality score
        quality_score = self._calculate_agent_quality(output)
        self.performance_scores.append(quality_score)

        # Update average performance
        avg_performance = sum(self.performance_scores) / \
            len(self.performance_scores)

        print(
            f"🤖 [AGENT {agent.name}] Quality: {quality_score:.1f}, Average: {avg_performance:.1f}")

    async def on_handoff(self, context: Any, agent: Agent, source: Agent) -> None:
        """Track agent-specific handoff metrics."""
        print(f"🤖 [AGENT {agent.name}] Handoff received from {source.name}")

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Track agent-specific tool usage."""
        self.tool_usage_count += 1

        print(
            f"🤖 [AGENT {agent.name}] Tool usage #{self.tool_usage_count}: {tool.name}")

    async def on_tool_end(self, context: Any, agent: Agent, tool, result: str) -> None:
        """Track agent-specific tool completion."""
        print(f"🤖 [AGENT {agent.name}] Tool {tool.name} completed")

    def _calculate_agent_quality(self, output: Any) -> float:
        """Calculate agent-specific quality score."""
        base_score = 60.0  # Higher base for agent-specific assessment
        output_str = str(output)

        # Agent-specific quality factors
        if len(output_str) > 100:
            base_score += 15
        if self.activation_count > 1:
            # Consistency bonus for experienced agent
            base_score += 10
        if self.tool_usage_count > 0:
            # Tool utilization bonus
            base_score += 10

        # Content assessment
        if any(word in output_str.lower() for word in ["comprehensive", "detailed", "thorough"]):
            base_score += 5

        return min(100.0, max(0.0, base_score))

    def get_agent_performance_report(self) -> Dict[str, Any]:
        """Get agent-specific performance report."""
        return {
            "agent_name": self.agent_name,
            "tenant_id": self.tenant_id,
            "total_activations": self.activation_count,
            "total_tool_usage": self.tool_usage_count,
            "performance_scores": self.performance_scores,
            "average_performance": sum(self.performance_scores) / len(self.performance_scores) if self.performance_scores else 0,
            "performance_trend": self._calculate_performance_trend()
        }

    def _calculate_performance_trend(self) -> str:
        """Calculate agent performance trend."""
        if len(self.performance_scores) < 3:
            return "insufficient_data"

        recent_scores = self.performance_scores[-3:]
        older_scores = self.performance_scores[:-
                                               3] if len(self.performance_scores) > 3 else []

        if not older_scores:
            return "new_agent"

        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)

        change = ((recent_avg - older_avg) / older_avg) * 100

        if change > 10:
            return "improving"
        elif change < -10:
            return "declining"
        else:
            return "stable"


# ================================
# 5. Demo Tools and Agents
# ================================

@function_tool
def process_payment(amount: float, currency: str = "USD") -> str:
    """Process a payment transaction."""
    if amount > 1000:
        return f"Payment of {amount} {currency} processed successfully - High value transaction logged"
    return f"Payment of {amount} {currency} processed successfully"


@function_tool
def validate_user(user_id: str) -> str:
    """Validate user credentials and permissions."""
    return f"User {user_id} validated successfully - Premium account confirmed"


@function_tool
def send_confirmation(recipient: str, message: str) -> str:
    """Send confirmation message to recipient."""
    return f"Confirmation sent to {recipient}: {message}"


def create_payment_agent(monitoring_system: ProductionMonitoringSystem, tenant_id: str) -> Agent:
    """Create payment processing agent with production monitoring."""
    agent = Agent(
        name="PaymentAgent",
        instructions="You are a payment processing agent. Handle transactions securely and provide clear confirmations.",
        tools=[process_payment, validate_user, send_confirmation]
    )

    # Attach production hooks
    agent.hooks = ProductionAgentHooks(
        "PaymentAgent", monitoring_system, tenant_id)
    return agent


def create_customer_service_agent(monitoring_system: ProductionMonitoringSystem, tenant_id: str) -> Agent:
    """Create customer service agent with production monitoring."""
    agent = Agent(
        name="CustomerServiceAgent",
        instructions="You are a customer service agent. Provide helpful, professional support and resolve customer issues efficiently.",
        tools=[validate_user, send_confirmation]
    )

    # Attach production hooks
    agent.hooks = ProductionAgentHooks(
        "CustomerServiceAgent", monitoring_system, tenant_id)
    return agent


# ================================
# 6. Demo Functions
# ================================

async def demo_production_monitoring():
    """Demonstrate production monitoring with SLA tracking."""
    print("=== Production Monitoring Demo ===")

    # Create production monitoring system
    monitoring_system = ProductionMonitoringSystem()

    # Multi-tenant demo
    tenants = ["tenant_a", "tenant_b", "tenant_c"]

    for tenant_id in tenants:
        print(f"\n--- Processing requests for {tenant_id} ---")

        # Create production hooks
        production_hooks = ProductionRunHooks(monitoring_system, tenant_id)

        # Create agents
        payment_agent = create_payment_agent(monitoring_system, tenant_id)
        customer_service_agent = create_customer_service_agent(
            monitoring_system, tenant_id)

        # Set up handoffs
        payment_agent.handoffs = [
            handoff(customer_service_agent,
                    tool_name_override="provide_support")
        ]

        # Process multiple requests for this tenant
        requests = [
            "Process a payment of $500 for user123 and send confirmation",
            "Validate user456 and process their $1200 premium payment",
            "Handle customer support request for payment issue"
        ]

        for i, request in enumerate(requests, 1):
            print(f"\n  Request {i}: {request[:50]}...")

            try:
                result = await Runner.run(
                    payment_agent,
                    input=request,
                    hooks=production_hooks
                )

                print(f"  ✅ Request completed successfully")

            except Exception as e:
                print(f"  ❌ Request failed: {e}")

                # Record error metric
                monitoring_system.record_metric(
                    MetricType.ERROR_RATE,
                    100.0,  # 100% error for this request
                    tenant_id=tenant_id,
                    context={"error": str(e), "request": request}
                )

            # Brief pause between requests
            await asyncio.sleep(0.3)

        # Get session summary
        session_summary = production_hooks.get_session_summary()
        print(f"\n  📋 Session Summary for {tenant_id}:")
        print(f"    Duration: {session_summary['duration_seconds']:.2f}s")
        print(f"    Tools Used: {session_summary['total_tools_used']}")
        print(f"    Handoffs: {session_summary['total_handoffs']}")
        print(f"    Avg Latency: {session_summary['avg_agent_latency']:.3f}s")


async def demo_sla_compliance_reporting():
    """Demonstrate SLA compliance monitoring and reporting."""
    print("\n=== SLA Compliance Reporting Demo ===")

    # Create monitoring system (already has data from previous demo)
    monitoring_system = ProductionMonitoringSystem()

    # Simulate some additional metrics to test SLA violations
    print("Simulating various performance scenarios...")

    # Good performance
    for i in range(5):
        monitoring_system.record_metric(
            MetricType.LATENCY, 1.5, "FastAgent", "tenant_a")
        monitoring_system.record_metric(
            MetricType.QUALITY_SCORE, 85.0, "FastAgent", "tenant_a")

    # Poor performance (SLA violations)
    for i in range(3):
        monitoring_system.record_metric(
            MetricType.LATENCY, 5.0, "SlowAgent", "tenant_b")  # Violates 2s SLA
        monitoring_system.record_metric(
            MetricType.ERROR_RATE, 10.0, "SlowAgent", "tenant_b")  # Violates 1% SLA

    # Generate compliance reports
    for tenant_id in ["tenant_a", "tenant_b", "overall"]:
        print(f"\n--- SLA Compliance Report for {tenant_id} ---")

        report = monitoring_system.get_sla_compliance_report(
            time_window_hours=1,
            tenant_id=tenant_id if tenant_id != "overall" else None
        )

        print(f"  Report Period: {report['time_window_hours']} hours")
        print(f"  Total Metrics: {report['total_metrics']}")
        print(
            f"  Overall SLAs Met: {report['overall_compliance']['all_slas_met']}")
        print(
            f"  Total Alerts: {report['overall_compliance']['total_alerts']}")
        print(
            f"  Critical Alerts: {report['overall_compliance']['critical_alerts']}")

        print("  SLA Target Details:")
        for sla_name, sla_data in report['sla_targets'].items():
            status = "✅ PASS" if sla_data['meets_sla'] else "❌ FAIL"
            print(f"    {sla_name}: {status}")
            print(
                f"      Compliance Rate: {sla_data['compliance_rate_percent']:.1f}%")
            print(
                f"      Violations: {sla_data['violations']}/{sla_data['total_measurements']}")


async def demo_performance_trends_analysis():
    """Demonstrate performance trends and capacity planning."""
    print("\n=== Performance Trends Analysis Demo ===")

    # Create fresh monitoring system for trends demo
    monitoring_system = ProductionMonitoringSystem()

    # Simulate performance data over time with trends
    print("Simulating performance data with various trends...")

    # Simulate improving latency trend
    for i in range(10):
        latency = 3.0 - (i * 0.2)  # Improving from 3s to 1s
        monitoring_system.record_metric(
            MetricType.LATENCY, max(0.5, latency), "OptimizedAgent")

    # Simulate degrading quality trend
    for i in range(10):
        quality = 90.0 - (i * 2)  # Degrading from 90 to 70
        monitoring_system.record_metric(
            MetricType.QUALITY_SCORE, max(50, quality), "DegradingAgent")

    # Simulate stable error rate
    for i in range(10):
        error_rate = 0.5  # Stable at 0.5%
        monitoring_system.record_metric(
            MetricType.ERROR_RATE, error_rate, "StableAgent")

    # Generate trends report
    trends_report = monitoring_system.get_performance_trends(
        time_window_hours=1)

    print(f"\n📈 Performance Trends Report:")
    print(f"  Time Window: {trends_report['time_window_hours']} hours")
    print(f"  Generated At: {trends_report['generated_at']}")

    for metric_name, trend_data in trends_report['trends'].items():
        print(f"\n  {metric_name.upper()}:")
        print(f"    Count: {trend_data['count']}")
        print(f"    Average: {trend_data['average']:.2f}")
        print(f"    Range: {trend_data['min']:.2f} - {trend_data['max']:.2f}")
        print(f"    Latest: {trend_data['latest']:.2f}")
        print(f"    Trend: {trend_data['trend'].upper()}")

        # Provide recommendations based on trends
        if trend_data['trend'] == 'increasing' and metric_name in ['latency', 'error_rate']:
            print(
                f"    🚨 RECOMMENDATION: {metric_name} is increasing - investigate and optimize")
        elif trend_data['trend'] == 'decreasing' and metric_name in ['quality_score', 'availability']:
            print(
                f"    🚨 RECOMMENDATION: {metric_name} is decreasing - immediate attention required")
        elif trend_data['trend'] == 'improving':
            print(
                f"    ✅ GOOD: {metric_name} is improving - continue current optimizations")


# ================================
# 7. Main Demo Function
# ================================

async def main():
    """Run all production lifecycle pattern demonstrations."""
    print("🏭 OpenAI Agents SDK - Production Lifecycle Patterns")
    print("=" * 60)

    # Run all demonstrations
    await demo_production_monitoring()
    await demo_sla_compliance_reporting()
    await demo_performance_trends_analysis()

    print("\n" + "=" * 60)
    print("✅ Production lifecycle patterns demonstration complete!")
    print("\nKey Production Features Demonstrated:")
    print("1. Multi-tenant monitoring and metrics collection")
    print("2. SLA compliance tracking and violation alerting")
    print("3. Performance trends analysis and capacity planning")
    print("4. Enterprise-grade observability and reporting")
    print("5. Automated alert generation and escalation")
    print("6. Production-ready performance optimization")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())


# ================================
# 8. Production Implementation Notes
# ================================

"""
Production Lifecycle Implementation Guide:

1. **Monitoring Infrastructure**:
   - Integrate with enterprise monitoring (Datadog, New Relic, Prometheus)
   - Use time-series databases for metric storage
   - Implement distributed tracing for complex workflows
   - Set up log aggregation and analysis

2. **SLA Management**:
   - Define business-critical SLA targets
   - Implement automated SLA violation alerts
   - Create escalation policies for critical issues
   - Generate compliance reports for stakeholders

3. **Performance Optimization**:
   - Implement automated performance tuning
   - Use machine learning for anomaly detection
   - Set up capacity planning and forecasting
   - Enable real-time performance dashboards

4. **Multi-Tenant Support**:
   - Isolate tenant metrics and alerts
   - Implement tenant-specific SLA targets
   - Provide tenant performance dashboards
   - Enable tenant-level resource quotas

5. **Enterprise Integration**:
   - Connect to ITSM systems (ServiceNow, Jira)
   - Integrate with notification systems (PagerDuty, Slack)
   - Export metrics to data warehouses
   - Enable API access for custom dashboards

6. **Compliance and Auditing**:
   - Maintain detailed audit logs
   - Generate compliance reports
   - Track data retention policies
   - Implement security monitoring
"""
