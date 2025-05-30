"""
04_agent_based_guardrails.py

This module demonstrates advanced agent-based guardrails where one agent acts as a guardrail
for another agent. This is based on the example from the OpenAI Agents SDK documentation.
"""

import asyncio
import logging
from pydantic import BaseModel
from agents import Agent, Runner
from agents.guardrail import input_guardrail, output_guardrail, GuardrailFunctionOutput
from agents.run_context import RunContextWrapper
from agents.items import TResponseInputItem
from agents.exceptions import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for structured guardrail outputs


class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str
    confidence_score: float = 0.0


class ContentModerationOutput(BaseModel):
    is_appropriate: bool
    issues_found: list[str] = []
    severity_level: str = "low"  # low, medium, high
    reasoning: str


class ResponseQualityOutput(BaseModel):
    is_helpful: bool
    is_accurate: bool
    is_complete: bool
    quality_score: float = 0.0
    improvement_suggestions: list[str] = []


# Create guardrail agents
math_homework_guardrail_agent = Agent(
    name="MathHomeworkDetector",
    instructions=(
        "You are a guardrail agent that detects if users are asking for help with math homework. "
        "Analyze the input and determine if it's a math homework question. "
        "Provide reasoning for your decision and a confidence score (0.0 to 1.0)."
    ),
    output_type=MathHomeworkOutput,
)

content_moderation_guardrail_agent = Agent(
    name="ContentModerator",
    instructions=(
        "You are a content moderation agent. Analyze responses for appropriateness. "
        "Check for offensive language, misinformation, harmful advice, or inappropriate content. "
        "Rate severity as low, medium, or high."
    ),
    output_type=ContentModerationOutput,
)

response_quality_guardrail_agent = Agent(
    name="QualityChecker",
    instructions=(
        "You are a response quality checker. Evaluate if responses are helpful, accurate, and complete. "
        "Provide a quality score (0.0 to 1.0) and suggestions for improvement if needed."
    ),
    output_type=ResponseQualityOutput,
)

# Input guardrail using agent-based detection


