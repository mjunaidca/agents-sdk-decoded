from typing import Any

from pydantic import BaseModel, ConfigDict
from openai import AsyncOpenAI
from agents import RunContextWrapper, FunctionTool, Runner, Agent, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GOOGLE_API_KEY")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)


def do_some_work(data: str) -> str:
    return "done"


class FunctionArgs(BaseModel):
    username: str
    age: int
    
    model_config = ConfigDict(
        # extra="ignore"
        extra="forbid"
    )


async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_some_work(data=f"{parsed.username} is {parsed.age} years old")
    # raise Exception("Something went wrong")


tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)

agent = Agent(
    name="Hello Agent",
    instructions="You are a helpful assistant that can process user data",
    tools=[tool],
)

for tool in agent.tools:
    print(tool)
    print(tool.name)
    print(tool.description)
    print(tool.params_json_schema)
    print(tool.on_invoke_tool)
    print()

result = Runner.run_sync(agent, "Use process_user tool to process user data: username='junaid', age=25")
print(result.final_output)