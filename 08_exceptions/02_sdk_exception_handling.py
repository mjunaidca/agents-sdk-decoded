"""
02_sdk_exception_handling.py

This module demonstrates handling common built-in exceptions from the OpenAI Agents SDK.
It focuses on UserError due to complexities in mocking model interactions for other exceptions.

Key SDK Exceptions Covered:
- agents.exceptions.UserError (demonstrated)
- agents.exceptions.MaxTurnsExceeded (commented out)
- agents.exceptions.ModelBehaviorError (commented out)
"""

import asyncio
import logging
from typing import Dict, Any # Added back for tool type hint
# from typing import Dict, Any, Optional, List # Not needed for simplified version
# import time # Not needed

from agents import Agent, Runner, function_tool, exceptions, RunConfig # Model, ModelProvider not needed
# from agents.usage import Usage as AgentsUsage # Not needed
# OpenAI Pydantic models not needed for simplified version
# from openai.types.chat import ChatCompletion, ChatCompletionMessage, ChatCompletionMessageToolCall
# from openai.types.chat.chat_completion import Choice, ChoiceLogprobs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tools are not strictly needed if not running agents that use them, but keep for context if we re-enable
@function_tool
def get_status() -> str:
    logger.info("Tool 'get_status' called.")
    return "Status: All systems nominal."

@function_tool
def process_structured_data(name: str, age: int, city: str) -> Dict[str, Any]:
    logger.info(f"Tool 'process_structured_data' called with: name={name}, age={age}, city={city}")
    return {"status": "processed", "name": name, "age": age, "city": city}

# --- Mock Model Definitions, Provider, and related Demos COMMENTED OUT --- 
# (All the BaseMockModel, LoopyModel, MisbehavingModelForToolError, MockModelProvider,
#  demo_max_turns_exceeded, demo_model_behavior_error code would be here and commented)

async def demo_user_error():
    logger.info("\n--- Demo: UserError ---")
    try:
        logger.info("Attempting to create an Agent with an invalid item in tools list...")
        Agent(
            name="FaultySetupAgent",
            instructions="This agent has a faulty setup.",
            tools=["this_is_not_a_tool_object"], # Invalid item: string instead of FunctionTool
            model="gpt-4o-mini" # Model string is fine, error should occur before model interaction
        )
        logger.info("Agent created with faulty setup (UNEXPECTED - UserError should have been raised).")
    except exceptions.UserError as e:
        logger.error(f"CAUGHT UserError: {e}")
    except Exception as e:
        logger.error(f"UNEXPECTED error in demo_user_error: {type(e).__name__} - {e}")
        logger.exception("Full traceback:")

# --- Main Execution --- 
async def main():
    print("🚀 Demonstrating SDK Built-in Exception Handling (Simplified for UserError) 🚀")
    
    await demo_user_error()
    
    # logger.info("\n--- MaxTurnsExceeded and ModelBehaviorError Demos are COMMENTED OUT ---")
    # logger.info("--- Due to complexities in accurately mocking the SDK Model interface. ---")

    logger.info("\n✅ SDK Exception Handling Demonstration Complete (UserError only).")

if __name__ == "__main__":
    asyncio.run(main())
