"""
03_guardrail_exceptions.py

This module demonstrates how to handle guardrail exceptions when tripwires are triggered.
Shows proper exception handling for InputGuardrailTripwireTriggered and OutputGuardrailTripwireTriggered.
"""

import asyncio
import logging
from agents import Agent, Runner
from agents.guardrail import input_guardrail, output_guardrail, GuardrailFunctionOutput
from agents.run_context import RunContextWrapper
from agents.items import TResponseInputItem
from agents.exceptions import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Input guardrail that will trigger for certain inputs


@input_guardrail(name="strict_content_filter")
def strict_input_filter(context: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    """Strict input filter that blocks any mention of sensitive topics."""

    # Extract user message from input
    if isinstance(input, str):
        user_message = input
    else:
        user_message = str(input[-1]) if input else ""

    # Strict filtering
    sensitive_topics = ["finances", "medical", "legal", "personal"]
    found_sensitive = [
        topic for topic in sensitive_topics if topic.lower() in user_message.lower()]

    if found_sensitive:
        logger.warning(
            f"Strict input filter TRIGGERED: Found sensitive topics: {found_sensitive}")
        return GuardrailFunctionOutput(
            output_info={
                "sensitive_topics_found": found_sensitive,
                "blocked_message": user_message,
                "reason": "Content violates input policy"
            },
            tripwire_triggered=True  # This will raise InputGuardrailTripwireTriggered
        )

    logger.info("Strict input filter PASSED")
    return GuardrailFunctionOutput(
        output_info={"status": "approved", "message": user_message},
        tripwire_triggered=False
    )

# Output guardrail that will trigger for certain outputs


@output_guardrail(name="strict_output_filter")
def strict_output_filter(context: RunContextWrapper, agent: Agent, agent_output) -> GuardrailFunctionOutput:
    """Strict output filter that blocks responses containing specific content."""

    response_text = str(agent_output) if agent_output else ""

    # Check for forbidden output patterns
    forbidden_patterns = ["disclaimer",
                          "not a substitute", "consult a professional"]
    found_forbidden = [pattern for pattern in forbidden_patterns if pattern.lower(
    ) in response_text.lower()]

    if found_forbidden:
        logger.warning(
            f"Strict output filter TRIGGERED: Found forbidden patterns: {found_forbidden}")
        return GuardrailFunctionOutput(
            output_info={
                "forbidden_patterns_found": found_forbidden,
                "blocked_response": response_text,
                "reason": "Response violates output policy"
            },
            tripwire_triggered=True  # This will raise OutputGuardrailTripwireTriggered
        )

    logger.info("Strict output filter PASSED")
    return GuardrailFunctionOutput(
        output_info={"status": "approved", "response": response_text},
        tripwire_triggered=False
    )


async def handle_input_guardrail_exception():
    """Demo: Handling InputGuardrailTripwireTriggered exceptions."""

    logger.info("\n=== Input Guardrail Exception Handling Demo ===")

    agent = Agent(
        name="InputGuardedAgent",
        instructions="You are a helpful assistant.",
        input_guardrails=[strict_input_filter]
    )

    test_inputs = [
        "Hello, how are you?",  # Should pass
        "I need help with my medical condition",  # Should trigger guardrail
        "What's the weather like?"  # Should pass
    ]

    for i, test_input in enumerate(test_inputs, 1):
        logger.info(f"\n--- Input Test {i}: '{test_input}' ---")

        try:
            result = await Runner.run(agent, test_input, max_turns=1)
            logger.info(f"✅ SUCCESS: Agent responded: {result.final_output}")

            # Show guardrail results when they don't trigger
            if result.input_guardrail_results:
                for gr in result.input_guardrail_results:
                    logger.info(f"Guardrail info: {gr.output.output_info}")

        except InputGuardrailTripwireTriggered as e:
            logger.error(f"🚫 INPUT GUARDRAIL TRIGGERED!")
            logger.error(
                f"Guardrail name: {e.guardrail_result.guardrail.get_name()}")
            logger.error(
                f"Trigger info: {e.guardrail_result.output.output_info}")
            logger.error(
                f"User-friendly message: Content blocked due to policy violation")

        except Exception as e:
            logger.error(f"❌ Unexpected error: {type(e).__name__}: {e}")


async def handle_output_guardrail_exception():
    """Demo: Handling OutputGuardrailTripwireTriggered exceptions."""

    logger.info("\n=== Output Guardrail Exception Handling Demo ===")

    agent = Agent(
        name="OutputGuardedAgent",
        instructions=(
            "You are a helpful assistant. Always include disclaimers like "
            "'this is not a substitute for professional advice' in your responses."
        ),
        output_guardrails=[strict_output_filter]
    )

    test_inputs = [
        "What's 2+2?",  # Simple math, likely won't trigger
        "How do I treat a headache?",  # Medical question, likely to include disclaimers
    ]

    for i, test_input in enumerate(test_inputs, 1):
        logger.info(f"\n--- Output Test {i}: '{test_input}' ---")

        try:
            result = await Runner.run(agent, test_input, max_turns=1)
            logger.info(f"✅ SUCCESS: Agent responded: {result.final_output}")

            # Show guardrail results when they don't trigger
            if result.output_guardrail_results:
                for gr in result.output_guardrail_results:
                    logger.info(f"Guardrail info: {gr.output.output_info}")

        except OutputGuardrailTripwireTriggered as e:
            logger.error(f"🚫 OUTPUT GUARDRAIL TRIGGERED!")
            logger.error(
                f"Guardrail name: {e.guardrail_result.guardrail.get_name()}")
            logger.error(
                f"Agent that was blocked: {e.guardrail_result.agent.name}")
            logger.error(
                f"Trigger info: {e.guardrail_result.output.output_info}")
            logger.error(
                f"User-friendly message: Response blocked due to policy violation")

        except Exception as e:
            logger.error(f"❌ Unexpected error: {type(e).__name__}: {e}")


async def comprehensive_exception_handling():
    """Demo: Comprehensive exception handling with both input and output guardrails."""

    logger.info("\n=== Comprehensive Exception Handling Demo ===")

    agent = Agent(
        name="FullyGuardedAgent",
        instructions="You are a helpful assistant. Be comprehensive in your responses.",
        input_guardrails=[strict_input_filter],
        output_guardrails=[strict_output_filter]
    )

    test_cases = [
        "Tell me about the weather",  # Should pass both
        "Help me with personal finances",  # Should trigger input guardrail
        "What is machine learning?",  # May or may not trigger output guardrail
    ]

    for i, test_input in enumerate(test_cases, 1):
        logger.info(f"\n--- Comprehensive Test {i}: '{test_input}' ---")

        try:
            result = await Runner.run(agent, test_input, max_turns=1)
            logger.info(f"✅ FULL SUCCESS: {result.final_output}")

            # Report on all guardrail results
            total_guardrails = len(
                result.input_guardrail_results) + len(result.output_guardrail_results)
            logger.info(f"Total guardrails executed: {total_guardrails}")

        except InputGuardrailTripwireTriggered as e:
            logger.error(
                f"🚫 BLOCKED AT INPUT: {e.guardrail_result.output.output_info}")
            # In a real app, you might want to return a polite error message to the user

        except OutputGuardrailTripwireTriggered as e:
            logger.error(
                f"🚫 BLOCKED AT OUTPUT: {e.guardrail_result.output.output_info}")
            # In a real app, you might want to retry with different instructions or return a safe fallback

        except Exception as e:
            logger.error(f"❌ SYSTEM ERROR: {type(e).__name__}: {e}")


async def main():
    print("⚠️ Guardrail Exception Handling Demo ⚠️")

    await handle_input_guardrail_exception()
    await handle_output_guardrail_exception()
    await comprehensive_exception_handling()

    logger.info("\n✅ Exception Handling Demo Complete")
    print("\n📝 Key Takeaways:")
    print("   • InputGuardrailTripwireTriggered: Blocks before agent processes input")
    print("   • OutputGuardrailTripwireTriggered: Blocks after agent generates response")
    print("   • Both provide detailed info about what triggered the guardrail")
    print("   • Use try/except blocks to handle gracefully and provide user feedback")

if __name__ == "__main__":
    asyncio.run(main())
