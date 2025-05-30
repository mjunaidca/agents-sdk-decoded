# Sync vs Async Execution Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
import time
import threading
from agents import Agent, Runner, function_tool


@function_tool
def slow_calculation(n: int) -> str:
    """Perform a slow calculation that takes time.

    Args:
        n: Number to process
    """
    # Simulate slow operation
    time.sleep(1)
    result = n * n
    return f"Calculated {n}^2 = {result}"


@function_tool
def get_thread_info() -> str:
    """Get information about the current thread."""
    thread_id = threading.get_ident()
    thread_name = threading.current_thread().name
    time.sleep(3)
    return f"Running in thread: {thread_name} (ID: {thread_id})"


def sync_execution_example():
    """Demonstrate synchronous execution using Runner.run_sync"""
    print("=== Synchronous Execution with Runner.run_sync ===")

    agent = Agent(
        name="Sync Agent",
        instructions="You are a calculation assistant. Use the tools to help with calculations.",
        tools=[slow_calculation, get_thread_info]
    )

    start_time = time.time()

    # Synchronous execution - blocks until complete
    print("Starting sync execution...")
    result = Runner.run_sync(
        agent,
        input="Calculate the square of 5 and tell me what thread you're running in"
    )

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"Sync result: {result.final_output}")
    print(f"Sync execution took: {elapsed:.2f} seconds\n")

    return result


async def async_execution_example():
    """Demonstrate asynchronous execution using Runner.run"""
    print("=== Asynchronous Execution with Runner.run ===")

    agent = Agent(
        name="Async Agent",
        instructions="You are a calculation assistant. Use the tools to help with calculations.",
        tools=[slow_calculation, get_thread_info]
    )

    start_time = time.time()

    # Asynchronous execution - can be awaited
    print("Starting async execution...")
    result = await Runner.run(
        agent,
        input="Calculate the square of 7 and tell me what thread you're running in"
    )

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"Async result: {result.final_output}")
    print(f"Async execution took: {elapsed:.2f} seconds\n")

    return result


async def concurrent_async_example():
    """Demonstrate running multiple agents concurrently"""
    print("=== Concurrent Async Execution ===")

    agent1 = Agent(
        name="Agent 1",
        instructions="Calculate squares quickly.",
        tools=[slow_calculation]
    )

    agent2 = Agent(
        name="Agent 2",
        instructions="Calculate squares quickly.",
        tools=[slow_calculation]
    )

    agent3 = Agent(
        name="Agent 3",
        instructions="Calculate squares quickly.",
        tools=[slow_calculation]
    )

    start_time = time.time()

    # Run multiple agents concurrently
    print("Starting concurrent async execution...")
    results = await asyncio.gather(
        Runner.run(agent1, "Calculate square of 3"),
        Runner.run(agent2, "Calculate square of 4"),
        Runner.run(agent3, "Calculate square of 6")
    )

    end_time = time.time()
    elapsed = end_time - start_time

    print("Concurrent results:")
    for i, result in enumerate(results, 1):
        print(f"  Agent {i}: {result.final_output}")
    print(f"Concurrent execution took: {elapsed:.2f} seconds")
    print("(Notice this is much faster than running sequentially)\n")


def mixed_execution_example():
    """Demonstrate mixing sync and async in different contexts"""
    print("=== Mixed Execution Example ===")

    agent = Agent(
        name="Mixed Agent",
        instructions="You help with calculations.",
        tools=[slow_calculation]
    )

    # In a synchronous context, use run_sync
    print("Using run_sync in synchronous context:")
    sync_result = Runner.run_sync(agent, "Calculate square of 2")
    print(f"Sync result: {sync_result.final_output}")

    # To use async in sync context, need event loop
    print("Using async in synchronous context (with asyncio.run):")

    async def async_task():
        return await Runner.run(agent, "Calculate square of 8")

    async_result = asyncio.run(async_task())
    print(f"Async result: {async_result.final_output}\n")


async def error_handling_comparison():
    """Compare error handling in sync vs async"""
    print("=== Error Handling Comparison ===")

    @function_tool
    def error_tool() -> str:
        """A tool that always raises an error."""
        raise ValueError("This tool always fails!")

    agent = Agent(
        name="Error Agent",
        instructions="Use the error tool.",
        tools=[error_tool]
    )

    # Sync error handling
    print("Sync error handling:")
    try:
        Runner.run_sync(agent, "Use the error tool")
    except Exception as e:
        print(f"Caught sync error: {type(e).__name__}: {e}")

    # Async error handling
    print("Async error handling:")
    try:
        await Runner.run(agent, "Use the error tool")
    except Exception as e:
        print(f"Caught async error: {type(e).__name__}: {e}")


def main():
    """Main function demonstrating different execution patterns"""
    print("OpenAI Agents SDK - Sync vs Async Execution Patterns")
    print("=" * 60)

    # 1. Synchronous execution
    sync_execution_example()

    # 2. Mixed execution (sync context)
    mixed_execution_example()

    # 3. Async execution (need to run in async context)
    async def async_main():
        await async_execution_example()
        await concurrent_async_example()
        await error_handling_comparison()

        # Performance comparison
        print("=== Performance Comparison ===")

        agent = Agent(
            name="Perf Agent",
            instructions="Calculate quickly.",
            tools=[slow_calculation]
        )

        # Sequential sync calls
        print("Sequential sync calls:")
        start = time.time()
        for i in range(3):
            Runner.run_sync(agent, f"Calculate square of {i+1}")
        sync_time = time.time() - start
        print(f"Sequential sync took: {sync_time:.2f} seconds")

        # Concurrent async calls
        print("Concurrent async calls:")
        start = time.time()
        await asyncio.gather(*[
            await Runner.run(agent, f"Calculate square of {i+1}")
            for i in range(3)
        ])
        async_time = time.time() - start
        print(f"Concurrent async took: {async_time:.2f} seconds")
        print(f"Speedup: {sync_time/async_time:.2f}x faster")

    # Run async examples
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
