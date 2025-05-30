# Complete Hosted Tools Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
from agents import Agent, Runner, WebSearchTool, LocalShellTool

# Note: Some hosted tools require specific configuration and may not work in all environments
# This example demonstrates the proper way to configure each hosted tool


async def main():
    print("OpenAI Agents SDK - Complete Hosted Tools Examples")
    print("=" * 60)

    # 1. Web Search Tool - Most commonly available
    print("=== Web Search Tool ===")
    web_agent = Agent(
        name="Web Search Assistant",
        instructions="You can search the web for current information. Always cite your sources.",
        tools=[
            WebSearchTool(
                user_location="San Francisco, CA",  # Optional: User location for better results
                search_context_size='medium'  # Optional: Number of search results to include
            )
        ]
    )

    try:
        result1 = await Runner.run(
            web_agent,
            input="What are the latest developments in AI agents in 2024?"
        )
        print(f"Web Search Result: {result1.final_output}\n")
    except Exception as e:
        print(f"Web Search Error: {e}\n")

    # 2. Local Shell Tool - Runs commands on local machine
    print("=== Local Shell Tool ===")
    shell_agent = Agent(
        name="Shell Assistant",
        instructions="""You can execute shell commands on the local machine. 
        Be careful and only run safe commands. Always explain what you're doing.""",
        # tools=[LocalShellTool(executor=LocalShellExecutor())]
    )

    try:
        result2 = await Runner.run(
            shell_agent,
            input="Show me the current directory and list its contents"
        )
        print(f"Shell Result: {result2.final_output}\n")
    except Exception as e:
        print(f"Shell Error: {e}\n")

    # 3. File Search Tool - Requires OpenAI Vector Store setup
    print("=== File Search Tool Configuration Example ===")
    print("Note: FileSearchTool requires pre-configured Vector Store IDs")

    # Example configuration (would need real vector store IDs)
    file_search_config = """
    from agents import FileSearchTool
    
    # FileSearchTool configuration
    file_search_tool = FileSearchTool(
        vector_store_ids=["vs_1234567890"],  # Your Vector Store IDs
        max_num_results=5,                   # Maximum results to return
        include_search_results=True,         # Include search results in response
        ranking_options={                    # Optional ranking configuration
            "ranker": "auto",
            "score_threshold": 0.7
        },
        filters={                           # Optional metadata filters
            "and": [
                {"key": "document_type", "value": "pdf"}
            ]
        }
    )
    """
    print(file_search_config)

    # 4. Code Interpreter Tool - Requires specific configuration
    print("=== Code Interpreter Tool Configuration Example ===")
    print("Note: CodeInterpreterTool requires specific tool configuration")

    code_interpreter_config = """
    from agents import CodeInterpreterTool
    
    # CodeInterpreterTool configuration
    code_tool = CodeInterpreterTool(
        tool_config={
            "type": "code_interpreter",
            # Additional configuration as needed
        }
    )
    """
    print(code_interpreter_config)

    # 5. Computer Tool - For computer automation
    print("=== Computer Tool Configuration Example ===")
    print("Note: ComputerTool requires environment setup")

    computer_tool_config = """
    from agents import ComputerTool
    
    # ComputerTool configuration
    computer_tool = ComputerTool(
        computer={
            "environment": "desktop",        # Environment type
            "dimensions": [1920, 1080]      # Screen dimensions [width, height]
        }
    )
    """
    print(computer_tool_config)

    # 6. Image Generation Tool
    print("=== Image Generation Tool Configuration Example ===")

    image_gen_config = """
    from agents import ImageGenerationTool
    
    # ImageGenerationTool configuration
    image_tool = ImageGenerationTool(
        tool_config={
            "type": "image_generation",
            # Model and quality settings
        }
    )
    """
    print(image_gen_config)

    # 7. Hosted MCP Tool
    print("=== Hosted MCP Tool Configuration Example ===")

    mcp_tool_config = """
    from agents import HostedMCPTool
    
    # HostedMCPTool configuration
    mcp_tool = HostedMCPTool(
        tool_config={
            "type": "mcp",
            "server_label": "my_mcp_server",  # MCP server identifier
            # Additional MCP configuration
        }
    )
    """
    print(mcp_tool_config)

    # 8. Multi-tool agent example
    print("=== Multi-Tool Agent Example ===")

    # Create an agent with multiple hosted tools
    multi_tool_agent = Agent(
        name="Multi-Tool Assistant",
        instructions="""You are a versatile assistant with access to multiple tools:
        1. Web search for current information
        2. Shell commands for system operations
        
        Use the appropriate tool based on the user's request.""",
        tools=[
            WebSearchTool(),
            # LocalShellTool(executor=LocalShellExecutor())
        ]
    )

    try:
        result8 = await Runner.run(
            multi_tool_agent,
            input="Search for Python best practices and then check if Python is installed on this system"
        )
        print(f"Multi-tool Result: {result8.final_output}\n")
    except Exception as e:
        print(f"Multi-tool Error: {e}\n")

    # 9. Tool configuration best practices
    print("=== Tool Configuration Best Practices ===")
    practices = """
    Best Practices for Hosted Tools:
    
    1. WebSearchTool:
       - Set user_location for localized results
       - Adjust search_context_size based on needs
       - Always instruct agent to cite sources
    
    2. LocalShellTool:
       - Use with caution in production
       - Implement proper security measures
       - Limit to safe commands only
    
    3. FileSearchTool:
       - Pre-populate Vector Stores with relevant content
       - Use filters to narrow search scope
       - Set appropriate max_num_results
    
    4. CodeInterpreterTool:
       - Monitor code execution carefully
       - Set execution timeouts
       - Validate inputs and outputs
    
    5. ComputerTool:
       - Configure appropriate screen dimensions
       - Use in controlled environments
       - Implement failsafes for automation
    
    6. Security Considerations:
       - Validate all tool inputs
       - Monitor tool usage and outputs
       - Implement rate limiting where appropriate
       - Use least privilege principle
    """
    print(practices)

if __name__ == "__main__":
    asyncio.run(main())
