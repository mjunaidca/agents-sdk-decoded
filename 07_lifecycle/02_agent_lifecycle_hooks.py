"""
02_agent_lifecycle_hooks.py

This example demonstrates AgentHooks - agent-specific lifecycle event monitoring
that allows individual agents to customize their behavior and track their own
performance. AgentHooks are useful for agent-specific optimization, personalization,
and specialized handling.

Key Concepts:
- AgentHooks for individual agent monitoring
- Agent-specific behavior customization
- Per-agent performance tracking and optimization
- Specialized agent lifecycle patterns
- Agent self-monitoring and adaptation

Based on: https://openai.github.io/openai-agents-python/ref/lifecycle/
"""

import asyncio
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from agents import Agent, Runner, handoff, function_tool, RunContextWrapper
from agents.lifecycle import AgentHooks



# ================================
# 1. Data Models for Agent Tracking
# ================================

@dataclass
class AgentPerformanceMetrics:
    """Performance metrics for an individual agent."""
    agent_name: str
    activations: int = 0
    total_processing_time: float = 0.0
    average_processing_time: float = 0.0
    tool_usage_count: int = 0
    handoffs_received: int = 0
    handoffs_given: int = 0
    success_rate: float = 100.0
    last_activation: Optional[datetime] = None
    response_quality_scores: List[float] = field(default_factory=list)


@dataclass
class AgentLearningData:
    """Learning and adaptation data for an agent."""
    successful_patterns: List[str] = field(default_factory=list)
    failed_patterns: List[str] = field(default_factory=list)
    user_feedback: List[Dict[str, Any]] = field(default_factory=list)
    optimization_suggestions: List[str] = field(default_factory=list)
    adaptation_history: List[Dict[str, Any]] = field(default_factory=list)


# ================================
# 2. Basic AgentHooks Implementation
# ================================

class BasicAgentHooks(AgentHooks):
    """Basic implementation of AgentHooks for individual agent monitoring."""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.activation_count = 0
        self.start_time: Optional[float] = None
        self.processing_times: List[float] = []
        self.tools_used: List[Dict[str, Any]] = []
        self.context_data: Dict[str, Any] = {}

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        """Called before the agent is invoked."""
        self.start_time = time.time()
        self.activation_count += 1
        
        print(f"🤖 [{agent.name}] Starting activation CONTEXT {context}")

        # Store context information
        self.context_data = {
            "activation_number": self.activation_count,
            "start_time": datetime.now().isoformat(),
            "context_id": str(id(context))
        }

        print(f"🤖 [{agent.name}] Starting activation #{self.activation_count} at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")

        # Agent-specific initialization
        if self.activation_count == 1:
            print(f"🎯 [{agent.name}] First activation - initializing agent state")
        elif self.activation_count > 10:
            avg_time = sum(self.processing_times) / \
                len(self.processing_times) if self.processing_times else 0
            print(
                f"📈 [{agent.name}] Experienced agent (10+ activations) - average processing time: {avg_time:.3f}s")

    async def on_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Called when the agent produces a final output."""
        if self.start_time:
            processing_time = time.time() - self.start_time
            self.processing_times.append(processing_time)

            # Calculate running statistics
            avg_time = sum(self.processing_times) / len(self.processing_times)

            print(
                f"✅ [{agent.name}] Completed in {processing_time:.3f}s (avg: {avg_time:.3f}s)")

            # Agent-specific performance feedback
            if processing_time > 5.0:
                print(
                    f"⚠️  [{agent.name}] Slow processing detected - consider optimization")
            elif processing_time < 1.0:
                print(
                    f"🚀 [{agent.name}] Fast processing - excellent performance!")

    async def on_handoff(self, context: Any, agent: Agent, source: Agent) -> None:
        """Called when the agent is being handed off to."""
        print(f"🔄 [{agent.name}] Receiving handoff from {source.name}")

        # Agent-specific handoff preparation
        if source.name != agent.name:
            print(
                f"📝 [{agent.name}] Preparing to handle context from {source.name}")

            # Store handoff information
            self.context_data["received_handoff_from"] = source.name
            self.context_data["handoff_time"] = datetime.now().isoformat()

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Called before a tool is invoked."""
        self.tools_used.append({
            "tool_name": tool.name,
            "start_time": time.time(),
            "activation": self.activation_count
        })

        print(f"🔧 [{agent.name}] Using tool: {tool.name}")

        # Agent-specific tool optimization
        tool_count = len(
            [t for t in self.tools_used if t["tool_name"] == tool.name])
        if tool_count > 5:
            print(
                f"💡 [{agent.name}] Frequent tool usage detected for {tool.name} (used {tool_count} times)")

    async def on_tool_end(self, context: Any, agent: Agent, tool, result: str) -> None:
        """Called after a tool is invoked."""
        # Find the corresponding tool start
        for tool_usage in reversed(self.tools_used):
            if tool_usage["tool_name"] == tool.name and "end_time" not in tool_usage:
                tool_usage["end_time"] = time.time()
                tool_usage["duration"] = tool_usage["end_time"] - \
                    tool_usage["start_time"]
                tool_usage["result_length"] = len(result)
                break

        print(f"✅ [{agent.name}] Tool {tool.name} completed")

    def get_agent_summary(self) -> Dict[str, Any]:
        """Get performance summary for this specific agent."""
        if not self.processing_times:
            return {"agent": self.agent_name, "status": "No activations yet"}

        completed_tools = [t for t in self.tools_used if "duration" in t]

        return {
            "agent_name": self.agent_name,
            "total_activations": self.activation_count,
            "average_processing_time": sum(self.processing_times) / len(self.processing_times),
            "fastest_processing": min(self.processing_times),
            "slowest_processing": max(self.processing_times),
            "total_tools_used": len(self.tools_used),
            "unique_tools": len(set(t["tool_name"] for t in self.tools_used)),
            "average_tool_time": sum(t["duration"] for t in completed_tools) / len(completed_tools) if completed_tools else 0,
            "context_data": self.context_data
        }


