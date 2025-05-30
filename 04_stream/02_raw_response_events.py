"""
02_raw_response_events.py

Demonstrates raw response events for token-by-token text streaming.

Core Concept: Capture text as it's generated token-by-token using raw response events

Based on:
- https://openai.github.io/openai-agents-python/streaming/
- Raw response events section
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, OpenAIChatCompletionsModel

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Agent for demonstration
joker = Agent(
    name="Joker",
    instructions="You are a helpful assistant that tells jokes.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gpt-4o-mini"
    )
)


async def token_by_token_streaming():
    """Stream text token-by-token using raw response events."""
    print("=== Token-by-Token Streaming ===")

    user_input = "Please tell me 3 short jokes"
    print(f"User: {user_input}")
    print("\nStreaming response token-by-token:")
    print("-" * 50)

    result = Runner.run_streamed(joker, user_input)

    collected_text = ""

    async for event in result.stream_events():
        # Check for raw response events with text deltas
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            token = event.data.delta
            print(token, end="", flush=True)
            collected_text += token

    print("\n" + "-" * 50)
    print(f"Collected text: {collected_text}")
    print(f"Final output: {result.final_output}")
    print(f"Text matches: {collected_text.strip() == result.final_output.strip()}")


async def analyze_all_raw_events():
    """Analyze all types of raw response events."""
    print("\n=== All Raw Response Events Analysis ===")

    result = Runner.run_streamed(joker, "Tell me a joke about programming")

    event_counts = {}
    text_deltas = []

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            event_data_type = type(event.data).__name__
            event_counts[event_data_type] = event_counts.get(
                event_data_type, 0) + 1

            # Collect text deltas specifically
            if isinstance(event.data, ResponseTextDeltaEvent):
                text_deltas.append(event.data.delta)

    print(f"Raw event types encountered:")
    for event_type, count in event_counts.items():
        print(f"  {event_type}: {count} events")

    print(f"\nText deltas collected: {len(text_deltas)}")
    print(f"Total text length: {sum(len(delta) for delta in text_deltas)} characters")

    # Show first few and last few deltas
    if text_deltas:
        print(f"First 3 deltas: {text_deltas[:3]}")
        print(f"Last 3 deltas: {text_deltas[-3:]}")


async def streaming_with_timing():
    """Demonstrate streaming with timing information."""
    print("\n=== Streaming with Timing ===")

    import time

    start_time = time.time()
    first_token_time = None
    token_count = 0

    result = Runner.run_streamed(
        joker, "Explain why streaming is useful in 2 sentences")

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            if first_token_time is None:
                first_token_time = time.time() - start_time
            token_count += 1

    total_time = time.time() - start_time

    print(f"Timing Analysis:")
    print(f"  Time to first token: {first_token_time:.3f}s")
    print(f"  Total streaming time: {total_time:.3f}s")
    print(f"  Tokens received: {token_count}")
    print(f"  Average tokens/second: {token_count/total_time:.1f}")


async def main():
    print("--- Running 02_raw_response_events.py ---")

    await token_by_token_streaming()
    await analyze_all_raw_events()
    await streaming_with_timing()

    print("\n--- Key Concepts Learned ---")
    print("✓ Raw response events provide token-level access")
    print("✓ ResponseTextDeltaEvent contains individual text tokens")
    print("✓ event.type == 'raw_response_event' identifies raw events")
    print("✓ isinstance(event.data, ResponseTextDeltaEvent) checks for text")
    print("✓ event.data.delta contains the actual text token")
    print("✓ Streaming enables real-time user feedback")

    print("\n--- Finished 02_raw_response_events.py ---")


if __name__ == "__main__":
    asyncio.run(main())
