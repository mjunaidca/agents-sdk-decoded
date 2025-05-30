"""
02_span_types.py

This module covers the built-in span types in the OpenAI Agents SDK.
Focus: Understanding what each span type captures and when they're created.

Learning Objectives:
- Understand all built-in span types
- See when each span type is automatically created
- Learn what data each span type captures
- Understand span hierarchy and nesting

Key Concepts:
- Agent spans wrap complete agent executions
- Generation spans capture LLM API calls
- Function spans capture tool executions
- Handoff spans capture agent-to-agent transfers
- Other specialized spans (guardrail, response, etc.)

Based on: https://openai.github.io/openai-agents-python/tracing/
"""

import asyncio
from agents import Agent, Runner, function_tool
from agents.handoffs import handoff

# ================== SPAN TYPES DEMONSTRATION ==================


async def demo_agent_spans():
    """Demonstrate agent spans that wrap complete agent executions."""
    print("=== Demo: Agent Spans ===")

    print("📊 Agent Spans:")
    print("   • Created for each complete agent execution")
    print("   • Contains agent reasoning and decision-making")
    print("   • Wraps the entire agent's processing cycle")
    print("   • Includes context about the agent itself")
    print()

    # Simple agent to generate an agent span
    reasoning_agent = Agent(
        name="ReasoningAgent",
        instructions="""
        You are an agent that demonstrates reasoning spans.
        Think through your response step by step and be explicit about your reasoning.
        """
    )

    print("🤖 Running agent to generate Agent Span...")
    print("   This will create:")
    print("   📈 1 Agent Span - wrapping the entire agent execution")
    print("   📈 1+ Generation Spans - for LLM calls within the agent")

    try:
        result = await Runner.run(
            reasoning_agent,
            "Please think through why the sky appears blue and explain your reasoning",
            max_turns=2
        )

        print(f"\n✅ Agent execution completed!")
        print(f"💭 Response: {result.final_output[:100]}...")
        print(f"\n📊 Agent Span Created:")
        print(f"   • Contains: Agent's reasoning process")
        print(f"   • Contains: Agent context and configuration")
        print(f"   • Contains: Decision-making flow")
        print(f"   • Contains: Agent's instructions and behavior")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_generation_spans():
    """Demonstrate generation spans that capture LLM API calls."""
    print("\n=== Demo: Generation Spans ===")

    print("🧠 Generation Spans:")
    print("   • Created for each LLM API call")
    print("   • Capture input prompts sent to the model")
    print("   • Capture model responses")
    print("   • Include model parameters (temperature, max_tokens, etc.)")
    print("   • Include token usage information")
    print()

    # Agent that will make multiple LLM calls
    multi_call_agent = Agent(
        name="MultiCallAgent",
        instructions="""
        You make multiple thoughtful responses. First acknowledge the request,
        then provide a detailed answer. This will generate multiple generation spans.
        """
    )

    print("🤖 Running agent that makes multiple LLM calls...")
    print("   This will create:")
    print("   📈 Multiple Generation Spans - one for each LLM API call")

    try:
        result = await Runner.run(
            multi_call_agent,
            "First acknowledge this message, then explain what machine learning is",
            max_turns=3
        )

        print(f"\n✅ Multi-call execution completed!")
        print(f"💬 Final response: {result.final_output[:100]}...")
        print(f"\n📊 Generation Spans Created:")
        print(f"   • Span 1: Initial acknowledgment generation")
        print(f"   • Span 2: Machine learning explanation generation")
        print(f"   • Each contains: Full prompt + response + model metadata")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_function_spans():
    """Demonstrate function spans that capture tool executions."""
    print("\n=== Demo: Function Spans ===")

    print("🔧 Function Spans:")
    print("   • Created for each tool/function execution")
    print("   • Capture function inputs (parameters)")
    print("   • Capture function outputs (return values)")
    print("   • Include function metadata and execution time")
    print("   • Show tool usage patterns")
    print()

    @function_tool
    def calculate_area(shape: str, dimension1: float, dimension2: float = None) -> str:
        """Calculate area of different shapes."""
        if shape.lower() == "rectangle" and dimension2:
            area = dimension1 * dimension2
            return f"Rectangle area: {area} square units"
        elif shape.lower() == "circle":
            import math
            area = math.pi * (dimension1 ** 2)
            return f"Circle area: {area:.2f} square units"
        else:
            return f"Unsupported shape: {shape}"

    @function_tool
    def get_weather_info(city: str) -> str:
        """Get weather information for a city (simulated)."""
        # Simulate weather data
        weather_data = {
            "New York": "Sunny, 72°F",
            "London": "Cloudy, 18°C",
            "Tokyo": "Rainy, 24°C"
        }
        return weather_data.get(city, f"Weather data not available for {city}")

    function_demo_agent = Agent(
        name="FunctionDemoAgent",
        instructions="Use the available tools to help with calculations and weather queries.",
        tools=[calculate_area, get_weather_info]
    )

    print("🤖 Running agent with multiple tools...")
    print("   This will create:")
    print("   📈 Function Spans - one for each tool call")

    try:
        result = await Runner.run(
            function_demo_agent,
            "Calculate the area of a rectangle 5x3, then tell me the weather in Tokyo",
            max_turns=4
        )

        print(f"\n✅ Tool execution completed!")
        print(f"🔧 Response: {result.final_output}")
        print(f"\n📊 Function Spans Created:")
        print(
            f"   • calculate_area span: inputs=[rectangle, 5, 3], output=[area calculation]")
        print(
            f"   • get_weather_info span: inputs=[Tokyo], output=[weather data]")
        print(f"   • Each contains: Function parameters + return values + timing")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_handoff_spans():
    """Demonstrate handoff spans that capture agent-to-agent transfers."""
    print("\n=== Demo: Handoff Spans ===")

    print("🔄 Handoff Spans:")
    print("   • Created when one agent hands off to another")
    print("   • Capture the transfer context and reasoning")
    print("   • Show which agent initiated the handoff")
    print("   • Show which agent received the handoff")
    print("   • Include handoff decision logic")
    print()

    # Specialist agent for calculations
    calculator_agent = Agent(
        name="CalculatorAgent",
        instructions="I am a specialist calculator. I focus only on mathematical calculations."
    )

    # Specialist agent for writing
    writer_agent = Agent(
        name="WriterAgent",
        instructions="I am a specialist writer. I focus only on creating written content."
    )

    # Main coordinator agent with handoffs
    coordinator_agent = Agent(
        name="CoordinatorAgent",
        instructions="""
        I coordinate tasks by handing off to specialists:
        - Mathematical questions go to CalculatorAgent
        - Writing tasks go to WriterAgent
        """,
        handoffs=[
            handoff(agent=calculator_agent),
            handoff(agent=writer_agent)
        ]
    )

    print("🤖 Running multi-agent workflow with handoffs...")
    print("   This will create:")
    print("   📈 Handoff Spans - for each agent-to-agent transfer")

    try:
        result = await Runner.run(
            coordinator_agent,
            "I need both a calculation (2+2) and a short poem about numbers",
            max_turns=6
        )

        print(f"\n✅ Multi-agent workflow completed!")
        print(f"📝 Final result: {result.final_output[:150]}...")
        print(f"\n📊 Handoff Spans Created:")
        print(f"   • Coordinator → Calculator: handoff span for math task")
        print(f"   • Calculator → Coordinator: return handoff span")
        print(f"   • Coordinator → Writer: handoff span for writing task")
        print(f"   • Writer → Coordinator: return handoff span")
        print(f"   • Each contains: Handoff reasoning + context + timing")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_span_hierarchy():
    """Demonstrate how spans are nested hierarchically."""
    print("\n=== Demo: Span Hierarchy and Nesting ===")

    print("🏗️ Span Hierarchy Structure:")
    print("   📊 TRACE: Complete workflow")
    print("   ├── 📈 Agent Span: Main agent execution")
    print("   │   ├── 📈 Generation Span: LLM call #1")
    print("   │   ├── 📈 Function Span: Tool call")
    print("   │   └── 📈 Generation Span: LLM call #2")
    print("   └── 📈 Handoff Span: Transfer to specialist")
    print("       └── 📈 Agent Span: Specialist execution")
    print("           └── 📈 Generation Span: Specialist LLM call")
    print()

    @function_tool
    def complex_calculation(expression: str) -> str:
        """Perform a complex calculation with multiple steps."""
        try:
            # This tool execution creates a Function Span
            # Note: In production, use safer evaluation
            result = eval(expression)
            return f"Calculation result: {expression} = {result}"
        except:
            return f"Could not calculate: {expression}"

    hierarchy_agent = Agent(
        name="HierarchyDemoAgent",
        instructions="""
        You demonstrate span hierarchy. When given a calculation request:
        1. First acknowledge the request (Generation Span)
        2. Use the calculation tool (Function Span)  
        3. Provide a summary response (Generation Span)
        """,
        tools=[complex_calculation]
    )

    print("🤖 Running agent to demonstrate span hierarchy...")

    try:
        result = await Runner.run(
            hierarchy_agent,
            "Please calculate (10 + 5) * 3 and explain the result",
            max_turns=3
        )

        print(f"\n✅ Hierarchical execution completed!")
        print(f"🔢 Result: {result.final_output}")
        print(f"\n📊 Hierarchical Span Structure Created:")
        print(f"   📊 TRACE: 'HierarchyDemo' workflow")
        print(f"   └── 📈 Agent Span: HierarchyDemoAgent execution")
        print(f"       ├── 📈 Generation Span: Initial acknowledgment")
        print(f"       ├── 📈 Function Span: complex_calculation tool")
        print(f"       └── 📈 Generation Span: Final summary response")
        print(f"\n🎯 Key Understanding:")
        print(f"   • Spans nest naturally based on execution flow")
        print(f"   • Parent spans contain child spans")
        print(f"   • Timing is hierarchical (parent >= sum of children)")

    except Exception as e:
        print(f"❌ Error: {e}")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all span type demonstrations."""
    print("📈 OpenAI Agents SDK - Built-in Span Types 📈")
    print("\nThis module covers the different types of spans automatically")
    print("created by the SDK and what they capture.\n")

    # Run all demonstrations
    await demo_agent_spans()
    await demo_generation_spans()
    await demo_function_spans()
    await demo_handoff_spans()
    await demo_span_hierarchy()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - Span Types:")
    print("• Agent Spans: Wrap complete agent executions")
    print("• Generation Spans: Capture LLM API calls and responses")
    print("• Function Spans: Capture tool/function executions")
    print("• Handoff Spans: Capture agent-to-agent transfers")
    print("• Spans nest hierarchically based on execution flow")
    print("• Each span type captures specific operation data")

    print(f"\n🔍 Span Type Summary:")
    print(f"   📈 Agent Span = Agent reasoning + decisions")
    print(f"   📈 Generation Span = LLM prompts + responses")
    print(f"   📈 Function Span = Tool inputs + outputs")
    print(f"   📈 Handoff Span = Transfer context + reasoning")

    print(f"\n🎯 Next Steps:")
    print(f"• Learn tracing controls in 03_tracing_control.py")
    print(f"• Understand data protection in 04_sensitive_data.py")


if __name__ == "__main__":
    asyncio.run(main())
