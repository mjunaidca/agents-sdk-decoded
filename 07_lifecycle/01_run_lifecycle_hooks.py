"""
01_run_lifecycle_hooks.py

This example demonstrates RunHooks - global lifecycle event monitoring that tracks
events across all agents in a run session. RunHooks are useful for system-wide
monitoring, logging, analytics, and orchestration across multiple agents.

Key Concepts:
- RunHooks for global lifecycle monitoring
- Event tracking across agent transitions
- Performance monitoring and metrics collection
- System-wide logging and observability
- Cross-agent analytics and insights

Based on: https://openai.github.io/openai-agents-python/ref/lifecycle/
"""

import asyncio
import time
from typing import Any, Dict, List
from datetime import datetime

from agents import Agent, Runner, handoff, function_tool
from agents.lifecycle import RunHooks


# ================================
# 1. Basic RunHooks Implementation
# ================================

class BasicRunHooks(RunHooks):
    """Basic implementation of RunHooks for lifecycle monitoring."""

    def __init__(self):
        self.events = []
        self.start_time = None
        self.agent_switches = 0
        self.tool_calls = 0

    async def on_agent_start(self, context: Any, agent: Agent) -> None:
        """Called before the agent is invoked."""
        event_time = datetime.now()
        if self.start_time is None:
            self.start_time = event_time

        self.events.append({
            "type": "agent_start",
            "agent_name": agent.name,
            "timestamp": event_time,
            "context_id": id(context)
        })

        print(
            f"🚀 [AGENT START] {agent.name} at {event_time.strftime('%H:%M:%S.%f')[:-3]}")

    async def on_agent_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Called when the agent produces a final output."""
        event_time = datetime.now()

        self.events.append({
            "type": "agent_end",
            "agent_name": agent.name,
            "timestamp": event_time,
            "output_preview": str(output)[:100] + "..." if len(str(output)) > 100 else str(output),
            "context_id": id(context)
        })

        print(
            f"🏁 [AGENT END] {agent.name} completed at {event_time.strftime('%H:%M:%S.%f')[:-3]}")

    async def on_handoff(self, context: Any, from_agent: Agent, to_agent: Agent) -> None:
        """Called when a handoff occurs."""
        event_time = datetime.now()
        self.agent_switches += 1

        self.events.append({
            "type": "handoff",
            "from_agent": from_agent.name,
            "to_agent": to_agent.name,
            "timestamp": event_time,
            "handoff_number": self.agent_switches,
            "context_id": id(context)
        })

        print(
            f"🔄 [HANDOFF #{self.agent_switches}] {from_agent.name} → {to_agent.name} at {event_time.strftime('%H:%M:%S.%f')[:-3]}")

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Called before a tool is invoked."""
        event_time = datetime.now()
        self.tool_calls += 1

        self.events.append({
            "type": "tool_start",
            "agent_name": agent.name,
            "tool_name": tool.name,
            "timestamp": event_time,
            "tool_call_number": self.tool_calls,
            "context_id": id(context)
        })

        print(
            f"🔧 [TOOL START #{self.tool_calls}] {agent.name} calling {tool.name} at {event_time.strftime('%H:%M:%S.%f')[:-3]}")

    async def on_tool_end(self, context: Any, agent: Agent, tool, result: str) -> None:
        """Called after a tool is invoked."""
        event_time = datetime.now()

        self.events.append({
            "type": "tool_end",
            "agent_name": agent.name,
            "tool_name": tool.name,
            "timestamp": event_time,
            "result_preview": result[:50] + "..." if len(result) > 50 else result,
            "context_id": id(context)
        })

        print(
            f"✅ [TOOL END] {agent.name} finished {tool.name} at {event_time.strftime('%H:%M:%S.%f')[:-3]}")

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all lifecycle events."""
        if not self.events or self.start_time is None:
            return {"status": "No events recorded"}

        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()

        # Count events by type
        event_counts = {}
        for event in self.events:
            event_type = event["type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        # Get unique agents
        unique_agents = set()
        for event in self.events:
            if "agent_name" in event:
                unique_agents.add(event["agent_name"])

        return {
            "total_duration_seconds": round(total_duration, 3),
            "total_events": len(self.events),
            "event_breakdown": event_counts,
            "unique_agents": list(unique_agents),
            "agent_switches": self.agent_switches,
            "tool_calls": self.tool_calls,
            "events_per_second": round(len(self.events) / total_duration, 2) if total_duration > 0 else 0
        }


# ================================
# 2. Advanced Performance Monitoring RunHooks
# ================================

class PerformanceMonitoringHooks(RunHooks):
    """Advanced RunHooks for detailed performance monitoring."""

    def __init__(self):
        self.performance_data = {
            "agents": {},
            "tools": {},
            "handoffs": [],
            "session_start": None,
            "memory_snapshots": []
        }
        self.active_operations = {}

    async def on_agent_start(self, context: Any, agent: Agent) -> None:
        """Track agent performance metrics."""
        start_time = time.time()

        if self.performance_data["session_start"] is None:
            self.performance_data["session_start"] = start_time

        # Initialize agent tracking
        if agent.name not in self.performance_data["agents"]:
            self.performance_data["agents"][agent.name] = {
                "activations": 0,
                "total_time": 0,
                "start_times": [],
                "peak_memory": 0
            }

        self.performance_data["agents"][agent.name]["activations"] += 1
        self.active_operations[f"agent_{agent.name}"] = start_time

        print(
            f"📊 [PERF] Agent {agent.name} started (activation #{self.performance_data['agents'][agent.name]['activations']})")

    async def on_agent_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Calculate agent performance metrics."""
        end_time = time.time()
        operation_key = f"agent_{agent.name}"

        if operation_key in self.active_operations:
            duration = end_time - self.active_operations[operation_key]
            self.performance_data["agents"][agent.name]["total_time"] += duration
            del self.active_operations[operation_key]

            print(f"📊 [PERF] Agent {agent.name} completed in {duration:.3f}s")

    async def on_handoff(self, context: Any, from_agent: Agent, to_agent: Agent) -> None:
        """Track handoff performance."""
        handoff_time = time.time()

        handoff_data = {
            "from": from_agent.name,
            "to": to_agent.name,
            "timestamp": handoff_time,
            "session_time": handoff_time - self.performance_data["session_start"] if self.performance_data["session_start"] else 0
        }

        self.performance_data["handoffs"].append(handoff_data)
        print(
            f"📊 [PERF] Handoff {from_agent.name} → {to_agent.name} at session time {handoff_data['session_time']:.3f}s")

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Track tool performance."""
        start_time = time.time()

        if tool.name not in self.performance_data["tools"]:
            self.performance_data["tools"][tool.name] = {
                "calls": 0,
                "total_time": 0,
                "average_time": 0,
                "called_by_agents": set()
            }

        self.performance_data["tools"][tool.name]["calls"] += 1
        self.performance_data["tools"][tool.name]["called_by_agents"].add(
            agent.name)
        self.active_operations[f"tool_{tool.name}_{agent.name}"] = start_time

        print(
            f"📊 [PERF] Tool {tool.name} started by {agent.name} (call #{self.performance_data['tools'][tool.name]['calls']})")

    async def on_tool_end(self, context: Any, agent: Agent, tool, result: str) -> None:
        """Calculate tool performance metrics."""
        end_time = time.time()
        operation_key = f"tool_{tool.name}_{agent.name}"

        if operation_key in self.active_operations:
            duration = end_time - self.active_operations[operation_key]
            tool_data = self.performance_data["tools"][tool.name]
            tool_data["total_time"] += duration
            tool_data["average_time"] = tool_data["total_time"] / \
                tool_data["calls"]
            del self.active_operations[operation_key]

            print(
                f"📊 [PERF] Tool {tool.name} completed in {duration:.3f}s (avg: {tool_data['average_time']:.3f}s)")

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        # Convert sets to lists for JSON serialization
        tools_report = {}
        for tool_name, data in self.performance_data["tools"].items():
            tools_report[tool_name] = {
                **data,
                "called_by_agents": list(data["called_by_agents"])
            }

        total_session_time = time.time() - \
            self.performance_data["session_start"] if self.performance_data["session_start"] else 0

        return {
            "session_duration": round(total_session_time, 3),
            "agents_performance": self.performance_data["agents"],
            "tools_performance": tools_report,
            "handoffs_timeline": self.performance_data["handoffs"],
            "efficiency_metrics": {
                "total_agent_time": sum(data["total_time"] for data in self.performance_data["agents"].values()),
                "total_tool_time": sum(data["total_time"] for data in self.performance_data["tools"].values()),
                "handoff_frequency": len(self.performance_data["handoffs"]) / total_session_time if total_session_time > 0 else 0
            }
        }


# ================================
# 3. Security & Audit RunHooks
# ================================

class SecurityAuditHooks(RunHooks):
    """RunHooks for security monitoring and audit trails."""

    def __init__(self):
        self.audit_log = []
        self.security_events = []
        self.access_patterns = {}
        self.sensitive_data_accessed = []

    async def on_agent_start(self, context: Any, agent: Agent) -> None:
        """Log agent activation for security audit."""
        audit_entry = {
            "event_type": "AGENT_ACTIVATION",
            "agent_name": agent.name,
            "timestamp": datetime.now().isoformat(),
            "context_id": str(id(context)),
            "session_id": getattr(context, 'session_id', 'unknown')
        }

        self.audit_log.append(audit_entry)

        # Track access patterns
        if agent.name not in self.access_patterns:
            self.access_patterns[agent.name] = {
                "activations": 0,
                "first_access": datetime.now().isoformat(),
                "last_access": datetime.now().isoformat(),
                "tools_accessed": set()
            }

        self.access_patterns[agent.name]["activations"] += 1
        self.access_patterns[agent.name]["last_access"] = datetime.now(
        ).isoformat()

        print(
            f"🔒 [AUDIT] Agent {agent.name} activated - Session: {audit_entry['session_id']}")

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Monitor tool access for security compliance."""
        audit_entry = {
            "event_type": "TOOL_ACCESS",
            "agent_name": agent.name,
            "tool_name": tool.name,
            "timestamp": datetime.now().isoformat(),
            "context_id": str(id(context))
        }

        self.audit_log.append(audit_entry)

        # Track tool access patterns
        if agent.name in self.access_patterns:
            self.access_patterns[agent.name]["tools_accessed"].add(tool.name)

        # Check for sensitive operations
        sensitive_tools = ["delete_data", "modify_permissions",
                           "access_credentials", "export_data"]
        if tool.name in sensitive_tools:
            security_event = {
                "type": "SENSITIVE_TOOL_ACCESS",
                "agent": agent.name,
                "tool": tool.name,
                "timestamp": datetime.now().isoformat(),
                "requires_review": True
            }
            self.security_events.append(security_event)
            print(
                f"⚠️  [SECURITY] Sensitive tool access: {agent.name} → {tool.name}")

        print(f"🔒 [AUDIT] Tool access: {agent.name} → {tool.name}")

    async def on_handoff(self, context: Any, from_agent: Agent, to_agent: Agent) -> None:
        """Log agent handoffs for audit trail."""
        audit_entry = {
            "event_type": "AGENT_HANDOFF",
            "from_agent": from_agent.name,
            "to_agent": to_agent.name,
            "timestamp": datetime.now().isoformat(),
            "context_id": str(id(context))
        }

        self.audit_log.append(audit_entry)

        # Check for privilege escalation patterns
        privileged_agents = ["admin_agent", "security_agent", "system_agent"]
        if to_agent.name in privileged_agents and from_agent.name not in privileged_agents:
            security_event = {
                "type": "PRIVILEGE_ESCALATION",
                "from_agent": from_agent.name,
                "to_agent": to_agent.name,
                "timestamp": datetime.now().isoformat(),
                "requires_review": True
            }
            self.security_events.append(security_event)
            print(
                f"⚠️  [SECURITY] Potential privilege escalation: {from_agent.name} → {to_agent.name}")

        print(f"🔒 [AUDIT] Agent handoff: {from_agent.name} → {to_agent.name}")

    def get_audit_report(self) -> Dict[str, Any]:
        """Generate security audit report."""
        # Convert sets to lists for serialization
        access_patterns_report = {}
        for agent_name, data in self.access_patterns.items():
            access_patterns_report[agent_name] = {
                **data,
                "tools_accessed": list(data["tools_accessed"])
            }

        return {
            "audit_summary": {
                "total_events": len(self.audit_log),
                "security_events": len(self.security_events),
                "agents_tracked": len(self.access_patterns),
                "report_generated": datetime.now().isoformat()
            },
            "security_events": self.security_events,
            "access_patterns": access_patterns_report,
            # Last 50 events for brevity
            "full_audit_log": self.audit_log[-50:]
        }


