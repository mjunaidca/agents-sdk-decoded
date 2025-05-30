"""
02_litellm_integration.py

This module covers LiteLLM integration in the OpenAI Agents SDK.
Focus: Using 100+ models through the LiteLLM library integration.

Learning Objectives:
- Understand LiteLLM integration setup and installation
- Learn how to use 100+ models with litellm/ prefix
- Master configuration patterns for different providers
- Understand beta limitations and considerations

Key Concepts:
- LiteLLM enables universal model access
- Uses "litellm/" prefix for model names
- Requires separate dependency installation
- Supports major providers (Anthropic, Google, etc.)

Based on: https://openai.github.io/openai-agents-python/models/litellm/
"""

import asyncio
import os
from agents import Agent, Runner, function_tool

# Note: LiteLLM imports would be here in a real implementation
# from agents.extensions.models.litellm_model import LitellmModel

# ================== LITELLM INTEGRATION FUNDAMENTALS ==================


async def demo_litellm_overview():
    """Demonstrate LiteLLM integration overview and capabilities."""
    print("=== Demo: LiteLLM Integration Overview ===")

    print("🌐 LiteLLM Integration Overview:")
    print("   • Access 100+ models via single interface")
    print("   • Universal model API across providers")
    print("   • Consistent usage patterns")
    print("   • Beta integration (actively evolving)")
    print("   • Extends SDK beyond OpenAI models")
    print()

    print("🏢 Supported Providers (Examples):")
    providers = {
        "OpenAI": ["gpt-4o", "gpt-3.5-turbo", "o1-preview"],
        "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-haiku"],
        "Google": ["gemini-2.5-flash-preview", "gemini-pro"],
        "Cohere": ["command-r-plus", "command-light"],
        "Meta": ["llama-2-70b-chat", "llama-3-8b"],
        "Mistral": ["mistral-large", "mistral-7b"],
        "Azure OpenAI": ["azure/gpt-4", "azure/gpt-35-turbo"],
        "AWS Bedrock": ["bedrock/claude-3", "bedrock/llama2"]
    }

    for provider, models in providers.items():
        print(f"   {provider}:")
        for model in models[:2]:  # Show first 2 models
            print(f"      • litellm/{model}")
        if len(models) > 2:
            print(f"      • ... and {len(models) - 2} more")
        print()

    print("🎯 Key Benefits:")
    print("   ✓ Model diversity and choice")
    print("   ✓ Provider-agnostic code")
    print("   ✓ Easy model switching")
    print("   ✓ Cost optimization opportunities")
    print("   ✓ Reduced vendor lock-in")


async def demo_installation_setup():
    """Demonstrate LiteLLM installation and setup requirements."""
    print("\n=== Demo: Installation and Setup ===")

    print("📦 Installation Requirements:")
    print("   LiteLLM is an optional dependency group")
    print("   Must be explicitly installed for usage")
    print()

    print("💻 Installation Command:")
    print('   pip install "openai-agents[litellm]"')
    print()

    print("📋 What This Installs:")
    print("   • Base OpenAI Agents SDK")
    print("   • LiteLLM library and dependencies")
    print("   • LiteLLM-specific model classes")
    print("   • Required provider adapters")
    print()

    print("🔍 Installation Verification:")
    try:
        # Simulate checking if LiteLLM is available
        print("   Checking LiteLLM availability...")

        # In real implementation, this would be:
        # from agents.extensions.models.litellm_model import LitellmModel
        # print("   ✅ LiteLLM integration available")

        print("   ⚠️  LiteLLM not installed (demo mode)")
        print("   To install: pip install 'openai-agents[litellm]'")

    except ImportError as e:
        print(f"   ❌ LiteLLM not available: {e}")
        print("   Run installation command to enable")

    print(f"\n🛠️ Setup Steps:")
    setup_steps = [
        "Install LiteLLM dependency group",
        "Import LitellmModel from extensions",
        "Configure API keys for desired providers",
        "Use litellm/ prefix for model names",
        "Test with simple agent configuration"
    ]

    for i, step in enumerate(setup_steps, 1):
        print(f"   {i}. {step}")


