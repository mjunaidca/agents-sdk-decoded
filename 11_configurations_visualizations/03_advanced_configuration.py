"""
03_advanced_configuration.py

This module demonstrates advanced configuration options in the OpenAI Agents SDK.
Covers RunConfig, custom tracing, model provider configuration, and production setups.

Key Advanced Features:
- RunConfig for workflow control
- Custom tracing and spans
- Model provider customization
- Production environment configuration
- Performance optimization settings

Based on: https://openai.github.io/openai-agents-python/config/
"""

import asyncio
import os
import uuid
from datetime import datetime

from openai import AsyncOpenAI
from agents import (
    Agent, Runner, function_tool, RunConfig,
    trace, custom_span, gen_trace_id, get_current_trace,
    set_default_openai_client,
    OpenAIChatCompletionsModel
)

# ================== ADVANCED CONFIGURATION EXAMPLES ==================


async def demo_run_config_options():
    """Demonstrate RunConfig for controlling agent execution."""
    print("=== Demo: RunConfig Options ===")

    print("1. Basic RunConfig Usage:")

    # Create a test agent
    test_agent = Agent(
        name="ConfigTestAgent",
        instructions="You are a test agent. Simply acknowledge the request and respond briefly."
    )

    try:
        # 1. Basic configuration
        basic_config = RunConfig(
            workflow_name="AdvancedConfigDemo",
            trace_id=gen_trace_id(),
        )

        print("✅ Basic RunConfig created")
        print(f"   Workflow name: {basic_config.workflow_name}")
        print(f"   Trace ID: {basic_config.trace_id}")

        # 2. Test with basic config
        print("\n🤖 Running agent with basic RunConfig...")
        result = await Runner.run(
            test_agent,
            "Hello, please acknowledge this message",
            run_config=basic_config,
            max_turns=5
        )

        print(f"✅ Agent run completed with basic config")
        print(f"   Final output: {result.final_output[:100]}...")

    except Exception as e:
        print(f"❌ Error with basic RunConfig: {e}")

    print("\n2. Advanced RunConfig Options:")

    try:
        # Advanced configuration with all options
        advanced_config = RunConfig(
            workflow_name="AdvancedWorkflow_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
            trace_id=gen_trace_id(),
            group_id=f"config_demo_group_{uuid.uuid4().hex[:8]}",
            trace_metadata={
                "environment": "development",
                "experiment": "advanced_config_demo",
                "version": "1.0.0",
                "user_id": "demo_user",
                "session_id": uuid.uuid4().hex
            },
            tracing_disabled=False,  # Explicitly enable tracing
            input_guardrails=None,   # Could add global input guardrails
            output_guardrails=None   # Could add global output guardrails
        )

        print("✅ Advanced RunConfig created")
        print(f"   Workflow name: {advanced_config.workflow_name}")
        print(f"   Group ID: {advanced_config.group_id}")
        print(
            f"   Metadata keys: {list(advanced_config.trace_metadata.keys())}")
        print(f"   Tracing disabled: {advanced_config.tracing_disabled}")

        # Test with advanced config
        print("\n🤖 Running agent with advanced RunConfig...")
        result = await Runner.run(
            test_agent,
            "Hello with advanced configuration",
            run_config=advanced_config,
            max_turns=3
        )

        print(f"✅ Agent run completed with advanced config")

    except Exception as e:
        print(f"❌ Error with advanced RunConfig: {e}")


async def demo_custom_tracing():
    """Demonstrate custom tracing and span management."""
    print("\n=== Demo: Custom Tracing ===")

    print("1. Manual Trace Management:")

    try:
        # Create custom trace
        custom_trace_id = gen_trace_id()

        with trace("CustomTraceDemo", trace_id=custom_trace_id):
            print(f"✅ Custom trace started with ID: {custom_trace_id}")

            # Get current trace info
            current_trace = get_current_trace()
            if current_trace:
                print(f"   Current trace ID: {current_trace.trace_id}")
                print(f"   Trace disabled: {current_trace.disabled}")

            # Create custom spans for different operations
            with custom_span("DataPreparation", metadata={"step": "prepare"}):
                print("📊 Simulating data preparation...")
                await asyncio.sleep(0.1)  # Simulate work

            with custom_span("AgentExecution", metadata={"step": "execute"}):
                print("🤖 Simulating agent execution...")

                # Create a simple agent for the demo
                tracing_agent = Agent(
                    name="TracingDemoAgent",
                    instructions="You are demonstrating tracing capabilities. Respond briefly."
                )

                # Run with custom trace context
                result = await Runner.run(
                    tracing_agent,
                    "Demonstrate tracing",
                    run_config=RunConfig(
                        workflow_name="TracingDemo",
                        trace_id=custom_trace_id,
                        trace_metadata={"operation": "demo_execution"}
                    ),
                    max_turns=2
                )

                print(
                    f"   Agent response received (length: {len(str(result.final_output))})")

            with custom_span("PostProcessing", metadata={"step": "finalize"}):
                print("🔄 Simulating post-processing...")
                await asyncio.sleep(0.05)  # Simulate work

        print("✅ Custom trace completed successfully")

    except Exception as e:
        print(f"❌ Error with custom tracing: {e}")

    print("\n2. Trace Metadata and Organization:")

    try:
        # Demonstrate rich metadata
        metadata = {
            "environment": "development",
            "component": "configuration_demo",
            "version": "1.2.3",
            "user_context": {
                "user_id": "demo_user_123",
                "session_id": uuid.uuid4().hex,
                "preferences": {"language": "en", "timezone": "UTC"}
            },
            "execution_context": {
                "timestamp": datetime.now().isoformat(),
                "host": os.uname().nodename if hasattr(os, 'uname') else "unknown",
                "python_version": "3.x"
            }
        }

        trace_id = gen_trace_id()

        with trace("MetadataDemo", trace_id=trace_id, metadata=metadata):
            print(f"✅ Trace with rich metadata created")
            print(f"   Trace ID: {trace_id}")
            print(f"   Metadata categories: {list(metadata.keys())}")

            # Show how metadata helps with debugging and monitoring
            print("   Metadata enables:")
            print("     • User session tracking")
            print("     • Environment-specific debugging")
            print("     • Performance monitoring")
            print("     • A/B testing support")

    except Exception as e:
        print(f"❌ Error with metadata demo: {e}")