# ================================
# 4. Demo Tools and Agents
# ================================

@function_tool
def get_user_data(user_id: str) -> str:
    """Retrieve user data - simulates data access."""
    return f"User data for {user_id}: name=John Doe, email=john@example.com"


@function_tool
def process_payment(amount: float) -> str:
    """Process payment - simulates financial operation."""
    return f"Payment of ${amount} processed successfully"


@function_tool
def delete_data(data_id: str) -> str:
    """Delete data - simulates sensitive operation."""
    return f"Data {data_id} has been deleted"


def create_customer_service_agent() -> Agent:
    """Create customer service agent."""
    return Agent(
        name="CustomerServiceAgent",
        instructions="You are a customer service agent. Help customers with their inquiries.",
        tools=[get_user_data]
    )


def create_billing_agent() -> Agent:
    """Create billing agent."""
    return Agent(
        name="BillingAgent",
        instructions="You are a billing specialist. Handle payment and billing inquiries.",
        tools=[process_payment, get_user_data]
    )


def create_admin_agent() -> Agent:
    """Create admin agent with elevated permissions."""
    return Agent(
        name="AdminAgent",
        instructions="You are an admin agent with elevated permissions for system operations.",
        tools=[delete_data, get_user_data, process_payment]
    )


# ================================
# 5. Demo Functions
# ================================

