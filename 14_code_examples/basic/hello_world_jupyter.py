import asyncio
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

# Intended for Jupyter notebooks where there's an existing event loop
async def main():
    result = await Runner.run(agent, "Write a haiku about recursion in programming.")  # type: ignore[top-level-await]  # noqa: F704
    print(result.final_output)

asyncio.run(main())

# Code within code loops,
# Infinite mirrors reflect—
# Logic folds on self.
