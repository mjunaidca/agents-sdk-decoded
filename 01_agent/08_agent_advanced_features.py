"""
Advanced Agent Features Demo
Covers: clone(), as_tool(), model_settings, tool_use_behavior, reset_tool_choice

This demonstrates the remaining Agent features not covered in previous examples.
"""

import asyncio
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from agents.agent import ToolsToFinalOutputResult
from agents.model_settings import ModelSettings
from agents.run_context import RunContextWrapper

load_dotenv(find_dotenv())

provider = AsyncOpenAI(base_url="https://api.openai.com/v1",
                       api_key=os.getenv("OPENAI_API_KEY"))


@dataclass
class TaskContext:
    task_count: int = 0
    completed_tasks: list[str] | None = None

    def __post_init__(self):
        if self.completed_tasks is None:
            self.completed_tasks = []

# =============================================================================
# DEMO 1: Agent.clone() - Creating Agent Variants
# =============================================================================


async def demo_agent_cloning():
    """Demonstrate agent cloning for creating specialized variants"""
    print("=" * 60)
    print("DEMO 1: Agent Cloning")
    print("=" * 60)

    # Base agent
    base_agent = Agent(
        name="BaseAssistant",
        instructions="You are a helpful assistant.",
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini"),
        model_settings=ModelSettings(temperature=0.7)
    )

    # Clone with different instructions
    creative_agent = base_agent.clone(
        name="CreativeAssistant",
        instructions="You are a creative writing assistant. Always respond with vivid, imaginative language.",
        model_settings=ModelSettings(temperature=0.9)
    )

    # Clone with different model settings
    precise_agent = base_agent.clone(
        name="PreciseAssistant",
        instructions="You are a precise, factual assistant. Be concise and accurate.",
        model_settings=ModelSettings(temperature=0.1, top_p=0.8)
    )

    query = "Describe a sunset."

    print("🤖 Base Agent Response:")
    result = await Runner.run(base_agent, query)
    print(f"   {result.final_output}\n")

    print("🎨 Creative Agent Response:")
    result = await Runner.run(creative_agent, query)
    print(f"   {result.final_output}\n")

    print("📊 Precise Agent Response:")
    result = await Runner.run(precise_agent, query)
    print(f"   {result.final_output}\n")

# =============================================================================
# DEMO 2: Agent.as_tool() - Converting Agents to Tools
# =============================================================================


@function_tool
async def get_weather(context: RunContextWrapper, city: str) -> str:
    """Get weather information for a city"""
    # Simulate weather API
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Cloudy, 15°C",
        "Tokyo": "Rainy, 18°C"
    }
    return weather_data.get(city, f"Weather data not available for {city}")