async def demo_model_provider_configuration():
    """Demonstrate custom model provider configuration."""
    print("\n=== Demo: Model Provider Configuration ===")

    print("1. Custom OpenAI Client Configuration:")

    try:
        # Configure custom OpenAI client with specific settings
        custom_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "demo-key"),
            base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
            timeout=30.0,
            max_retries=3,
            default_headers={
                "X-Custom-Header": "AdvancedConfigDemo",
                "X-Environment": "development"
            }
        )

        print("✅ Custom OpenAI client configured")
        print(f"   Base URL: {custom_client.base_url}")
        print(f"   Timeout: {custom_client.timeout} seconds")
        print(f"   Max retries: {custom_client.max_retries}")
        print(
            f"   Custom headers: {len(custom_client.default_headers)} headers")

        # Set as default for SDK
        set_default_openai_client(custom_client)
        print("   Set as default client for SDK")

    except Exception as e:
        print(f"❌ Error configuring custom client: {e}")

    print("\n2. Model-Specific Configuration:")

    try:
        # Create model with specific settings
        chat_model = OpenAIChatCompletionsModel(
            openai_client=custom_client,
            model="gpt-4o-mini",  # Specific model
            temperature=0.7,       # Custom temperature
            max_tokens=1000,       # Token limit
            top_p=0.9,            # Nucleus sampling
            frequency_penalty=0.1,  # Reduce repetition
            presence_penalty=0.1   # Encourage diversity
        )

        print("✅ Custom model configuration created")
        print(f"   Model: gpt-4o-mini")
        print(f"   Temperature: 0.7")
        print(f"   Max tokens: 1000")
        print(f"   Custom sampling parameters configured")

        # Test agent with custom model
        model_test_agent = Agent(
            name="ModelConfigAgent",
            instructions="You are testing custom model configuration. Be creative but concise.",
            model=chat_model
        )

        print("\n🤖 Testing agent with custom model...")
        result = await Runner.run(
            model_test_agent,
            "Tell me a creative fact about artificial intelligence",
            max_turns=2
        )

        print(f"✅ Custom model test successful")
        print(
            f"   Response length: {len(str(result.final_output))} characters")

    except Exception as e:
        print(f"❌ Error with model configuration: {e}")


async def demo_production_configuration():
    """Demonstrate production-ready configuration patterns."""
    print("\n=== Demo: Production Configuration ===")

    print("1. Environment-Based Configuration:")

    # Simulate environment detection
    environment = os.getenv("ENVIRONMENT", "development")
    print(f"   Detected environment: {environment}")

    # Environment-specific configurations
    config_profiles = {
        "development": {
            "tracing_enabled": True,
            "verbose_logging": True,
            "timeout": 30.0,
            "max_retries": 3,
            "max_turns": 10,
            "log_sensitive_data": True
        },
        "staging": {
            "tracing_enabled": True,
            "verbose_logging": False,
            "timeout": 20.0,
            "max_retries": 2,
            "max_turns": 8,
            "log_sensitive_data": False
        },
        "production": {
            "tracing_enabled": True,
            "verbose_logging": False,
            "timeout": 15.0,
            "max_retries": 2,
            "max_turns": 5,
            "log_sensitive_data": False
        }
    }

    profile = config_profiles.get(environment, config_profiles["development"])

    print("   Configuration profile:")
    for key, value in profile.items():
        print(f"     {key}: {value}")

    print("\n2. Security and Compliance Configuration:")

    security_settings = {
        "api_key_source": "environment_variable",
        "log_model_data": not profile["log_sensitive_data"],
        "log_tool_data": not profile["log_sensitive_data"],
        "trace_export_enabled": profile["tracing_enabled"],
        "custom_headers_allowed": environment != "production"
    }

    print("   Security settings:")
    for key, value in security_settings.items():
        print(f"     {key}: {value}")

    # Apply security settings
    if not security_settings["log_model_data"]:
        os.environ["OPENAI_AGENTS_DONT_LOG_MODEL_DATA"] = "1"

    if not security_settings["log_tool_data"]:
        os.environ["OPENAI_AGENTS_DONT_LOG_TOOL_DATA"] = "1"

    print("\n3. Performance Configuration:")

    performance_config = {
        "connection_pool_size": 10 if environment == "production" else 5,
        "request_timeout": profile["timeout"],
        "max_retries": profile["max_retries"],
        "backoff_factor": 2.0,
        "circuit_breaker_enabled": environment == "production"
    }

    print("   Performance settings:")
    for key, value in performance_config.items():
        print(f"     {key}: {value}")

    print("\n4. Monitoring and Observability:")

    monitoring_config = {
        "metrics_enabled": True,
        "health_check_interval": 30,
        "alert_on_errors": environment == "production",
        "trace_sampling_rate": 0.1 if environment == "production" else 1.0,
        "log_level": "ERROR" if environment == "production" else "INFO"
    }

    print("   Monitoring settings:")
    for key, value in monitoring_config.items():
        print(f"     {key}: {value}")


