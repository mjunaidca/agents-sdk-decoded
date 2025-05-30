"""
01_default_models.py

This module covers the default OpenAI model types in the OpenAI Agents SDK.
Focus: Understanding ResponsesModel vs ChatCompletionsModel and when to use each.

Learning Objectives:
- Understand the two OpenAI model types available
- Learn when to use ResponsesModel (recommended) vs ChatCompletionsModel
- See practical differences in feature support
- Understand the transition from Chat Completions to Responses API

Key Concepts:
- OpenAIResponsesModel: Uses new Responses API (recommended)
- OpenAIChatCompletionsModel: Uses traditional Chat Completions API
- Feature differences and capabilities
- Migration patterns and best practices

Based on: https://openai.github.io/openai-agents-python/models/
"""

import asyncio
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# ================== DEFAULT MODELS FUNDAMENTALS ==================


async def demo_responses_model():
    """Demonstrate the recommended OpenAIResponsesModel."""
    print("=== Demo: OpenAI Responses Model (Recommended) ===")

    print("🎯 OpenAIResponsesModel Overview:")
    print("   • Uses the new OpenAI Responses API")
    print("   • Recommended by OpenAI for new applications")
    print("   • Enhanced features and capabilities")
    print("   • Better structured outputs support")
    print("   • Improved function calling")
    print()

    print("✨ Key Features of Responses API:")
    print("   ✓ Advanced structured outputs")
    print("   ✓ Enhanced function calling")
    print("   ✓ Better response formatting")
    print("   ✓ Improved context handling")
    print("   ✓ Future-proof API design")
    print()

    try:
        # Create agent using default (Responses) model
        responses_agent = Agent(
            name="ResponsesAgent",
            instructions="You demonstrate the Responses API model. Respond clearly and concisely."
        )

        print("🤖 Creating agent with default OpenAIResponsesModel...")
        print("   • Default model type: OpenAIResponsesModel")
        print("   • Uses: Responses API endpoint")
        print("   • Features: All latest capabilities enabled")

        # Note: This would use the Responses API if API key is available
        print(f"\n📊 Agent Configuration:")
        print(f"   Model Type: {type(responses_agent.model).__name__}")
        print(f"   API Endpoint: Responses API")
        print(f"   Capabilities: Enhanced structured outputs, function calling")

        print(f"\n💡 When to Use ResponsesModel:")
        print(f"   ✓ New applications and projects")
        print(f"   ✓ When you need structured outputs")
        print(f"   ✓ Advanced function calling scenarios")
        print(f"   ✓ Future-proofing your application")

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print(f"   This is expected without proper API setup")


async def demo_chat_completions_model():
    """Demonstrate the traditional OpenAIChatCompletionsModel."""
    print("\n=== Demo: OpenAI Chat Completions Model ===")

    print("🔄 OpenAIChatCompletionsModel Overview:")
    print("   • Uses traditional Chat Completions API")
    print("   • Widely supported across LLM providers")
    print("   • Stable and well-established")
    print("   • Maximum compatibility")
    print("   • Legacy applications support")
    print()

    print("🛠️ Key Characteristics:")
    print("   ✓ Universal provider compatibility")
    print("   ✓ Stable API interface")
    print("   ✓ Proven reliability")
    print("   ✓ Extensive ecosystem support")
    print("   ✓ Backward compatibility")
    print()

    try:
        # Create agent explicitly using Chat Completions model
        chat_completions_agent = Agent(
            name="ChatCompletionsAgent",
            instructions="You demonstrate the Chat Completions API model.",
            model=OpenAIChatCompletionsModel(
                model="gpt-4o",
                openai_client=AsyncOpenAI()
            )
        )

        print("🤖 Creating agent with explicit OpenAIChatCompletionsModel...")
        print("   • Model type: OpenAIChatCompletionsModel")
        print("   • Uses: Chat Completions API endpoint")
        print("   • Features: Traditional capabilities")

        print(f"\n📊 Agent Configuration:")
        print(f"   Model Type: {type(chat_completions_agent.model).__name__}")
        print(f"   API Endpoint: Chat Completions API")
        print(f"   Compatibility: Maximum provider support")

        print(f"\n💡 When to Use ChatCompletionsModel:")
        print(f"   ✓ Legacy application compatibility")
        print(f"   ✓ Multi-provider support needed")
        print(f"   ✓ Proven stability requirements")
        print(f"   ✓ Existing infrastructure integration")

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print(f"   This demonstrates configuration patterns")