async def demo_agent_as_tool():
    """Demonstrate converting an agent into a tool for other agents"""
    print("=" * 60)
    print("DEMO 2: Agent as Tool")
    print("=" * 60)

    # Specialized research agent
    research_agent = Agent(
        name="ResearchSpecialist",
        instructions="""You are a research specialist. When given a topic, provide:
        1. Key facts and statistics
        2. Recent developments
        3. Expert opinions
        Always be thorough and cite your reasoning.""",
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    # Convert research agent to a tool
    research_tool = research_agent.as_tool(
        tool_name="research_topic",
        tool_description="Research a topic thoroughly and provide comprehensive information"
    )

    # Main agent that can use the research tool
    main_agent = Agent(
        name="MainAssistant",
        instructions="You are a helpful assistant. Use the research tool when you need detailed information about a topic.",
        tools=[research_tool, get_weather],
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    print("🔍 Using Research Agent as Tool:")
    result = await Runner.run(
        main_agent,
        "I need comprehensive information about renewable energy trends, and also what's the weather like in Tokyo?"
    )
    print(f"   {result.final_output}\n")

# =============================================================================
# DEMO 3: tool_use_behavior - Controlling Tool Execution Flow
# =============================================================================


@function_tool
async def calculate_sum(context: RunContextWrapper, numbers: list[int]) -> str:
    """Calculate the sum of a list of numbers"""
    total = sum(numbers)
    context.context.task_count += 1
    return f"Sum of {numbers} = {total}"


@function_tool
async def calculate_product(context: RunContextWrapper, numbers: list[int]) -> str:
    """Calculate the product of a list of numbers"""
    product = 1
    for num in numbers:
        product *= num
    context.context.task_count += 1
    return f"Product of {numbers} = {product}"


@function_tool
async def final_calculation(context: RunContextWrapper, operation: str, result: str) -> str:
    """Mark a calculation as complete"""
    context.context.completed_tasks.append(f"{operation}: {result}")
    return f"✅ Completed {operation} - {result}"


async def demo_tool_use_behavior():
    """Demonstrate different tool_use_behavior settings"""
    print("=" * 60)
    print("DEMO 3: Tool Use Behavior")
    print("=" * 60)

    context = TaskContext()

    # 1. Default behavior: "run_llm_again"
    print("🔄 Default Behavior (run_llm_again):")
    agent_default = Agent(
        name="DefaultAgent",
        instructions="You are a calculator. Use tools to perform calculations and explain the results.",
        tools=[calculate_sum, calculate_product],
        tool_use_behavior="run_llm_again",  # Default
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    result = await Runner.run(agent_default, "Calculate the sum of [1, 2, 3, 4, 5]", context=context)
    print(f"   {result.final_output}")
    print(f"   Task count: {context.task_count}\n")

    # 2. Stop on first tool
    print("⏹️  Stop on First Tool:")
    context = TaskContext()  # Reset context
    agent_stop_first = Agent(
        name="StopFirstAgent",
        instructions="Use tools to perform calculations.",
        tools=[calculate_sum, calculate_product],
        tool_use_behavior="stop_on_first_tool",
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    result = await Runner.run(agent_stop_first, "Calculate the sum of [1, 2, 3, 4, 5]", context=context)
    print(f"   {result.final_output}")
    print(f"   Task count: {context.task_count}\n")

    # 3. Stop at specific tools
    print("🎯 Stop at Specific Tools:")
    context = TaskContext()  # Reset context
    agent_stop_specific = Agent(
        name="StopSpecificAgent",
        instructions="Use tools to perform calculations.",
        tools=[calculate_sum, calculate_product, final_calculation],
        tool_use_behavior={"stop_at_tool_names": ["final_calculation"]},
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    result = await Runner.run(
        agent_stop_specific,
        "Calculate the sum of [1, 2, 3] and mark it as complete",
        context=context
    )
    print(f"   {result.final_output}")
    print(f"   Completed tasks: {context.completed_tasks}\n")

# =============================================================================
# DEMO 4: Custom Tool Behavior Function
# =============================================================================


async def custom_tool_behavior(
    context: RunContextWrapper[TaskContext],
    tool_results: list[Any]
) -> ToolsToFinalOutputResult:
    """Custom function to determine when to stop based on tool results"""

    # Stop if we've completed 2 or more tasks
    if context.context.task_count >= 2:
        return ToolsToFinalOutputResult(
            is_final_output=True,
            final_output=f"Completed {context.context.task_count} calculations. Stopping here."
        )

    # Continue if less than 2 tasks
    return ToolsToFinalOutputResult(is_final_output=False)


async def demo_custom_tool_behavior():
    """Demonstrate custom tool behavior function"""
    print("=" * 60)
    print("DEMO 4: Custom Tool Behavior Function")
    print("=" * 60)

    context = TaskContext()

    agent_custom = Agent(
        name="CustomBehaviorAgent",
        instructions="You are a calculator. Perform multiple calculations as requested.",
        tools=[calculate_sum, calculate_product],
        tool_use_behavior=custom_tool_behavior,
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    result = await Runner.run(
        agent_custom,
        "Calculate the sum of [1, 2, 3], then the product of [2, 3, 4], then the sum of [5, 6, 7]",
        context=context
    )
    print(f"   {result.final_output}")
    print(f"   Final task count: {context.task_count}\n")

# =============================================================================
# DEMO 5: reset_tool_choice Setting
# =============================================================================


async def demo_reset_tool_choice():
    """Demonstrate reset_tool_choice behavior"""
    print("=" * 60)
    print("DEMO 5: Reset Tool Choice")
    print("=" * 60)

    # Agent with reset_tool_choice=True (default)
    print("✅ With reset_tool_choice=True (prevents tool loops):")
    agent_reset_true = Agent(
        name="ResetTrueAgent",
        instructions="Use calculation tools. After using a tool, provide a summary.",
        tools=[calculate_sum],
        reset_tool_choice=True,  # Default
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    result = await Runner.run(agent_reset_true, "Calculate sum of [1, 2, 3]", context=TaskContext())
    print(f"   {result.final_output}\n")

    # Agent with reset_tool_choice=False
    print("⚠️  With reset_tool_choice=False (may cause repeated tool use):")
    agent_reset_false = Agent(
        name="ResetFalseAgent",
        instructions="Use calculation tools once and provide a brief response.",
        tools=[calculate_sum],
        reset_tool_choice=False,
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    result = await Runner.run(agent_reset_false, "Calculate sum of [1, 2, 3]", context=TaskContext())
    print(f"   {result.final_output}\n")

# =============================================================================
# MAIN EXECUTION
# =============================================================================


async def main():
    """Run all advanced agent feature demonstrations"""
    print("🚀 ADVANCED AGENT FEATURES DEMONSTRATION")
    print("=" * 80)

    await demo_agent_cloning()
    await demo_agent_as_tool()
    await demo_tool_use_behavior()
    await demo_custom_tool_behavior()
    await demo_reset_tool_choice()

    print("=" * 80)
    print("🎓 KEY TAKEAWAYS:")
    print("""
    1. 🔄 clone() - Create agent variants with different settings
    2. 🛠️  as_tool() - Convert agents into tools for other agents  
    3. ⚙️  tool_use_behavior - Control when tool execution stops
    4. 🎯 Custom behavior functions - Advanced tool flow control
    5. 🔒 reset_tool_choice - Prevent infinite tool loops
    
    These features enable sophisticated agent architectures and workflows!
    """)

if __name__ == "__main__":
    asyncio.run(main())
