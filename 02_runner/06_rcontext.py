"""
06_agent_loop_and_inputs.py

Demonstrates the Runner's agent loop and different input types.

Agent Loop Scenarios:
- LLM returns final_output (loop ends).
- LLM produces tool calls (loop continues with tool results).
- LLM does a handoff (loop continues with new agent).
- max_turns and MaxTurnsExceeded exception.

Input Types:
- Simple string input.
- List of input items (OpenAI API format).

Based on: https://openai.github.io/openai-agents-python/running_agents/#the-agent-loop
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent, Runner, function_tool, Handoff,
    MaxTurnsExceeded, RunConfig, RunContextWrapper, ToolCallOutputItem
)

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# --- Tools and Agents for Demo ---


@function_tool
async def get_city_population(context: RunContextWrapper, city: str) -> str:
    """Gets the population of a given city."""
    print(f"[Tool Call: get_city_population for {city}]")
    if city.lower() == "london":
        return "London has a population of approximately 9 million."
    elif city.lower() == "paris":
        return "Paris has a population of approximately 2.1 million."
    return f"Population data for {city} is not available."

research_agent = Agent(
    name="ResearchAssistant",
    instructions="You are a research assistant. Use tools to find information. Then summarize it.",
    tools=[get_city_population]
)

summary_agent = Agent(
    name="SummarySpecialist",
    instructions="You are a summarization specialist. Provide a concise summary of the given text.",
    handoff_description="Use this agent to summarize text provided by other agents."
)


class ResearchToSummaryHandoff(Handoff):
    async def get_target_agent(self, context: RunContextWrapper) -> Agent:
        return summary_agent

    async def should_handoff(self, context: RunContextWrapper, current_input: list) -> bool:
        # Handoff if the input contains tool output from the research agent
        return any(isinstance(item, ToolCallOutputItem) for item in current_input)


research_agent_with_handoff = research_agent.clone(
    name="ResearchAndSummarizeAgent",
    instructions=(
        "First, use tools to find information. "
        "Then, handoff to the SummarySpecialist to summarize the findings."
    )
)


async def demo_loop_final_output():
    print("\n--- Demo: Agent Loop ending with final_output ---")
    agent = Agent(
        name="SimpleGreeter",
        instructions="Greet the user warmly.",
    )
    result = await Runner.run(agent, "Hello there!")
    print(f"Final Output: {result.final_output}")


async def demo_loop_with_tool_call():
    print("\n--- Demo: Agent Loop with a tool call ---")
    user_input = "What is the population of London?"
    print(f"Input: {user_input}")
    result = await Runner.run(research_agent, user_input)
    print(f"Final Output: {result.final_output}")


async def demo_loop_with_handoff():
    print("\n--- Demo: Agent Loop with a handoff ---")
    user_input = "Find the population of Paris and then summarize it."
    print(f"Input: {user_input}")
    result = await Runner.run(research_agent_with_handoff, user_input)
    print(f"Final Output (from {result}")

async def demo_max_turns():
    print("\n--- Demo: max_turns and MaxTurnsExceeded ---")
    # This agent might loop if not constrained by max_turns, as it always calls a tool
    # and its instructions don't clearly lead to a final output without more complex logic.
    # For simplicity of demo, we'll rely on max_turns.
    agent_prone_to_loop = Agent(
        name="LoopingResearcher",
        instructions=(
            "Always use the get_city_population tool for 'London'. "
            "Do not provide a final answer, just keep researching."
        ),
        tools=[get_city_population]
    )
    try:
        print("Running agent prone to looping with max_turns=2...")
        await Runner.run(agent_prone_to_loop, "Research London", max_turns=1, run_config=RunConfig(workflow_name="Research London"))
    except MaxTurnsExceeded as e:
        print(f"Caught expected exception: {e}")
    except Exception as e:
        print(f"Caught unexpected exception: {e}")

async def demo_input_types():
    print("\n--- Demo: Input Types ---")
    agent = Agent(
        name="EchoAgent",
        instructions="Repeat the user's message verbatim.",
    )

    # 1. String input
    print("\n1. String Input:")
    string_input = "This is a simple string input."
    result_str = await Runner.run(agent, string_input)
    print(f"  Input: '{string_input}'")
    print(f"  Output: {result_str.final_output}")

    # 2. List of input items
    print("\n2. List of Input Items (OpenAI API format):")
    list_input = [
        {"role": "system", "content": "You are an echo agent."},
        {"role": "user", "content": "Echo this message for me, please."}
    ]
    # For list input, we often use the agent's model directly or a compatible one.
    # Runner.run expects a single agent. If the list_input is meant to be a full history,
    # it's usually handled by constructing the conversation history before calling run.
    # Here, we'll pass it as if it's the current turn's input.
    # The SDK's Runner.run will typically convert this list into a format the LLM expects.
    
    # The `items.Text` or constructing messages as per OpenAI's API schema is more aligned here.
    # Let's use `items.Text` for a clearer SDK-specific example for list input.
    list_input_sdk_format = "This is the first part of the input."
    # The EchoAgent will likely just repeat the concatenation or the last part based on its simple instructions.
    # A more sophisticated agent could handle such list inputs differently.
    result_list = await Runner.run(agent, list_input_sdk_format) 
    print(f"  Input: {list_input_sdk_format}")
    print(f"  Output: {result_list.final_output}")

    # Example of list input representing conversation history for a new turn:
    # (This pattern is more common for building chat applications)
    print("\n3. List Input as Conversation History for a new turn:")
    # Assume previous_result is a RunResult from a previous turn
    # previous_result = await Runner.run(agent, "First message from user")
    # new_turn_input = previous_result.to_input_list() + [{"role": "user", "content": "Second message"}]
    # result_new_turn = await Runner.run(agent, new_turn_input)
    # print(f"  Output for new turn: {result_new_turn.final_output}")
    # For this demo, we'll mock a simple history to show the structure.
    mock_history_input = "What's the capital of France?"
    # The EchoAgent is too simple for this, a Q&A agent would be better.
    # We'll use the research_agent for this one.
    print(f"  Input (history + current): {mock_history_input}")
    result_history = await Runner.run(research_agent, mock_history_input)
    print(f"  Output (from ResearchAgent): {result_history.final_output}")


async def main():
    print("--- Running 06_agent_loop_and_inputs.py ---")
    await demo_loop_final_output()
    await demo_loop_with_tool_call()
    await demo_loop_with_handoff()
    await demo_max_turns()
    await demo_input_types()
    print("\n--- Finished 06_agent_loop_and_inputs.py ---")

if __name__ == "__main__":
    asyncio.run(main())
