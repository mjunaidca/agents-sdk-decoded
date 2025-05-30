import json

from typing_extensions import TypedDict, Any

from agents import Agent, FunctionTool, RunContextWrapper, function_tool, Runner
from pydantic import BaseModel

class Location(BaseModel):
    lat: float
    long: float

@function_tool  
async def fetch_weather(location: Location) -> str:
    
    """Fetch the weather for a given location.

    Args:
        location: The location to fetch the weather for.
    """
    # In real life, we'd fetch the weather from a weather API
    print("^" * 10, type(location), "^" * 10)
    print(location.lat)
    print(location.long)
    print(location.model_dump_json())
    print(location.model_dump())
    return "sunny"


@function_tool(name_override="fetch_data")  
def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
    """Read the contents of a file.

    Args:
        path: The path to the file to read.
        directory: The directory to read the file from.
    """
    # In real life, we'd read the file from the file system
    return "<file contents>"


agent = Agent(
    name="Assistant",
    tools=[fetch_weather, read_file],  
)

for tool in agent.tools:
    print("^" * 10, type(tool), "^" * 10)
    print(tool)
#     if isinstance(tool, FunctionTool):
#         print(tool.name)
#         print(tool.description)
#         print(json.dumps(tool.params_json_schema, indent=2))
#         print()
        
# result = Runner.run_sync(agent, "What is the weather in Tokyo?")
# print("^" * 10)
# print(result.final_output)
# print("^" * 10)
# print(result.new_items)
# print("^" * 10)
# print(result)