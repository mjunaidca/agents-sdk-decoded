# Custom Function Tools Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
from typing import Any
from pydantic import BaseModel
from agents import Agent, Runner, FunctionTool, RunContextWrapper


class UserData(BaseModel):
    username: str
    age: int
    email: str


class DatabaseQuery(BaseModel):
    table: str
    query: str
    limit: int


async def process_user_data(ctx: RunContextWrapper[Any], args: str) -> str:
    """Process user data and return formatted information."""
    parsed = UserData.model_validate_json(args)

    # Simulate processing user data
    result = {
        "status": "processed",
        "user_id": f"user_{parsed.username.lower()}",
        "profile": f"{parsed.username} ({parsed.age} years old)",
        "contact": parsed.email,
        "created_at": "2024-01-01T00:00:00Z"
    }

    return f"User data processed successfully:\n{result}"


async def execute_database_query(ctx: RunContextWrapper[Any], args: str) -> str:
    """Execute a simulated database query."""
    parsed = DatabaseQuery.model_validate_json(args)

    # Simulate database query execution
    mock_results = [
        {"id": i, "name": f"Record {i}", "value": f"Data {i}"}
        for i in range(1, min(parsed.limit + 1, 6))
    ]

    return f"Query executed on table '{parsed.table}':\nSQL: {parsed.query}\nResults: {mock_results}"


async def main():
    # Create custom function tools
    user_processor_tool = FunctionTool(
        name="process_user",
        description="Processes user data and creates a user profile",
        params_json_schema=UserData.model_json_schema(),
        on_invoke_tool=process_user_data,
    )

    database_tool = FunctionTool(
        name="query_database",
        description="Execute database queries to retrieve information",
        params_json_schema=DatabaseQuery.model_json_schema(),
        on_invoke_tool=execute_database_query,
    )

    agent = Agent(
        name="Data Processing Assistant",
        instructions="""You are a data processing assistant that can:
        1. Process user data and create user profiles
        2. Execute database queries to retrieve information
        
        Always validate the data before processing and provide clear feedback.""",
        tools=[user_processor_tool, database_tool]
    )
    
    for tool in agent.tools:
        print(tool)
        print(tool.name)


    print("=== Testing User Data Processing ===")
    result1 = await Runner.run(
        agent,
        input='Process this user data: username="john_doe", age=30, email="john@example.com"'
    )
    print(result1.final_output)
    print("\n" + "="*50 + "\n")

    print("=== Testing Database Query ===")
    result2 = await Runner.run(
        agent,
        input='Query the "users" table to find all users with age > 25, limit to 3 results'
    )
    print(result2.final_output)

if __name__ == "__main__":
    asyncio.run(main())