async def demo_basic_usage_patterns():
    """Demonstrate basic LiteLLM usage patterns."""
    print("\n=== Demo: Basic Usage Patterns ===")

    print("🎯 Basic LiteLLM Usage Pattern:")
    print("   Use 'litellm/' prefix + provider/model format")
    print()

    print("📝 Code Pattern Examples:")

    # Example 1: Claude
    print("\n   Example 1 - Anthropic Claude:")
    print("   ```python")
    print("   claude_agent = Agent(")
    print("       name='ClaudeAgent',")
    print("       model='litellm/anthropic/claude-3-5-sonnet-20240620',")
    print("       instructions='You are a helpful assistant.'")
    print("   )")
    print("   ```")

    # Example 2: Gemini
    print("\n   Example 2 - Google Gemini:")
    print("   ```python")
    print("   gemini_agent = Agent(")
    print("       name='GeminiAgent',")
    print("       model='litellm/gemini/gemini-2.5-flash-preview',")
    print("       instructions='You provide fast responses.'")
    print("   )")
    print("   ```")

    # Example 3: Explicit model class
    print("\n   Example 3 - Explicit LitellmModel:")
    print("   ```python")
    print("   explicit_agent = Agent(")
    print("       name='ExplicitAgent',")
    print("       model=LitellmModel(")
    print("           model='anthropic/claude-3-5-sonnet-20240620',")
    print("           api_key='your_anthropic_key'")
    print("       )")
    print("   )")
    print("   ```")

    print(f"\n🔑 API Key Configuration:")
    print(f"   Environment variables (recommended):")
    print(f"   • ANTHROPIC_API_KEY='your_anthropic_key'")
    print(f"   • GOOGLE_API_KEY='your_google_key'")
    print(f"   • COHERE_API_KEY='your_cohere_key'")
    print(f"   Programmatic (for demos/testing):")
    print(f"   • LitellmModel(api_key='key') parameter")


async def demo_provider_specific_configuration():
    """Demonstrate configuration for specific providers."""
    print("\n=== Demo: Provider-Specific Configuration ===")

    print("🏢 Provider Configuration Examples:")
    print()

    # Anthropic Configuration
    print("   🤖 Anthropic Claude:")
    print("      Model Format: litellm/anthropic/claude-3-5-sonnet-20240620")
    print("      API Key: ANTHROPIC_API_KEY environment variable")
    print("      Features: Large context, reasoning, coding")
    print("      Use Case: Complex reasoning and analysis")
    print()

    # Google Configuration
    print("   🔍 Google Gemini:")
    print("      Model Format: litellm/gemini/gemini-2.5-flash-preview")
    print("      API Key: GOOGLE_API_KEY environment variable")
    print("      Features: Multimodal, fast responses")
    print("      Use Case: Quick queries and multimodal tasks")
    print()

    # Cohere Configuration
    print("   💬 Cohere:")
    print("      Model Format: litellm/cohere/command-r-plus")
    print("      API Key: COHERE_API_KEY environment variable")
    print("      Features: RAG optimization, enterprise focus")
    print("      Use Case: Search and retrieval applications")
    print()

    # Azure OpenAI Configuration
    print("   ☁️  Azure OpenAI:")
    print("      Model Format: litellm/azure/your-deployment-name")
    print("      Environment Variables: AZURE_API_KEY, AZURE_API_BASE")
    print("      Features: Enterprise security, compliance")
    print("      Use Case: Enterprise OpenAI deployments")

    print(f"\n⚙️ Configuration Best Practices:")
    print(f"   ✓ Use environment variables for API keys")
    print(f"   ✓ Test with small requests first")
    print(f"   ✓ Check provider-specific rate limits")
    print(f"   ✓ Understand cost differences between providers")
    print(f"   ✓ Monitor usage across different providers")


