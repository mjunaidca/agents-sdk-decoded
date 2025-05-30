"""
03_model_configuration.py

This module covers model configuration in the OpenAI Agents SDK.
Focus: ModelSettings, parameters, and customization options.

Learning Objectives:
- Understand ModelSettings for configuring model behavior
- Learn about temperature, max_tokens, and other parameters
- Master configuration patterns for different use cases
- Understand model-specific settings and constraints

Key Concepts:
- ModelSettings class for parameter configuration
- Temperature controls randomness and creativity
- Token limits and context management
- Provider-specific parameter support
- Configuration best practices

Based on: https://openai.github.io/openai-agents-python/models/
"""

import asyncio
from agents import Agent, Runner, ModelSettings, function_tool
from openai import AsyncOpenAI

# ================== MODEL CONFIGURATION FUNDAMENTALS ==================


async def demo_model_settings_overview():
    """Demonstrate ModelSettings overview and basic usage."""
    print("=== Demo: ModelSettings Overview ===")

    print("⚙️ ModelSettings Overview:")
    print("   • Configure model behavior parameters")
    print("   • Control randomness, creativity, and output length")
    print("   • Fine-tune model responses for specific use cases")
    print("   • Provider-agnostic parameter specification")
    print("   • Optional configuration (defaults are sensible)")
    print()

    print("🎛️ Key Configuration Parameters:")
    parameters = {
        "temperature": "Controls randomness (0.0 = deterministic, 2.0 = very random)",
        "max_tokens": "Maximum tokens in response (output length limit)",
        "top_p": "Nucleus sampling parameter (0.1 = focused, 1.0 = full vocabulary)",
        "frequency_penalty": "Reduces repetition (-2.0 to 2.0)",
        "presence_penalty": "Encourages topic diversity (-2.0 to 2.0)",
        "tool_choice": "Controls tool usage ('auto', 'required', 'none')",
        "parallel_tool_calls": "Enable parallel tool execution",
        "truncation": "Context truncation strategy ('auto', 'disabled')",
        "reasoning": "Configuration for reasoning models",
        "metadata": "Custom metadata for requests"
    }

    for param, description in parameters.items():
        print(f"   • {param:18}: {description}")

    print(f"\n💡 Configuration Philosophy:")
    print(f"   ✓ Start with defaults and adjust incrementally")
    print(f"   ✓ Test configuration changes with real use cases")
    print(f"   ✓ Different tasks may need different settings")
    print(f"   ✓ Balance performance with cost and latency")


async def demo_temperature_control():
    """Demonstrate temperature parameter for controlling randomness."""
    print("\n=== Demo: Temperature Control ===")

    print("🌡️ Temperature Parameter (0.0 - 2.0):")
    print("   • 0.0: Deterministic, consistent responses")
    print("   • 0.3: Slightly creative, mostly consistent")
    print("   • 0.7: Balanced creativity and consistency")
    print("   • 1.0: Creative, varied responses")
    print("   • 1.5+: Very creative, potentially unpredictable")
    print()

    print("🎯 Temperature Use Cases:")
    use_cases = {
        "0.0 - 0.2": ["Code generation", "Data extraction", "Factual Q&A", "Classification"],
        "0.3 - 0.5": ["Technical writing", "Summaries", "Analysis", "Documentation"],
        "0.6 - 0.8": ["Creative writing", "Brainstorming", "Marketing copy", "General chat"],
        "0.9 - 1.2": ["Poetry", "Stories", "Art descriptions", "Experimental ideas"],
        "1.3 - 2.0": ["Abstract art", "Surreal content", "Highly experimental", "Research"]
    }

    for temp_range, cases in use_cases.items():
        print(f"   {temp_range:8}: {', '.join(cases)}")

    print(f"\n🧪 Temperature Configuration Examples:")

    # Conservative agent (low temperature)
    print(f"\n   📊 Conservative Agent (temperature=0.1):")
    try:
        conservative_agent = Agent(
            name="ConservativeAgent",
            instructions="Provide factual, consistent responses.",
            model_settings=ModelSettings(temperature=0.1)
        )

        print(f"      Configuration: temperature=0.1")
        print(f"      Use case: Factual information, code generation")
        print(f"      Behavior: Highly consistent, minimal variation")

    except Exception as e:
        print(f"      Configuration demo: temperature=0.1")
        print(f"      ✓ Low randomness for consistent outputs")

    # Creative agent (high temperature)
    print(f"\n   🎨 Creative Agent (temperature=0.8):")
    try:
        creative_agent = Agent(
            name="CreativeAgent",
            instructions="Provide creative, engaging responses.",
            model_settings=ModelSettings(temperature=0.8)
        )

        print(f"      Configuration: temperature=0.8")
        print(f"      Use case: Creative writing, brainstorming")
        print(f"      Behavior: Varied, creative responses")

    except Exception as e:
        print(f"      Configuration demo: temperature=0.8")
        print(f"      ✓ Higher randomness for creative outputs")


