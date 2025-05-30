"""
01_basic_configuration.py

This module demonstrates the basic configuration options available in the OpenAI Agents SDK.
Covers API keys, custom clients, tracing configuration, and debug logging.

Key Configuration Areas:
- API keys and client setup
- Tracing configuration and control
- Debug logging configuration
- Environment variable setup

Based on: https://openai.github.io/openai-agents-python/config/
"""

import asyncio
import logging
import os
from typing import Optional

from openai import AsyncOpenAI
from agents import (
    Agent, Runner, function_tool,
    set_default_openai_key, set_default_openai_client, set_default_openai_api,
    set_tracing_export_api_key, set_tracing_disabled,
    enable_verbose_stdout_logging
)

# ================== CONFIGURATION EXAMPLES ==================


async def demo_basic_configuration():
    """Demonstrate basic SDK configuration."""
    print("=== Demo: Basic SDK Configuration ===")

    # 1. Set API key programmatically (if not using environment variable)
    print("\n1. API Key Configuration:")

    # Option A: Use environment variable (recommended)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ Using API key from OPENAI_API_KEY environment variable")
    else:
        print("⚠️ OPENAI_API_KEY not found in environment")
        # Option B: Set programmatically
        # set_default_openai_key("sk-your-api-key-here")
        print("💡 You can set it programmatically with set_default_openai_key()")

    # 2. Custom OpenAI client configuration
    print("\n2. Custom Client Configuration:")

    try:
        # Create a custom client with specific settings
        custom_client = AsyncOpenAI(
            api_key=api_key or "demo-key",
            base_url="https://api.openai.com/v1",  # Default, but you can customize
            timeout=30.0,  # Custom timeout
            max_retries=3,  # Custom retry logic
        )

        # Set as default client for the SDK
        set_default_openai_client(custom_client)
        print("✅ Custom OpenAI client configured successfully")

        # Show client configuration
        print(f"   Base URL: {custom_client.base_url}")
        print(f"   Timeout: {custom_client.timeout}")
        print(f"   Max retries: {custom_client.max_retries}")

    except Exception as e:
        print(f"❌ Error configuring custom client: {e}")

    # 3. API selection (Responses API vs Chat Completions API)
    print("\n3. API Selection:")

    try:
        # By default, SDK uses OpenAI Responses API
        print("🔄 Default: Using OpenAI Responses API")

        # Switch to Chat Completions API if needed
        # set_default_openai_api("chat_completions")
        print("💡 Can switch to Chat Completions API with set_default_openai_api('chat_completions')")

    except Exception as e:
        print(f"❌ Error configuring API selection: {e}")


async def demo_tracing_configuration():
    """Demonstrate tracing configuration options."""
    print("\n=== Demo: Tracing Configuration ===")

    print("1. Tracing Status:")
    print("✅ Tracing is enabled by default")

    # 2. Custom tracing API key
    print("\n2. Custom Tracing API Key:")
    tracing_key = os.getenv("OPENAI_API_KEY")  # Usually same as main API key
    if tracing_key:
        try:
            set_tracing_export_api_key(tracing_key)
            print("✅ Custom tracing API key configured")
        except Exception as e:
            print(f"❌ Error setting tracing key: {e}")
    else:
        print("💡 Can set custom tracing key with set_tracing_export_api_key()")

    # 3. Disable tracing if needed
    print("\n3. Tracing Control:")
    print("💡 Tracing can be disabled with set_tracing_disabled(True)")
    # set_tracing_disabled(True)  # Uncomment to disable
    print("   (Keeping tracing enabled for this demo)")

    # 4. Environment variables for sensitive data
    print("\n4. Sensitive Data Protection:")
    print("Environment variables to control sensitive data logging:")
    print("   OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1  - Disables LLM input/output logging")
    print("   OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1   - Disables tool input/output logging")

    model_data_logging = os.getenv("OPENAI_AGENTS_DONT_LOG_MODEL_DATA")
    tool_data_logging = os.getenv("OPENAI_AGENTS_DONT_LOG_TOOL_DATA")

    print(
        f"   Model data logging: {'DISABLED' if model_data_logging else 'ENABLED'}")
    print(
        f"   Tool data logging: {'DISABLED' if tool_data_logging else 'ENABLED'}")


async def demo_logging_configuration():
    """Demonstrate debug logging configuration."""
    print("\n=== Demo: Logging Configuration ===")

    print("1. Default Logging Behavior:")
    print("   - Warnings and errors sent to stdout")
    print("   - Other logs suppressed by default")

    print("\n2. Enable Verbose Logging:")
    try:
        # Enable verbose logging for the demo
        enable_verbose_stdout_logging()
        print("✅ Verbose stdout logging enabled")

        # Test logging levels
        logger = logging.getLogger("openai.agents")
        print(f"   Logger level: {logger.level}")
        print(f"   Handlers: {len(logger.handlers)} handler(s)")

    except Exception as e:
        print(f"❌ Error enabling verbose logging: {e}")

    print("\n3. Custom Logging Configuration:")
    print("💡 For custom logging, configure the 'openai.agents' logger:")
    print("   import logging")
    print("   logger = logging.getLogger('openai.agents')")
    print("   logger.setLevel(logging.DEBUG)")
    print("   logger.addHandler(logging.StreamHandler())")

    print("\n4. Tracing Logger:")
    print("💡 Separate tracing logger available: 'openai.agents.tracing'")


