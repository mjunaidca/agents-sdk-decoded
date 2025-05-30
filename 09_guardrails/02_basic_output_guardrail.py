"""
02_basic_output_guardrail.py

This module demonstrates basic output guardrails using the OpenAI Agents SDK.
Output guardrails check and potentially filter agent output before it's returned to the user.
"""

import asyncio
import logging
from agents import Agent, Runner, OutputGuardrailTripwireTriggered
from agents.guardrail import output_guardrail, GuardrailFunctionOutput
from agents.run_context import RunContextWrapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@output_guardrail
def response_safety_guardrail(context: RunContextWrapper, agent: Agent, agent_output) -> GuardrailFunctionOutput:
    """
    Output guardrail that checks for unsafe or inappropriate content in agent responses.
    Returns GuardrailFunctionOutput with tripwire_triggered=True to halt execution.
    """
    print(f"response_safety_guardrail: {agent_output}")
    print(f"type: {type(agent_output)}")
    # Convert agent output to string for analysis
    response_text = str(agent_output) if agent_output else ""

    # Check for unsafe content patterns
    unsafe_patterns = ["password", "secret", "confidential", "internal"]
    found_unsafe = [pattern for pattern in unsafe_patterns if pattern.lower(
    ) in response_text.lower()]

    if found_unsafe:
        logger.warning(
            f"Output guardrail triggered: Found unsafe patterns: {found_unsafe}")
        return GuardrailFunctionOutput(
            output_info={
                "unsafe_patterns_found": found_unsafe,
                "original_response": response_text,
                "agent_name": agent.name
            },
            tripwire_triggered=True  # This will halt and prevent the response from being returned
        )

    logger.info("Output guardrail passed: No unsafe patterns found")
    return GuardrailFunctionOutput(
        output_info={"status": "safe", "response_length": len(
            response_text), "agent_name": agent.name},
        tripwire_triggered=False  # Allow response to be returned
    )


@output_guardrail(name="response_length_check")
def response_length_guardrail(context: RunContextWrapper, agent: Agent, agent_output) -> GuardrailFunctionOutput:
    """
    Output guardrail that ensures responses aren't too long.
    Demonstrates named guardrail using decorator parameters.
    """
    response_text = str(agent_output) if agent_output else ""
    max_length = 500  # Arbitrary limit for demonstration

    if len(response_text) > max_length:
        logger.warning(
            f"Output guardrail triggered: Response too long ({len(response_text)} > {max_length})")
        return GuardrailFunctionOutput(
            output_info={
                "response_length": len(response_text),
                "max_allowed": max_length,
                "excess_chars": len(response_text) - max_length,
                "agent_name": agent.name
            },
            tripwire_triggered=True
        )

    logger.info(f"Response length OK: {len(response_text)} chars")
    return GuardrailFunctionOutput(
        output_info={"response_length": len(
            response_text), "status": "acceptable", "agent_name": agent.name},
        tripwire_triggered=False
    )


@output_guardrail(name="politeness_check")
async def politeness_guardrail(context: RunContextWrapper, agent: Agent, agent_output) -> GuardrailFunctionOutput:
    """
    Async output guardrail that checks if responses are polite.
    Demonstrates async guardrail implementation.
    """
    response_text = str(agent_output) if agent_output else ""

    # Simulate async processing (e.g., calling external API for sentiment analysis)
    await asyncio.sleep(0.1)  # Simulated async operation

    # Simple politeness check
    rude_words = ["stupid", "dumb", "idiot", "shut up"]
    found_rude = [word for word in rude_words if word.lower()
                  in response_text.lower()]

    if found_rude:
        logger.warning(
            f"Async output guardrail triggered: Found rude words: {found_rude}")
        return GuardrailFunctionOutput(
            output_info={
                "rude_words_found": found_rude,
                "original_response": response_text,
                "agent_name": agent.name,
                "check_type": "async_politeness"
            },
            tripwire_triggered=True
        )

    logger.info("Async politeness guardrail passed")
    return GuardrailFunctionOutput(
        output_info={"status": "polite", "agent_name": agent.name,
                     "check_type": "async_politeness"},
        tripwire_triggered=False
    )


async def demo_output_guardrails():
    """Demonstrate output guardrails with different scenarios."""

    # Create agents with different output guardrails
    agent_with_safety = Agent(
        name="SafetyGuardedAgent",
        instructions="You are a helpful assistant. Sometimes mention passwords or secrets in your responses for testing.",
        output_guardrails=[response_safety_guardrail]
    )

    agent_with_length = Agent(
        name="LengthGuardedAgent",
        instructions="You are a helpful assistant. Give very detailed, long responses.",
        output_guardrails=[response_length_guardrail]
    )

    agent_with_all = Agent(
        name="FullyGuardedAgent",
        instructions="You are a helpful assistant.",
        output_guardrails=[response_safety_guardrail,
                           response_length_guardrail, politeness_guardrail]
    )

    test_scenarios = [
        (agent_with_safety, "What's your password?", "Safety Guardrail Test"),
        (agent_with_length, "Tell me everything about artificial intelligence in great detail with examples.",
         "Length Guardrail Test"),
        (agent_with_all, "Hello, how are you?", "All Guardrails Test"),
    ]

    for i, (agent, test_input, scenario_name) in enumerate(test_scenarios, 1):
        logger.info(f"\n--- Test Scenario {i}: {scenario_name} ---")
        logger.info(f"Input: {test_input}")
        logger.info(f"Agent: {agent.name}")

        try:
            result = await Runner.run(agent, test_input, max_turns=1)
            logger.info(f"Agent response: {result.final_output}")

            # Check output guardrail results
            if result.output_guardrail_results:
                logger.info(
                    f"Output guardrail results ({len(result.output_guardrail_results)}):")
                for guardrail_result in result.output_guardrail_results:
                    logger.info(
                        f"  - Guardrail '{guardrail_result.guardrail.get_name()}': {guardrail_result.output.output_info}")
            else:
                logger.info("No output guardrail results recorded")

        except Exception as e:
            logger.error(f"Error in scenario {i}: {e}")


async def main():
    print("🛡️ Basic Output Guardrails Demo 🛡️")
    await demo_output_guardrails()
    logger.info("\n✅ Output Guardrails Demo Complete")

if __name__ == "__main__":
    asyncio.run(main())
