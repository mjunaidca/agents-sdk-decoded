import os
from dotenv import load_dotenv, find_dotenv
from mistralai import Any
from openai import AsyncOpenAI  # Still need AsyncOpenAI for the model provider
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunResult, function_tool, RunContextWrapper

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client (even for run_sync, the underlying model might be async)
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def custom_tool_error_function(ctx: RunContextWrapper[Any], error: Exception) -> str:
    """The default tool error function, which just returns a generic error message."""
    raise Exception(f"An error occurred Error: {str(error)}")


@function_tool(failure_error_function=False)
async def fetch_weather(location: str) -> str:
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    raise Exception("Something Went Wrong")


def main_sync():
    """Runs a simple agent synchronously and prints its output."""
    print("--- Running 02_run_sync.py ---")

    # 1. Create a simple agent
    math_assistant_agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Provide concise answers.",
        model=OpenAIChatCompletionsModel(
            openai_client=provider,
            model="gpt-4o-mini"
        ),
        tools=[fetch_weather],
        input_guardrails=[]
    )

    # 2. Define an input string
    user_input = "What is the weather in Tokyo?"

    # 3. Run the agent synchronously
    print(f"\n🤖 Assistant: Running agent synchronously with input: '{user_input}'")

    result: RunResult = Runner.run_sync(
        starting_agent=math_assistant_agent,
        input=user_input
    )
    
    print(result)

    print(f"\n--- Finished 02_run_sync.py ---")

if __name__ == "__main__":
    main_sync()