async def demo_token_management():
    """Demonstrate token limits and context management."""
    print("\n=== Demo: Token Management ===")

    print("🎫 Token Management Overview:")
    print("   • max_tokens: Limits response length (not total context)")
    print("   • Context includes input + output tokens")
    print("   • Different models have different context limits")
    print("   • Tokens ≈ 0.75 words for English text")
    print("   • Cost is typically based on total token usage")
    print()

    print("📏 Common Token Limits by Model:")
    token_limits = {
        "gpt-3.5-turbo": "4,096 tokens (older) / 16,385 tokens (newer)",
        "gpt-4": "8,192 tokens (original) / 32,768 tokens (extended)",
        "gpt-4o": "128,000 tokens (large context)",
        "claude-3-sonnet": "200,000 tokens (very large context)",
        "gemini-pro": "32,768 tokens (standard context)"
    }

    for model, limit in token_limits.items():
        print(f"   • {model:15}: {limit}")

    print(f"\n⚙️ Token Configuration Examples:")

    # Short response agent
    print(f"\n   📝 Short Response Agent (max_tokens=50):")
    try:
        short_agent = Agent(
            name="ShortAgent",
            instructions="Provide brief, concise responses.",
            model_settings=ModelSettings(max_tokens=50)
        )

        print(f"      Configuration: max_tokens=50")
        print(f"      Use case: Quick answers, status updates")
        print(f"      Expected length: ~37 words maximum")

    except Exception as e:
        print(f"      Configuration demo: max_tokens=50")
        print(f"      ✓ Very short responses for quick answers")

    # Detailed response agent
    print(f"\n   📖 Detailed Response Agent (max_tokens=1000):")
    try:
        detailed_agent = Agent(
            name="DetailedAgent",
            instructions="Provide comprehensive, detailed responses.",
            model_settings=ModelSettings(max_tokens=1000)
        )

        print(f"      Configuration: max_tokens=1000")
        print(f"      Use case: Detailed explanations, analysis")
        print(f"      Expected length: ~750 words maximum")

    except Exception as e:
        print(f"      Configuration demo: max_tokens=1000")
        print(f"      ✓ Long responses for detailed content")

    print(f"\n💡 Token Management Best Practices:")
    print(f"   ✓ Set max_tokens based on expected response length")
    print(f"   ✓ Monitor token usage for cost optimization")
    print(f"   ✓ Consider context limit when processing long inputs")
    print(f"   ✓ Use shorter max_tokens for faster responses")


async def demo_advanced_parameters():
    """Demonstrate advanced model parameters."""
    print("\n=== Demo: Advanced Parameters ===")

    print("🔧 Advanced Parameter Configuration:")
    print()

    # Nucleus sampling (top_p)
    print("   🎯 Nucleus Sampling (top_p):")
    print("      • Controls vocabulary diversity during generation")
    print("      • 0.1: Only top 10% probability tokens considered")
    print("      • 0.5: Top 50% probability tokens considered")
    print("      • 1.0: All tokens considered (default)")
    print("      • Often used instead of temperature")
    print()

    # Frequency penalty
    print("   🔄 Frequency Penalty (-2.0 to 2.0):")
    print("      • Reduces repetition of tokens based on frequency")
    print("      • Positive values discourage repetition")
    print("      • Negative values encourage repetition")
    print("      • 0.0: No penalty (default)")
    print()

    # Presence penalty
    print("   📈 Presence Penalty (-2.0 to 2.0):")
    print("      • Reduces repetition based on token presence")
    print("      • Encourages new topics and ideas")
    print("      • Positive values encourage topic diversity")
    print("      • 0.0: No penalty (default)")
    print()

    # Tool choice
    print("   🛠️ Tool Choice Configuration:")
    print("      • 'auto': Model chooses when to use tools (default)")
    print("      • 'required': Model must use a tool")
    print("      • 'none': Model cannot use tools")
    print("      • Specific tool name: Force use of particular tool")
    print()

    print("🧪 Advanced Configuration Examples:")

    # Anti-repetition agent
    print(f"\n   🚫 Anti-Repetition Agent:")
    try:
        anti_repeat_agent = Agent(
            name="AntiRepeatAgent",
            instructions="Provide diverse responses without repetition.",
            model_settings=ModelSettings(
                frequency_penalty=0.5,
                presence_penalty=0.3,
                temperature=0.7
            )
        )

        print(f"      frequency_penalty=0.5 (reduces word repetition)")
        print(f"      presence_penalty=0.3 (encourages topic diversity)")
        print(f"      temperature=0.7 (balanced creativity)")
        print(f"      Use case: Long-form content, varied writing")

    except Exception as e:
        print(f"      Configuration demo: Anti-repetition settings")
        print(f"      ✓ Reduces repetitive content")

    # Focused agent
    print(f"\n   🎯 Focused Agent:")
    try:
        focused_agent = Agent(
            name="FocusedAgent",
            instructions="Stay focused on the main topic.",
            model_settings=ModelSettings(
                top_p=0.3,
                temperature=0.4,
                frequency_penalty=0.0
            )
        )

        print(f"      top_p=0.3 (limited vocabulary diversity)")
        print(f"      temperature=0.4 (moderate creativity)")
        print(f"      frequency_penalty=0.0 (no repetition penalty)")
        print(f"      Use case: Technical documentation, focused analysis")

    except Exception as e:
        print(f"      Configuration demo: Focused response settings")
        print(f"      ✓ Maintains topic focus")

    # Tool-controlled agent
    print(f"\n   🛠️ Tool-Controlled Agent:")
    try:
        tool_agent = Agent(
            name="ToolAgent",
            instructions="Use tools when needed for accurate information.",
            model_settings=ModelSettings(
                tool_choice="auto",
                parallel_tool_calls=True,
                temperature=0.2
            ),
            tools=[function_tool(lambda: "Tool result")(lambda: "Tool result")]
        )

        print(f"      tool_choice='auto' (model decides when to use tools)")
        print(f"      parallel_tool_calls=True (execute tools in parallel)")
        print(f"      temperature=0.2 (consistent tool usage)")
        print(f"      Use case: Research, data retrieval, fact-checking")

    except Exception as e:
        print(f"      Configuration demo: Tool-controlled settings")
        print(f"      ✓ Optimized for tool usage")


