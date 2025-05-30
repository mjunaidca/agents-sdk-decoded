"""
01_run.py

Demonstrates the basic asynchronous Runner.run() method.

- Executes an agent asynchronously.
- Passes a string input.
- Retrieves and prints RunResult.final_output.

Based on: https://openai.github.io/openai-agents-python/running_agents/
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunResult


# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    # Use your specific API base if needed
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)


async def main():
    """Runs a simple agent and prints its output."""
    print("--- Running 01_run.py --- ")

    # 1. Create a simple agent
    assistant_agent = Agent(
        name="HaikuAssistant",
        instructions="You are a poetic assistant, skilled in writing haikus.",
        model=OpenAIChatCompletionsModel(
            openai_client=provider,
            model="gpt-4o-mini"  # or your preferred model
        )
    )

    # 2. Define an input string
    user_input = "Write a haiku about a diligent software engineer."

    # 3. Run the agent asynchronously
    print(f"\n🤖 Assistant: Running agent with input: '{user_input}'")
    try:
        result: RunResult = await Runner.run(
            starting_agent=assistant_agent,
            input=user_input
        )

        print(f"\n\n[OUT]\n\n: {result} \n\n\n, {type(result)}")
        
        print(f"\n\n[final_output]\n\n: {result.final_output} \n\n\n, {type(result.final_output)}")
        
        print(f"\n\n[raw_responses]\n\n: {result.raw_responses} \n\n\n, {type(result.raw_responses)}")
        
        print(f"\n\n[input_guardrail_results]\n\n: {result.input_guardrail_results} \n\n\n, {type(result.input_guardrail_results)}")
        
        print(f"\n\n[output_guardrail_results]\n\n: {result.output_guardrail_results} \n\n\n, {type(result.output_guardrail_results)}")
        
        print(f"\n\n[context_wrapper]\n\n: {result.context_wrapper} \n\n\n, {type(result.context_wrapper)}")
        
        print(f"\n\n[last_agent]\n\n: {result.last_agent} \n\n\n, {type(result.last_agent)}")
        
        print(f"\n\n[last_response_id]\n\n: {result.last_response_id} \n\n\n, {type(result.last_response_id)}")
        
        print(f"\n\n[new_items]\n\n: {result.new_items} \n\n\n, {type(result.new_items)}")
        
        print(f"\n\n[input]\n\n: {result.input} \n\n\n, {type(result.input)}")
        
        print(f"\n\n[to_input_list]\n\n: {result.to_input_list()} \n\n\n, {type(result.to_input_list())}")
        
        print(f"\n\n[final_output_as]\n\n: {result.final_output_as(str)} \n\n\n, {type(result.final_output_as(str))}")

        print(f"\n--- Finished 01_run.py --- ")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print(f"--- Finished 01_run.py with error --- ")

if __name__ == "__main__":
    asyncio.run(main())
