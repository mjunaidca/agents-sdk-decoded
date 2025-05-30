"""
05_provider_integration.py

This module covers provider integration in the OpenAI Agents SDK.
Focus: LiteLLM integration, custom providers, and multi-provider workflows.

Learning Objectives:
- Understand provider integration patterns
- Learn LiteLLM setup for 100+ models
- Master custom provider configuration
- Implement multi-provider workflows

Key Concepts:
- LiteLLM universal interface for multiple providers
- Provider-specific configuration patterns
- Custom provider implementation
- API compatibility and model mapping
- Provider switching and fallback strategies

Based on: https://openai.github.io/openai-agents-python/models/
"""

import asyncio
from agents import Agent, Runner, ModelSettings, set_default_openai_client, set_default_openai_api
from openai import AsyncOpenAI

# ================== PROVIDER INTEGRATION FUNDAMENTALS ==================


async def demo_provider_overview():
    """Demonstrate provider integration overview."""
    print("=== Demo: Provider Integration Overview ===")

    print("🌐 Supported Provider Ecosystem:")
    print("   • OpenAI: GPT-4o, GPT-4o-mini, GPT-3.5-turbo")
    print("   • Anthropic: Claude-3.5-sonnet, Claude-3-haiku")
    print("   • Google: Gemini-2.5-flash, Gemini-1.5-pro")
    print("   • Meta: LLaMA models via various providers")
    print("   • Mistral: Mistral-large, Mistral-7B")
    print("   • 100+ models through LiteLLM integration")
    print()

    print("🔧 Integration Methods:")
    methods = {
        "Direct OpenAI API": "Native gpt-4o, gpt-3.5-turbo support",
        "LiteLLM Extension": "Universal interface for 100+ models",
        "Custom Provider": "Custom AsyncOpenAI client implementation",
        "Provider Switching": "Dynamic provider selection"
    }

    for method, description in methods.items():
        print(f"   • {method:18}: {description}")

    print(f"\n💡 Provider Selection Criteria:")
    criteria = {
        "Capability": "Reasoning, coding, multimodal, context length",
        "Performance": "Latency, throughput, reliability",
        "Cost": "Price per token, volume discounts",
        "Features": "Tool use, structured output, safety",
        "Availability": "Geographic regions, API limits"
    }

    for criterion, considerations in criteria.items():
        print(f"   • {criterion:12}: {considerations}")

    print(f"\n🎯 Integration Strategy:")
    print(f"   1. Start with OpenAI for proven performance")
    print(f"   2. Add LiteLLM for provider diversity")
    print(f"   3. Implement custom providers for specific needs")
    print(f"   4. Use provider mixing for optimization")


async def demo_litellm_integration():
    """Demonstrate LiteLLM integration for multiple providers."""
    print("\n=== Demo: LiteLLM Integration ===")

    print("⚡ LiteLLM Universal Interface:")
    print("   • Single API for 100+ models across providers")
    print("   • Consistent model interface and formatting")
    print("   • Automatic request/response translation")
    print("   • Provider failover and load balancing")
    print("   • Cost tracking and optimization")
    print()

    print("🏗️ LiteLLM Setup Requirements:")
    print("   ```bash")
    print("   # Install LiteLLM extension")
    print("   pip install 'agents[litellm]'")
    print("   ")
    print("   # Or install LiteLLM directly")
    print("   pip install litellm")
    print("   ```")

    print(f"\n🌐 Provider Model Examples:")
    provider_models = {
        "Anthropic": [
            "litellm/anthropic/claude-3-5-sonnet-20240620",
            "litellm/anthropic/claude-3-haiku-20240307"
        ],
        "Google": [
            "litellm/gemini/gemini-2.5-flash-preview",
            "litellm/gemini/gemini-1.5-pro"
        ],
        "Mistral": [
            "litellm/mistral/mistral-large-latest",
            "litellm/mistral/mistral-small-latest"
        ],
        "Cohere": [
            "litellm/cohere/command-r-plus",
            "litellm/cohere/command-r"
        ]
    }

    for provider, models in provider_models.items():
        print(f"   {provider}:")
        for model in models:
            print(f"      • {model}")
        print()

    print("🧪 LiteLLM Agent Examples:")

    # Anthropic Claude agent
    print(f"\n   🧠 Anthropic Claude Agent:")
    try:
        claude_agent = Agent(
            name="ClaudeAgent",
            instructions="Provide thoughtful, detailed analysis with strong reasoning.",
            model="litellm/anthropic/claude-3-5-sonnet-20240620",
            model_settings=ModelSettings(
                temperature=0.4,
                max_tokens=1500
            )
        )

        print(f"      Model: claude-3-5-sonnet (reasoning specialist)")
        print(f"      Use case: Complex analysis, code review")
        print(f"      Strengths: Large context, safety, reasoning")

    except Exception as e:
        print(f"      Configuration: Claude agent example")
        print(f"      ✓ Strong reasoning and large context window")

    # Google Gemini agent
    print(f"\n   ⚡ Google Gemini Agent:")
    try:
        gemini_agent = Agent(
            name="GeminiAgent",
            instructions="Provide fast, efficient responses with multimodal capabilities.",
            model="litellm/gemini/gemini-2.5-flash-preview",
            model_settings=ModelSettings(
                temperature=0.3,
                max_tokens=800
            )
        )

        print(f"      Model: gemini-2.5-flash (speed optimized)")
        print(f"      Use case: Real-time responses, multimodal")
        print(f"      Strengths: Speed, cost-effectiveness")

    except Exception as e:
        print(f"      Configuration: Gemini agent example")
        print(f"      ✓ Fast responses and multimodal support")

    print(f"\n💰 Cost Comparison (Approximate):")
    cost_comparison = {
        "gpt-4o": "$15/$3 per 1M tokens (input/output)",
        "claude-3-5-sonnet": "$3/$15 per 1M tokens",
        "gemini-1.5-pro": "$1.25/$5 per 1M tokens",
        "mistral-large": "$4/$12 per 1M tokens"
    }

    for model, cost in cost_comparison.items():
        print(f"   • {model:18}: {cost}")


