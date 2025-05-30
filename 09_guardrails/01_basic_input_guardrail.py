"""
01_basic_input_guardrail.py

This module demonstrates basic input guardrails using the OpenAI Agents SDK.
Input guardrails check and potentially filter user input before it reaches the agent.
"""

import asyncio
import logging
from agents import Agent, Runner, InputGuardrailTripwireTriggered
from agents.guardrail import input_guardrail, GuardrailFunctionOutput
from agents.run_context import RunContextWrapper
from agents.items import TResponseInputItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@input_guardrail
def content_filter_guardrail(context: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    """
    Basic input guardrail that checks for inappropriate content.
    Returns GuardrailFunctionOutput with tripwire_triggered=True to halt execution.
    """
    print(f"content_filter_guardrail: {input}")
    print(f"context: {context}")
    print(f"agent: {agent}")
    # Extract user message from input
    if isinstance(input, str):
        user_message = input
    else:
        # For list of items, get the last text content
        user_message = str(input[-1]) if input else ""

    # Check for inappropriate content
    banned_words = ["spam", "hack", "virus"]
    found_banned = [word for word in banned_words if word.lower()
                    in user_message.lower()]

    if found_banned:
        logger.warning(
            f"Input guardrail triggered: Found banned words: {found_banned}")
        return GuardrailFunctionOutput(
            output_info={"banned_words_found": found_banned,
                         "original_message": user_message},
            tripwire_triggered=True  # This will halt agent execution
        )

    logger.info("Input guardrail passed: No banned words found")
    return GuardrailFunctionOutput(
        output_info={"status": "clean", "message_length": len(user_message)},
        tripwire_triggered=False  # Allow execution to continue
    )


@input_guardrail(name="message_length_check")
def message_length_guardrail(context: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    """
    Input guardrail that checks message length.
    Demonstrates named guardrail using decorator parameters.
    """
    # Extract user message from input
    if isinstance(input, str):
        user_message = input
    else:
        # For list of items, get the last text content
        user_message = str(input[-1]) if input else ""
    max_length = 1000

    if len(user_message) > max_length:
        logger.warning(
            f"Input guardrail triggered: Message too long ({len(user_message)} > {max_length})")
        return GuardrailFunctionOutput(
            output_info={
                "message_length": len(user_message),
                "max_allowed": max_length,
                "excess_chars": len(user_message) - max_length
            },
            tripwire_triggered=True
        )

    logger.info(f"Message length OK: {len(user_message)} chars")
    return GuardrailFunctionOutput(
        output_info={"message_length": len(
            user_message), "status": "acceptable"},
        tripwire_triggered=False
    )


async def demo_input_guardrails():
    """Demonstrate input guardrails with different scenarios."""

    # Create agent with input guardrails
    agent = Agent(
        name="GuardedAgent",
        instructions="You are a helpful assistant. Respond to user queries politely.",
        input_guardrails=[content_filter_guardrail, message_length_guardrail]
    )

    test_cases = [
        "Hello, how are you today?",  # Should pass both guardrails
        "I want to hack into this system",  # Should trigger content filter
        "A" * 1001  # Should trigger length check
    ]

    for i, test_input in enumerate(test_cases, 1):
        logger.info(
            f"\n--- Test Case {i}: {test_input[:50]}{'...' if len(test_input) > 50 else ''} ---")

        try:
            result = await Runner.run(agent, test_input, max_turns=1)
            logger.info(f"Agent response: {result.final_output}")

            # Check guardrail results
            if result.input_guardrail_results:
                for guardrail_result in result.input_guardrail_results:
                    logger.info(
                        f"Guardrail '{guardrail_result.guardrail.get_name()}': {guardrail_result.output.output_info}")
            else:
                logger.info("No input guardrail results recorded")

        except InputGuardrailTripwireTriggered as e:
            logger.info(f"Input guardrail tripwire triggered: {e}")
            logger.info(f"Input guardrail tripwire triggered: {e.guardrail_result}")

        except Exception as e:
            logger.error(f"Error in test case {i}: {e}")


async def main():
    print("🔒 Basic Input Guardrails Demo 🔒")
    await demo_input_guardrails()
    logger.info("\n✅ Input Guardrails Demo Complete")

if __name__ == "__main__":
    asyncio.run(main())
