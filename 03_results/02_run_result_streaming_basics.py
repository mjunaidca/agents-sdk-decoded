"""
02_run_result_streaming_basics.py

Demonstrates basic attributes and methods of RunResultStreaming.

Covers:
- Iterating through stream_events()
- Accessing final_output, last_agent, new_items after stream completion
- Using to_input_list() after stream completion
- Checking is_complete

Based on:
- https://openai.github.io/openai-agents-python/results/
- https://openai.github.io/openai-agents-python/ref/result/#agents.result.RunResultStreaming
- https://openai.github.io/openai-agents-python/streaming/
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    RunResultStreaming
)

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Simple agent for demonstration
streaming_agent = Agent(
    name="StoryTellerAgent",
    instructions="You are a Story Teller. Tell a very short story (2-3 sentences) about a brave knight.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini")
)


async def main():
    print("--- Running 02_run_result_streaming_basics.py ---")

    user_input = "Tell me a story."
    print(f"\nUser Input: '{user_input}'")

    try:
        run_result_stream: RunResultStreaming = Runner.run_streamed(
            starting_agent=streaming_agent,
            input=user_input
        )

        print("\n--- Iterating through Stream Events ---")
        full_streamed_text = ""
        async for event in run_result_stream.stream_events():
            print(f"  Event Type: {type(event).__name__}", end="")
            # Check if event has text_delta attribute (for text streaming events)
            if hasattr(event, 'text_delta') and event.text_delta:
                text_chunk = event.text_delta
                print(f" - TextDelta: '{text_chunk}'")
                full_streamed_text += text_chunk
            else:
                # Print some info for other event types
                print(f" - Data: {str(event)[:100]}...")

        print(f"\nFull text collected from TextDelta events: '{full_streamed_text}'")

        print("\n--- Accessing RunResultStreaming Attributes (After Stream) ---")
        # Should be True now
        print(f"Is Complete: {run_result_stream.is_complete}")

        # 1. Final Output
        final_output_stream = run_result_stream.final_output
        print(f"1. Final Output: '{final_output_stream}' (Type: {type(final_output_stream)})")

        # 2. Last Agent
        last_agent_stream = run_result_stream.last_agent
        print(f"2. Last Agent: Name='{last_agent_stream.name}' (Type: {type(last_agent_stream)})")

        # 3. New Items
        new_items_stream = run_result_stream.new_items
        print(f"3. New Items (Count: {len(new_items_stream)}):")
        if new_items_stream:
            for i, item in enumerate(new_items_stream):
                print(f"   - Item {i+1}: {str(item)[:100]}... (Type: {type(item)})")
        else:
            print("   No new items listed.")

        # 4. to_input_list()
        input_list_for_next_turn = run_result_stream.to_input_list()
        print(f"4. Input List for Next Turn (Count: {len(input_list_for_next_turn)}):")
        if input_list_for_next_turn:
            print(f"   First item for next turn: {str(input_list_for_next_turn[0])[:100]}...")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()

    print("\n--- Finished 02_run_result_streaming_basics.py ---")

if __name__ == "__main__":
    asyncio.run(main())
