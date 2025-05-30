"""
01_basic_streaming.py

Simple introduction to streaming responses with OpenAI Agents SDK.

Core Concept: Stream responses in real-time as they're generated

Based on:
- https://openai.github.io/openai-agents-python/streaming/
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Simple agent for streaming demonstration
storyteller = Agent(
    name="Storyteller",
    instructions="You are a storyteller. Tell engaging short stories.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gpt-4o-mini"
    )
)


async def basic_streaming_example():
    """Demonstrate basic streaming with stream_events()."""
    print("=== Basic Streaming Example ===")

    user_input = "Tell me a short story about a brave cat"
    print(f"User: {user_input}")
    print("\nStreaming response:")
    print("-" * 40)

    # Start streaming execution
    result = Runner.run_streamed(
        starting_agent=storyteller,
        input=user_input
    )

    # Stream events as they arrive
    async for event in result.stream_events():
        # For now, just print the event type to see what we get
        print(f"Event: {type(event).__name__}")

    print("-" * 40)
    print(f"Final result: {result.final_output}")


async def compare_regular_vs_streaming():
    """Compare regular execution vs streaming execution."""
    print("\n=== Regular vs Streaming Comparison ===")

    user_input = "Tell me about the benefits of AI"

    # Regular execution
    print("1. Regular execution (all at once):")
    regular_result = await Runner.run(storyteller, user_input)
    print(f"Result: {regular_result.final_output}")

    # Streaming execution
    print("\n2. Streaming execution (real-time):")
    stream_result = Runner.run_streamed(storyteller, user_input)

    async for event in stream_result.stream_events():
        # Just show that events are happening
        print(".", end="", flush=True)

    print(f"\nFinal: {stream_result.final_output}")


async def main():
    print("--- Running 01_basic_streaming.py ---")

    await basic_streaming_example()
    await compare_regular_vs_streaming()

    print("\n--- Key Concepts Learned ---")
    print("✓ Runner.run_streamed() starts streaming execution")
    print("✓ stream_events() provides real-time event iteration")
    print("✓ Events arrive as the response is generated")
    print("✓ final_output is available after streaming completes")

    print("\n--- Finished 01_basic_streaming.py ---")


if __name__ == "__main__":
    asyncio.run(main())