async def demo_client_level_configuration():
    """Demonstrate client-level configuration including timeouts."""
    print("\n=== Demo: Client-Level Configuration ===")

    print("⚙️ Client-Level vs ModelSettings Configuration:")
    print("   • ModelSettings: Model behavior parameters")
    print("   • Client-Level: Network, timeout, authentication")
    print("   • Some parameters are handled at client level")
    print()

    print("⏱️ Timeout Configuration (Client-Level):")
    print("   • Handled by AsyncOpenAI client, not ModelSettings")
    print("   • Controls network timeout, not model generation time")
    print("   • Important for production reliability")
    print()

    print("🧪 Client Configuration Examples:")

    # Example 1: Custom timeout client
    print(f"\n   ⚡ Custom Timeout Client:")
    print(f"   ```python")
    print(f"   from openai import AsyncOpenAI")
    print(f"   from agents import set_default_openai_client")
    print(f"   ")
    print(f"   # Create client with custom timeout")
    print(f"   custom_client = AsyncOpenAI(")
    print(f"       api_key='your_key',")
    print(f"       timeout=30.0  # 30 second timeout")
    print(f"   )")
    print(f"   ")
    print(f"   # Set as default for all agents")
    print(f"   set_default_openai_client(custom_client)")
    print(f"   ```")

    # Example 2: Provider-specific client
    print(f"\n   🌐 Provider-Specific Client:")
    print(f"   ```python")
    print(f"   # For OpenAI-compatible providers")
    print(f"   provider_client = AsyncOpenAI(")
    print(f"       base_url='https://api.provider.com/v1',")
    print(f"       api_key='provider_key',")
    print(f"       timeout=60.0")
    print(f"   )")
    print(f"   ")
    print(f"   set_default_openai_client(provider_client)")
    print(f"   set_default_openai_api('chat_completions')")
    print(f"   ```")

    print(f"\n🎯 Configuration Separation:")
    print(f"   ModelSettings Parameters:")
    print(f"   ✓ temperature, top_p, frequency_penalty")
    print(f"   ✓ max_tokens, tool_choice, parallel_tool_calls")
    print(f"   ✓ truncation, reasoning, metadata")
    print(f"   ")
    print(f"   Client-Level Parameters:")
    print(f"   ✓ timeout, base_url, api_key")
    print(f"   ✓ http_client, retries, max_connections")