async def demo_basic_run_hooks():
    """Demonstrate basic RunHooks functionality."""
    print("=== Basic RunHooks Demo ===")

    # Create agents with handoffs
    customer_agent = create_customer_service_agent()
    billing_agent = create_billing_agent()

    # Set up handoffs
    customer_agent.handoffs = [
        handoff(billing_agent, tool_name_override="transfer_to_billing")
    ]

    # Create RunHooks instance
    hooks = BasicRunHooks()

    # Run with hooks
    result = await Runner.run(
        customer_agent,
        input="I need help with my account and billing",
        hooks=hooks
    )

    print(f"\nFinal Result: {result.final_output}")

    # Show summary
    summary = hooks.get_summary()
    print(f"\n📊 Run Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")


async def demo_performance_monitoring():
    """Demonstrate performance monitoring hooks."""
    print("\n=== Performance Monitoring Demo ===")

    # Create agents
    customer_agent = create_customer_service_agent()
    billing_agent = create_billing_agent()
    admin_agent = create_admin_agent()

    # Set up complex handoff chain
    customer_agent.handoffs = [
        handoff(billing_agent, tool_name_override="transfer_to_billing"),
        handoff(admin_agent, tool_name_override="escalate_to_admin")
    ]
    billing_agent.handoffs = [
        handoff(admin_agent, tool_name_override="escalate_to_admin")
    ]

    # Create performance monitoring hooks
    perf_hooks = PerformanceMonitoringHooks()

    # Run complex workflow
    result = await Runner.run(
        customer_agent,
        input="I need to delete my account data and get a refund",
        hooks=perf_hooks
    )

    print(f"\nFinal Result: {result.final_output}")

    # Show performance report
    report = perf_hooks.get_performance_report()
    print(f"\n📈 Performance Report:")
    print(f"  Session Duration: {report['session_duration']}s")
    print(f"  Agents Performance: {report['agents_performance']}")
    print(f"  Tools Performance: {report['tools_performance']}")
    print(f"  Efficiency Metrics: {report['efficiency_metrics']}")


