# Context-Aware Tools Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
from dataclasses import dataclass
from agents import Agent, Runner, function_tool, RunContextWrapper


@dataclass
class AppContext:
    """Application context that will be passed to tools."""
    user_name: str
    session_id: str
    app_version: str = "1.0.0"


@function_tool
def read_file(ctx: RunContextWrapper[AppContext], path: str, directory: str | None = None) -> str:
    """Read the contents of a file with context awareness.

    Args:
        path: The path to the file to read
        directory: Optional directory to read from
    """
    # Access context information
    user_name = ctx.context.user_name if ctx.context else "Unknown User"
    session_id = ctx.context.session_id if ctx.context else "unknown_session"

    # Simulate file reading with context
    if directory:
        full_path = f"{directory}/{path}"
    else:
        full_path = path

    # Simulate file content based on path
    if path.endswith(".txt"):
        content = f"This is a text file content from {full_path}"
    elif path.endswith(".json"):
        content = f'{{"message": "JSON content from {full_path}", "user": "{user_name}", "session": "{session_id}"}}'
    elif path.endswith(".py"):
        content = f"# Python file: {full_path}\nprint('Hello from {user_name}')"
    else:
        content = f"Binary or unknown file type: {full_path}"

    return f"File read by {user_name} (session: {session_id}):\nPath: {full_path}\nContent:\n{content}"


@function_tool
def log_action(ctx: RunContextWrapper[AppContext], action: str, details: str = "") -> str:
    """Log an action with application context.

    Args:
        action: The action being performed
        details: Additional details about the action
    """
    user_name = ctx.context.user_name if ctx.context else "Unknown User"
    session_id = ctx.context.session_id if ctx.context else "unknown_session"
    app_version = ctx.context.app_version if ctx.context else "unknown_version"

    # Simulate logging with context
    log_entry = {
        "user": user_name,
        "session": session_id,
        "app_version": app_version,
        "action": action,
        "details": details,
        "timestamp": "2024-01-01T12:00:00Z"
    }

    return f"Action logged: {log_entry}"


@function_tool
def get_context_info(ctx: RunContextWrapper[AppContext]) -> str:
    """Get information about the current context.

    This tool demonstrates accessing context information and usage data.
    """
    if not ctx.context:
        return "No context available"

    info = {
        "user_name": ctx.context.user_name,
        "session_id": ctx.context.session_id,
        "app_version": ctx.context.app_version,
        "usage_info": {
            "completion_tokens": ctx.usage.completion_tokens,
            "prompt_tokens": ctx.usage.prompt_tokens,
            "total_tokens": ctx.usage.total_tokens
        }
    }

    return f"Context Information:\n{info}"


@function_tool
def process_with_memory(ctx: RunContextWrapper[AppContext], data: str, operation: str) -> str:
    """Process data with context-aware memory tracking.

    Args:
        data: The data to process
        operation: The operation to perform (uppercase, lowercase, reverse)
    """
    user_name = ctx.context.user_name if ctx.context else "Unknown User"
    session_id = ctx.context.session_id if ctx.context else "unknown_session"

    # Simulate processing based on operation
    if operation.lower() == "uppercase":
        result = data.upper()
    elif operation.lower() == "lowercase":
        result = data.lower()
    elif operation.lower() == "reverse":
        result = data[::-1]
    else:
        result = f"Unknown operation: {operation}"

    # Simulate memory tracking with context
    memory_entry = f"User {user_name} (session {session_id}) processed '{data}' with operation '{operation}' -> '{result}'"

    return f"Processing complete!\nResult: {result}\nMemory: {memory_entry}"


async def main():
    # Create application context
    app_context = AppContext(
        user_name="John Doe",
        session_id="sess_12345",
        app_version="2.1.0"
    )

    # Create agent with context-aware tools
    agent = Agent[AppContext](
        name="Context-Aware Assistant",
        instructions="""You are a context-aware assistant that can:
        1. Read files from the filesystem
        2. Log actions and activities
        3. Access context information
        4. Process data with memory tracking
        
        Always use context information to provide personalized responses.""",
        tools=[read_file, log_action, get_context_info, process_with_memory]
    )

    print("=== Context Information ===")
    result1 = await Runner.run(
        agent,
        input="Show me the current context information including usage stats",
        context=app_context
    )
    print(result1.final_output)
    print("\n" + "="*50 + "\n")

    print("=== File Reading with Context ===")
    result2 = await Runner.run(
        agent,
        input="Read the file 'config.json' from the 'settings' directory",
        context=app_context
    )
    print(result2.final_output)
    print("\n" + "="*50 + "\n")

    print("=== Action Logging ===")
    result3 = await Runner.run(
        agent,
        input="Log that I'm starting a data processing task with details about processing user preferences",
        context=app_context
    )
    print(result3.final_output)
    print("\n" + "="*50 + "\n")

    print("=== Data Processing with Memory ===")
    result4 = await Runner.run(
        agent,
        input="Process the text 'Hello World' by converting it to uppercase, then also reverse it",
        context=app_context
    )
    print(result4.final_output)

if __name__ == "__main__":
    asyncio.run(main())