# ================================
# 3. Advanced Performance Tracking AgentHooks
# ================================

class PerformanceTrackingHooks(AgentHooks):
    """Advanced AgentHooks for detailed performance tracking and optimization."""

    def __init__(self, agent_name: str):
        self.metrics = AgentPerformanceMetrics(agent_name=agent_name)
        self.session_data: List[Dict[str, Any]] = []
        self.optimization_recommendations: List[str] = []

    async def on_start(self, context: Any, agent: Agent) -> None:
        """Track detailed performance metrics on agent start."""
        start_time = time.time()
        self.metrics.activations += 1
        self.metrics.last_activation = datetime.now()

        # Start new session tracking
        session = {
            "session_id": self.metrics.activations,
            "start_time": start_time,
            "context_id": str(id(context)),
            "input_preview": str(getattr(context, 'input', 'N/A'))[:100]
        }
        self.session_data.append(session)

        print(
            f"📊 [{agent.name}] Performance tracking started - Session #{self.metrics.activations}")

        # Performance-based recommendations
        if self.metrics.activations > 5:
            if self.metrics.average_processing_time > 3.0:
                recommendation = f"Consider optimizing {agent.name} - average processing time is {self.metrics.average_processing_time:.2f}s"
                if recommendation not in self.optimization_recommendations:
                    self.optimization_recommendations.append(recommendation)
                    print(
                        f"💡 [{agent.name}] Optimization suggestion: {recommendation}")

    async def on_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Calculate detailed performance metrics on agent end."""
        end_time = time.time()

        # Find current session
        current_session = None
        for session in reversed(self.session_data):
            if "end_time" not in session:
                current_session = session
                break

        if current_session:
            processing_time = end_time - current_session["start_time"]
            current_session["end_time"] = end_time
            current_session["processing_time"] = processing_time
            current_session["output_preview"] = str(output)[:100]

            # Update metrics
            self.metrics.total_processing_time += processing_time
            self.metrics.average_processing_time = self.metrics.total_processing_time / \
                self.metrics.activations

            # Quality assessment (simplified)
            quality_score = self._assess_response_quality(
                output, processing_time)
            self.metrics.response_quality_scores.append(quality_score)

            print(
                f"📊 [{agent.name}] Session completed - Time: {processing_time:.3f}s, Quality: {quality_score:.2f}")

    async def on_handoff(self, context: Any, agent: Agent, source: Agent) -> None:
        """Track handoff performance."""
        self.metrics.handoffs_received += 1

        # Analyze handoff patterns
        if self.metrics.handoffs_received > 3:
            handoff_rate = self.metrics.handoffs_received / self.metrics.activations
            if handoff_rate > 0.5:
                print(
                    f"📈 [{agent.name}] High handoff rate detected: {handoff_rate:.2f} (receiving many handoffs)")

        print(
            f"📊 [{agent.name}] Handoff received from {source.name} (total: {self.metrics.handoffs_received})")

    async def on_tool_start(self, context: Any, agent: Agent, tool) -> None:
        """Track tool usage performance."""
        self.metrics.tool_usage_count += 1

        # Find current session and add tool tracking
        for session in reversed(self.session_data):
            if "end_time" not in session:
                if "tools_used" not in session:
                    session["tools_used"] = []
                session["tools_used"].append({
                    "tool_name": tool.name,
                    "start_time": time.time()
                })
                break

        print(
            f"📊 [{agent.name}] Tool usage: {tool.name} (total tools used: {self.metrics.tool_usage_count})")

    async def on_tool_end(self, context: Any, agent: Agent, tool, result: str) -> None:
        """Complete tool usage tracking."""
        end_time = time.time()

        # Find current session and complete tool tracking
        for session in reversed(self.session_data):
            if "end_time" not in session and "tools_used" in session:
                for tool_usage in reversed(session["tools_used"]):
                    if tool_usage["tool_name"] == tool.name and "end_time" not in tool_usage:
                        tool_usage["end_time"] = end_time
                        tool_usage["duration"] = end_time - \
                            tool_usage["start_time"]
                        tool_usage["result_length"] = len(result)
                        break
                break

    def _assess_response_quality(self, output: Any, processing_time: float) -> float:
        """Assess response quality based on various factors."""
        base_score = 50.0

        # Response length factor
        output_length = len(str(output))
        if 50 <= output_length <= 500:
            base_score += 20
        elif output_length > 500:
            base_score += 10

        # Processing time factor
        if processing_time < 2.0:
            base_score += 20
        elif processing_time < 5.0:
            base_score += 10
        else:
            base_score -= 10

        # Ensure score is between 0-100
        return max(0, min(100, base_score))

    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        if not self.session_data:
            return {"agent": self.metrics.agent_name, "status": "No sessions recorded"}

        completed_sessions = [
            s for s in self.session_data if "processing_time" in s]

        if not completed_sessions:
            return {"agent": self.metrics.agent_name, "status": "No completed sessions"}

        # Calculate advanced metrics
        processing_times = [s["processing_time"] for s in completed_sessions]
        quality_scores = self.metrics.response_quality_scores

        return {
            "agent_metrics": {
                "name": self.metrics.agent_name,
                "total_activations": self.metrics.activations,
                "handoffs_received": self.metrics.handoffs_received,
                "tool_usage_count": self.metrics.tool_usage_count,
                "success_rate": self.metrics.success_rate
            },
            "performance_stats": {
                "average_processing_time": self.metrics.average_processing_time,
                "fastest_session": min(processing_times),
                "slowest_session": max(processing_times),
                "processing_time_variance": self._calculate_variance(processing_times)
            },
            "quality_metrics": {
                "average_quality_score": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
                "quality_trend": self._calculate_quality_trend()
            },
            "optimization_recommendations": self.optimization_recommendations,
            "recent_sessions": completed_sessions[-5:]  # Last 5 sessions
        }

    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of values."""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

    def _calculate_quality_trend(self) -> str:
        """Calculate quality trend over recent sessions."""
        if len(self.metrics.response_quality_scores) < 3:
            return "insufficient_data"

        recent_scores = self.metrics.response_quality_scores[-5:]
        if len(recent_scores) < 3:
            return "insufficient_data"

        # Simple trend calculation
        first_half = recent_scores[:len(recent_scores)//2]
        second_half = recent_scores[len(recent_scores)//2:]

        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)

        if avg_second > avg_first + 5:
            return "improving"
        elif avg_second < avg_first - 5:
            return "declining"
        else:
            return "stable"


# ================================
# 4. Learning and Adaptation AgentHooks
# ================================

class LearningAgentHooks(AgentHooks):
    """AgentHooks that enable agent learning and adaptation over time."""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.learning_data = AgentLearningData()
        self.conversation_patterns: List[Dict[str, Any]] = []
        self.adaptation_threshold = 5  # Number of interactions before adaptation

    async def on_start(self, context: Any, agent: Agent) -> None:
        """Learn from conversation patterns on agent start."""
        # Extract conversation context
        conversation_context = self._extract_conversation_context(context)
        self.conversation_patterns.append({
            "timestamp": datetime.now(),
            "context": conversation_context,
            "session_start": True
        })

        # Apply learned optimizations
        if len(self.conversation_patterns) >= self.adaptation_threshold:
            await self._apply_learned_optimizations(agent)

        print(
            f"🧠 [{agent.name}] Learning session started - Pattern #{len(self.conversation_patterns)}")

    async def on_end(self, context: Any, agent: Agent, output: Any) -> None:
        """Learn from successful outputs."""
        # Analyze output quality and patterns
        output_analysis = self._analyze_output(output)

        # Record successful patterns
        if output_analysis["quality_score"] > 70:
            pattern = self._extract_success_pattern(context, output)
            self.learning_data.successful_patterns.append(pattern)
            print(
                f"✅ [{agent.name}] Successful pattern learned: {pattern[:50]}...")
        else:
            pattern = self._extract_failure_pattern(context, output)
            self.learning_data.failed_patterns.append(pattern)
            print(
                f"⚠️  [{agent.name}] Failure pattern identified: {pattern[:50]}...")

        # Suggest adaptations
        if len(self.learning_data.successful_patterns) > 3:
            suggestion = self._generate_adaptation_suggestion()
            if suggestion not in self.learning_data.optimization_suggestions:
                self.learning_data.optimization_suggestions.append(suggestion)
                print(
                    f"💡 [{agent.name}] New optimization suggestion: {suggestion}")

    async def on_handoff(self, context: Any, agent: Agent, source: Agent) -> None:
        """Learn from handoff patterns."""
        handoff_pattern = {
            "from_agent": source.name,
            "to_agent": agent.name,
            "timestamp": datetime.now(),
            "context_similarity": self._calculate_context_similarity(context)
        }

        # Record handoff learning
        self.learning_data.adaptation_history.append({
            "type": "handoff_received",
            "pattern": handoff_pattern,
            "timestamp": datetime.now().isoformat()
        })

        print(f"🧠 [{agent.name}] Learning from handoff pattern with {source.name}")

    async def _apply_learned_optimizations(self, agent: Agent) -> None:
        """Apply learned optimizations to agent behavior."""
        # Analyze successful patterns
        if len(self.learning_data.successful_patterns) > 2:
            common_elements = self._find_common_elements(
                self.learning_data.successful_patterns)
            if common_elements:
                optimization = f"Focus on {', '.join(common_elements[:3])}"
                print(
                    f"🎯 [{agent.name}] Applying learned optimization: {optimization}")

        # Avoid failed patterns
        if len(self.learning_data.failed_patterns) > 1:
            avoid_elements = self._find_common_elements(
                self.learning_data.failed_patterns)
            if avoid_elements:
                avoidance = f"Avoid {', '.join(avoid_elements[:2])}"
                print(
                    f"🚫 [{agent.name}] Applying learned avoidance: {avoidance}")

    def _extract_conversation_context(self, context: Any) -> str:
        """Extract key elements from conversation context."""
        # Simplified context extraction
        context_str = str(getattr(context, 'input', ''))
        keywords = ["help", "problem", "issue",
                    "question", "urgent", "billing", "technical"]
        found_keywords = [kw for kw in keywords if kw in context_str.lower()]
        return f"Keywords: {', '.join(found_keywords)}" if found_keywords else "General inquiry"

    def _analyze_output(self, output: Any) -> Dict[str, Any]:
        """Analyze output quality and characteristics."""
        output_str = str(output)

        quality_indicators = {
            "length": len(output_str),
            "helpful_words": len([w for w in ["help", "assist", "solve", "support"] if w in output_str.lower()]),
            "professional_tone": len([w for w in ["please", "thank", "appreciate"] if w in output_str.lower()]),
            "question_answered": "?" not in output_str or "answer" in output_str.lower()
        }

        # Simple quality scoring
        quality_score = 50
        if quality_indicators["length"] > 50:
            quality_score += 20
        if quality_indicators["helpful_words"] > 0:
            quality_score += 15
        if quality_indicators["professional_tone"] > 0:
            quality_score += 10
        if quality_indicators["question_answered"]:
            quality_score += 5

        return {
            "quality_score": min(100, quality_score),
            "indicators": quality_indicators
        }

    def _extract_success_pattern(self, context: Any, output: Any) -> str:
        """Extract pattern from successful interaction."""
        context_type = self._extract_conversation_context(context)
        output_type = "helpful_response" if "help" in str(
            output).lower() else "informative_response"
        return f"{context_type} → {output_type}"

    def _extract_failure_pattern(self, context: Any, output: Any) -> str:
        """Extract pattern from failed interaction."""
        context_type = self._extract_conversation_context(context)
        output_type = "unclear_response" if len(
            str(output)) < 30 else "verbose_response"
        return f"{context_type} → {output_type}"

    def _generate_adaptation_suggestion(self) -> str:
        """Generate adaptation suggestion based on learned patterns."""
        if len(self.learning_data.successful_patterns) > len(self.learning_data.failed_patterns):
            return "Continue current approach - success rate is high"
        else:
            return "Consider adjusting response style - improvement needed"

    def _find_common_elements(self, patterns: List[str]) -> List[str]:
        """Find common elements in patterns."""
        if len(patterns) < 2:
            return []

        # Simple word frequency analysis
        all_words = []
        for pattern in patterns[-5:]:  # Last 5 patterns
            all_words.extend(pattern.lower().split())

        word_counts: Dict[str, int] = {}
        for word in all_words:
            word_counts[word] = word_counts.get(word, 0) + 1

        # Return words that appear in multiple patterns
        common_words = [word for word,
                        count in word_counts.items() if count > 1]
        return common_words[:5]  # Top 5 common elements

    def _calculate_context_similarity(self, context: Any) -> float:
        """Calculate similarity with previous contexts."""
        # Simplified similarity calculation
        current_context = self._extract_conversation_context(context)

        if not self.conversation_patterns:
            return 0.0

        similarities = []
        for pattern in self.conversation_patterns[-5:]:  # Last 5 patterns
            if pattern["context"] == current_context:
                similarities.append(1.0)
            elif any(word in pattern["context"] for word in current_context.split()):
                similarities.append(0.5)
            else:
                similarities.append(0.0)

        return sum(similarities) / len(similarities) if similarities else 0.0

    def get_learning_report(self) -> Dict[str, Any]:
        """Generate learning and adaptation report."""
        return {
            "agent_name": self.agent_name,
            "learning_progress": {
                "successful_patterns": len(self.learning_data.successful_patterns),
                "failed_patterns": len(self.learning_data.failed_patterns),
                "adaptation_events": len(self.learning_data.adaptation_history),
                "optimization_suggestions": len(self.learning_data.optimization_suggestions)
            },
            "recent_patterns": {
                "successful": self.learning_data.successful_patterns[-3:] if self.learning_data.successful_patterns else [],
                "failed": self.learning_data.failed_patterns[-3:] if self.learning_data.failed_patterns else []
            },
            "current_optimizations": self.learning_data.optimization_suggestions[-3:] if self.learning_data.optimization_suggestions else [],
            "conversation_pattern_count": len(self.conversation_patterns),
            "learning_status": "active" if len(self.conversation_patterns) >= self.adaptation_threshold else "collecting_data"
        }


# ================================
# 5. Demo Tools and Agents with Hooks
# ================================

@function_tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information."""
    return f"Knowledge base results for '{query}': Found 3 relevant articles about {query}"


@function_tool
def create_ticket(issue: str) -> str:
    """Create a support ticket for the issue."""
    return f"Support ticket created for: {issue}. Ticket ID: TK-{hash(issue) % 10000}"


@function_tool
def escalate_issue(reason: str) -> str:
    """Escalate issue to higher level support."""
    return f"Issue escalated to senior support team. Reason: {reason}"


def create_smart_customer_agent() -> Agent:
    """Create a customer service agent with learning capabilities."""
    agent = Agent(
        name="SmartCustomerAgent",
        instructions="You are an intelligent customer service agent that learns and adapts. Provide helpful, personalized assistance.",
        tools=[search_knowledge_base, create_ticket]
    )

    # Attach learning hooks
    agent.hooks = LearningAgentHooks("SmartCustomerAgent")
    return agent


def create_performance_optimized_agent() -> Agent:
    """Create an agent focused on performance optimization."""
    agent = Agent(
        name="PerformanceAgent",
        instructions="You are a performance-optimized agent. Focus on quick, accurate responses.",
        tools=[search_knowledge_base, escalate_issue]
    )

    # Attach performance tracking hooks
    agent.hooks = PerformanceTrackingHooks("PerformanceAgent")
    return agent


def create_basic_monitored_agent() -> Agent:
    """Create an agent with basic monitoring."""
    agent = Agent(
        name="MonitoredAgent",
        instructions="You are a basic agent with lifecycle monitoring.",
        tools=[search_knowledge_base]
    )

    # Attach basic hooks
    agent.hooks = BasicAgentHooks("MonitoredAgent")
    return agent


# ================================
# 6. Demo Functions
# ================================

async def demo_basic_agent_hooks():
    """Demonstrate basic AgentHooks functionality."""
    print("=== Basic Agent Hooks Demo ===")

    # Create agent with basic hooks
    agent = create_basic_monitored_agent()

    # Multiple interactions to show hook behavior
    interactions = [
        "Help me find information about billing policies",
        "I need support with a technical issue",
        "Can you search for troubleshooting guides?"
    ]

    result = await Runner.run(agent, input="Help me find information about billing policies", context="test")
    print(result)
    # for i, interaction in enumerate(interactions, 1):
    #     print(f"\n--- Interaction {i} ---")
    #     print(f"Result: {result.final_output}")

    # # Show agent summary
    # if isinstance(agent.hooks, BasicAgentHooks):
    #     summary = agent.hooks.get_agent_summary()
    #     print(f"\n📊 Agent Summary:")
    #     for key, value in summary.items():
    #         print(f"  {key}: {value}")



async def demo_agent_hooks_with_handoffs():
    """Demonstrate agent hooks with handoff scenarios."""
    print("\n=== Agent Hooks with Handoffs Demo ===")

    # Create agents with different hook types
    customer_agent = create_smart_customer_agent()
    performance_agent = create_performance_optimized_agent()

    # Set up handoffs
    customer_agent.handoffs = [
        handoff(performance_agent,
                tool_name_override="escalate_to_performance_team")
    ]

    # Run handoff scenario
    result = await Runner.run(
        customer_agent,
        input="I have a complex issue that needs specialized performance analysis"
    )

    print(f"Final Result: {result.final_output}")

    # Show reports from both agents
    if isinstance(customer_agent.hooks, LearningAgentHooks):
        customer_report = customer_agent.hooks.get_learning_report()
        print(f"\n🧠 Customer Agent Learning Report:")
        print(f"  Learning Status: {customer_report['learning_status']}")
        print(
            f"  Pattern Count: {customer_report['conversation_pattern_count']}")

    if isinstance(performance_agent.hooks, PerformanceTrackingHooks):
        perf_report = performance_agent.hooks.get_performance_report()
        print(f"\n📈 Performance Agent Report:")
        if "agent_metrics" in perf_report:
            print(
                f"  Activations: {perf_report['agent_metrics']['total_activations']}")
            print(
                f"  Handoffs Received: {perf_report['agent_metrics']['handoffs_received']}")


# ================================
# 7. Main Demo Function
# ================================

async def main():
    """Run all AgentHooks demonstrations."""
    print("🤖 OpenAI Agents SDK - Agent Lifecycle Hooks")
    print("=" * 60)

    # Run all demonstrations
    await demo_basic_agent_hooks()
    # await demo_performance_tracking()
    # await demo_learning_agent()
    # await demo_agent_hooks_with_handoffs()

    # print("\n" + "=" * 60)
    # print("✅ Agent lifecycle hooks demonstration complete!")
    # print("\nKey Takeaways:")
    # print("1. AgentHooks enable per-agent customization and monitoring")
    # print("2. Performance tracking helps optimize individual agent behavior")
    # print("3. Learning hooks enable agents to adapt and improve over time")
    # print("4. Different hook types can be combined for comprehensive monitoring")
    # print("5. Agent hooks work seamlessly with handoffs and tool usage")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(main())


# ================================
# 8. Production Implementation Notes
# ================================

"""
AgentHooks Production Patterns:

1. **Performance Optimization**:
   - Individual agent performance tuning
   - A/B testing different agent configurations
   - Dynamic agent optimization based on metrics
   - Resource allocation optimization per agent

2. **Learning and Adaptation**:
   - Continuous learning from user interactions
   - Personalization based on user behavior patterns
   - Adaptive response strategies per agent type
   - Knowledge base updates from successful patterns

3. **Specialized Monitoring**:
   - Domain-specific metrics per agent type
   - Custom KPIs for different agent roles
   - Business logic validation per agent
   - Compliance monitoring for regulated environments

4. **Agent Health Monitoring**:
   - Individual agent health checks
   - Performance degradation detection
   - Automatic agent replacement/restart
   - Load balancing based on agent performance

5. **Behavioral Analytics**:
   - User satisfaction correlation per agent
   - Success pattern identification
   - Failure mode analysis per agent type
   - Recommendation engine improvements

6. **Production Considerations**:
   - Hook performance impact monitoring
   - Memory usage optimization for long-running agents
   - Graceful degradation when hooks fail
   - Scalability with thousands of agent instances
"""
