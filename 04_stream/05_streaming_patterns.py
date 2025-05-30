"""
05_streaming_patterns.py

Demonstrates practical streaming patterns and best practices.

Core Concept: Real-world streaming patterns for production applications

Based on:
- https://openai.github.io/openai-agents-python/streaming/
- Production streaming best practices
"""

import asyncio
import os
import time
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)


@function_tool
def search_database(query: str) -> str:
    """Simulate database search."""
    time.sleep(0.5)  # Simulate processing time
    return f"Found 3 results for '{query}': Result1, Result2, Result3"


# Agent for demonstrations
assistant = Agent(
    name="StreamingAssistant",
    instructions="You are a helpful assistant. Use tools when needed and provide detailed responses.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider,
        model="gpt-4o-mini"
    ),
    tools=[search_database]
)


class StreamingUI:
    """Simulates a UI that processes streaming responses."""

    def __init__(self):
        self.current_text = ""
        self.status = "idle"
        self.progress_indicators = []

    def update_status(self, status: str):
        """Update UI status."""
        self.status = status
        print(f"[UI] Status: {status}")

    def add_text_chunk(self, chunk: str):
        """Add text chunk to UI."""
        self.current_text += chunk
        # In real UI, this would update the display
        print(chunk, end="", flush=True)

    def show_progress(self, message: str):
        """Show progress indicator."""
        self.progress_indicators.append(message)
        print(f"\n[UI] {message}")

    def finalize(self):
        """Finalize the UI display."""
        print(f"\n[UI] Final text length: {len(self.current_text)} characters")
        print(f"[UI] Progress steps: {len(self.progress_indicators)}")


async def ui_friendly_streaming():
    """Demonstrate UI-friendly streaming pattern."""
    print("=== UI-Friendly Streaming Pattern ===")

    ui = StreamingUI()
    ui.update_status("starting")

    user_input = "Search for 'AI agents' and explain what you found"
    print(f"User: {user_input}")
    print("\nStreaming response:")
    print("-" * 50)

    result = Runner.run_streamed(assistant, user_input)

    async for event in result.stream_events():
        # Handle different event types for UI
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            ui.add_text_chunk(event.data.delta)

        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                ui.show_progress("🔍 Searching database...")

            elif event.item.type == "tool_call_output_item":
                ui.show_progress("✅ Search complete")

            elif event.item.type == "message_output_item":
                ui.show_progress("📝 Generating response...")

    ui.update_status("complete")
    ui.finalize()


async def buffered_streaming():
    """Demonstrate buffered streaming for smoother output."""
    print("\n=== Buffered Streaming Pattern ===")

    user_input = "Explain machine learning in simple terms"
    print(f"User: {user_input}")
    print("\nBuffered streaming (word-by-word):")
    print("-" * 50)

    result = Runner.run_streamed(assistant, user_input)

    buffer = ""

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            buffer += event.data.delta

            # Output complete words
            while " " in buffer:
                word, buffer = buffer.split(" ", 1)
                print(word + " ", end="", flush=True)
                await asyncio.sleep(0.1)  # Smooth output

    # Output remaining buffer
    if buffer.strip():
        print(buffer, end="")

    print("\n" + "-" * 50)


async def error_handling_streaming():
    """Demonstrate error handling in streaming."""
    print("\n=== Error Handling Pattern ===")

    user_input = "Tell me about quantum computing"
    print(f"User: {user_input}")
    print("\nStreaming with error handling:")
    print("-" * 50)

    try:
        result = Runner.run_streamed(assistant, user_input)

        collected_text = ""
        event_count = 0

        async for event in result.stream_events():
            event_count += 1

            # Simulate error detection
            if event_count > 100:  # Arbitrary limit for demo
                print("\n[ERROR] Too many events, stopping stream")
                break

            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                chunk = event.data.delta
                collected_text += chunk
                print(chunk, end="", flush=True)

        print(f"\n[SUCCESS] Streamed {len(collected_text)} characters")

    except Exception as e:
        print(f"\n[ERROR] Streaming failed: {e}")
        # Fallback to regular execution
        print("[FALLBACK] Using regular execution...")
        fallback_result = await Runner.run(assistant, user_input)
        print(f"Fallback result: {fallback_result.final_output}")


