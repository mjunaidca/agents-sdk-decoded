"""
04_model_mixing.py

This module covers model mixing and multi-model workflows in the OpenAI Agents SDK.
Focus: Using different models for different agents and cost optimization strategies.

Learning Objectives:
- Understand multi-model architectures and workflows
- Learn cost optimization through model selection
- Master performance vs capability trade-offs
- Implement dynamic model selection patterns

Key Concepts:
- Different models for different agent roles
- Cost vs capability optimization
- Model provider mixing strategies
- Dynamic model selection based on task complexity
- Performance monitoring and optimization

Based on: https://openai.github.io/openai-agents-python/models/
"""

import asyncio
from agents import Agent, Runner, ModelSettings, function_tool
from openai import AsyncOpenAI

# ================== MODEL MIXING FUNDAMENTALS ==================


async def demo_multi_model_overview():
    """Demonstrate multi-model architecture overview."""
    print("=== Demo: Multi-Model Architecture Overview ===")

    print("🏗️ Multi-Model Architecture Benefits:")
    print("   • Cost optimization through appropriate model selection")
    print("   • Performance optimization for different task types")
    print("   • Risk mitigation through provider diversification")
    print("   • Capability specialization for complex workflows")
    print("   • Scalability through resource allocation")
    print()

    print("🎯 Model Selection Strategies:")
    strategies = {
        "Cost-Based": "Use cheaper models for simple tasks, expensive for complex",
        "Speed-Based": "Fast models for real-time, powerful for batch processing",
        "Capability-Based": "Specialized models for specific domain expertise",
        "Reliability-Based": "Primary and fallback models for high availability",
        "Provider-Based": "Mix OpenAI, Anthropic, Google for diverse capabilities"
    }

    for strategy, description in strategies.items():
        print(f"   • {strategy:18}: {description}")

    print(f"\n💰 Cost Optimization Examples:")
    cost_examples = {
        "Triage → Specialist": "gpt-3.5-turbo for routing, gpt-4o for processing",
        "Draft → Review": "Fast model for initial draft, powerful for refinement",
        "Simple → Complex": "Small model for FAQs, large for complex analysis",
        "Real-time → Batch": "Quick responses live, detailed processing offline"
    }

    for pattern, example in cost_examples.items():
        print(f"   • {pattern:18}: {example}")

    print(f"\n🎮 Performance Trade-offs:")
    print(f"   Speed vs Quality: Faster models vs more accurate models")
    print(f"   Cost vs Capability: Cheaper models vs more capable models")
    print(f"   Latency vs Throughput: Real-time vs batch processing")
    print(f"   Consistency vs Creativity: Deterministic vs innovative responses")


async def demo_triage_specialist_pattern():
    """Demonstrate the triage-specialist pattern for cost optimization."""
    print("\n=== Demo: Triage-Specialist Pattern ===")

    print("🚦 Triage-Specialist Pattern Overview:")
    print("   • Fast, cheap model for initial classification")
    print("   • Powerful, expensive model for complex processing")
    print("   • Significant cost savings on simple requests")
    print("   • Maintained quality for complex requests")
    print()

    @function_tool
    def escalate_to_specialist(request: str) -> str:
        """Escalate a request to the specialist agent."""
        return f"Escalated to specialist: {request}"

    @function_tool
    def provide_simple_answer(question: str) -> str:
        """Provide a simple answer for basic questions."""
        if "hello" in question.lower():
            return "Hello! How can I help you today?"
        elif "weather" in question.lower():
            return "I'd be happy to help with weather information."
        else:
            return "Let me help you with that basic question."

    print("🧪 Triage-Specialist Implementation:")

    # Triage agent - fast and cheap
    print(f"\n   🚦 Triage Agent (gpt-3.5-turbo):")
    try:
        triage_agent = Agent(
            name="TriageAgent",
            instructions="""You are a triage agent. Your job is to:
            1. Handle simple questions directly using provided tools
            2. Escalate complex requests to the specialist
            
            Handle directly: greetings, basic info, simple FAQs
            Escalate: complex analysis, detailed explanations, specialized topics""",
            model="gpt-3.5-turbo",
            model_settings=ModelSettings(
                temperature=0.2,
                max_tokens=200
            ),
            tools=[provide_simple_answer, escalate_to_specialist]
        )

        print(f"      Model: gpt-3.5-turbo (fast, cost-effective)")
        print(f"      Temperature: 0.2 (consistent routing decisions)")
        print(f"      Max tokens: 200 (brief responses)")
        print(f"      Tools: Simple answers + escalation")

    except Exception as e:
        print(f"      Configuration: Triage agent with gpt-3.5-turbo")
        print(f"      ✓ Fast routing and simple question handling")

    # Specialist agent - powerful and expensive
    print(f"\n   🎓 Specialist Agent (gpt-4o):")
    try:
        specialist_agent = Agent(
            name="SpecialistAgent",
            instructions="""You are a specialist agent for complex requests.
            Provide detailed, accurate, and comprehensive responses.
            Use your advanced capabilities for in-depth analysis.""",
            model="gpt-4o",
            model_settings=ModelSettings(
                temperature=0.4,
                max_tokens=1500
            )
        )

        print(f"      Model: gpt-4o (powerful, comprehensive)")
        print(f"      Temperature: 0.4 (balanced accuracy and insight)")
        print(f"      Max tokens: 1500 (detailed responses)")
        print(f"      Use case: Complex analysis and detailed explanations")

    except Exception as e:
        print(f"      Configuration: Specialist agent with gpt-4o")
        print(f"      ✓ High-quality processing for complex requests")

    print(f"\n💰 Cost Analysis:")
    print(f"   Scenario: 1000 requests/day, 70% simple, 30% complex")
    print(f"   Without triage: 1000 × gpt-4o = High cost")
    print(f"   With triage: 700 × gpt-3.5-turbo + 300 × gpt-4o = 60-80% savings")
    print(f"   Quality: Simple requests → same quality, Complex → same quality")