async def demo_model_comparison():
    """Compare the two model types side by side."""
    print("\n=== Demo: Model Type Comparison ===")

    print("⚖️ ResponsesModel vs ChatCompletionsModel:")
    print()

    comparison_table = {
        "Feature": ["API Endpoint", "Structured Outputs", "Function Calling", "Provider Support", "Future Updates", "Stability", "Performance", "Compatibility"],
        "ResponsesModel": [
            "Responses API",
            "Advanced ✓✓",
            "Enhanced ✓✓",
            "OpenAI only",
            "Latest features ✓✓",
            "New (evolving)",
            "Optimized ✓✓",
            "OpenAI specific"
        ],
        "ChatCompletionsModel": [
            "Chat Completions API",
            "Basic ✓",
            "Standard ✓",
            "Universal ✓✓",
            "Stable updates",
            "Very stable ✓✓",
            "Standard ✓",
            "Universal ✓✓"
        ]
    }

    # Print comparison table
    for i, feature in enumerate(comparison_table["Feature"]):
        print(
            f"   {feature:20} | {comparison_table['ResponsesModel'][i]:20} | {comparison_table['ChatCompletionsModel'][i]}")

    print(f"\n🎯 Decision Matrix:")
    print(f"   Choose ResponsesModel when:")
    print(f"   ✓ Building new OpenAI-specific applications")
    print(f"   ✓ Need advanced structured outputs")
    print(f"   ✓ Want latest features and performance")
    print(f"   ✓ Future-proofing is important")
    print()
    print(f"   Choose ChatCompletionsModel when:")
    print(f"   ✓ Need multi-provider compatibility")
    print(f"   ✓ Have existing legacy integrations")
    print(f"   ✓ Stability is more important than features")
    print(f"   ✓ Working with non-OpenAI providers")


async def demo_default_behavior():
    """Demonstrate the default model selection behavior."""
    print("\n=== Demo: Default Model Selection ===")

    print("🔧 SDK Default Behavior:")
    print("   • ResponsesModel is used by default")
    print("   • No explicit model configuration needed")
    print("   • Automatic selection of optimal API")
    print("   • Best practice for new applications")
    print()

    try:
        # Default agent (uses ResponsesModel automatically)
        default_agent = Agent(
            name="DefaultAgent",
            instructions="You use the default model configuration."
        )

        print("🤖 Default Agent Configuration:")
        print(f"   Model Class: {type(default_agent.model).__name__}")
        print(f"   Selection: Automatic (SDK default)")
        print(f"   API: Responses API (recommended)")

        print(f"\n⚙️ Configuration Patterns:")

        # Pattern 1: Explicit default (same as implicit)
        print(f"   Pattern 1 - Implicit Default:")
        print(f"   Agent(name='Agent', instructions='...')")
        print(f"   → Uses: OpenAIResponsesModel")

        # Pattern 2: Explicit model specification
        print(f"\n   Pattern 2 - Explicit Responses:")
        print(f"   Agent(model=OpenAIResponsesModel(model='gpt-4o'))")
        print(f"   → Uses: OpenAIResponsesModel (explicit)")

        # Pattern 3: Chat Completions override
        print(f"\n   Pattern 3 - Chat Completions Override:")
        print(f"   Agent(model=OpenAIChatCompletionsModel(...))")
        print(f"   → Uses: OpenAIChatCompletionsModel (explicit)")

        print(f"\n💡 Best Practice Recommendations:")
        print(f"   ✓ Use default (ResponsesModel) for new projects")
        print(f"   ✓ Explicitly specify only when needed")
        print(f"   ✓ Document model choice reasoning")
        print(f"   ✓ Consider migration path for legacy apps")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_feature_support():
    """Demonstrate feature differences between model types."""
    print("\n=== Demo: Feature Support Differences ===")

    print("🌟 Feature Support Matrix:")
    print()

    features = {
        "Basic Chat": {"Responses": "✓ Supported", "ChatCompletions": "✓ Supported"},
        "Function Calling": {"Responses": "✓ Enhanced", "ChatCompletions": "✓ Standard"},
        "Structured Outputs": {"Responses": "✓ Advanced", "ChatCompletions": "✓ Basic"},
        "JSON Schema": {"Responses": "✓ Full support", "ChatCompletions": "✓ Limited"},
        "Tool Use": {"Responses": "✓ Optimized", "ChatCompletions": "✓ Standard"},
        "Streaming": {"Responses": "✓ Enhanced", "ChatCompletions": "✓ Standard"},
        "Context Management": {"Responses": "✓ Advanced", "ChatCompletions": "✓ Basic"},
        "Multi-turn": {"Responses": "✓ Optimized", "ChatCompletions": "✓ Standard"},
        "Provider Portability": {"Responses": "❌ OpenAI only", "ChatCompletions": "✓ Universal"},
        "Legacy Support": {"Responses": "❌ New only", "ChatCompletions": "✓ Full"}
    }

    for feature, support in features.items():
        print(
            f"   {feature:20} | {support['Responses']:15} | {support['ChatCompletions']}")

    print(f"\n🎯 Feature Selection Guide:")
    print(f"   For Advanced AI Applications:")
    print(f"   → Choose ResponsesModel for enhanced capabilities")
    print(f"   For Maximum Compatibility:")
    print(f"   → Choose ChatCompletionsModel for broad support")
    print(f"   For Future-Proofing:")
    print(f"   → Choose ResponsesModel for latest developments")
    print(f"   For Legacy Integration:")
    print(f"   → Choose ChatCompletionsModel for compatibility")


