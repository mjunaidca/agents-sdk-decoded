"""
04_max_turns_exceeded_demo.py

This module demonstrates handling the agents.exceptions.MaxTurnsExceeded error.
This error is raised when an agent's execution surpasses the maximum number of
interactions (turns) allowed, as defined in RunConfig.
"""

import asyncio
import logging
from agents import Agent, Runner, exceptions, RunConfig, OpenAIChatCompletionsModel # Using a real model provider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A very simple agent that is likely to take at least one turn.
# We will set max_turns to 0 or 1 to try and trigger the exception.

async def demo_max_turns_exceeded():
    logger.info("\n--- Demo: MaxTurnsExceeded ---")
    try:
        # Initialize a simple agent
        # Ensure you have OPENAI_API_KEY set in your environment for this to attempt a call
        simple_agent = Agent(
            name="BriefAgent",
            instructions="You are a helpful assistant. Just say hello once.",
        )

        logger.info("Attempting to run the agent with max_turns set to 0...")
        # Configure RunConfig to allow a very small number of turns
        await Runner.run(simple_agent, "Hi there!", max_turns=0)
        logger.info("Agent run completed without MaxTurnsExceeded (UNEXPECTED with max_turns=0).")

    except exceptions.MaxTurnsExceeded as e:
        logger.error(f"CAUGHT MaxTurnsExceeded: {e}")
        logger.error(f"TYPE: {type(e).__name__} - {e}")
    except Exception as e:
        logger.error(f"UNEXPECTED error in demo_max_turns_exceeded: {type(e).__name__} - {e}")
        logger.exception("Full traceback:")

async def main():
    print("🚀 Demonstrating MaxTurnsExceeded from OpenAI Agents SDK 🚀")
    await demo_max_turns_exceeded()
    logger.info("\n✅ MaxTurnsExceeded Demonstration Complete.")

if __name__ == "__main__":
    # Note: This demo uses OpenAIChatCompletionsModel, which requires an OpenAI API key.
    # If the API key is not available or there's a network issue, other errors might occur first.
    # The goal is to show MaxTurnsExceeded if the agent tries to take even one turn when max_turns=0.
    asyncio.run(main()) 