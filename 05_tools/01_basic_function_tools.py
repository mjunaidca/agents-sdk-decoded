# Basic Function Tools Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
import json
from typing_extensions import TypedDict
from agents import Agent, Runner, function_tool


class Location(TypedDict):
    lat: float
    long: float


@function_tool
def get_weather(location: Location) -> str:
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for with latitude and longitude.
    """
    # Simulate weather API call
    return f"The weather at {location['lat']}, {location['long']} is sunny and 72°F"


@function_tool
def calculate_distance(from_lat: float, from_long: float, to_lat: float, to_long: float) -> str:
    """Calculate distance between two geographic points.

    Args:
        from_lat: Starting latitude
        from_long: Starting longitude  
        to_lat: Destination latitude
        to_long: Destination longitude
    """
    # Simple distance calculation (not accurate, just for demo)
    distance = ((to_lat - from_lat) ** 2 + (to_long - from_long) ** 2) ** 0.5
    return f"Distance is approximately {distance:.2f} degrees"


async def main():
    agent = Agent(
        name="Weather Assistant",
        instructions="You help users with weather and location information. Use the available tools to provide accurate responses.",
        tools=[get_weather, calculate_distance]
    )

    # Print tool information
    print("=== Available Tools ===")
    for tool in agent.tools:
        if hasattr(tool, 'name'):
            print(f"Tool: {tool.name}")
            # Only FunctionTool has description attribute
            if hasattr(tool, 'description'):
                print(f"Description: {tool.description}")
            # Only FunctionTool has params_json_schema attribute
            if hasattr(tool, 'params_json_schema'):
                print("Schema:")
                print(json.dumps(tool.params_json_schema, indent=2))
            print()

    # Test the agent
    result = await Runner.run(
        agent,
        input="What's the weather in San Francisco (37.7749, -122.4194)?"
    )
    print("=== Result ===")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