@input_guardrail(name="math_homework_detector")
async def math_homework_guardrail(
    context: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """
    Agent-based input guardrail that detects math homework requests.
    Uses a dedicated guardrail agent to make the determination.
    """
    logger.info(
        f"Running math homework detection guardrail... {input} {type(input)}")

    # Run the guardrail agent to analyze the input
    guardrail_result = await Runner.run(
        math_homework_guardrail_agent,
        input,
        context=context.context
    )

    final_output = guardrail_result.final_output_as(MathHomeworkOutput)

    # Trigger if it's math homework with high confidence
    should_trigger = final_output.is_math_homework and final_output.confidence_score > 0.7

    if should_trigger:
        logger.warning(
            f"Math homework detected! Confidence: {final_output.confidence_score}")
        return GuardrailFunctionOutput(
            output_info={
                "detection_result": final_output.model_dump(),
                "reason": "Math homework requests are not allowed",
                "guardrail_agent": math_homework_guardrail_agent.name
            },
            tripwire_triggered=True
        )

    logger.info(
        f"Input approved. Homework confidence: {final_output.confidence_score}")
    return GuardrailFunctionOutput(
        output_info={
            "detection_result": final_output.model_dump(),
            "status": "approved",
            "guardrail_agent": math_homework_guardrail_agent.name
        },
        tripwire_triggered=False
    )

# Output guardrail using agent-based content moderation


@output_guardrail(name="content_moderation")
async def content_moderation_guardrail(
    context: RunContextWrapper, agent: Agent, agent_output
) -> GuardrailFunctionOutput:
    """
    Agent-based output guardrail that moderates content for appropriateness.
    """
    logger.info(
        f"Running content moderation guardrail... {agent_output} {type(agent_output)}")

    # Run the content moderation agent
    guardrail_result = await Runner.run(
        content_moderation_guardrail_agent,
        f"Please moderate this response: {agent_output}",
        context=context.context
    )

    final_output = guardrail_result.final_output_as(ContentModerationOutput)

    # Trigger if content is inappropriate or high severity
    should_trigger = not final_output.is_appropriate or final_output.severity_level == "high"

    if should_trigger:
        logger.warning(
            f"Content moderation triggered! Issues: {final_output.issues_found}")
        return GuardrailFunctionOutput(
            output_info={
                "moderation_result": final_output.model_dump(),
                "reason": "Response contains inappropriate content",
                "guardrail_agent": content_moderation_guardrail_agent.name
            },
            tripwire_triggered=True
        )

    logger.info("Content moderation passed")
    return GuardrailFunctionOutput(
        output_info={
            "moderation_result": final_output.model_dump(),
            "status": "approved",
            "guardrail_agent": content_moderation_guardrail_agent.name
        },
        tripwire_triggered=False
    )

# Output guardrail for response quality


@output_guardrail(name="quality_check")
async def quality_check_guardrail(
    context: RunContextWrapper, agent: Agent, agent_output
) -> GuardrailFunctionOutput:
    """
    Agent-based output guardrail that checks response quality.
    This one doesn't trigger (block) but provides quality metrics.
    """
    logger.info("Running quality check guardrail...")

    # Run the quality checker agent
    guardrail_result = await Runner.run(
        response_quality_guardrail_agent,
        f"Please evaluate the quality of this response: {agent_output}",
        context=context.context
    )

    final_output = guardrail_result.final_output_as(ResponseQualityOutput)

    # This guardrail provides feedback but doesn't block (for demonstration)
    # In a real system, you might trigger on very low quality scores
    low_quality_threshold = 0.3
    should_trigger = final_output.quality_score < low_quality_threshold

    if should_trigger:
        logger.warning(
            f"Low quality response detected! Score: {final_output.quality_score}")
    else:
        logger.info(
            f"Quality check complete. Score: {final_output.quality_score}")

    return GuardrailFunctionOutput(
        output_info={
            "quality_result": final_output.model_dump(),
            "status": "low_quality" if should_trigger else "acceptable",
            "guardrail_agent": response_quality_guardrail_agent.name
        },
        tripwire_triggered=should_trigger
    )


async def demo_agent_based_guardrails():
    """Demonstrate agent-based guardrails in action."""

    logger.info("\n=== Agent-Based Guardrails Demo ===")

    # Create a customer support agent with agent-based guardrails
    customer_support_agent = Agent(
        name="CustomerSupportAgent",
        instructions=(
            "You are a helpful customer support agent. Answer questions about products and services. "
            "Be friendly and informative in your responses."
        ),
        input_guardrails=[math_homework_guardrail],
        output_guardrails=[
            content_moderation_guardrail, quality_check_guardrail]
    )

    test_scenarios = [
        ("What is 2 + 2?", "Simple Math Question"),
        ("Can you solve this calculus problem for my homework?", "Math Homework Request"),
        ("What are your business hours?", "Normal Customer Query"),
        ("Tell me about your return policy", "Policy Question"),
    ]

    for i, (test_input, scenario_name) in enumerate(test_scenarios, 1):
        logger.info(f"\n--- Scenario {i}: {scenario_name} ---")
        logger.info(f"Input: '{test_input}'")

        try:
            result = await Runner.run(customer_support_agent, test_input, max_turns=1)
            logger.info(f"✅ SUCCESS: {result.final_output}")

            # Report guardrail results
            logger.info(f"\nGuardrail Results:")
            logger.info(
                f"  Input guardrails: {len(result.input_guardrail_results)}")
            for gr in result.input_guardrail_results:
                logger.info(
                    f"    - {gr.guardrail.get_name()}: {gr.output.output_info.get('status', 'checked')}")

            logger.info(
                f"  Output guardrails: {len(result.output_guardrail_results)}")
            for output_gr in result.output_guardrail_results:
                logger.info(
                    f"    - {output_gr.guardrail.get_name()}: {output_gr.output.output_info.get('status', 'checked')}")

        except InputGuardrailTripwireTriggered as e:
            logger.error(
                f"🚫 INPUT BLOCKED: {e.guardrail_result.output.output_info.get('reason', 'Policy violation')}")

        except OutputGuardrailTripwireTriggered as e:
            logger.error(
                f"🚫 OUTPUT BLOCKED: {e.guardrail_result.output.output_info.get('reason', 'Content violation')}")

        except Exception as e:
            logger.error(f"❌ ERROR: {type(e).__name__}: {e}")


async def demo_guardrail_performance():
    """Demonstrate the performance characteristics of agent-based guardrails."""

    logger.info("\n=== Guardrail Performance Demo ===")

    import time

    # Simple agent for comparison
    simple_agent = Agent(
        name="SimpleAgent",
        instructions="You are a helpful assistant."
    )

    # Agent with multiple agent-based guardrails
    guarded_agent = Agent(
        name="GuardedAgent",
        instructions="You are a helpful assistant.",
        input_guardrails=[math_homework_guardrail],
        output_guardrails=[
            content_moderation_guardrail, quality_check_guardrail]
    )

    test_input = "What's the weather like today?"

    # Time simple agent
    start_time = time.time()
    try:
        simple_result = await Runner.run(simple_agent, test_input, max_turns=1)
        simple_time = time.time() - start_time
        logger.info(f"Simple agent response time: {simple_time:.2f}s")
    except Exception as e:
        logger.error(f"Simple agent error: {e}")
        simple_time = 0

    # Time guarded agent
    start_time = time.time()
    try:
        guarded_result = await Runner.run(guarded_agent, test_input, max_turns=1)
        guarded_time = time.time() - start_time
        logger.info(f"Guarded agent response time: {guarded_time:.2f}s")

        total_guardrails = len(guarded_result.input_guardrail_results) + \
            len(guarded_result.output_guardrail_results)
        logger.info(f"Total guardrails executed: {total_guardrails}")

        if simple_time > 0:
            overhead = ((guarded_time - simple_time) / simple_time) * 100
            logger.info(f"Guardrail overhead: {overhead:.1f}%")

    except Exception as e:
        logger.error(f"Guarded agent error: {e}")


async def main():
    print("🤖 Agent-Based Guardrails Demo 🤖")

    await demo_agent_based_guardrails()
    await demo_guardrail_performance()

    logger.info("\n✅ Agent-Based Guardrails Demo Complete")
    print("\n📝 Key Benefits of Agent-Based Guardrails:")
    print("   • More sophisticated reasoning and context understanding")
    print("   • Structured outputs with detailed explanations")
    print("   • Configurable confidence thresholds")
    print("   • Can be fine-tuned or specialized for specific domains")
    print("   • Provide rich debugging and monitoring information")
    print("\n⚠️ Considerations:")
    print("   • Higher latency due to additional LLM calls")
    print("   • Increased costs from multiple agent invocations")
    print("   • Need to balance guardrail complexity with performance")

if __name__ == "__main__":
    asyncio.run(main())
