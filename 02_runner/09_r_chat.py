"""
11_conversations_chat_threads.py

Demonstrates managing multi-turn conversations (chat threads) with Runner.

- Running an initial turn.
- Using RunResultBase.to_input_list() to get conversation history.
- Appending new user messages to the history.
- Running subsequent turns with the updated history.
- Using RunConfig.group_id to link traces for a conversation thread.

Based on: https://openai.github.io/openai-agents-python/running_agents/#conversationschat-threads
"""

import asyncio
import os
import uuid
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel, RunConfig, trace
)

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# --- Conversational Agent ---
conversational_agent = Agent(
    name="ConversationalAgent",
    instructions="You are a helpful and concise conversational AI. Remember previous parts of the conversation.",
    model=OpenAIChatCompletionsModel(
        openai_client=provider, model="gpt-4o-mini")
)

async def main():
    print("--- Running 09_conversations_chat_threads.py ---")
    agent = Agent(name="Assistant", instructions="Reply very concisely.")

    with trace(workflow_name="Conversation", group_id="123"):
        # First turn
        result = await Runner.run(agent, "What city is the Golden Gate Bridge in?")
        print(result.final_output)
        # San Francisco

        # Second turn
        new_input = result.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
        result = await Runner.run(agent, new_input)
        print(result.final_output)
        # California
    print("\n--- Finished 09_conversations_chat_threads.py ---")

if __name__ == "__main__":
    asyncio.run(main())