async def demo_provider_mixing():
    """Demonstrate mixing different model providers."""
    print("\n=== Demo: Provider Mixing Strategies ===")

    print("🌐 Multi-Provider Architecture:")
    print("   • OpenAI: Strong general capabilities, latest features")
    print("   • Anthropic: Strong reasoning, safety, large context")
    print("   • Google: Fast responses, multimodal capabilities")
    print("   • Diverse capabilities and pricing models")
    print()

    print("🎯 Provider Selection Matrix:")
    provider_strengths = {
        "OpenAI (gpt-4o)": ["General intelligence", "Latest features", "Tool use", "Structured outputs"],
        "Anthropic (Claude)": ["Reasoning", "Safety", "Large context", "Code analysis"],
        "Google (Gemini)": ["Speed", "Multimodal", "Real-time", "Cost-effective"],
        "LiteLLM Universal": ["Provider flexibility", "Fallback options", "Cost comparison"]
    }

    for provider, strengths in provider_strengths.items():
        print(f"   {provider}:")
        for strength in strengths:
            print(f"      ✓ {strength}")
        print()

    print("🧪 Provider Mixing Examples:")

    # Example 1: OpenAI for primary, Anthropic for reasoning
    print(f"\n   🔄 Primary + Reasoning Pattern:")
    print(f"   ```python")
    print(f"   # Primary agent - OpenAI for general tasks")
    print(f"   primary_agent = Agent(")
    print(f"       model='gpt-4o',")
    print(f"       instructions='Handle general requests efficiently'")
    print(f"   )")
    print(f"   ")
    print(f"   # Reasoning agent - Claude for complex logic")
    print(f"   reasoning_agent = Agent(")
    print(f"       model='litellm/anthropic/claude-3-5-sonnet-20240620',")
    print(f"       instructions='Provide deep logical analysis'")
    print(f"   )")
    print(f"   ```")

    # Example 2: Speed vs quality tiers
    print(f"\n   ⚡ Speed vs Quality Tiers:")
    print(f"   ```python")
    print(f"   # Fast tier - Gemini for quick responses")
    print(f"   fast_agent = Agent(")
    print(f"       model='litellm/gemini/gemini-2.5-flash-preview',")
    print(f"       model_settings=ModelSettings(temperature=0.3, max_tokens=300)")
    print(f"   )")
    print(f"   ")
    print(f"   # Quality tier - GPT-4o for detailed analysis")
    print(f"   quality_agent = Agent(")
    print(f"       model='gpt-4o',")
    print(f"       model_settings=ModelSettings(temperature=0.4, max_tokens=1500)")
    print(f"   )")
    print(f"   ```")

    print(f"\n🎯 Provider Mixing Benefits:")
    print(f"   ✓ Risk mitigation through diversification")
    print(f"   ✓ Cost optimization through competition")
    print(f"   ✓ Capability specialization for optimal results")
    print(f"   ✓ Reduced vendor lock-in")