async def demo_model_switching():
    """Demonstrate switching between different models."""
    print("\n=== Demo: Model Switching Capabilities ===")

    print("🔄 Model Switching Benefits:")
    print("   • Easy A/B testing between providers")
    print("   • Cost optimization by use case")
    print("   • Fallback strategies for availability")
    print("   • Feature-specific model selection")
    print()

    @function_tool
    def analyze_sentiment(text: str) -> str:
        """Analyze sentiment of text (demo function)."""
        # Demo implementation
        if "great" in text.lower() or "excellent" in text.lower():
            return "Positive sentiment detected"
        elif "bad" in text.lower() or "terrible" in text.lower():
            return "Negative sentiment detected"
        else:
            return "Neutral sentiment detected"

    print("🧪 Model Switching Example:")
    print("   Different models for different tasks:")
    print()

    # Fast model for simple tasks
    print("   📈 Fast Model (Simple Tasks):")
    print("   ```python")
    print("   fast_agent = Agent(")
    print("       name='FastAgent',")
    print("       model='litellm/gemini/gemini-2.5-flash-preview',")
    print("       instructions='Provide quick, concise responses.',")
    print("       tools=[analyze_sentiment]")
    print("   )")
    print("   # Use for: Quick queries, simple analysis")
    print("   ```")
    print()

    # Advanced model for complex tasks
    print("   🧠 Advanced Model (Complex Tasks):")
    print("   ```python")
    print("   advanced_agent = Agent(")
    print("       name='AdvancedAgent',")
    print("       model='litellm/anthropic/claude-3-5-sonnet-20240620',")
    print("       instructions='Provide detailed, nuanced analysis.',")
    print("       tools=[analyze_sentiment]")
    print("   )")
    print("   # Use for: Complex reasoning, detailed analysis")
    print("   ```")

    print(f"\n🎯 Switching Strategies:")
    switching_strategies = {
        "Cost-Based": "Use cheaper models for simple tasks, expensive for complex",
        "Speed-Based": "Use fast models for real-time, slower for batch",
        "Feature-Based": "Use specialized models for specific capabilities",
        "Quality-Based": "Use best models for critical tasks, good enough for others",
        "Availability-Based": "Switch models based on uptime and rate limits"
    }

    for strategy, description in switching_strategies.items():
        print(f"   • {strategy}: {description}")


async def demo_error_handling():
    """Demonstrate error handling patterns for LiteLLM."""
    print("\n=== Demo: Error Handling Patterns ===")

    print("⚠️ Common LiteLLM Errors and Solutions:")
    print()

    error_patterns = {
        "Import Error": {
            "error": "ModuleNotFoundError: No module named 'litellm'",
            "solution": "Install: pip install 'openai-agents[litellm]'",
            "prevention": "Include litellm in requirements.txt"
        },
        "API Key Error": {
            "error": "Authentication failed: Invalid API key",
            "solution": "Set correct environment variable for provider",
            "prevention": "Use environment variable validation"
        },
        "Model Not Found": {
            "error": "Model 'provider/model' not found",
            "solution": "Check LiteLLM provider docs for correct model names",
            "prevention": "Validate model names against provider docs"
        },
        "Rate Limit Error": {
            "error": "Rate limit exceeded for provider",
            "solution": "Implement exponential backoff and retry logic",
            "prevention": "Monitor usage and implement rate limiting"
        },
        "Provider Unavailable": {
            "error": "Provider service temporarily unavailable",
            "solution": "Implement fallback to alternative provider",
            "prevention": "Use multiple providers for redundancy"
        }
    }

    for error_type, details in error_patterns.items():
        print(f"   🚨 {error_type}:")
        print(f"      Error: {details['error']}")
        print(f"      Solution: {details['solution']}")
        print(f"      Prevention: {details['prevention']}")
        print()

    print("🛡️ Robust Error Handling Pattern:")
    print("   ```python")
    print("   try:")
    print("       # Primary model")
    print("       agent = Agent(model='litellm/anthropic/claude-3-5-sonnet')")
    print("       result = await Runner.run(agent, message)")
    print("   except Exception as e:")
    print("       # Fallback model")
    print("       fallback_agent = Agent(model='litellm/openai/gpt-4o')")
    print("       result = await Runner.run(fallback_agent, message)")
    print("   ```")


