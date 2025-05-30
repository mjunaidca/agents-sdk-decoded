# Error Handling in Function Tools Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
import random
from typing import Any
from agents import Agent, Runner, function_tool, RunContextWrapper


@function_tool
def divide_numbers(a: float, b: float) -> str:
    """Divide two numbers.

    Args:
        a: The dividend (number to be divided)
        b: The divisor (number to divide by)
    """
    if b == 0:
        raise ValueError("Cannot divide by zero!")

    result = a / b
    return f"{a} ÷ {b} = {result}"


@function_tool
def random_error_function() -> str:
    """A function that randomly succeeds or fails for demonstration."""
    if random.random() < 0.5:
        raise RuntimeError("Random error occurred!")
    return "Function executed successfully!"


def custom_error_handler(ctx: RunContextWrapper[Any], error: Exception) -> str:
    """Custom error handler that provides more helpful error messages."""
    if isinstance(error, ValueError):
        return f"Math error: {str(error)} Please check your input values."
    elif isinstance(error, RuntimeError):
        return f"Runtime issue: {str(error)} You might want to try again."
    else:
        return f"Unexpected error: {str(error)} Please contact support if this persists."


@function_tool(failure_error_function=custom_error_handler)
def protected_divide(a: float, b: float) -> str:
    """Divide two numbers with custom error handling.

    Args:
        a: The dividend (number to be divided)
        b: The divisor (number to divide by)
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")

    result = a / b
    return f"Protected division result: {a} ÷ {b} = {result}"


@function_tool(failure_error_function=None)  # Re-raise errors
def strict_divide(a: float, b: float) -> str:
    """Divide two numbers with strict error handling (re-raises errors).

    Args:
        a: The dividend (number to be divided)
        b: The divisor (number to divide by)
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")

    result = a / b
    return f"Strict division result: {a} ÷ {b} = {result}"


async def main():
    # Agent with various error handling approaches
    agent = Agent(
        name="Math Assistant",
        instructions="""You are a math assistant that can perform various calculations.
        When errors occur, try to understand what went wrong and provide helpful guidance to the user.
        If a calculation fails, suggest alternative approaches or corrected inputs.""",
        tools=[divide_numbers, random_error_function,
               protected_divide, strict_divide]
    )

    # Test cases for different error scenarios
    test_cases = [
        "Divide 10 by 2",           # Success case
        "Divide 10 by 0",           # Error case - division by zero
        "Run the random error function",  # May succeed or fail randomly
        "Use protected_divide to divide 15 by 3",  # Success with custom handler
        "Use protected_divide to divide 15 by 0",  # Error with custom handler
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"=== Test Case {i}: {test_case} ===")
        try:
            result = await Runner.run(agent, input=test_case)
            print(f"Result: {result.final_output}")
        except Exception as e:
            print(f"Caught exception: {e}")
        print()

    # Demonstrate handling multiple operations
    print("=== Complex Math Operations ===")
    complex_result = await Runner.run(
        agent,
        input="Calculate these divisions: 100÷5, 50÷10, and 25÷0. For any that fail, explain what went wrong."
    )
    print(complex_result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
