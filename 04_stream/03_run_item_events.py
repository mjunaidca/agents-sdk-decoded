"""
03_run_item_events.py

Demonstrates run item events and agent events for higher-level streaming.

Core Concept: Stream higher-level events like tool calls, messages, and agent updates

Based on:
- https://openai.github.io/openai-agents-python/streaming/
- Run item events and agent events section
"""

import asyncio
import os
import random
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, ItemHelpers

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Tool function for demonstration


@function_tool
def how_many_jokes() -> int:
    """Determine how many jokes to tell."""
    return random.randint(1, 3)


# Agent with tools for streaming demonstration
joker_with_tools = Agent(
    name="JokerWithTools",
    instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gpt-4o-mini"
    ),
    tools=[how_many_jokes]
)


async def stream_high_level_events():
    """Demonstrate streaming high-level events (ignoring raw events)."""
    print("=== High-Level Event Streaming ===")

    user_input = "Hello, tell me some jokes!"
    print(f"User: {user_input}")
    print("\nStreaming high-level events:")
    print("-" * 50)

    result = Runner.run_streamed(
        starting_agent=joker_with_tools,
        input=user_input
    )

    async for event in result.stream_events():
        # Ignore raw response events - focus on high-level events
        if event.type == "raw_response_event":
            continue

        # Handle agent updates
        elif event.type == "agent_updated_stream_event":
            print(f"🤖 Agent updated: {event.new_agent.name}")

        # Handle run item events
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("🔧 Tool was called")

            elif event.item.type == "tool_call_output_item":
                print(f"📤 Tool output: {event.item.output}")

            elif event.item.type == "message_output_item":
                message_text = ItemHelpers.text_message_output(event.item)
                print(f"💬 Message output:\n{message_text}")

            else:
                print(f"📋 Other item: {event.item.type}")

    print("-" * 50)
    print("✅ Run complete!")


async def analyze_event_types():
    """Analyze different types of streaming events."""
    print("\n=== Event Type Analysis ===")

    result = Runner.run_streamed(joker_with_tools, "Give me 2 jokes")

    event_counts = {}
    item_types = {}

    async for event in result.stream_events():
        # Count event types
        event_type = event.type
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

        # Count item types for run_item_stream_events
        if event_type == "run_item_stream_event":
            item_type = event.item.type
            item_types[item_type] = item_types.get(item_type, 0) + 1

    print("Event type counts:")
    for event_type, count in event_counts.items():
        print(f"  {event_type}: {count}")

    print("\nItem type counts (within run_item_stream_events):")
    for item_type, count in item_types.items():
        print(f"  {item_type}: {count}")


async def stream_with_progress_updates():
    """Demonstrate streaming with user-friendly progress updates."""
    print("\n=== Progress Updates Demo ===")

    result = Runner.run_streamed(joker_with_tools, "Tell me jokes!")

    print("🚀 Starting joke generation...")

    async for event in result.stream_events():
        # Skip raw events for cleaner output
        if event.type == "raw_response_event":
            continue

        elif event.type == "agent_updated_stream_event":
            print(f"🔄 Switched to agent: {event.new_agent.name}")

        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("🎲 Deciding how many jokes to tell...")

            elif event.item.type == "tool_call_output_item":
                joke_count = event.item.output
                print(f"📊 Will tell {joke_count} jokes")

            elif event.item.type == "message_output_item":
                print("📝 Generating jokes...")

    print("🎉 All done! Here's what we got:")
    print(f"Final result: {result.final_output}")


async def compare_streaming_approaches():
    """Compare raw events vs high-level events."""
    print("\n=== Streaming Approaches Comparison ===")

    user_input = "Quick joke please"

    # Approach 1: Raw events only
    print("1. Raw events approach (token-by-token):")
    result1 = Runner.run_streamed(joker_with_tools, user_input)

    token_count = 0
    async for event in result1.stream_events():
        if event.type == "raw_response_event":
            token_count += 1

    print(f"   Processed {token_count} raw events")

    # Approach 2: High-level events only
    print("\n2. High-level events approach (structured updates):")
    result2 = Runner.run_streamed(joker_with_tools, user_input)

    high_level_count = 0
    async for event in result2.stream_events():
        if event.type != "raw_response_event":
            high_level_count += 1
            print(f"   {event.type}")

    print(f"   Processed {high_level_count} high-level events")


async def main():
    print("--- Running 03_run_item_events.py ---")

    await stream_high_level_events()
    await analyze_event_types()
    await stream_with_progress_updates()
    await compare_streaming_approaches()

    print("\n--- Key Concepts Learned ---")
    print("✓ run_item_stream_event provides structured item updates")
    print("✓ agent_updated_stream_event tracks agent changes")
    print("✓ tool_call_item and tool_call_output_item track tool usage")
    print("✓ message_output_item contains final message content")
    print("✓ ItemHelpers.text_message_output() extracts text from messages")
    print("✓ High-level events are better for user progress updates")

    print("\n--- Finished 03_run_item_events.py ---")


if __name__ == "__main__":
    asyncio.run(main())
