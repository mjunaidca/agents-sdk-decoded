"""
03_tracing_control.py

This module covers tracing control mechanisms in the OpenAI Agents SDK.
Focus: How to enable, disable, and configure tracing behavior.

Learning Objectives:
- Learn global tracing control methods
- Understand per-run tracing configuration
- Master environment variable controls
- Learn when and why to control tracing

Key Concepts:
- Global control with set_tracing_disabled()
- Environment variable controls
- Per-run control with RunConfig
- Tracing export configuration

Based on: https://openai.github.io/openai-agents-python/tracing/
"""

import asyncio
import os
from agents import Agent, Runner, RunConfig, set_tracing_disabled, set_tracing_export_api_key

# ================== TRACING CONTROL DEMONSTRATIONS ==================


async def demo_global_tracing_control():
    """Demonstrate global tracing enable/disable control."""
    print("=== Demo: Global Tracing Control ===")

    print("🎛️ Global Tracing Control:")
    print("   • set_tracing_disabled(True) - Disable all tracing")
    print("   • set_tracing_disabled(False) - Re-enable tracing")
    print("   • Affects all subsequent agent runs")
    print("   • No restart required - immediate effect")
    print()

    # Create test agent
    control_agent = Agent(
        name="ControlTestAgent",
        instructions="You help demonstrate tracing control. Respond briefly."
    )

    print("🤖 Testing global tracing control with 3 runs...")

    try:
        # Run 1: Normal tracing (enabled)
        print("\n   📊 Run 1: Tracing ENABLED (default)")
        print("      ✓ This run will be fully traced")

        result1 = await Runner.run(
            control_agent,
            "Hello with tracing enabled",
            max_turns=2
        )
        print(f"      Response: {result1.final_output}")
        print("      ✅ Trace created with all spans")

        # Run 2: Disable tracing globally
        print("\n   🚫 Run 2: Disabling tracing globally...")
        set_tracing_disabled(True)
        print("      ❌ Tracing is now disabled for all runs")

        result2 = await Runner.run(
            control_agent,
            "Hello with tracing disabled",
            max_turns=2
        )
        print(f"      Response: {result2.final_output}")
        print("      ❌ No trace created - tracing disabled")

        # Run 3: Re-enable tracing
        print("\n   📊 Run 3: Re-enabling tracing...")
        set_tracing_disabled(False)
        print("      ✓ Tracing is now enabled again")

        result3 = await Runner.run(
            control_agent,
            "Hello with tracing re-enabled",
            max_turns=2
        )
        print(f"      Response: {result3.final_output}")
        print("      ✅ Trace created again")

        print(f"\n🎯 Global Control Summary:")
        print(f"   • Run 1: Traced (default enabled state)")
        print(f"   • Run 2: Not traced (globally disabled)")
        print(f"   • Run 3: Traced (globally re-enabled)")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Ensure tracing is re-enabled for other demos
        set_tracing_disabled(False)


async def demo_environment_variable_control():
    """Demonstrate environment variable tracing controls."""
    print("\n=== Demo: Environment Variable Control ===")

    print("🌍 Environment Variable Controls:")
    print("   OPENAI_AGENTS_DISABLE_TRACING=1")
    print("   • Disables ALL tracing globally")
    print("   • Set before importing agents module")
    print("   • Cannot be overridden programmatically")
    print("   • Most secure way to disable tracing")
    print()

    print("🔍 Other Tracing Environment Variables:")
    tracing_env_vars = {
        "OPENAI_AGENTS_DISABLE_TRACING": "Completely disable tracing",
        "OPENAI_AGENTS_DONT_LOG_MODEL_DATA": "Don't log LLM inputs/outputs",
        "OPENAI_AGENTS_DONT_LOG_TOOL_DATA": "Don't log tool inputs/outputs",
        "OPENAI_AGENTS_TRACING_EXPORT_API_KEY": "API key for trace export"
    }

    for var, description in tracing_env_vars.items():
        current_value = os.getenv(var, "Not set")
        print(f"   {var}:")
        print(f"      Purpose: {description}")
        print(f"      Current value: {current_value}")
        print()

    print("💡 Environment Variable Best Practices:")
    print("   • Set in production deployment configurations")
    print("   • Use container orchestration secrets management")
    print("   • Document which variables your app expects")
    print("   • Test environment variable behavior in staging")

    # Demonstrate checking environment variables
    print("\n🔍 Checking Current Environment:")
    tracing_disabled = os.getenv("OPENAI_AGENTS_DISABLE_TRACING")
    if tracing_disabled:
        print(f"   ⚠️  Tracing is disabled via environment variable")
        print(f"   Value: {tracing_disabled}")
    else:
        print(f"   ✅ No global tracing disable environment variable set")

    model_data_disabled = os.getenv("OPENAI_AGENTS_DONT_LOG_MODEL_DATA")
    if model_data_disabled:
        print(f"   🔒 Model data logging disabled: {model_data_disabled}")
    else:
        print(f"   📝 Model data logging enabled (default)")


