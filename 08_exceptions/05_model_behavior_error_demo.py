"""
05_model_behavior_error_demo.py

This module demonstrates handling the agents.exceptions.ModelBehaviorError.
This error is raised when the model behaves unexpectedly, such as trying to call
a non-existent tool or providing malformed JSON for a tool call.
"""

import asyncio
import logging
from agents import Agent, Runner, exceptions, function_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@function_tool
def get_current_weather(location: str) -> str:
    """Gets the current weather for a given location."""
    logger.info(f"Tool 'get_current_weather' called for {location}")
    if location == "testville":
        return "The weather in Testville is sunny."
    return f"Weather data not available for {location}."

async def demo_model_behavior_error():
    logger.info("\n--- Demo: ModelBehaviorError ---")
    try:
        # Ensure you have OPENAI_API_KEY set in your environment
        agent_with_tool = Agent(
            name="ToolUserAgent",
            instructions=(
                "You are a helpful assistant. You have one tool 'get_current_weather'. "
                "VERY IMPORTANT: You MUST try to call a tool named 'get_stock_price' with any argument, even though it does not exist."
            ),
            tools=[get_current_weather]
        )

        logger.info("Attempting to run the agent and provoke it to call a non-existent tool...")
        # We expect the model to try calling 'get_stock_price', which isn't defined.
        await Runner.run(agent_with_tool, "What is the weather and stock price?", max_turns=3)
        logger.info("Agent run completed without ModelBehaviorError (UNEXPECTED - model did not call non-existent tool as instructed or error was not raised).")

    except exceptions.ModelBehaviorError as e:
        logger.error(f"CAUGHT ModelBehaviorError: {e}")
    except exceptions.AgentsException as e:
        logger.error(f"CAUGHT other AgentsException: {type(e).__name__} - {e}")
    except Exception as e:
        logger.error(f"UNEXPECTED error in demo_model_behavior_error: {type(e).__name__} - {e}")
        logger.exception("Full traceback:")

async def main():
    print("🚀 Demonstrating ModelBehaviorError from OpenAI Agents SDK 🚀")
    await demo_model_behavior_error()
    logger.info("\n✅ ModelBehaviorError Demonstration Complete.")

if __name__ == "__main__":
    # This demo uses OpenAIChatCompletionsModel and relies on prompting it to misbehave.
    # Success in triggering ModelBehaviorError this way isn't guaranteed with LLMs.
    # A mock model would be more reliable for testing this specific exception.
    asyncio.run(main()) 