async def demo_use_case_configurations():
    """Demonstrate configurations for specific use cases."""
    print("\n=== Demo: Use Case Configurations ===")

    print("🎯 Task-Specific Model Configurations:")
    print()

    configurations = {
        "Code Generation": {
            "temperature": 0.1,
            "max_tokens": 1000,
            "tool_choice": "auto",
            "frequency_penalty": 0.0,
            "reasoning": "Low temperature for consistency, tools for documentation"
        },
        "Creative Writing": {
            "temperature": 0.8,
            "max_tokens": 2000,
            "presence_penalty": 0.4,
            "frequency_penalty": 0.3,
            "reasoning": "High temperature for creativity, penalties reduce repetition"
        },
        "Data Extraction": {
            "temperature": 0.0,
            "max_tokens": 100,
            "top_p": 0.1,
            "tool_choice": "none",
            "reasoning": "Deterministic output, short responses, focused vocabulary"
        },
        "Conversational AI": {
            "temperature": 0.7,
            "max_tokens": 300,
            "presence_penalty": 0.2,
            "frequency_penalty": 0.1,
            "reasoning": "Balanced creativity, moderate length, slight variety encouragement"
        },
        "Technical Documentation": {
            "temperature": 0.3,
            "max_tokens": 1500,
            "top_p": 0.5,
            "frequency_penalty": 0.0,
            "reasoning": "Low creativity for accuracy, longer responses, focused vocabulary"
        }
    }

    for use_case, config in configurations.items():
        print(f"   📋 {use_case}:")
        for param, value in config.items():
            if param != "reasoning":
                print(f"      {param}: {value}")
        print(f"      Reasoning: {config['reasoning']}")
        print()

    print("🧪 Configuration Factory Pattern:")
    print("   ```python")
    print("   def get_model_settings(use_case: str) -> ModelSettings:")
    print("       configs = {")
    print("           'code': ModelSettings(temperature=0.1, max_tokens=1000),")
    print("           'creative': ModelSettings(temperature=0.8, max_tokens=2000),")
    print("           'extraction': ModelSettings(temperature=0.0, max_tokens=100)")
    print("       }")
    print("       return configs.get(use_case, ModelSettings())")
    print("   ```")


async def demo_reasoning_models():
    """Demonstrate reasoning model configuration."""
    print("\n=== Demo: Reasoning Models Configuration ===")

    print("🧠 Reasoning Models Overview:")
    print("   • Special configuration for reasoning models (o1, o3)")
    print("   • Uses reasoning parameter in ModelSettings")
    print("   • Different behavior from standard models")
    print("   • Enhanced logical processing capabilities")
    print()

    print("⚙️ Reasoning Configuration:")
    print("   • reasoning parameter controls reasoning behavior")
    print("   • Specific to OpenAI's reasoning models")
    print("   • May affect response time and cost")
    print("   • Enhanced problem-solving capabilities")
    print()

    print("🧪 Reasoning Model Example:")
    print("   ```python")
    print("   from agents import Agent, ModelSettings")
    print("   ")
    print("   reasoning_agent = Agent(")
    print("       name='ReasoningAgent',")
    print("       instructions='Think step by step through complex problems.',")
    print("       model='o1-preview',  # Reasoning model")
    print("       model_settings=ModelSettings(")
    print("           temperature=0.3,")
    print("           # reasoning=ReasoningConfig(...)  # If available")
    print("       )")
    print("   )")
    print("   ```")

    print(f"\n🎯 Reasoning Model Benefits:")
    print(f"   ✓ Enhanced logical reasoning")
    print(f"   ✓ Better problem decomposition")
    print(f"   ✓ Improved mathematical capabilities")
    print(f"   ✓ More accurate complex analysis")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all model configuration demonstrations."""
    print("⚙️ OpenAI Agents SDK - Model Configuration ⚙️")
    print("\nThis module covers ModelSettings and parameter configuration")
    print("for fine-tuning model behavior.\n")

    # Run all demonstrations
    await demo_model_settings_overview()
    await demo_temperature_control()
    await demo_token_management()
    await demo_advanced_parameters()
    await demo_client_level_configuration()
    await demo_use_case_configurations()
    await demo_reasoning_models()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - Model Configuration:")
    print("• ModelSettings enables fine-tuning of model behavior")
    print("• Temperature controls creativity vs consistency (0.0-2.0)")
    print("• max_tokens limits response length, not total context")
    print("• Advanced parameters (top_p, penalties) provide nuanced control")
    print("• Tool choice controls when and how tools are used")
    print("• Client-level configuration handles timeouts and networking")
    print("• Different use cases benefit from different configurations")
    print("• Reasoning models have special configuration options")

    print(f"\n⚙️ Configuration Summary:")
    print(f"   🌡️ Temperature: Creativity control (0.0 = consistent, 2.0 = creative)")
    print(f"   🎫 max_tokens: Response length limit")
    print(f"   🎯 top_p: Vocabulary focus control")
    print(f"   🛠️ tool_choice: Tool usage control")
    print(f"   ⏱️ timeout: Client-level timeout configuration")

    print(f"\n🎯 Next Steps:")
    print(f"• Learn model mixing in 04_model_mixing.py")
    print(f"• Understand provider integration in 05_provider_integration.py")


if __name__ == "__main__":
    asyncio.run(main())