async def demo_security_audit():
    """Demonstrate security audit hooks."""
    print("\n=== Security Audit Demo ===")

    # Create agents with different privilege levels
    customer_agent = create_customer_service_agent()
    admin_agent = create_admin_agent()

    # Set up potential privilege escalation
    customer_agent.handoffs = [
        handoff(admin_agent, tool_name_override="escalate_to_admin")
    ]

    # Create security audit hooks
    security_hooks = SecurityAuditHooks()

    # Run with security monitoring
    result = await Runner.run(
        customer_agent,
        input="I need to delete some data from the system",
        hooks=security_hooks
    )

    print(f"\nFinal Result: {result.final_output}")

    # Show audit report
    audit_report = security_hooks.get_audit_report()
    print(f"\n🔒 Security Audit Report:")
    print(f"  Total Events: {audit_report['audit_summary']['total_events']}")
    print(
        f"  Security Events: {audit_report['audit_summary']['security_events']}")
    if audit_report['security_events']:
        print(f"  Security Alerts:")
        for event in audit_report['security_events']:
            print(
                f"    - {event['type']}: {event.get('agent', 'N/A')} → {event.get('tool', event.get('to_agent', 'N/A'))}")


async def demo_combined_hooks():
    """Demonstrate combining multiple hook types."""
    print("\n=== Combined Hooks Demo ===")

    # Create all hooks
    basic_hooks = BasicRunHooks()
    perf_hooks = PerformanceMonitoringHooks()
    security_hooks = SecurityAuditHooks()

    # Note: In practice, you'd create a composite hooks class or use a monitoring system
    # For this demo, we'll run with basic hooks and show how to combine insights

    # Create complex agent setup
    customer_agent = create_customer_service_agent()
    billing_agent = create_billing_agent()
    admin_agent = create_admin_agent()

    customer_agent.handoffs = [
        handoff(billing_agent, tool_name_override="transfer_to_billing"),
        handoff(admin_agent, tool_name_override="escalate_to_admin")
    ]

    # Run with basic hooks (in production, you'd implement a composite hooks pattern)
    result = await Runner.run(
        customer_agent,
        input="I have a billing issue that may require admin intervention",
        hooks=basic_hooks
    )

    print(f"\nFinal Result: {result.final_output}")

    # Show combined insights
    summary = basic_hooks.get_summary()
    print(f"\n🔄 Combined Monitoring Summary:")
    print(f"  Total Events: {summary['total_events']}")
    print(f"  Agent Switches: {summary['agent_switches']}")
    print(f"  Tool Calls: {summary['tool_calls']}")
    print(f"  Duration: {summary['total_duration_seconds']}s")
    print(f"  Events/Second: {summary['events_per_second']}")