async def demo_custom_provider_setup():
    """Demonstrate custom provider configuration."""
    print("\n=== Demo: Custom Provider Setup ===")

    print("🔧 Custom Provider Configuration:")
    print("   • Direct AsyncOpenAI client configuration")
    print("   • OpenAI-compatible API endpoints")
    print("   • Custom authentication and headers")
    print("   • Provider-specific optimizations")
    print()

    print("🏗️ Custom Provider Implementation:")
    print("   ```python")
    print("   from openai import AsyncOpenAI")
    print("   from agents import set_default_openai_client, set_default_openai_api")
    print("   ")
    print("   # Custom provider client")
    print("   custom_client = AsyncOpenAI(")
    print("       base_url='https://api.custom-provider.com/v1',")
    print("       api_key='your_custom_api_key',")
    print("       timeout=30.0,")
    print("       max_retries=3")
    print("   )")
    print("   ")
    print("   # Set as global default")
    print("   set_default_openai_client(custom_client)")
    print("   set_default_openai_api('chat_completions')")
    print("   ```")

    print(f"\n🌐 Provider-Specific Examples:")

    # Azure OpenAI
    print(f"\n   ☁️ Azure OpenAI Configuration:")
    print(f"   ```python")
    print(f"   azure_client = AsyncOpenAI(")
    print(f"       base_url='https://your-resource.openai.azure.com',")
    print(f"       api_key='your_azure_key',")
    print(f"       api_version='2024-02-15-preview',")
    print(f"       default_headers={{'api-key': 'your_azure_key'}}")
    print(f"   )")
    print(f"   ```")

    # Together.ai
    print(f"\n   🤝 Together.ai Configuration:")
    print(f"   ```python")
    print(f"   together_client = AsyncOpenAI(")
    print(f"       base_url='https://api.together.xyz/v1',")
    print(f"       api_key='your_together_key'")
    print(f"   )")
    print(f"   ```")

    # Hugging Face
    print(f"\n   🤗 Hugging Face Configuration:")
    print(f"   ```python")
    print(f"   hf_client = AsyncOpenAI(")
    print(f"       base_url='https://api-inference.huggingface.co/v1',")
    print(f"       api_key='your_hf_token'")
    print(f"   )")
    print(f"   ```")

    print(f"\n⚙️ Provider Configuration Patterns:")
    patterns = {
        "Global Default": "set_default_openai_client() for all agents",
        "Per-Agent": "Pass client directly to Agent constructor",
        "Context Manager": "Temporary provider switching for specific operations",
        "Environment-Based": "Provider selection based on deployment environment"
    }

    for pattern, description in patterns.items():
        print(f"   • {pattern:15}: {description}")