async def demo_per_run_control():
    """Demonstrate per-run tracing control with RunConfig."""
    print("\n=== Demo: Per-Run Tracing Control ===")

    print("⚙️ Per-Run Control with RunConfig:")
    print("   • RunConfig(tracing_disabled=True) - Disable for specific run")
    print("   • RunConfig(tracing_disabled=False) - Ensure enabled for specific run")
    print("   • Overrides global settings for that run only")
    print("   • Useful for selective tracing")
    print()

    per_run_agent = Agent(
        name="PerRunAgent",
        instructions="You demonstrate per-run tracing control. Respond briefly."
    )

    print("🤖 Testing per-run tracing control...")

    try:
        # Run 1: Default tracing (should be enabled)
        print("\n   📊 Run 1: Default RunConfig (tracing enabled)")
        result1 = await Runner.run(
            per_run_agent,
            "Run 1: Default tracing behavior",
            max_turns=2
        )
        print(f"      Response: {result1.final_output}")
        print("      ✅ Traced with default settings")

        # Run 2: Explicitly disable tracing for this run
        print("\n   🚫 Run 2: RunConfig with tracing_disabled=True")
        config_disabled = RunConfig(tracing_disabled=True)

        result2 = await Runner.run(
            per_run_agent,
            "Run 2: Tracing disabled for this run only",
            run_config=config_disabled,
            max_turns=2
        )
        print(f"      Response: {result2.final_output}")
        print("      ❌ Not traced (disabled for this run)")

        # Run 3: Back to default (should be enabled)
        print("\n   📊 Run 3: Back to default (no RunConfig)")
        result3 = await Runner.run(
            per_run_agent,
            "Run 3: Back to default tracing",
            max_turns=2
        )
        print(f"      Response: {result3.final_output}")
        print("      ✅ Traced again (default behavior)")

        print(f"\n🎯 Per-Run Control Summary:")
        print(f"   • Selective tracing without affecting global state")
        print(f"   • Useful for privacy-sensitive operations")
        print(f"   • Useful for high-volume operations where tracing overhead matters")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_tracing_export_configuration():
    """Demonstrate tracing export API key configuration."""
    print("\n=== Demo: Tracing Export Configuration ===")

    print("📤 Tracing Export Configuration:")
    print("   • Traces can be exported to external systems")
    print("   • Requires API key configuration")
    print("   • Can be set via environment variable or programmatically")
    print("   • Used for production monitoring and analysis")
    print()

    print("🔑 API Key Configuration Methods:")
    print("   1. Environment Variable:")
    print("      export OPENAI_AGENTS_TRACING_EXPORT_API_KEY='your_key'")
    print("   2. Programmatic:")
    print("      set_tracing_export_api_key('your_key')")
    print()

    # Check current export configuration
    current_export_key = os.getenv("OPENAI_AGENTS_TRACING_EXPORT_API_KEY")

    print("🔍 Current Export Configuration:")
    if current_export_key:
        # Mask the key for security
        masked_key = current_export_key[:8] + "..." + \
            current_export_key[-4:] if len(current_export_key) > 12 else "***"
        print(f"   ✅ Export API key configured: {masked_key}")
    else:
        print(f"   ⚠️  No export API key configured")
        print(f"   Traces will be processed locally only")

    print("\n⚙️ Demonstrating programmatic API key configuration...")

    try:
        # Demonstrate setting API key (with dummy key)
        demo_api_key = "demo_key_12345_not_real"

        print(f"   Setting demo API key: {demo_api_key[:10]}...")
        set_tracing_export_api_key(demo_api_key)
        print(f"   ✅ API key configured programmatically")

        print(f"\n💡 Export Configuration Best Practices:")
        print(f"   • Use environment variables in production")
        print(f"   • Never hardcode API keys in source code")
        print(f"   • Rotate API keys regularly")
        print(f"   • Use secret management systems in cloud deployments")
        print(f"   • Monitor export success rates and failures")

    except Exception as e:
        print(f"❌ Error configuring export: {e}")