async def demo_dynamic_model_selection():
    """Demonstrate dynamic model selection based on request characteristics."""
    print("\n=== Demo: Dynamic Model Selection ===")

    print("🧠 Dynamic Selection Criteria:")
    print("   • Request complexity analysis")
    print("   • User context and history")
    print("   • Performance requirements")
    print("   • Cost budget constraints")
    print("   • Provider availability")
    print()

    print("⚙️ Selection Algorithm Factors:")
    factors = {
        "Request Length": "Short → fast model, Long → capable model",
        "Technical Terms": "High density → specialized model",
        "Urgency Level": "High → fast model, Normal → quality model",
        "User Tier": "Premium → best model, Standard → balanced",
        "Time of Day": "Peak → distributed, Off-peak → premium"
    }

    for factor, logic in factors.items():
        print(f"   • {factor:15}: {logic}")

    print(f"\n🧪 Dynamic Selection Implementation:")

    def analyze_request_complexity(request: str) -> str:
        """Analyze request complexity for model selection."""
        complexity_indicators = {
            "simple": ["hello", "hi", "thanks", "yes", "no"],
            "medium": ["explain", "how", "what", "why", "when"],
            "complex": ["analyze", "compare", "evaluate", "design", "optimize"]
        }

        request_lower = request.lower()

        # Count indicators
        simple_count = sum(
            1 for word in complexity_indicators["simple"] if word in request_lower)
        medium_count = sum(
            1 for word in complexity_indicators["medium"] if word in request_lower)
        complex_count = sum(
            1 for word in complexity_indicators["complex"] if word in request_lower)

        # Determine complexity
        if complex_count > 0 or len(request.split()) > 20:
            return "complex"
        elif medium_count > 0 or len(request.split()) > 10:
            return "medium"
        else:
            return "simple"

    def select_model_for_request(request: str, user_tier: str = "standard") -> str:
        """Select optimal model based on request characteristics."""
        complexity = analyze_request_complexity(request)

        # Model selection matrix
        model_matrix = {
            ("simple", "standard"): "gpt-3.5-turbo",
            ("simple", "premium"): "gpt-4o",
            ("medium", "standard"): "gpt-4o-mini",
            ("medium", "premium"): "gpt-4o",
            ("complex", "standard"): "gpt-4o",
            ("complex", "premium"): "litellm/anthropic/claude-3-5-sonnet-20240620"
        }

        return model_matrix.get((complexity, user_tier), "gpt-4o")

    print(f"\n   🎛️ Model Selection Matrix:")
    print(f"   ```python")
    print(f"   def select_model_for_request(request, user_tier):")
    print(f"       complexity = analyze_complexity(request)")
    print(f"       ")
    print(f"       matrix = {{")
    print(f"           ('simple', 'standard'): 'gpt-3.5-turbo',")
    print(f"           ('medium', 'standard'): 'gpt-4o-mini',")
    print(f"           ('complex', 'premium'): 'claude-3-5-sonnet'")
    print(f"       }}")
    print(f"       return matrix.get((complexity, user_tier))")
    print(f"   ```")

    # Demonstrate selection logic
    test_requests = [
        ("Hello there!", "standard"),
        ("How does machine learning work?", "standard"),
        ("Analyze the market implications of AI advancement", "premium")
    ]

    print(f"\n   🧪 Selection Examples:")
    for request, tier in test_requests:
        selected_model = select_model_for_request(request, tier)
        complexity = analyze_request_complexity(request)
        print(
            f"   Request: '{request[:40]}{'...' if len(request) > 40 else ''}'")
        print(f"      Complexity: {complexity}, Tier: {tier}")
        print(f"      Selected: {selected_model}")
        print()


async def demo_performance_monitoring():
    """Demonstrate performance monitoring for multi-model systems."""
    print("\n=== Demo: Performance Monitoring ===")

    print("📊 Multi-Model Performance Metrics:")
    print("   • Response time by model and task type")
    print("   • Cost per request and monthly budgets")
    print("   • Quality scores from user feedback")
    print("   • Error rates and availability")
    print("   • Token usage and efficiency")
    print()

    print("🎯 Monitoring Dashboard Metrics:")
    metrics = {
        "Cost Metrics": ["$/request by model", "Monthly spend by provider", "Cost per task type"],
        "Performance": ["Response latency", "Throughput (req/min)", "Success rate"],
        "Quality": ["User satisfaction", "Task completion rate", "Accuracy scores"],
        "Usage": ["Token consumption", "API rate limits", "Provider quotas"]
    }

    for category, metric_list in metrics.items():
        print(f"   {category}:")
        for metric in metric_list:
            print(f"      • {metric}")
        print()

    print("🧪 Monitoring Implementation Pattern:")
    print("   ```python")
    print("   import time")
    print("   from dataclasses import dataclass")
    print("   ")
    print("   @dataclass")
    print("   class RequestMetrics:")
    print("       model: str")
    print("       task_type: str")
    print("       latency: float")
    print("       tokens_used: int")
    print("       cost: float")
    print("       success: bool")
    print("   ")
    print("   async def run_with_monitoring(agent, request):")
    print("       start_time = time.time()")
    print("       try:")
    print("           result = await Runner.run(agent, request)")
    print("           metrics = RequestMetrics(")
    print("               model=agent.model,")
    print("               latency=time.time() - start_time,")
    print("               success=True")
    print("           )")
    print("           log_metrics(metrics)")
    print("           return result")
    print("       except Exception as e:")
    print("           log_error(agent.model, str(e))")
    print("           raise")
    print("   ```")

    print(f"\n📈 Optimization Strategies:")
    optimization_strategies = [
        "Monitor cost per task type to optimize model selection",
        "Track latency to identify performance bottlenecks",
        "Analyze quality scores to refine model assignments",
        "Use A/B testing to compare model effectiveness",
        "Implement automatic failover for high availability"
    ]

    for i, strategy in enumerate(optimization_strategies, 1):
        print(f"   {i}. {strategy}")