async def demo_multi_provider_workflow():
    """Demonstrate multi-provider workflow patterns."""
    print("\n=== Demo: Multi-Provider Workflow ===")

    print("🔄 Multi-Provider Workflow Patterns:")
    print("   • Provider-specific agent specialization")
    print("   • Automatic failover between providers")
    print("   • Cost-optimized provider selection")
    print("   • Geographic provider distribution")
    print()

    print("🏗️ Workflow Architecture:")
    print("   ```python")
    print("   class MultiProviderWorkflow:")
    print("       def __init__(self):")
    print("           # Initialize provider clients")
    print("           self.openai_client = AsyncOpenAI(api_key='...')")
    print("           self.anthropic_client = AsyncOpenAI(")
    print("               base_url='https://api.anthropic.com/v1')")
    print("           ")
    print("           # Create specialized agents")
    print("           self.speed_agent = Agent(")
    print("               model='gpt-3.5-turbo',")
    print("               client=self.openai_client")
    print("           )")
    print("           self.reasoning_agent = Agent(")
    print("               model='claude-3-5-sonnet',")
    print("               client=self.anthropic_client")
    print("           )")
    print("   ```")

    print(f"\n🎯 Provider Selection Logic:")
    print(f"   ```python")
    print(f"   async def select_provider_for_task(task_type, urgency):")
    print(f"       if task_type == 'reasoning' and urgency == 'low':")
    print(f"           return 'anthropic'  # Best reasoning")
    print(f"       elif urgency == 'high':")
    print(f"           return 'gemini'     # Fastest response")
    print(f"       else:")
    print(f"           return 'openai'     # Balanced performance")
    print(f"   ```")

    print(f"\n🛡️ Provider Failover Strategy:")
    print(f"   ```python")
    print(f"   async def robust_completion(request, max_retries=3):")
    print(f"       providers = ['openai', 'anthropic', 'gemini']")
    print(f"       ")
    print(f"       for provider in providers:")
    print(f"           try:")
    print(f"               agent = get_agent_for_provider(provider)")
    print(f"               return await Runner.run(agent, request)")
    print(f"           except Exception as e:")
    print(f"               log_provider_error(provider, e)")
    print(f"               continue")
    print(f"       ")
    print(f"       raise Exception('All providers failed')")
    print(f"   ```")

    print(f"\n💡 Best Practice Patterns:")
    best_practices = [
        "Use OpenAI for general tasks with proven reliability",
        "Use Anthropic for complex reasoning and safety-critical tasks",
        "Use Google Gemini for speed-critical and cost-sensitive tasks",
        "Implement graceful degradation between providers",
        "Monitor provider performance and costs continuously"
    ]

    for i, practice in enumerate(best_practices, 1):
        print(f"   {i}. {practice}")


async def demo_provider_specific_features():
    """Demonstrate provider-specific features and capabilities."""
    print("\n=== Demo: Provider-Specific Features ===")

    print("🎯 Provider Capability Matrix:")
    capabilities = {
        "OpenAI": {
            "Strengths": ["Tool use", "Structured outputs", "Function calling", "JSON mode"],
            "Models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
            "Limits": ["8K-128K context", "Rate limits by tier"],
            "Use Cases": ["General AI", "Code generation", "Tool integration"]
        },
        "Anthropic": {
            "Strengths": ["Reasoning", "Safety", "Large context", "Code analysis"],
            "Models": ["claude-3-5-sonnet", "claude-3-haiku"],
            "Limits": ["200K context", "Rate limits"],
            "Use Cases": ["Complex analysis", "Long documents", "Safety-critical"]
        },
        "Google": {
            "Strengths": ["Speed", "Multimodal", "Cost", "Real-time"],
            "Models": ["gemini-2.5-flash", "gemini-1.5-pro"],
            "Limits": ["32K-1M context", "Regional availability"],
            "Use Cases": ["Real-time chat", "Multimodal", "Cost optimization"]
        }
    }

    for provider, details in capabilities.items():
        print(f"\n   {provider}:")
        for category, items in details.items():
            print(f"      {category}:")
            if isinstance(items, list):
                for item in items:
                    print(f"         • {item}")
            else:
                print(f"         • {items}")

    print(f"\n🧪 Feature-Specific Agent Examples:")

    # OpenAI with tools
    print(f"\n   🛠️ OpenAI Tool-Using Agent:")
    print(f"   ```python")
    print(f"   @function_tool")
    print(f"   def get_weather(location: str) -> str:")
    print(f"       return f'Weather in {{location}}: Sunny, 75°F'")
    print(f"   ")
    print(f"   tool_agent = Agent(")
    print(f"       model='gpt-4o',")
    print(f"       tools=[get_weather],")
    print(f"       model_settings=ModelSettings(")
    print(f"           tool_choice='auto',")
    print(f"           parallel_tool_calls=True")
    print(f"       )")
    print(f"   )")
    print(f"   ```")

    # Anthropic for reasoning
    print(f"\n   🧠 Anthropic Reasoning Agent:")
    print(f"   ```python")
    print(f"   reasoning_agent = Agent(")
    print(f"       model='litellm/anthropic/claude-3-5-sonnet-20240620',")
    print(f"       instructions='Think step by step through complex problems.',")
    print(f"       model_settings=ModelSettings(")
    print(f"           temperature=0.3,")
    print(f"           max_tokens=2000")
    print(f"       )")
    print(f"   )")
    print(f"   ```")

    # Gemini for speed
    print(f"\n   ⚡ Gemini Speed Agent:")
    print(f"   ```python")
    print(f"   speed_agent = Agent(")
    print(f"       model='litellm/gemini/gemini-2.5-flash-preview',")
    print(f"       instructions='Provide quick, concise responses.',")
    print(f"       model_settings=ModelSettings(")
    print(f"           temperature=0.4,")
    print(f"           max_tokens=500")
    print(f"       )")
    print(f"   )")
    print(f"   ```")