@function_tool
def demo_calculation(x: int, y: int) -> str:
    """Perform a simple calculation for testing configuration."""
    result = x + y
    return f"The sum of {x} and {y} is {result}"


async def demo_configured_agent():
    """Demonstrate using an agent with the configured SDK."""
    print("\n=== Demo: Agent with Configuration ===")

    # Create a simple agent to test the configuration
    agent = Agent(
        name="ConfigTestAgent",
        instructions="""
        You are a test agent for configuration demonstration.
        Use the demo_calculation tool to add two numbers.
        Keep your response brief and friendly.
        """,
        tools=[demo_calculation]
    )

    try:
        print("🤖 Running agent with current configuration...")

        # Test the agent
        result = await Runner.run(
            agent,
            "Please calculate 15 + 27 using the available tool",
            max_turns=3
        )

        print(f"✅ Agent execution successful!")
        print(f"📤 Response: {result.final_output}")

        # Show some result metadata
        print(f"📊 Execution details:")
        print(f"   - New items: {len(result.new_items)}")
        print(f"   - Raw responses: {len(result.raw_responses)}")
        print(f"   - Last agent: {result.last_agent.name}")

    except Exception as e:
        print(f"❌ Agent execution failed: {e}")
        print("💡 This might be due to missing API key or configuration issues")


async def demo_environment_variables():
    """Demonstrate important environment variables."""
    print("\n=== Demo: Environment Variables ===")

    # Key environment variables for the SDK
    env_vars = {
        "OPENAI_API_KEY": "Your OpenAI API key (required)",
        "OPENAI_API_BASE": "Custom API base URL (optional)",
        "OPENAI_AGENTS_DONT_LOG_MODEL_DATA": "Disable model data logging (optional)",
        "OPENAI_AGENTS_DONT_LOG_TOOL_DATA": "Disable tool data logging (optional)",
    }

    print("Important environment variables:")
    for var, description in env_vars.items():
        value = os.getenv(var)
        status = "✅ SET" if value else "❌ NOT SET"
        print(f"   {var}: {status}")
        print(f"      Description: {description}")
        if value and var != "OPENAI_API_KEY":  # Don't show API key value
            print(f"      Value: {value}")
        print()


async def demo_configuration_best_practices():
    """Demonstrate configuration best practices."""
    print("\n=== Configuration Best Practices ===")

    practices = [
        "🔐 Store API keys in environment variables, not in code",
        "🏠 Use .env files for local development with python-dotenv",
        "📊 Enable tracing in development, consider disabling in production",
        "🔍 Use verbose logging during development and debugging",
        "🛡️ Protect sensitive data with appropriate environment variables",
        "⚙️ Configure custom clients for specific timeout/retry requirements",
        "🔄 Use Chat Completions API if you need specific model behaviors",
        "📝 Monitor and log configuration issues for debugging",
    ]

    print("Configuration best practices:")
    for practice in practices:
        print(f"   {practice}")

    print("\n💡 Sample .env file:")
    print("""
   OPENAI_API_KEY=your-actual-api-key-here
   OPENAI_API_BASE=https://api.openai.com/v1
   OPENAI_AGENTS_DONT_LOG_MODEL_DATA=0
   OPENAI_AGENTS_DONT_LOG_TOOL_DATA=0
   """)

    print("💡 Load with python-dotenv:")
    print("""
   from dotenv import load_dotenv
   load_dotenv()  # Loads .env file
   """)


# ================== MAIN EXECUTION ==================


async def main():
    """Run all configuration demonstrations."""
    print("🔧 OpenAI Agents SDK - Configuration Guide 🔧")
    print("\nThis demonstrates how to configure the OpenAI Agents SDK")
    print("for optimal performance and security.\n")

    # Run all configuration demos
    await demo_basic_configuration()
    await demo_tracing_configuration()
    await demo_logging_configuration()
    await demo_environment_variables()
    await demo_configured_agent()
    await demo_configuration_best_practices()

    print("\n" + "="*60)
    print("🎓 Key Configuration Takeaways:")
    print("• Use environment variables for sensitive configuration")
    print("• Enable verbose logging during development")
    print("• Configure tracing based on your monitoring needs")
    print("• Protect sensitive data with appropriate settings")
    print("• Test your configuration with a simple agent")
    print("• Follow security best practices for API keys")

if __name__ == "__main__":
    asyncio.run(main())
