# Tool Choice Control Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
from agents import Agent, Runner, function_tool, ModelSettings


@function_tool
def get_weather(city: str) -> str:
    """Get weather information for a city.

    Args:
        city: The name of the city
    """
    return f"The weather in {city} is sunny and 72°F"


@function_tool
def get_time(timezone: str = "UTC") -> str:
    """Get current time for a timezone.

    Args:
        timezone: The timezone (default: UTC)
    """
    return f"Current time in {timezone}: 2024-01-01 12:00:00"


@function_tool
def calculate_sum(numbers: list[float]) -> str:
    """Calculate the sum of a list of numbers.

    Args:
        numbers: List of numbers to sum
    """
    total = sum(numbers)
    return f"Sum of {numbers} = {total}"


async def safe_run(agent, input_text, test_name):
    """Safely run an agent with error handling"""
    try:
        result = await Runner.run(agent, input=input_text)
        print(f"Result: {result.final_output}\n")
        return result
    except Exception as e:
        print(f"Error in {test_name}: {type(e).__name__}: {str(e)[:100]}...\n")
        return None


async def main():
    # Base agent with all tools
    base_agent = Agent(
        name="Multi-Tool Assistant",
        instructions="You are a helpful assistant with access to weather, time, and calculation tools.",
        tools=[get_weather, get_time, calculate_sum]
    )

    # Test 1: Default behavior (auto tool choice)
    print("=== Test 1: Default Tool Choice (auto) ===")
    await safe_run(base_agent, "What's the weather in Tokyo?", "Test 1")

    # Test 2: Force tool use (required)
    print("=== Test 2: Required Tool Use ===")
    agent_required = base_agent.clone(
        model_settings=ModelSettings(tool_choice="required")
    )
    await safe_run(agent_required, "Hello, how are you?", "Test 2")

    # Test 3: Forbid tool use (none)
    print("=== Test 3: No Tool Use Allowed ===")
    agent_no_tools = base_agent.clone(
        model_settings=ModelSettings(tool_choice="none")
    )
    await safe_run(agent_no_tools, "What's the weather in London?", "Test 3")

    # Test 4: Force specific tool
    print("=== Test 4: Force Specific Tool (get_weather) ===")
    agent_specific = base_agent.clone(
        model_settings=ModelSettings(tool_choice="get_weather")
    )
    await safe_run(agent_specific, "I need some information", "Test 4")

    # Test 5: Tool choice with reset behavior
    print("=== Test 5: Tool Choice with Reset Behavior ===")
    agent_reset_false = base_agent.clone(
        model_settings=ModelSettings(tool_choice="required"),
        reset_tool_choice=False  # Don't reset after first tool call
    )
    await safe_run(agent_reset_false, "Give me weather and time information", "Test 5")

    # Test 6: Parallel tool calls
    print("=== Test 6: Parallel Tool Calls ===")
    agent_parallel = base_agent.clone(
        model_settings=ModelSettings(
            tool_choice="auto",
            parallel_tool_calls=True
        )
    )
    await safe_run(agent_parallel, "Get weather for Tokyo and calculate sum of [1, 2, 3]", "Test 6")

    # Test 7: Sequential tool calls
    print("=== Test 7: Sequential Tool Calls ===")
    agent_sequential = base_agent.clone(
        model_settings=ModelSettings(
            tool_choice="auto",
            parallel_tool_calls=False
        )
    )
    await safe_run(agent_sequential, "Get weather for Tokyo and calculate sum of [1, 2, 3]", "Test 7")

    # Demonstrate configuration differences
    print("=== Configuration Summary ===")
    configs = [
        ("Default", "tool_choice=auto, parallel_tool_calls=default"),
        ("Required", "tool_choice=required, reset_tool_choice=True"),
        ("None", "tool_choice=none (no tools allowed)"),
        ("Specific", "tool_choice=specific_tool_name"),
        ("Parallel", "parallel_tool_calls=True"),
        ("Sequential", "parallel_tool_calls=False")
    ]

    for config_name, description in configs:
        print(f"{config_name:12} | {description}")

if __name__ == "__main__":
    asyncio.run(main())