@function_tool
def validate_configuration(component: str) -> str:
    """Validate a specific configuration component."""
    validations = {
        "api_key": "API key validation passed" if os.getenv("OPENAI_API_KEY") else "API key missing",
        "tracing": "Tracing configuration valid",
        "logging": "Logging configuration valid",
        "security": "Security settings applied"
    }
    return validations.get(component, f"Unknown component: {component}")


async def demo_configuration_validation():
    """Demonstrate configuration validation and testing."""
    print("\n=== Demo: Configuration Validation ===")

    # Create validation agent
    validator_agent = Agent(
        name="ConfigValidator",
        instructions="""
        You are a configuration validator. Use the validate_configuration tool 
        to check different components. Report the validation results clearly.
        """,
        tools=[validate_configuration]
    )

    try:
        print("🔍 Running configuration validation...")

        result = await Runner.run(
            validator_agent,
            "Please validate the following components: api_key, tracing, logging, security",
            run_config=RunConfig(
                workflow_name="ConfigValidation",
                trace_metadata={"operation": "validation"}
            ),
            max_turns=5
        )

        print("✅ Configuration validation completed")
        print(f"📋 Validation report:\n{result.final_output}")

    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")


def demo_configuration_best_practices():
    """Demonstrate configuration best practices for production."""
    print("\n=== Configuration Best Practices ===")

    practices = {
        "🔐 Security": [
            "Store API keys in environment variables or secret managers",
            "Disable sensitive data logging in production",
            "Use least-privilege access for service accounts",
            "Implement API key rotation policies",
            "Monitor for unauthorized API usage"
        ],
        "🚀 Performance": [
            "Configure appropriate timeouts for your use case",
            "Set retry policies based on expected failure rates",
            "Use connection pooling for high-throughput scenarios",
            "Implement circuit breakers for external dependencies",
            "Monitor latency and error rates"
        ],
        "📊 Observability": [
            "Enable tracing with appropriate sampling rates",
            "Use structured logging with correlation IDs",
            "Set up alerts for critical errors",
            "Monitor token usage and costs",
            "Track agent performance metrics"
        ],
        "🔧 Operations": [
            "Use environment-specific configurations",
            "Validate configurations on startup",
            "Implement health checks",
            "Plan for graceful degradation",
            "Document configuration changes"
        ]
    }

    for category, items in practices.items():
        print(f"\n{category}:")
        for item in items:
            print(f"   • {item}")

    print("\n📋 Configuration Checklist:")
    checklist = [
        "✅ API keys stored securely",
        "✅ Environment-specific configs defined",
        "✅ Tracing and logging configured",
        "✅ Error handling and retries set up",
        "✅ Security settings applied",
        "✅ Performance parameters tuned",
        "✅ Monitoring and alerts configured",
        "✅ Configuration validation in place"
    ]

    for item in checklist:
        print(f"   {item}")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all advanced configuration demonstrations."""
    print("🔧 OpenAI Agents SDK - Advanced Configuration Guide 🔧")
    print("\nThis demonstrates advanced configuration patterns for")
    print("production-ready deployments of the OpenAI Agents SDK.\n")

    # Run advanced configuration demos
    await demo_run_config_options()
    await demo_custom_tracing()
    await demo_model_provider_configuration()
    await demo_production_configuration()
    await demo_configuration_validation()
    demo_configuration_best_practices()

    print("\n" + "="*60)
    print("🎓 Advanced Configuration Takeaways:")
    print("• Use RunConfig for fine-grained execution control")
    print("• Implement custom tracing for better observability")
    print("• Configure model providers for specific requirements")
    print("• Apply environment-specific configuration profiles")
    print("• Validate configurations before deployment")
    print("• Follow security best practices for production")
    print("• Monitor and optimize performance continuously")

if __name__ == "__main__":
    asyncio.run(main())