async def demo_migration_patterns():
    """Demonstrate migration from Chat Completions to Responses."""
    print("\n=== Demo: Migration Patterns ===")

    print("🔄 Migration from Chat Completions to Responses:")
    print()

    print("📋 Migration Checklist:")
    migration_steps = [
        "Assess current Chat Completions usage",
        "Identify advanced features needed",
        "Test Responses API compatibility",
        "Update model configuration",
        "Verify functionality works",
        "Monitor performance improvements",
        "Complete migration rollout"
    ]

    for i, step in enumerate(migration_steps, 1):
        print(f"   {i}. {step}")

    print(f"\n⚙️ Migration Code Patterns:")

    print(f"\n   Before (Chat Completions):")
    print(f"   ```python")
    print(f"   agent = Agent(")
    print(f"       model=OpenAIChatCompletionsModel(")
    print(f"           model='gpt-4o',")
    print(f"           openai_client=AsyncOpenAI()")
    print(f"       )")
    print(f"   )")
    print(f"   ```")

    print(f"\n   After (Responses - Default):")
    print(f"   ```python")
    print(f"   agent = Agent(")
    print(f"       # Uses ResponsesModel by default")
    print(f"       model='gpt-4o'  # or omit for default")
    print(f"   )")
    print(f"   ```")

    print(f"\n   After (Responses - Explicit):")
    print(f"   ```python")
    print(f"   agent = Agent(")
    print(f"       model=OpenAIResponsesModel(")
    print(f"           model='gpt-4o'")
    print(f"       )")
    print(f"   )")
    print(f"   ```")

    print(f"\n🎯 Migration Benefits:")
    print(f"   ✓ Access to latest OpenAI features")
    print(f"   ✓ Improved performance and reliability")
    print(f"   ✓ Enhanced structured outputs")
    print(f"   ✓ Better function calling")
    print(f"   ✓ Future feature compatibility")

    print(f"\n⚠️ Migration Considerations:")
    print(f"   • Test thoroughly in staging environment")
    print(f"   • Verify all existing functionality works")
    print(f"   • Plan for any API differences")
    print(f"   • Monitor performance after migration")
    print(f"   • Have rollback plan ready")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all default models demonstrations."""
    print("🤖 OpenAI Agents SDK - Default Models 🤖")
    print("\nThis module covers the two OpenAI model types and when to use each.")
    print("Focus: Understanding ResponsesModel vs ChatCompletionsModel\n")

    # Run all demonstrations
    await demo_responses_model()
    await demo_chat_completions_model()
    await demo_model_comparison()
    await demo_default_behavior()
    await demo_feature_support()
    await demo_migration_patterns()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - Default Models:")
    print("• ResponsesModel: Recommended for new OpenAI applications")
    print("• ChatCompletionsModel: Best for multi-provider compatibility")
    print("• Default behavior uses ResponsesModel automatically")
    print("• Feature support varies between model types")
    print("• Migration to ResponsesModel provides enhanced capabilities")

    print(f"\n🤖 Model Selection Summary:")
    print(f"   🎯 ResponsesModel: Latest features, OpenAI-specific")
    print(f"   🔄 ChatCompletionsModel: Universal compatibility")
    print(f"   ⚙️ Default: ResponsesModel (recommended)")

    print(f"\n🎯 Next Steps:")
    print(f"• Learn LiteLLM integration in 02_litellm_integration.py")
    print(f"• Understand model configuration in 03_model_configuration.py")


if __name__ == "__main__":
    asyncio.run(main())