async def demo_fallback_strategies():
    """Demonstrate fallback strategies for model reliability."""
    print("\n=== Demo: Fallback Strategies ===")

    print("🛡️ Fallback Strategy Types:")
    print("   • Provider failover for availability")
    print("   • Model downgrade for rate limits")
    print("   • Capability degradation for errors")
    print("   • Cache responses for outages")
    print()

    print("🎯 Fallback Decision Tree:")
    print("   1. Primary model unavailable → Secondary provider")
    print("   2. Rate limit exceeded → Cheaper/faster model")
    print("   3. Context too long → Model with larger context")
    print("   4. Feature unsupported → Compatible model")
    print("   5. All models fail → Cached/default response")
    print()

    print("🧪 Fallback Implementation:")
    print("   ```python")
    print("   async def robust_model_call(request, user_tier='standard'):")
    print("       # Define fallback chain")
    print("       models = [")
    print("           'gpt-4o',  # Primary")
    print("           'gpt-4o-mini',  # Faster fallback")
    print("           'gpt-3.5-turbo'  # Most reliable")
    print("       ]")
    print("       ")
    print("       for model in models:")
    print("           try:")
    print("               agent = Agent(model=model)")
    print("               return await Runner.run(agent, request)")
    print("           except RateLimitError:")
    print("               await asyncio.sleep(1)  # Brief delay")
    print("               continue")
    print("           except Exception as e:")
    print("               log_error(model, str(e))")
    print("               continue")
    print("       ")
    print("       # All models failed")
    print("       return get_cached_response(request)")
    print("   ```")

    print(f"\n🎮 Graceful Degradation:")
    degradation_levels = {
        "Level 1": "Premium model → Standard model (slight quality reduction)",
        "Level 2": "Complex features → Basic features (functionality reduction)",
        "Level 3": "Real-time → Async processing (latency increase)",
        "Level 4": "Dynamic → Cached responses (staleness acceptable)"
    }

    for level, description in degradation_levels.items():
        print(f"   {level}: {description}")

    print(f"\n✅ Reliability Best Practices:")
    best_practices = [
        "Always have a fallback model from a different provider",
        "Implement exponential backoff for retries",
        "Cache successful responses for emergency use",
        "Monitor provider status pages for proactive switching",
        "Test fallback paths regularly in staging"
    ]

    for i, practice in enumerate(best_practices, 1):
        print(f"   {i}. {practice}")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all model mixing demonstrations."""
    print("🏗️ OpenAI Agents SDK - Model Mixing 🏗️")
    print("\nThis module covers multi-model workflows and optimization strategies.")
    print("Focus: Cost optimization and performance through model diversity\n")

    # Run all demonstrations
    await demo_multi_model_overview()
    await demo_triage_specialist_pattern()
    await demo_provider_mixing()
    await demo_dynamic_model_selection()
    await demo_performance_monitoring()
    await demo_fallback_strategies()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - Model Mixing:")
    print("• Multi-model architectures enable cost and performance optimization")
    print("• Triage-specialist pattern provides 60-80% cost savings")
    print("• Provider mixing reduces vendor lock-in and increases capabilities")
    print("• Dynamic selection adapts to request complexity and user needs")
    print("• Performance monitoring enables continuous optimization")
    print("• Fallback strategies ensure reliability and graceful degradation")

    print(f"\n🏗️ Architecture Summary:")
    print(f"   🚦 Triage Pattern: Fast routing + specialized processing")
    print(f"   🌐 Provider Mixing: OpenAI + Anthropic + Google diversity")
    print(f"   🧠 Dynamic Selection: Request-based model optimization")
    print(f"   📊 Monitoring: Cost, performance, quality tracking")
    print(f"   🛡️ Fallbacks: Reliability through redundancy")

    print(f"\n🎯 Next Steps:")
    print(f"• Learn provider integration in 05_provider_integration.py")
    print(f"• Understand troubleshooting in 06_troubleshooting.py")


if __name__ == "__main__":
    asyncio.run(main())
