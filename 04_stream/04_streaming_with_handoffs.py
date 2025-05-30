"""
04_streaming_with_handoffs.py

Demonstrates streaming with agent handoffs and transitions.

Core Concept: Stream agent handoffs and see how agent transitions work in real-time

Based on:
- https://openai.github.io/openai-agents-python/streaming/
- https://openai.github.io/openai-agents-python/handoffs/
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, handoff, function_tool

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Tool for math specialist


@function_tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression safely."""
    try:
        # Simple evaluation for demo (in production, use safer methods)
        result = eval(expression.replace("^", "**"))
        return str(result)
    except:
        return "Error in calculation"


# Specialized agents
math_specialist = Agent(
    name="MathSpecialist",
    instructions="You are a math expert. Use the calculate tool for mathematical operations.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gpt-4o-mini"
    ),
    tools=[calculate]
)

story_specialist = Agent(
    name="StorySpecialist",
    instructions="You are a creative storyteller. Tell engaging short stories.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gpt-4o-mini"
    )
)

# Coordinator agent with handoffs
coordinator = Agent(
    name="Coordinator",
    instructions="""You are a helpful coordinator. 
    - For math questions, hand off to MathSpecialist
    - For story requests, hand off to StorySpecialist
    - For other questions, handle them yourself""",
    model=OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gpt-4o-mini"
    ),
    handoffs=[
        handoff(agent=math_specialist,
                tool_description_override="Hand off math problems to the math specialist"),
        handoff(agent=story_specialist,
                tool_description_override="Hand off story requests to the story specialist")
    ]
)


async def stream_math_handoff():
    """Demonstrate streaming with math handoff."""
    print("=== Math Handoff Streaming ===")

    user_input = "What is 15 * 23 + 47?"
    print(f"User: {user_input}")
    print("\nStreaming with handoff:")
    print("-" * 50)

    result = Runner.run_streamed(coordinator, user_input)

    current_agent = "Unknown"

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue

        elif event.type == "agent_updated_stream_event":
            current_agent = event.new_agent.name
            print(f"🔄 Agent changed to: {current_agent}")

        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print(f"🔧 {current_agent} is calling a tool...")

            elif event.item.type == "tool_call_output_item":
                print(f"📤 Tool result: {event.item.output}")

            elif event.item.type == "message_output_item":
                print(f"💬 {current_agent} says: {event.item.content}")

    print("-" * 50)
    print(f"Final result: {result.final_output}")


async def stream_story_handoff():
    """Demonstrate streaming with story handoff."""
    print("\n=== Story Handoff Streaming ===")

    user_input = "Tell me a short story about a robot learning to paint"
    print(f"User: {user_input}")
    print("\nStreaming with handoff:")
    print("-" * 50)

    result = Runner.run_streamed(coordinator, user_input)

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue

        elif event.type == "agent_updated_stream_event":
            print(f"🔄 Handed off to: {event.new_agent.name}")

        elif event.type == "run_item_stream_event":
            if event.item.type == "message_output_item":
                print(f"📖 Story content received")

    print("-" * 50)
    print("Story complete!")


async def stream_no_handoff():
    """Demonstrate streaming without handoff (coordinator handles directly)."""
    print("\n=== No Handoff Streaming ===")

    user_input = "What's the weather like today?"
    print(f"User: {user_input}")
    print("\nStreaming without handoff:")
    print("-" * 50)

    result = Runner.run_streamed(coordinator, user_input)

    agent_changes = 0

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue

        elif event.type == "agent_updated_stream_event":
            agent_changes += 1
            print(f"🔄 Agent: {event.new_agent.name}")

        elif event.type == "run_item_stream_event":
            if event.item.type == "message_output_item":
                print(f"💬 Direct response from coordinator")

    print(f"Agent changes: {agent_changes}")
    print("-" * 50)


async def analyze_handoff_patterns():
    """Analyze different handoff patterns in streaming."""
    print("\n=== Handoff Pattern Analysis ===")

    test_cases = [
        ("Math", "Calculate 100 / 5"),
        ("Story", "Write a haiku about coding"),
        ("General", "What is the capital of France?")
    ]

    for case_type, user_input in test_cases:
        print(f"\n{case_type} case: '{user_input}'")

        result = Runner.run_streamed(coordinator, user_input)

        agents_used = []
        handoff_count = 0

        async for event in result.stream_events():
            if event.type == "agent_updated_stream_event":
                agent_name = event.new_agent.name
                if agent_name not in agents_used:
                    agents_used.append(agent_name)
                    if len(agents_used) > 1:  # First agent is always coordinator
                        handoff_count += 1

        print(f"  Agents used: {' → '.join(agents_used)}")
        print(f"  Handoffs: {handoff_count}")


async def stream_with_detailed_tracking():
    """Stream with detailed event tracking."""
    print("\n=== Detailed Streaming Tracking ===")

    user_input = "Calculate 7 * 8, then tell me a story about the number 56"
    print(f"User: {user_input}")
    print("\nDetailed streaming events:")
    print("-" * 60)

    result = Runner.run_streamed(coordinator, user_input)

    event_sequence = []

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue

        elif event.type == "agent_updated_stream_event":
            event_info = f"AGENT_CHANGE: {event.new_agent.name}"
            event_sequence.append(event_info)
            print(f"🔄 {event_info}")

        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                event_info = "TOOL_CALL"
                event_sequence.append(event_info)
                print(f"🔧 {event_info}")

            elif event.item.type == "tool_call_output_item":
                event_info = f"TOOL_OUTPUT: {event.item.output}"
                event_sequence.append(event_info)
                print(f"📤 {event_info}")

            elif event.item.type == "message_output_item":
                event_info = "MESSAGE_OUTPUT"
                event_sequence.append(event_info)
                print(f"💬 {event_info}")

    print("-" * 60)
    print("Event sequence:")
    for i, event in enumerate(event_sequence, 1):
        print(f"  {i}. {event}")


async def main():
    print("--- Running 04_streaming_with_handoffs.py ---")

    await stream_math_handoff()
    await stream_story_handoff()
    await stream_no_handoff()
    await analyze_handoff_patterns()
    await stream_with_detailed_tracking()

    print("\n--- Key Concepts Learned ---")
    print("✓ agent_updated_stream_event tracks handoffs in real-time")
    print("✓ Handoffs are seamless in streaming - no interruption")
    print("✓ Each agent's work is visible through streaming events")
    print("✓ Tool usage by specialized agents is tracked")
    print("✓ Complex workflows with multiple handoffs stream smoothly")
    print("✓ event.new_agent shows which agent is currently active")

    print("\n--- Finished 04_streaming_with_handoffs.py ---")


if __name__ == "__main__":
    asyncio.run(main())
