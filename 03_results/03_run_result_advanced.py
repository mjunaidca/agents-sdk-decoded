"""
03_run_result_advanced.py

Demonstrates advanced RunResult usage with tools, handoffs, and error scenarios.

Covers:
- RunResult with tool usage and complex new_items
- Handoff scenarios and agent transitions
- Error handling and partial results
- Performance analysis and timing
- Memory usage and optimization patterns

Based on:
- https://openai.github.io/openai-agents-python/results/
- https://openai.github.io/openai-agents-python/tools/
- https://openai.github.io/openai-agents-python/handoffs/
"""

import asyncio
import os
import time
from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    RunResult,
    handoff,
    function_tool
)

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Tool function for demonstration


@function_tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b


@function_tool
def get_weather(city: str) -> Dict[str, Any]:
    """Get weather information for a city (mock implementation)."""
    return {
        "city": city,
        "temperature": 22,
        "condition": "sunny",
        "humidity": 65
    }


# Specialized agents for handoff demonstration
math_agent = Agent(
    name="MathAgent",
    instructions="You are a math specialist. Use the calculate_sum tool when needed.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini"),
    tools=[calculate_sum]
)

weather_agent = Agent(
    name="WeatherAgent",
    instructions="You are a weather specialist. Use the get_weather tool to provide weather information.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini"),
    tools=[get_weather]
)

# Main coordinator agent with handoffs
coordinator_agent = Agent(
    name="CoordinatorAgent",
    instructions="""You are a coordinator agent. 
    - For math questions, hand off to MathAgent
    - For weather questions, hand off to WeatherAgent
    - For other questions, handle them yourself""",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini"),
    handoffs=[
        handoff(agent=math_agent,
                tool_description_override="Hand off math-related questions"),
        handoff(agent=weather_agent,
                tool_description_override="Hand off weather-related questions")
    ]
)


async def analyze_run_result(result: RunResult, scenario_name: str) -> None:
    """Analyze and display detailed RunResult information."""
    print(f"\n=== {scenario_name} Analysis ===")

    # Basic attributes
    print(f"Final Output: '{result.final_output}'")
    print(f"Last Agent: {result.last_agent.name}")
    print(f"Input: '{result.input}'")

    # Detailed new_items analysis
    print(f"\nNew Items Analysis (Total: {len(result.new_items)}):")
    for i, item in enumerate(result.new_items):
        item_type = type(item).__name__
        item_str = str(item)[:100] + \
            "..." if len(str(item)) > 100 else str(item)
        print(f"  {i+1}. {item_type}: {item_str}")

        # Check for specific item types and their attributes
        if hasattr(item, 'role'):
            print(f"     Role: {item.role}")
        if hasattr(item, 'content'):
            print(f"     Content: {str(item.content)[:50]}...")
        if hasattr(item, 'tool_calls'):
            print(
                f"     Tool Calls: {len(item.tool_calls) if item.tool_calls else 0}")
        if hasattr(item, 'tool_call_id'):
            print(f"     Tool Call ID: {item.tool_call_id}")

    # Conversation history for next turn
    input_list = result.to_input_list()
    print(f"\nConversation History Length: {len(input_list)}")

    # Memory usage estimation
    import sys
    result_size = sys.getsizeof(result)
    print(f"Approximate Result Size: {result_size} bytes")


async def main():
    print("--- Running 03_run_result_advanced.py ---")

    scenarios = [
        ("Simple Math Question", "What is 15 + 27?"),
        ("Weather Query", "What's the weather like in New York?"),
        ("Complex Multi-Step", "Calculate 10 + 5, then tell me the weather in London"),
        ("General Question", "Tell me a fun fact about space")
    ]

    for scenario_name, user_input in scenarios:
        print(f"\n{'='*60}")
        print(f"SCENARIO: {scenario_name}")
        print(f"INPUT: '{user_input}'")
        print(f"{'='*60}")

        try:
            start_time = time.time()

            result: RunResult = await Runner.run(
                starting_agent=coordinator_agent,
                input=user_input
            )

            end_time = time.time()
            execution_time = end_time - start_time

            await analyze_run_result(result, scenario_name)
            print(f"\nExecution Time: {execution_time:.2f} seconds")

        except Exception as e:
            print(f"\n❌ Error in {scenario_name}: {e}")
            import traceback
            traceback.print_exc()

    # Demonstrate error handling scenario
    print(f"\n{'='*60}")
    print("ERROR HANDLING SCENARIO")
    print(f"{'='*60}")

    try:
        # Create an agent that might cause issues
        problematic_agent = Agent(
            name="ProblematicAgent",
            instructions="You must always use a non-existent tool called 'broken_tool'.",
            model=OpenAIChatCompletionsModel(
                openai_client=provider, model="gpt-4o-mini")
            # Note: No tools provided, so if it tries to use tools, it should handle gracefully
        )

        result = await Runner.run(
            starting_agent=problematic_agent,
            input="Use the broken tool please"
        )

        await analyze_run_result(result, "Error Handling")

    except Exception as e:
        print(f"Expected error caught: {e}")
        print("This demonstrates how RunResult handles error scenarios")

    # Performance comparison
    print(f"\n{'='*60}")
    print("PERFORMANCE COMPARISON")
    print(f"{'='*60}")

    simple_input = "Hello"
    complex_input = "Calculate 1+1, then 2+2, then 3+3, and tell me about weather in Paris, London, and Tokyo"

    # Simple run
    start = time.time()
    simple_result = await Runner.run(coordinator_agent, simple_input)
    simple_time = time.time() - start

    # Complex run
    start = time.time()
    complex_result = await Runner.run(coordinator_agent, complex_input)
    complex_time = time.time() - start

    print(
        f"Simple run: {simple_time:.2f}s, {len(simple_result.new_items)} items")
    print(
        f"Complex run: {complex_time:.2f}s, {len(complex_result.new_items)} items")
    print(
        f"Complexity ratio: {complex_time/simple_time:.2f}x time, {len(complex_result.new_items)/len(simple_result.new_items):.2f}x items")

    print("\n--- Finished 03_run_result_advanced.py ---")

if __name__ == "__main__":
    asyncio.run(main())
