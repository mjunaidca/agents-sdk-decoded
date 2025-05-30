# Hosted Tools Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
from agents import Agent, Runner, WebSearchTool


async def main():
    # Create agent with hosted tools
    agent = Agent(
        name="Research Assistant",
        instructions="""You are a helpful research assistant. You can:
        1. Search the web for current information
        
        Always cite your sources when using web search results.""",
        tools=[
            WebSearchTool(),
            # Note: CodeInterpreterTool requires specific configuration
            # Commenting out for this example to avoid configuration issues
            # CodeInterpreterTool(),
        ]
    )

    print("=== Testing Web Search Tool ===")
    result1 = await Runner.run(
        agent,
        input="What are the latest developments in AI agents in 2024?"
    )
    print(result1.final_output)
    print("\n" + "="*50 + "\n")

    print("=== Testing Basic Query ===")
    result2 = await Runner.run(
        agent,
        input="Search for information about OpenAI Agents SDK and summarize the key features."
    )
    print(result2.final_output)

if __name__ == "__main__":
    asyncio.run(main())
 