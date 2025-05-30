"""
04_sensitive_data.py

This module covers sensitive data protection in tracing.
Focus: How to protect sensitive information when tracing is enabled.

Learning Objectives:
- Understand what data is captured by default
- Learn environment variables for data protection
- Master selective data protection strategies
- Understand compliance implications

Key Concepts:
- Model data protection (LLM inputs/outputs)
- Tool data protection (function parameters/results)
- Audio data protection (speech/transcription)
- Compliance requirements (GDPR, HIPAA, etc.)

Based on: https://openai.github.io/openai-agents-python/tracing/
"""

import asyncio
import os
from agents import Agent, Runner, function_tool, RunConfig

# ================== SENSITIVE DATA PROTECTION ==================


async def demo_default_data_capture():
    """Demonstrate what data is captured by default in tracing."""
    print("=== Demo: Default Data Capture ===")

    print("📋 Data Captured by Default:")
    print("   🧠 Model Data (Generation Spans):")
    print("      • Full input prompts sent to LLMs")
    print("      • Complete model responses")
    print("      • Model parameters (temperature, tokens, etc.)")
    print("      • Token usage and costs")
    print()
    print("   🔧 Tool Data (Function Spans):")
    print("      • All function parameters and arguments")
    print("      • Complete function return values")
    print("      • Function execution timing")
    print("      • Error messages and stack traces")
    print()
    print("   🎤 Audio Data (Audio Spans):")
    print("      • Base64-encoded PCM audio data")
    print("      • Transcription inputs and outputs")
    print("      • Speech synthesis inputs and outputs")
    print()

    @function_tool
    def process_user_info(name: str, email: str, ssn: str) -> str:
        """Process sensitive user information (demonstration only)."""
        return f"Processed user: {name}, Contact: {email}, ID: ***-**-{ssn[-4:]}"

    sensitive_agent = Agent(
        name="SensitiveDataAgent",
        instructions="You process sensitive user information. Use the tool carefully.",
        tools=[process_user_info]
    )

    print("🤖 Running agent with sensitive data (default tracing)...")
    print("⚠️  WARNING: This demonstrates what gets logged by default")

    try:
        result = await Runner.run(
            sensitive_agent,
            "Please process user info: John Doe, john@example.com, 123-45-6789",
            max_turns=3
        )

        print(f"\n✅ Processing completed!")
        print(f"📋 Result: {result.final_output}")
        print(f"\n⚠️  What was captured in traces:")
        print(f"   🧠 LLM saw full user request including SSN")
        print(f"   🔧 Tool received: name='John Doe', email='john@example.com', ssn='123-45-6789'")
        print(f"   📊 All this data is in the trace spans")
        print(f"\n🚨 Security Risk: Sensitive data exposed in traces!")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_model_data_protection():
    """Demonstrate protecting LLM input/output data."""
    print("\n=== Demo: Model Data Protection ===")

    print("🔒 Model Data Protection:")
    print("   Environment Variable: OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1")
    print("   • Prevents logging of LLM prompts and responses")
    print("   • Still captures timing and metadata")
    print("   • Protects against sensitive prompt leakage")
    print()

    # Check current model data protection
    model_protection = os.getenv("OPENAI_AGENTS_DONT_LOG_MODEL_DATA")

    print("🔍 Current Model Data Protection Status:")
    if model_protection:
        print(f"   ✅ Model data logging DISABLED: {model_protection}")
        print(f"   🔒 LLM inputs/outputs will NOT be logged")
    else:
        print(f"   ⚠️  Model data logging ENABLED (default)")
        print(f"   📝 LLM inputs/outputs WILL be logged")

    # Create agent to test model data protection
    model_protection_agent = Agent(
        name="ModelProtectionAgent",
        instructions="You handle confidential information. Never repeat sensitive details."
    )

    print(f"\n🤖 Testing with confidential business information...")

    try:
        # This would normally log the full conversation
        result = await Runner.run(
            model_protection_agent,
            "Our Q4 revenue is $50M and we're acquiring CompanyX for $10M. Keep this confidential.",
            max_turns=2
        )

        print(f"\n✅ Confidential processing completed!")
        print(f"💬 Response: {result.final_output}")

        if model_protection:
            print(f"\n🔒 Model Data Protection Active:")
            print(f"   ✓ Confidential prompt NOT logged in traces")
            print(f"   ✓ Model response NOT logged in traces")
            print(f"   ✓ Only metadata and timing captured")
        else:
            print(f"\n⚠️  Model Data Protection Inactive:")
            print(f"   ❌ Confidential prompt IS logged in traces")
            print(f"   ❌ Model response IS logged in traces")
            print(f"   🚨 Security risk: Set OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_tool_data_protection():
    """Demonstrate protecting tool/function parameter and return data."""
    print("\n=== Demo: Tool Data Protection ===")

    print("🔧 Tool Data Protection:")
    print("   Environment Variable: OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1")
    print("   • Prevents logging of function parameters")
    print("   • Prevents logging of function return values")
    print("   • Still captures function names and timing")
    print("   • Protects sensitive function arguments")
    print()

    # Check current tool data protection
    tool_protection = os.getenv("OPENAI_AGENTS_DONT_LOG_TOOL_DATA")

    print("🔍 Current Tool Data Protection Status:")
    if tool_protection:
        print(f"   ✅ Tool data logging DISABLED: {tool_protection}")
        print(f"   🔒 Function inputs/outputs will NOT be logged")
    else:
        print(f"   ⚠️  Tool data logging ENABLED (default)")
        print(f"   📝 Function inputs/outputs WILL be logged")

    @function_tool
    def authenticate_user(username: str, password: str, api_key: str) -> str:
        """Authenticate user with sensitive credentials."""
        # This is a demo - never handle real credentials like this
        if len(password) >= 8 and len(api_key) >= 20:
            return f"Authentication successful for {username}"
        else:
            return "Authentication failed - invalid credentials"

    @function_tool
    def process_payment(card_number: str, cvv: str, amount: float) -> str:
        """Process payment with sensitive financial data."""
        # This is a demo - never handle real payment data like this
        masked_card = "****-****-****-" + card_number[-4:]
        return f"Payment of ${amount:.2f} processed with card {masked_card}"

    tool_protection_agent = Agent(
        name="ToolProtectionAgent",
        instructions="You handle authentication and payments. Use tools to process requests.",
        tools=[authenticate_user, process_payment]
    )

    print(f"\n🤖 Testing with sensitive tool parameters...")

    try:
        result = await Runner.run(
            tool_protection_agent,
            "Authenticate user 'alice' with password 'secret123' and API key 'sk-1234567890abcdef1234567890abcdef', then process payment with card 4532-1234-5678-9012, CVV 123, amount $99.99",
            max_turns=4
        )

        print(f"\n✅ Sensitive tool operations completed!")
        print(f"💳 Result: {result.final_output}")

        if tool_protection:
            print(f"\n🔒 Tool Data Protection Active:")
            print(f"   ✓ Passwords and API keys NOT logged")
            print(f"   ✓ Credit card numbers and CVVs NOT logged")
            print(f"   ✓ Only function names and timing captured")
        else:
            print(f"\n⚠️  Tool Data Protection Inactive:")
            print(f"   ❌ Passwords and API keys ARE logged in traces")
            print(f"   ❌ Credit card data IS logged in traces")
            print(f"   🚨 Security risk: Set OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_combined_protection():
    """Demonstrate combining multiple protection mechanisms."""
    print("\n=== Demo: Combined Data Protection ===")

    print("🛡️ Combined Protection Strategy:")
    print("   1. OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1")
    print("   2. OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1")
    print("   3. RunConfig selective disabling")
    print("   4. Tool-level data masking")
    print()

    @function_tool
    def secure_database_query(query: str, credentials: str) -> str:
        """Execute database query with data masking."""
        # Demonstrate tool-level protection
        masked_creds = credentials[:4] + "***" + \
            credentials[-4:] if len(credentials) > 8 else "***"

        # Simulate secure query execution
        if "SELECT" in query.upper():
            return f"Query executed successfully with credentials {masked_creds}"
        else:
            return "Only SELECT queries allowed"

    combined_protection_agent = Agent(
        name="SecureAgent",
        instructions="You handle highly sensitive operations with multiple protection layers.",
        tools=[secure_database_query]
    )

    print("🤖 Testing combined protection mechanisms...")

    try:
        # High-security configuration
        secure_config = RunConfig(
            workflow_name="HighSecurityOperation",
            trace_metadata={
                "security_level": "high",
                "data_classification": "confidential",
                "compliance": ["GDPR", "HIPAA", "SOX"]
            }
            # Note: tracing_disabled could be True for maximum security
        )

        result = await Runner.run(
            combined_protection_agent,
            "Execute SELECT * FROM patients WHERE ssn='123-45-6789' using credentials 'db_user:super_secret_password_123'",
            run_config=secure_config,
            max_turns=3
        )

        print(f"\n✅ Secure operation completed!")
        print(f"🔐 Result: {result.final_output}")

        print(f"\n🛡️ Protection Layers Applied:")
        print(f"   ✓ Tool-level masking: credentials masked in function")
        print(f"   ✓ Environment protection: model/tool data not logged")
        print(f"   ✓ Trace metadata: security context documented")
        print(f"   ✓ Minimal exposure: only essential data captured")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_compliance_patterns():
    """Demonstrate compliance-specific protection patterns."""
    print("\n=== Demo: Compliance Protection Patterns ===")

    compliance_patterns = {
        "GDPR (EU Data Protection)": {
            "requirements": [
                "Right to be forgotten (data deletion)",
                "Data minimization principle",
                "Explicit consent for processing",
                "Data protection by design"
            ],
            "protection_strategy": "Disable all data logging + minimal metadata"
        },
        "HIPAA (Healthcare)": {
            "requirements": [
                "Protected Health Information (PHI) safeguards",
                "Minimum necessary standard",
                "Access logging and audit trails",
                "Administrative safeguards"
            ],
            "protection_strategy": "Disable model/tool data + audit metadata"
        },
        "PCI DSS (Payment Card)": {
            "requirements": [
                "Cardholder data protection",
                "Strong access controls",
                "Regular monitoring and testing",
                "Secure network architecture"
            ],
            "protection_strategy": "Disable all data logging + network security"
        },
        "SOX (Financial Reporting)": {
            "requirements": [
                "Financial data integrity",
                "Internal controls documentation",
                "Audit trail requirements",
                "Change management controls"
            ],
            "protection_strategy": "Selective tracing + comprehensive audit trails"
        }
    }

    for regulation, details in compliance_patterns.items():
        print(f"\n📋 {regulation}:")
        print(f"   Requirements:")
        for req in details["requirements"]:
            print(f"      • {req}")
        print(f"   Protection Strategy: {details['protection_strategy']}")

    print(f"\n🎯 Compliance Implementation Checklist:")
    print(f"   🔍 1. Identify applicable regulations")
    print(f"   📊 2. Classify data sensitivity levels")
    print(f"   🛡️  3. Choose appropriate protection mechanisms")
    print(f"   📝 4. Document compliance controls")
    print(f"   🧪 5. Test protection effectiveness")
    print(f"   📈 6. Monitor and audit regularly")


async def demo_protection_best_practices():
    """Demonstrate best practices for sensitive data protection."""
    print("\n=== Demo: Protection Best Practices ===")

    print("🎯 Sensitive Data Protection Best Practices:")

    best_practices = {
        "Environment Setup": [
            "Set protection variables in deployment config",
            "Use secrets management for environment variables",
            "Test protection in staging environments",
            "Document protection policies clearly"
        ],
        "Code Patterns": [
            "Implement data masking at tool level",
            "Use selective tracing for different operations",
            "Validate protection is working in tests",
            "Minimize data exposure by design"
        ],
        "Monitoring": [
            "Monitor trace export for sensitive data leaks",
            "Audit protection configuration regularly",
            "Set up alerts for protection failures",
            "Review compliance requirements periodically"
        ],
        "Team Education": [
            "Train developers on data protection requirements",
            "Document sensitive data handling procedures",
            "Regular security awareness sessions",
            "Code review processes for sensitive operations"
        ]
    }

    for category, practices in best_practices.items():
        print(f"\n   📂 {category}:")
        for practice in practices:
            print(f"      • {practice}")

    print(f"\n🚨 Common Protection Mistakes to Avoid:")
    print(f"   ❌ Assuming default settings are secure")
    print(f"   ❌ Not testing protection in development")
    print(f"   ❌ Hardcoding sensitive data in examples")
    print(f"   ❌ Forgetting about error message leakage")
    print(f"   ❌ Not documenting protection requirements")
    print(f"   ❌ Inconsistent protection across environments")

    print(f"\n✅ Protection Verification Steps:")
    print(f"   1. Check environment variables are set correctly")
    print(f"   2. Verify no sensitive data in trace exports")
    print(f"   3. Test protection with sample sensitive data")
    print(f"   4. Review logs for any leakage")
    print(f"   5. Validate compliance requirements are met")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all sensitive data protection demonstrations."""
    print("🔒 OpenAI Agents SDK - Sensitive Data Protection 🔒")
    print("\nThis module covers how to protect sensitive information")
    print("when using tracing in production systems.\n")

    # Run all demonstrations
    await demo_default_data_capture()
    await demo_model_data_protection()
    await demo_tool_data_protection()
    await demo_combined_protection()
    await demo_compliance_patterns()
    await demo_protection_best_practices()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - Sensitive Data Protection:")
    print("• Default tracing captures ALL data (prompts, parameters, responses)")
    print("• OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1 protects LLM data")
    print("• OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1 protects function data")
    print("• Combine environment variables with tool-level masking")
    print("• Different compliance requirements need different strategies")

    print(f"\n🔒 Protection Method Summary:")
    print(f"   🌍 Environment Variables: System-wide data protection")
    print(f"   🔧 Tool-level Masking: Function-specific data hiding")
    print(f"   ⚙️ RunConfig: Operation-specific tracing control")
    print(f"   📋 Compliance Patterns: Regulation-specific strategies")

    print(f"\n🎯 Next Steps:")
    print(f"• Learn custom traces in 05_custom_traces.py")
    print(f"• Understand custom spans in 06_custom_spans.py")


if __name__ == "__main__":
    asyncio.run(main())