async def demo_tracing_control_patterns():
    """Demonstrate common tracing control patterns."""
    print("\n=== Demo: Common Tracing Control Patterns ===")

    print("🎯 Common Tracing Control Patterns:")

    patterns = {
        "Development Mode": {
            "description": "Enable all tracing for debugging",
            "configuration": "Default settings (all tracing enabled)"
        },
        "Production Mode": {
            "description": "Selective tracing with data protection",
            "configuration": "DONT_LOG_MODEL_DATA=1, DONT_LOG_TOOL_DATA=1"
        },
        "High-Volume Mode": {
            "description": "Minimal tracing to reduce overhead",
            "configuration": "Use sampling or selective per-run disabling"
        },
        "Privacy Mode": {
            "description": "No tracing for sensitive operations",
            "configuration": "RunConfig(tracing_disabled=True) for sensitive runs"
        },
        "Debug Mode": {
            "description": "Enhanced tracing for troubleshooting",
            "configuration": "Enable all tracing + export to external systems"
        }
    }

    for pattern, info in patterns.items():
        print(f"\n   📋 {pattern}:")
        print(f"      Use case: {info['description']}")
        print(f"      Configuration: {info['configuration']}")

    print(f"\n🔄 Pattern Selection Decision Tree:")
    print(f"   📊 Is this development? → Enable all tracing")
    print(f"   🔒 Contains sensitive data? → Disable data logging or tracing")
    print(f"   ⚡ High-volume production? → Use sampling")
    print(f"   🐛 Debugging issues? → Enable enhanced tracing")
    print(f"   💰 Cost-sensitive? → Disable or sample tracing")

    # Demonstrate a pattern switch
    pattern_agent = Agent(
        name="PatternAgent",
        instructions="You help demonstrate tracing patterns."
    )

    print(f"\n🤖 Demonstrating pattern switching...")

    try:
        # Pattern 1: Development mode (default)
        print(f"\n   🔧 Development Mode: Full tracing")
        result1 = await Runner.run(
            pattern_agent,
            "Development mode operation",
            max_turns=2
        )
        print(f"      ✅ Full tracing enabled")

        # Pattern 2: Privacy mode (disabled for sensitive data)
        print(f"\n   🔒 Privacy Mode: Tracing disabled")
        privacy_config = RunConfig(tracing_disabled=True)
        result2 = await Runner.run(
            pattern_agent,
            "Privacy-sensitive operation",
            run_config=privacy_config,
            max_turns=2
        )
        print(f"      ❌ Tracing disabled for privacy")

        print(f"\n✅ Pattern switching demonstrated successfully")

    except Exception as e:
        print(f"❌ Error in pattern demo: {e}")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all tracing control demonstrations."""
    print("🎛️ OpenAI Agents SDK - Tracing Control 🎛️")
    print("\nThis module covers how to control when and how tracing occurs")
    print("in your applications.\n")

    # Run all demonstrations
    await demo_global_tracing_control()
    await demo_environment_variable_control()
    await demo_per_run_control()
    await demo_tracing_export_configuration()
    await demo_tracing_control_patterns()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - Tracing Control:")
    print("• Global control: set_tracing_disabled(True/False)")
    print("• Environment variables: OPENAI_AGENTS_DISABLE_TRACING")
    print("• Per-run control: RunConfig(tracing_disabled=True)")
    print("• Export configuration: set_tracing_export_api_key()")
    print("• Choose patterns based on environment and requirements")

    print(f"\n⚙️ Control Method Summary:")
    print(f"   🌍 Environment Variables: Secure, deployment-time control")
    print(f"   🎛️ Global Functions: Runtime control across all operations")
    print(f"   ⚙️ RunConfig: Selective control per operation")
    print(f"   📤 Export Config: External system integration")

    print(f"\n🎯 Next Steps:")
    print(f"• Learn data protection in 04_sensitive_data.py")
    print(f"• Understand custom traces in 05_custom_traces.py")


if __name__ == "__main__":
    asyncio.run(main())
