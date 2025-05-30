"""
03_user_error_demo.py

This module demonstrates handling the agents.exceptions.UserError.
A UserError is typically raised when the SDK is used incorrectly,
such as providing invalid parameters or configurations.
"""

import asyncio
import logging
from agents import Agent, exceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demo_user_error():
    logger.info("\n--- Demo: UserError ---")
    try:
        logger.info("Attempting to create an Agent with an invalid 'model' parameter type (e.g., an integer)...")
        Agent(
            name="MisconfiguredAgent",
            instructions="This agent is intentionally misconfigured.",
            tools=[], # No tools needed for this demo
            model=12345 # Invalid: model should be a string (model name) or a ModelProvider instance
        )
        logger.info("Agent created with invalid model parameter (UNEXPECTED - UserError should have been raised).")
    except exceptions.UserError as e:
        logger.error(f"CAUGHT UserError: {e}")
    except Exception as e:
        logger.error(f"UNEXPECTED error in demo_user_error: {type(e).__name__} - {e}")
        logger.exception("Full traceback:")

async def main():
    print("🚀 Demonstrating UserError from OpenAI Agents SDK 🚀")
    await demo_user_error()
    logger.info("\n✅ UserError Demonstration Complete.")

if __name__ == "__main__":
    asyncio.run(main()) 