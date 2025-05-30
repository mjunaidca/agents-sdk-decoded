"""
04_run_result_streaming_advanced.py

Demonstrates advanced RunResultStreaming usage with tools, handoffs, and complex scenarios.

Covers:
- Streaming with tool usage and complex event types
- Real-time event processing and filtering
- Performance monitoring during streaming
- Error handling in streaming scenarios
- Memory-efficient streaming patterns

Based on:
- https://openai.github.io/openai-agents-python/results/
- https://openai.github.io/openai-agents-python/streaming/
- https://openai.github.io/openai-agents-python/tools/
"""

import asyncio
import os
import time
from typing import Dict, Any, List
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    RunResultStreaming,
    StreamEvent,
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

# Tool functions for demonstration


@function_tool
def analyze_data(data: str) -> Dict[str, Any]:
    """Analyze data and return insights (mock implementation)."""
    return {
        "data_length": len(data),
        "word_count": len(data.split()),
        "analysis": "Data appears to be well-structured",
        "confidence": 0.85
    }


@function_tool
def generate_report(title: str, content: str) -> str:
    """Generate a formatted report."""
    return f"""
# {title}

## Content Analysis
{content}

## Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""


# Specialized agents
data_analyst = Agent(
    name="DataAnalyst",
    instructions="You are a data analyst. Use the analyze_data tool to analyze information.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini"),
    tools=[analyze_data]
)

report_generator = Agent(
    name="ReportGenerator",
    instructions="You are a report generator. Use the generate_report tool to create formatted reports.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini"),
    tools=[generate_report]
)

# Main streaming agent with handoffs
streaming_coordinator = Agent(
    name="StreamingCoordinator",
    instructions="""You are a streaming coordinator agent that processes requests in real-time.
    - For data analysis requests, hand off to DataAnalyst
    - For report generation requests, hand off to ReportGenerator
    - Provide detailed, step-by-step responses for complex tasks""",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini"),
    handoffs=[
        handoff(agent=data_analyst,
                tool_description_override="Hand off data analysis tasks"),
        handoff(agent=report_generator,
                tool_description_override="Hand off report generation tasks")
    ]
)


class StreamEventAnalyzer:
    """Analyzes streaming events in real-time."""

    def __init__(self):
        self.event_counts: Dict[str, int] = {}
        self.text_chunks: List[str] = []
        self.start_time = time.time()
        self.total_events = 0

    def process_event(self, event: StreamEvent) -> None:
        """Process a single stream event."""
        self.total_events += 1
        event_type = type(event).__name__
        self.event_counts[event_type] = self.event_counts.get(
            event_type, 0) + 1

        # Collect text chunks if available
        if hasattr(event, 'text_delta') and event.text_delta:
            self.text_chunks.append(event.text_delta)

    def get_statistics(self) -> Dict[str, Any]:
        """Get streaming statistics."""
        elapsed_time = time.time() - self.start_time
        return {
            "total_events": self.total_events,
            "event_types": self.event_counts,
            "elapsed_time": elapsed_time,
            "events_per_second": self.total_events / elapsed_time if elapsed_time > 0 else 0,
            "text_chunks_count": len(self.text_chunks),
            "total_text_length": sum(len(chunk) for chunk in self.text_chunks)
        }


async def stream_with_analysis(agent: Agent, user_input: str, scenario_name: str) -> None:
    """Stream a request and analyze the events in real-time."""
    print(f"\n{'='*60}")
    print(f"STREAMING SCENARIO: {scenario_name}")
    print(f"INPUT: '{user_input}'")
    print(f"{'='*60}")

    analyzer = StreamEventAnalyzer()

    try:
        run_result_stream: RunResultStreaming = Runner.run_streamed(
            starting_agent=agent,
            input=user_input
        )

        print("\n--- Real-time Stream Events ---")
        collected_text = ""

        async for event in run_result_stream.stream_events():
            analyzer.process_event(event)

            event_type = type(event).__name__

            # Handle different event types
            if hasattr(event, 'text_delta') and event.text_delta:
                text_chunk = event.text_delta
                collected_text += text_chunk
                print(f"[TEXT] {text_chunk}", end="", flush=True)
            elif hasattr(event, 'tool_call'):
                print(f"\n[TOOL_CALL] {event_type}")
            elif hasattr(event, 'handoff'):
                print(f"\n[HANDOFF] {event_type}")
            else:
                print(f"\n[EVENT] {event_type}: {str(event)[:50]}...")

        print(f"\n\n--- Stream Completed ---")
        print(f"Is Complete: {run_result_stream.is_complete}")

        # Final result analysis
        print(f"\n--- Final Result Analysis ---")
        print(f"Final Output: '{run_result_stream.final_output}'")
        print(f"Last Agent: {run_result_stream.last_agent.name}")
        print(f"New Items Count: {len(run_result_stream.new_items)}")

        # Streaming statistics
        stats = analyzer.get_statistics()
        print(f"\n--- Streaming Statistics ---")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")

        # Verify text consistency
        if collected_text.strip() != run_result_stream.final_output.strip():
            print(f"\n⚠️  Text mismatch detected!")
            print(f"Streamed: '{collected_text[:100]}...'")
            print(f"Final: '{run_result_stream.final_output[:100]}...'")
        else:
            print(f"\n✅ Text consistency verified")

    except Exception as e:
        print(f"\n❌ Streaming error: {e}")
        import traceback
        traceback.print_exc()


async def demonstrate_streaming_patterns():
    """Demonstrate various streaming patterns and use cases."""

    scenarios = [
        ("Simple Response", "Tell me about artificial intelligence in 2 sentences."),
        ("Data Analysis Task",
         "Analyze this data: 'AI adoption rates: 2020: 15%, 2021: 25%, 2022: 40%, 2023: 60%'"),
        ("Report Generation", "Generate a report titled 'AI Trends 2024' with content about machine learning advances"),
        ("Complex Multi-Step", "First analyze the data 'Sales Q1: $100k, Q2: $150k, Q3: $200k', then generate a quarterly report"),
        ("Error Scenario",
         "Use a non-existent tool called 'magic_analyzer' to process some data")
    ]

    for scenario_name, user_input in scenarios:
        await stream_with_analysis(streaming_coordinator, user_input, scenario_name)

        # Small delay between scenarios
        await asyncio.sleep(1)


async def compare_streaming_vs_regular():
    """Compare streaming vs regular execution performance."""
    print(f"\n{'='*60}")
    print("PERFORMANCE COMPARISON: Streaming vs Regular")
    print(f"{'='*60}")

    test_input = "Explain the benefits of streaming responses in AI applications"

    # Regular execution
    print("\n--- Regular Execution ---")
    start_time = time.time()
    regular_result = await Runner.run(streaming_coordinator, test_input)
    regular_time = time.time() - start_time

    print(f"Regular execution time: {regular_time:.2f}s")
    print(f"Final output length: {len(regular_result.final_output)} chars")

    # Streaming execution
    print("\n--- Streaming Execution ---")
    start_time = time.time()
    stream_result = Runner.run_streamed(streaming_coordinator, test_input)

    first_chunk_time = None
    total_chunks = 0

    async for event in stream_result.stream_events():
        if hasattr(event, 'text_delta') and event.text_delta and first_chunk_time is None:
            first_chunk_time = time.time() - start_time
        if hasattr(event, 'text_delta') and event.text_delta:
            total_chunks += 1

    streaming_time = time.time() - start_time

    print(f"Streaming execution time: {streaming_time:.2f}s")
    print(
        f"Time to first chunk: {first_chunk_time:.2f}s" if first_chunk_time else "No text chunks received")
    print(f"Total text chunks: {total_chunks}")
    print(f"Final output length: {len(stream_result.final_output)} chars")

    # Performance analysis
    print(f"\n--- Performance Analysis ---")
    print(f"Time difference: {abs(streaming_time - regular_time):.2f}s")
    print(
        f"First chunk advantage: {(regular_time - first_chunk_time):.2f}s" if first_chunk_time else "N/A")
    print(
        f"Streaming overhead: {((streaming_time - regular_time) / regular_time * 100):.1f}%" if regular_time > 0 else "N/A")


async def main():
    print("--- Running 04_run_result_streaming_advanced.py ---")

    # Demonstrate various streaming scenarios
    await demonstrate_streaming_patterns()

    # Performance comparison
    await compare_streaming_vs_regular()

    print("\n--- Finished 04_run_result_streaming_advanced.py ---")

if __name__ == "__main__":
    asyncio.run(main())