# ================================
# 6. Main Demo Function
# ================================

async def main():
    """Run all RunHooks demonstrations."""
    print("🔄 OpenAI Agents SDK - Run Lifecycle Hooks")
    print("=" * 60)

    # Run all demonstrations
    await demo_basic_run_hooks()
    await demo_performance_monitoring()
    await demo_security_audit()
    await demo_combined_hooks()

    print("\n" + "=" * 60)
    print("✅ Run lifecycle hooks demonstration complete!")
    print("\nKey Takeaways:")
    print("1. RunHooks provide global monitoring across all agents")
    print("2. Performance monitoring helps optimize multi-agent workflows")
    print("3. Security audit trails ensure compliance and governance")
    print("4. Combined hooks enable comprehensive system observability")
    print("5. Lifecycle events are crucial for production monitoring")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())


# ================================
# 7. Production Implementation Notes
# ================================

"""
RunHooks Production Patterns:

1. **Monitoring & Observability**:
   - Integrate with monitoring systems (Prometheus, DataDog)
   - Stream events to logging infrastructure (ELK, CloudWatch)
   - Set up alerting for anomalous patterns
   - Track SLA compliance and performance metrics

2. **Security & Compliance**:
   - Audit trails for regulatory compliance (SOX, GDPR, HIPAA)
   - Real-time security event detection
   - Access pattern analysis and anomaly detection
   - Integration with SIEM systems

3. **Performance Optimization**:
   - Identify bottlenecks in agent workflows
   - Optimize handoff patterns and timing
   - Monitor resource utilization
   - A/B testing for workflow improvements

4. **Business Intelligence**:
   - Track agent effectiveness and usage patterns
   - Analyze customer journey through agent handoffs
   - Measure resolution times and success rates
   - Generate insights for process improvement

5. **Error Handling & Recovery**:
   - Detect and respond to failed operations
   - Implement automatic recovery strategies
   - Track error patterns and root causes
   - Enable circuit breaker patterns

6. **Scalability Considerations**:
   - Efficient event storage and processing
   - Asynchronous event handling to avoid blocking
   - Event filtering and sampling for high-volume systems
   - Distributed monitoring across multiple instances
"""
