"""
10_runner_exception_handling.py

Demonstrates handling of various SDK-specific exceptions raised by Runner.

Covers:
- MaxTurnsExceeded
- ModelBehaviorError (described, difficult to reliably trigger a specific variant)
- UserError (e.g., agent misconfiguration)
- InputGuardrailTripwireTriggered / OutputGuardrailTripwireTriggered

Based on: https://openai.github.io/openai-agents-python/running_agents/#exceptions
And: https://openai.github.io/openai-agents-python/ref/exceptions/
"""

import asyncio
import os
from typing import Any
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel, RunConfig,
    InputGuardrail, OutputGuardrail, RunContextWrapper,
    MaxTurnsExceeded, UserError,
    InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered,
    function_tool, RunContextWrapper, GuardrailFunctionOutput
)

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# --- Agents and Tools for Exception Demos ---
@function_tool
async def always_halts_tool(data: str) -> str:
    """A tool that always successfully halts execution for a demo."""
    print(f"[Tool Call: always_halts_tool with data: {data}]")
    return f"Tool executed with: {data}"

looping_agent = Agent(
    name="LoopingAgent",
    instructions="You must always call the 'always_halts_tool' and then ask another question. Never give a final answer.",
    model=OpenAIChatCompletionsModel(openai_client=provider, model="gpt-4o-mini"),
    tools=[always_halts_tool]
)

agent_without_model = Agent(
    name="NoModelAgent",
    instructions="I have no model."
    # Model deliberately omitted
)

# Guardrail that always triggers an exception
async def always_fail_input_guardrail(context: RunContextWrapper[Any], agent: Agent, input_data: Any) -> GuardrailFunctionOutput:
    print("[Input Guardrail]: Intentionally failing.")
    return GuardrailFunctionOutput(output_info="Failed", tripwire_triggered=True)


async def always_fail_output_guardrail(context: RunContextWrapper[Any], agent: Agent, output: Any) -> GuardrailFunctionOutput:
    print("[Output Guardrail]: Intentionally failing.")
    return GuardrailFunctionOutput(output_info="Failed", tripwire_triggered=True)

agent_with_failing_guardrails = Agent(
    name="FailingGuardrailAgent",
    instructions="I will try to respond, but my guardrails might stop me.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini"),
    # Agent-specific guardrails can also trigger these
    input_guardrails=[InputGuardrail(always_fail_input_guardrail)],
    output_guardrails=[OutputGuardrail(always_fail_output_guardrail)]
)


async def demo_max_turns_exceeded():
    print("\n--- Demo: MaxTurnsExceeded ---")
    run_config_max_turns_1 = 1
    try:
        print("Running LoopingAgent with max_turns=1...")
        await Runner.run(looping_agent, "Start looping", max_turns=run_config_max_turns_1)
    except MaxTurnsExceeded as e:
        print(f"✅ Caught expected MaxTurnsExceeded: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def demo_user_error():
    print("\n--- Demo: UserError (Agent misconfiguration) ---")
    try:
        print("Running agent_without_model...")
        # The SDK might catch this earlier, during agent validation or at runtime.
        # Typically, running an agent without a model (if it tries to call an LLM) will cause an error.
        await Runner.run(agent_without_model, "Hello?")
    except UserError as e:
        # This specific error might be different depending on when the SDK checks for the model.
        # e.g., "Agent SimpleAgent has no model and no way to get one from the environment or RunConfig."
        print(f"✅ Caught expected UserError (or similar): {e}")
    except Exception as e:
        print(f"❌ Unexpected error (might be specific validation error): {e}")


async def demo_model_behavior_error():
    print("\n--- Demo: ModelBehaviorError (Conceptual) ---")
    print("ModelBehaviorError is raised for issues like malformed JSON from LLM or using non-existent tools.")
    print("Reliably triggering a specific ModelBehaviorError is hard without a controlled, misbehaving LLM.")
    print("If an LLM tried to call a tool not registered with the agent, it would likely result in a ModelBehaviorError.")

    print("  For testing, one might mock an LLM response to be invalid JSON for a tool call.")


async def demo_guardrail_exceptions():
    print("\n--- Demo: Guardrail Exceptions ---")

    # Test InputGuardrailTripwireTriggered
    print("\nTesting InputGuardrailTripwireTriggered...")
    try:
        # Using global guardrail via RunConfig for this demo
        run_config_failing_input = RunConfig(
            input_guardrails=[InputGuardrail(always_fail_input_guardrail)])
        agent_for_input_fail = Agent(
            "TempAgent", model=OpenAIChatCompletionsModel(openai_client=provider, model="gpt-4o-mini"))
        await Runner.run(agent_for_input_fail, "This input will fail guardrail.", run_config=run_config_failing_input)
    except InputGuardrailTripwireTriggered as e:
        print(f"✅ Caught expected InputGuardrailTripwireTriggered: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    # Test OutputGuardrailTripwireTriggered
    print("\nTesting OutputGuardrailTripwireTriggered...")
    try:
        # Using global guardrail via RunConfig for this demo
        run_config_failing_output = RunConfig(
            output_guardrails=[OutputGuardrail(always_fail_output_guardrail)])
        agent_for_output_fail = Agent("TempAgentOutput", model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini"), instructions="Respond normally")
        await Runner.run(agent_for_output_fail, "Generate any output.", run_config=run_config_failing_output)
    except OutputGuardrailTripwireTriggered as e:
        print(f"✅ Caught expected OutputGuardrailTripwireTriggered: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def main():
    print("--- Running 12_runner_exception_handling.py ---")
    await demo_max_turns_exceeded()
    await demo_user_error()
    await demo_model_behavior_error()
    await demo_guardrail_exceptions()
    print("\n--- Finished 12_runner_exception_handling.py ---")

if __name__ == "__main__":
    asyncio.run(main())
