"""
02_run_sync.py

Demonstrates the synchronous Runner.run_sync() method.

- A synchronous wrapper around the asynchronous Runner.run().
- Useful for integrating agent calls into synchronous codebases.

Based on: https://openai.github.io/openai-agents-python/running_agents/
"""

import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI  # Still need AsyncOpenAI for the model provider
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunResult

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client (even for run_sync, the underlying model might be async)
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)


def main_sync():
    """Runs a simple agent synchronously and prints its output."""
    print("--- Running 02_run_sync.py ---")

    # 1. Create a simple agent
    math_assistant_agent = Agent(
        name="MathAssistant",
        instructions="You are a helpful math assistant. Provide concise answers.",
        model=OpenAIChatCompletionsModel(
            openai_client=provider,
            model="gpt-4o-mini"
        ),
        tool_use_behavior="stop_on_first_tool"
    )

    # 2. Define an input string
    user_input = "What is 1024 divided by 256?"

    # 3. Run the agent synchronously
    print(f"\n🤖 Assistant: Running agent synchronously with input: '{user_input}'")
    try:
        result: RunResult = Runner.run_sync(
            starting_agent=math_assistant_agent,
            input=user_input
        )

        # 4. Print the final output
        if result.final_output:
            print("\n📝 Final Output from MathAssistant:")
            print(result.final_output)
        else:
            print("\n⚠️ No final output received.")

        print(f"\n--- Finished 02_run_sync.py ---")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print(f"--- Finished 02_run_sync.py with error ---")


if __name__ == "__main__":
    main_sync()
