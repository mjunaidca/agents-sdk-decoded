from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper
import asyncio

@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

def create_prompt(ctx: RunContextWrapper[str], agent: Agent[str]) -> str:
    print(f"Creating prompt for {ctx.context}")
    return f"You are a helpful assistant that provides concise answers. You are talking to {ctx.context}."


# Example 1: Basic string instructions
agent_basic = Agent[str](
    name="BasicAgent",
    instructions=create_prompt
)

async def test_basic():
    name = "junaid"
    result1 = await Runner.run(agent_basic, "What is my name?", context=name)
    print("Basic Agent:", result1.final_output)
    

async def main():
    await test_basic()

if __name__ == "__main__":
    asyncio.run(main())