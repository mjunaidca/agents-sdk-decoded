"""
03_stream.py

Demonstrates Runner.run_streamed() for receiving real-time events.

- Calls the LLM in streaming mode.
- Returns RunResultStreaming, which provides an async iterator for StreamEvents.
- Shows how to process different event types (TextDelta, ToolCall, etc.).
- After the stream, RunResultStreaming contains the complete run information.

Based on: https://openai.github.io/openai-agents-python/running_agents/#streaming
And: https://openai.github.io/openai-agents-python/streaming/
"""

from agents import function_tool
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

# A simple tool for the streaming agent to use


@function_tool
async def get_current_weather(city: str) -> str:
    """Gets the current weather for a given city."""
    print(f"[Tool Call: get_current_weather for {city}]")
    if "london" in city.lower():
        return "The weather in London is partly cloudy with a chance of rain."
    elif "paris" in city.lower():
        return "Paris is sunny and pleasant."
    else:
        return f"Sorry, I don't have weather information for {city}."


async def main():
    """Runs an agent with streaming and processes events."""
    print("--- Running 03_stream.py ---")

    streaming_agent = Agent(
        name="StreamingWeatherAssistant",
        instructions=(
            "You are a helpful assistant that can provide weather information. "
            "When asked for weather, use the get_current_weather tool. "
            "Politely explain the weather after getting it."
        ),
        model=OpenAIChatCompletionsModel(
            openai_client=provider,
            model="gpt-4o-mini"
        ),
        tools=[get_current_weather]
    )

    user_input = "What's the weather like in London today?"
    print(
        f"\n🤖 Assistant: Running agent with streaming for input: '{user_input}'")

    try:
        run_result_streaming: RunResultStreaming = Runner.run_streamed(
            starting_agent=streaming_agent,
            input=user_input
        )

        print("\n🌊 Streaming Events:")
        final_text_output = ""
        async for event in run_result_streaming.stream_events():
            print(f"\n\n\n  -> Event Type: {type(event).__name__}\n\n\n")
            print(f"\n\n\n  -> Event: {event}\n\n\n")
        print("\n--- Stream Complete ---")

        # The RunResultStreaming object now contains the full result
        print("\n📝 Full RunResultStreaming content (after stream):")
        if run_result_streaming.final_output:
            print(f"  Final Output: {run_result_streaming.final_output}")
        else:
            print("  No final output in RunResultStreaming.")

        # Compare with final_output
        print(f"  Actual Final Text from Deltas: {final_text_output}")

        print(f"\n  Number of new items produced: {len(run_result_streaming.new_items)}")
        for i, item in enumerate(run_result_streaming.new_items):
            print(f"    Item {i+1}: {type(item).__name__} - {str(item)[:100]}...")

        print(f"\n--- Finished 03_stream.py --- ")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print(f"--- Finished 03_stream.py with error --- ")

if __name__ == "__main__":
    asyncio.run(main())
