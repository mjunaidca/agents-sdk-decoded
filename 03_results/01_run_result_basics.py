"""
01_run_result_basics.py

Demonstrates basic attributes and methods of RunResult.

Covers:
- Accessing final_output
- Accessing last_agent
- Using to_input_list() for subsequent turns
- Inspecting new_items (content and type)
- Accessing the original input

Based on:
- https://openai.github.io/openai-agents-python/results/
- https://openai.github.io/openai-agents-python/ref/result/#agents.result.RunResultBase
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
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Simple agent for demonstration
simple_agent = Agent(
    name="EchoAgent",
    instructions="You are an Echo Agent. Repeat the user's input prefixed with 'Echo: '.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini")
)


async def main():
    print("--- Running 01_run_result_basics.py ---")

    user_input_turn1 = "Hello, Agent!"
    print(f"\nOriginal User Input (Turn 1): '{user_input_turn1}'")

    try:
        # --- First Run ---
        result_turn1: RunResult = await Runner.run(
            starting_agent=simple_agent,
            input=user_input_turn1
        )

        print("\n--- Accessing RunResult Attributes (Turn 1) ---")

        # 1. Final Output
        final_output_t1 = result_turn1.final_output
        print(f"1. Final Output: '{final_output_t1}' (Type: {type(final_output_t1)})")

        # 2. Last Agent
        last_agent_t1 = result_turn1.last_agent
        print(f"2. Last Agent: Name='{last_agent_t1.name}' (Type: {type(last_agent_t1)})")

        # 3. New Items (items generated during this run)
        new_items_t1 = result_turn1.new_items
        print(f"3. New Items (Count: {len(new_items_t1)}):")
        if new_items_t1:
            for i, item in enumerate(new_items_t1):
                print(f"   - Item {i+1}: {str(item)[:100]}... (Type: {type(item)})")
        else:
            print("   No new items generated in this simple run (besides final_output which is part of it).")

        # Note: For a simple agent like this, new_items might primarily contain the final Text output.
        # For agents using tools or handoffs, new_items would be more diverse.

        # 4. Original Input
        original_input_t1 = result_turn1.input
        print(f"4. Original Input stored in result: '{original_input_t1}' (Type: {type(original_input_t1)})")

        # --- Preparing for a hypothetical Second Turn ---
        print("\n--- Preparing for Next Turn using to_input_list() ---")

        # 5. Inputs for the next turn
        input_list_for_turn2 = result_turn1.to_input_list()
        print(f"5. Input List for Next Turn (from to_input_list(), Count: {len(input_list_for_turn2)}):")
        for i, item_dict in enumerate(input_list_for_turn2):
            # to_input_list() returns a list of dicts or SDK items suitable for OpenAI API
            print(f"   - Item {i+1}: {str(item_dict)[:100]}... (Type: {type(item_dict)})")

        # Example of adding a new user message for turn 2
        user_input_turn2 = "How are you today?"
        # If to_input_list() returns dicts, you add a dict. If it returns items, use items format
        # Most commonly, to_input_list() returns dicts compatible with OpenAI API format
        if input_list_for_turn2 and isinstance(input_list_for_turn2[0], dict):
            current_conversation_history = input_list_for_turn2 + \
                [{"role": "user", "content": user_input_turn2}]
        else:  # If it returns other item types, convert to dict format
            current_conversation_history = input_list_for_turn2 + \
                [{"role": "user", "content": user_input_turn2}]

        print(f"\n   New user message for Turn 2: '{user_input_turn2}'")
        print(
            f"   Combined history for Turn 2 (Count: {len(current_conversation_history)}):")
        for i, item_dict in enumerate(current_conversation_history):
            print(f"     - Item {i+1}: {str(item_dict)[:100]}...")

        # You would then pass `current_conversation_history` to another `Runner.run()` call.

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

    print("\n--- Finished 01_run_result_basics.py ---")

if __name__ == "__main__":
    asyncio.run(main())
