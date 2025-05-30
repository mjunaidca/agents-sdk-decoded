import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

load_dotenv(find_dotenv())

provider = AsyncOpenAI(base_url="https://api.openai.com/v1",
                       api_key=os.getenv("OPENAI_API_KEY"))


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in eng.",
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini"),

    )

    result = await Runner.run(agent, "Tell me about agents!")
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":
    print("\n[STARTING AGENT]\n")
    asyncio.run(main())