async def demo_beta_considerations():
    """Demonstrate beta limitations and considerations."""
    print("\n=== Demo: Beta Limitations and Considerations ===")

    print("🧪 Beta Integration Status:")
    print("   • LiteLLM integration is currently in beta")
    print("   • Actively evolving with new features")
    print("   • Some providers may have issues")
    print("   • Breaking changes possible in updates")
    print("   • Community feedback drives improvements")
    print()

    print("⚠️ Known Beta Limitations:")
    limitations = [
        "Some smaller model providers may not work reliably",
        "Feature parity may vary between providers",
        "Error messages may be inconsistent across providers",
        "Some advanced features may not be supported",
        "Performance characteristics may vary"
    ]

    for i, limitation in enumerate(limitations, 1):
        print(f"   {i}. {limitation}")

    print(f"\n🎯 Beta Best Practices:")
    best_practices = [
        "Test thoroughly with your specific providers",
        "Have fallback strategies for critical applications",
        "Monitor for SDK updates and breaking changes",
        "Report issues via GitHub for community benefit",
        "Start with major providers (Anthropic, Google) for reliability"
    ]

    for i, practice in enumerate(best_practices, 1):
        print(f"   {i}. {practice}")

    print(f"\n📈 Production Readiness Checklist:")
    checklist = [
        "✓ Test all planned model providers",
        "✓ Implement comprehensive error handling",
        "✓ Set up monitoring for model usage",
        "✓ Plan for provider rate limits",
        "✓ Create fallback model strategies",
        "✓ Monitor LiteLLM updates and changelogs"
    ]

    for item in checklist:
        print(f"   {item}")

    print(f"\n🔮 Future of LiteLLM Integration:")
    print(f"   • Moving toward stable release")
    print(f"   • Expanding provider support")
    print(f"   • Improving error handling")
    print(f"   • Enhanced feature parity")
    print(f"   • Better performance optimization")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all LiteLLM integration demonstrations."""
    print("🌐 OpenAI Agents SDK - LiteLLM Integration 🌐")
    print("\nThis module covers using 100+ models through LiteLLM integration.")
    print("Focus: Universal model access via litellm/ prefix\n")

    # Run all demonstrations
    await demo_litellm_overview()
    await demo_installation_setup()
    await demo_basic_usage_patterns()
    await demo_provider_specific_configuration()
    await demo_model_switching()
    await demo_error_handling()
    await demo_beta_considerations()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - LiteLLM Integration:")
    print("• LiteLLM enables access to 100+ models via single interface")
    print("• Use 'litellm/' prefix with provider/model format")
    print("• Requires separate installation of litellm dependency group")
    print("• Beta status requires careful testing and error handling")
    print("• Enables model diversity and provider flexibility")

    print(f"\n🌐 LiteLLM Summary:")
    print(f"   📦 Installation: pip install 'openai-agents[litellm]'")
    print(f"   🎯 Usage: model='litellm/provider/model-name'")
    print(f"   🔑 Config: Environment variables for API keys")
    print(f"   🧪 Status: Beta (test thoroughly)")

    print(f"\n🎯 Next Steps:")
    print(f"• Learn model configuration in 03_model_configuration.py")
    print(f"• Understand model mixing in 04_model_mixing.py")


if __name__ == "__main__":
    asyncio.run(main())