async def demo_environment_configuration():
    """Demonstrate environment-based provider configuration."""
    print("\n=== Demo: Environment Configuration ===")

    print("🌍 Environment-Based Provider Selection:")
    print("   • Development: Free tiers and local models")
    print("   • Staging: Production providers with limits")
    print("   • Production: Premium providers with full features")
    print("   • Edge: Regional providers for low latency")
    print()

    print("⚙️ Configuration Management:")
    print("   ```python")
    print("   import os")
    print("   from agents import Agent, set_default_openai_client")
    print("   ")
    print("   def setup_environment_provider():")
    print("       env = os.getenv('ENVIRONMENT', 'development')")
    print("       ")
    print("       if env == 'development':")
    print("           # Use free models for development")
    print("           client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))")
    print("           default_model = 'gpt-3.5-turbo'")
    print("       elif env == 'staging':")
    print("           # Use balanced performance for staging")
    print("           client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))")
    print("           default_model = 'gpt-4o-mini'")
    print("       else:  # production")
    print("           # Use premium models for production")
    print("           client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))")
    print("           default_model = 'gpt-4o'")
    print("       ")
    print("       set_default_openai_client(client)")
    print("       return default_model")
    print("   ```")

    print(f"\n🔧 Environment Variables Pattern:")
    env_vars = {
        "OPENAI_API_KEY": "OpenAI API authentication",
        "ANTHROPIC_API_KEY": "Anthropic Claude authentication",
        "GOOGLE_API_KEY": "Google Gemini authentication",
        "DEFAULT_MODEL": "Default model for environment",
        "PROVIDER_TIMEOUT": "Request timeout configuration",
        "RATE_LIMIT_STRATEGY": "Rate limiting approach"
    }

    for var, description in env_vars.items():
        print(f"   • {var:20}: {description}")

    print(f"\n🎯 Deployment Patterns:")
    deployment_patterns = {
        "Single Provider": "One provider, multiple models",
        "Multi-Provider": "Different providers for different services",
        "Hybrid Cloud": "Cloud providers + self-hosted models",
        "Geographic": "Regional providers for global deployment"
    }

    for pattern, description in deployment_patterns.items():
        print(f"   • {pattern:15}: {description}")

    print(f"\n💡 Configuration Best Practices:")
    config_practices = [
        "Use environment variables for API keys and configuration",
        "Implement provider health checks and monitoring",
        "Cache provider responses for improved performance",
        "Use feature flags for provider switching",
        "Monitor costs across all providers"
    ]

    for i, practice in enumerate(config_practices, 1):
        print(f"   {i}. {practice}")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all provider integration demonstrations."""
    print("🌐 OpenAI Agents SDK - Provider Integration 🌐")
    print("\nThis module covers provider integration and multi-provider workflows.")
    print("Focus: LiteLLM, custom providers, and provider optimization\n")

    # Run all demonstrations
    await demo_provider_overview()
    await demo_litellm_integration()
    await demo_custom_provider_setup()
    await demo_multi_provider_workflow()
    await demo_provider_specific_features()
    await demo_environment_configuration()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - Provider Integration:")
    print("• LiteLLM enables access to 100+ models through unified interface")
    print("• Custom providers support OpenAI-compatible APIs")
    print("• Multi-provider workflows optimize cost and performance")
    print("• Provider-specific features require different configurations")
    print("• Environment-based setup enables deployment flexibility")
    print("• Monitoring and failover ensure production reliability")

    print(f"\n🌐 Provider Integration Summary:")
    print(f"   ⚡ LiteLLM: Universal interface for multiple providers")
    print(f"   🔧 Custom: Direct AsyncOpenAI client configuration")
    print(f"   🔄 Multi-Provider: Specialized agents for different tasks")
    print(f"   🎯 Features: Provider-specific capabilities and limits")
    print(f"   🌍 Environment: Deployment-specific configuration")

    print(f"\n🎯 Next Steps:")
    print(f"• Complete the models module with troubleshooting")
    print(f"• Practice with real provider configurations")
    print(f"• Implement monitoring and cost optimization")


if __name__ == "__main__":
    asyncio.run(main())