async def performance_monitoring():
    """Demonstrate performance monitoring during streaming."""
    print("\n=== Performance Monitoring Pattern ===")

    user_input = "Explain the benefits of streaming responses"
    print(f"User: {user_input}")
    print("\nStreaming with performance monitoring:")
    print("-" * 50)

    start_time = time.time()
    first_chunk_time = None
    chunk_count = 0
    total_chars = 0

    result = Runner.run_streamed(assistant, user_input)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            if first_chunk_time is None:
                first_chunk_time = time.time() - start_time

            chunk = event.data.delta
            chunk_count += 1
            total_chars += len(chunk)

            print(chunk, end="", flush=True)

    total_time = time.time() - start_time

    print(f"\n" + "-" * 50)
    print("Performance Metrics:")
    print(f"  Time to first chunk: {first_chunk_time:.3f}s")
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Chunks received: {chunk_count}")
    print(f"  Characters streamed: {total_chars}")
    print(f"  Average chars/second: {total_chars/total_time:.1f}")


async def multi_stream_coordination():
    """Demonstrate coordinating multiple streams."""
    print("\n=== Multi-Stream Coordination Pattern ===")

    queries = [
        "What is AI?",
        "What is ML?",
        "What is NLP?"
    ]

    print("Starting multiple streams:")

    # Start multiple streams
    streams = []
    for query in queries:
        result = Runner.run_streamed(assistant, query)
        streams.append((query, result))

    # Process streams concurrently
    async def process_stream(query: str, stream_result):
        print(f"\n[{query}] Starting...")
        char_count = 0

        async for event in stream_result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                char_count += len(event.data.delta)

        print(f"[{query}] Complete - {char_count} characters")
        return char_count

    # Wait for all streams to complete
    tasks = [process_stream(query, stream) for query, stream in streams]
    results = await asyncio.gather(*tasks)

    print(f"\nAll streams complete. Total characters: {sum(results)}")


async def streaming_with_cancellation():
    """Demonstrate stream cancellation."""
    print("\n=== Stream Cancellation Pattern ===")

    user_input = "Write a very long essay about the history of computing"
    print(f"User: {user_input}")
    print("\nStreaming with cancellation after 3 seconds:")
    print("-" * 50)

    result = Runner.run_streamed(assistant, user_input)

    start_time = time.time()
    collected_text = ""

    try:
        async for event in result.stream_events():
            # Check for cancellation condition
            if time.time() - start_time > 3.0:
                print("\n[CANCELLED] Stream cancelled by user")
                break

            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                chunk = event.data.delta
                collected_text += chunk
                print(chunk, end="", flush=True)

    except asyncio.CancelledError:
        print("\n[CANCELLED] Stream was cancelled")

    print(
        f"\nPartial result ({len(collected_text)} chars): {collected_text[:100]}...")


async def main():
    print("--- Running 05_streaming_patterns.py ---")

    await ui_friendly_streaming()
    await buffered_streaming()
    await error_handling_streaming()
    await performance_monitoring()
    await multi_stream_coordination()
    await streaming_with_cancellation()

    print("\n--- Key Patterns Learned ---")
    print("✓ UI-friendly streaming with status updates")
    print("✓ Buffered streaming for smoother output")
    print("✓ Error handling with fallback strategies")
    print("✓ Performance monitoring and metrics")
    print("✓ Multi-stream coordination")
    print("✓ Stream cancellation and cleanup")
    print("✓ Real-time user feedback patterns")

    print("\n--- Finished 05_streaming_patterns.py ---")


if __name__ == "__main__":
    asyncio.run(main())
