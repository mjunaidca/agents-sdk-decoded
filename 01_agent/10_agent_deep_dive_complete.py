"""
🎯 AGENT DEEP DIVE - COMPLETE MASTERY
Covers ALL remaining Agent concepts for expert-level understanding

This comprehensive deep dive covers:
1. Input/Output Guardrails (FIXED)
2. Agent Hooks (Lifecycle Events)
3. Advanced Handoffs (FIXED)
4. Dynamic System Prompt Generation
5. Production Error Handling & Edge Cases

Focus: Core Agent concepts without tool complexity (tools covered separately)
"""

import asyncio
import os
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.guardrail import InputGuardrail, OutputGuardrail
from agents.lifecycle import AgentHooks
from agents.handoffs import Handoff
from agents.run_context import RunContextWrapper
from agents.result import RunResult
from agents.exceptions import UserError

load_dotenv(find_dotenv())

provider = AsyncOpenAI(base_url="https://api.openai.com/v1",
                       api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# ADVANCED CONTEXT FOR DEEP DIVE
# =============================================================================


@dataclass
class SecurityContext:
    user_id: str = ""
    role: str = "user"
    permissions: list[str] = field(default_factory=list)
    session_id: str = ""
    risk_score: float = 0.0


class TaskType(str, Enum):
    RESEARCH = "research"
    CALCULATION = "calculation"
    CREATIVE = "creative"
    ANALYSIS = "analysis"
    SENSITIVE = "sensitive"


@dataclass
class EnterpriseContext:
    security: SecurityContext = field(default_factory=SecurityContext)
    task_type: TaskType = TaskType.RESEARCH
    audit_trail: list[str] = field(default_factory=list)
    compliance_level: str = "standard"

# =============================================================================
# DEMO 1: Input/Output Guardrails - Security & Compliance (FIXED)
# =============================================================================


async def security_input_guardrail(context: RunContextWrapper[EnterpriseContext], agent: Agent, input_data: Any) -> None:
    """Validates input for security threats and compliance"""

    input_text = str(input_data)

    # Check for sensitive data patterns
    sensitive_patterns = ["ssn:", "credit_card:", "password:", "api_key:"]
    for pattern in sensitive_patterns:
        if pattern in input_text.lower():
            context.context.security.risk_score += 0.3
            context.context.audit_trail.append(
                f"SECURITY: Detected {pattern} in input")

    # Check user permissions for sensitive tasks
    if "sensitive" in input_text.lower() and "admin" not in context.context.security.permissions:
        raise UserError(
            "Insufficient permissions for sensitive operations")

    # Update audit trail
    context.context.audit_trail.append(
        f"INPUT_VALIDATED: User {context.context.security.user_id}")


async def compliance_output_guardrail(context: RunContextWrapper[EnterpriseContext], agent: Agent, output: Any) -> None:
    """Ensures output meets compliance requirements"""
    output_text = str(output)

    # Check for data leakage
    if any(word in output_text.lower() for word in ["internal", "confidential", "proprietary"]):
        context.context.security.risk_score += 0.5
        context.context.audit_trail.append(
            "COMPLIANCE: Potential data leakage detected")

    # Ensure proper disclaimers for financial advice
    if any(word in output_text.lower() for word in ["invest", "financial", "stock", "trading"]):
        if "not financial advice" not in output_text.lower():
            raise UserError(
                "Financial content must include appropriate disclaimers")

    context.context.audit_trail.append(
        f"OUTPUT_VALIDATED: Compliance level {context.context.compliance_level}")


async def demo_guardrails():
    """Demonstrate comprehensive input/output guardrails"""
    print("=" * 80)
    print("DEMO 1: Advanced Guardrails - Security & Compliance")
    print("=" * 80)

    context = EnterpriseContext(
        security=SecurityContext(
            user_id="user123",
            role="analyst",
            permissions=["read", "analyze"],
            session_id="sess_456"
        ),
        compliance_level="high"
    )

    # Agent with guardrails (FIXED: Using function references, not class instances)
    secure_agent = Agent(
        name="SecureAnalyst",
        instructions="You are a secure financial analyst. Provide analysis while maintaining compliance.",
        input_guardrails=[InputGuardrail(security_input_guardrail)],
        output_guardrails=[OutputGuardrail(compliance_output_guardrail)],
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    # Test 1: Normal query
    print("🔒 Test 1: Normal Analysis Query")
    try:
        result = await Runner.run(
            secure_agent,
            "Analyze the current market trends for technology stocks",
            context=context
        )
        print(f"✅ Success: {result.final_output[:100]}...")
        print(f"📊 Risk Score: {context.security.risk_score}")
        print(f"📋 Audit Trail: {len(context.audit_trail)} entries\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 2: Sensitive data detection
    print("🚨 Test 2: Sensitive Data Detection")
    context.security.risk_score = 0.0  # Reset
    context.audit_trail.clear()  # Reset
    try:
        result = await Runner.run(
            secure_agent,
            "Analyze this data: SSN: 123-45-6789, Credit_Card: 4111-1111-1111-1111",
            context=context
        )
        print(
            f"⚠️  Processed with warnings. Risk Score: {context.security.risk_score}")
    except Exception as e:
        print(f"❌ Blocked: {e}\n")

    # Test 3: Permission check
    print("🔐 Test 3: Permission Validation")
    try:
        result = await Runner.run(
            secure_agent,
            "I need access to sensitive internal financial data",
            context=context
        )
    except Exception as e:
        print(f"❌ Access Denied: {e}\n")

# =============================================================================
# DEMO 2: Agent Hooks - Lifecycle Event Monitoring
# =============================================================================


class ProductionAgentHooks(AgentHooks[EnterpriseContext]):
    """Production-grade agent lifecycle monitoring"""

    async def before_agent_run(self, context: RunContextWrapper[EnterpriseContext], agent: Agent) -> None:
        """Called before agent execution starts"""
        context.context.audit_trail.append(
            f"AGENT_START: {agent.name} at {asyncio.get_event_loop().time()}")
        print(f"🚀 Starting agent: {agent.name}")

    async def after_agent_run(self, context: RunContextWrapper[EnterpriseContext], agent: Agent, result: RunResult) -> None:
        """Called after agent execution completes"""
        context.context.audit_trail.append(
            f"AGENT_COMPLETE: {agent.name} - Success: {result.final_output is not None}")
        print(f"✅ Completed agent: {agent.name}")

    async def on_agent_error(self, context: RunContextWrapper[EnterpriseContext], agent: Agent, error: Exception) -> None:
        """Called when agent encounters an error"""
        context.context.audit_trail.append(
            f"AGENT_ERROR: {agent.name} - {type(error).__name__}: {str(error)}")
        context.context.security.risk_score += 0.2
        print(f"❌ Agent error in {agent.name}: {error}")


async def demo_agent_hooks():
    """Demonstrate comprehensive agent lifecycle monitoring"""
    print("=" * 80)
    print("DEMO 2: Agent Hooks - Lifecycle Event Monitoring")
    print("=" * 80)

    context = EnterpriseContext(
        security=SecurityContext(user_id="admin_user", permissions=[
                                 "admin", "read", "write"])
    )

    # Agent with comprehensive hooks
    monitored_agent = Agent(
        name="MonitoredAgent",
        instructions="You are a monitored agent. Provide helpful responses while maintaining audit compliance.",
        hooks=ProductionAgentHooks(),
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    print("📊 Running monitored agent with lifecycle tracking...")

    try:
        result = await Runner.run(
            monitored_agent,
            "Explain the benefits of using agent lifecycle hooks in production systems",
            context=context
        )
        print(f"\n📋 Final Result: {result.final_output}")
    except Exception as e:
        print(f"\n❌ Execution failed: {e}")

    print(f"\n📈 Audit Trail ({len(context.audit_trail)} entries):")
    for i, entry in enumerate(context.audit_trail, 1):
        print(f"   {i}. {entry}")

    print(f"\n🔍 Final Risk Score: {context.security.risk_score}")

# =============================================================================
# DEMO 3: Advanced Handoffs with Descriptions (FIXED)
# =============================================================================


class SpecializedHandoff(Handoff[EnterpriseContext]):
    """Custom handoff with advanced routing logic (FIXED)"""

    def __init__(self, target_agent: Agent, condition_func=None, description: str = ""):
        self.target_agent = target_agent
        self.condition_func = condition_func
        self.description = description

    async def should_handoff(self, context: RunContextWrapper[EnterpriseContext], input_data: Any) -> bool:
        """Custom logic to determine if handoff should occur"""
        if self.condition_func:
            result = await self.condition_func(context, input_data)
            return bool(result)
        return True

    async def get_target_agent(self, context: RunContextWrapper[EnterpriseContext]) -> Agent:
        """Return the target agent for handoff"""
        return self.target_agent


async def requires_financial_analysis(context: RunContextWrapper[EnterpriseContext], input_data: Any) -> bool:
    """Determine if input requires financial analysis"""
    financial_keywords = ["stock", "investment",
                          "portfolio", "financial", "market", "trading"]
    input_text = str(input_data).lower()
    return any(keyword in input_text for keyword in financial_keywords)


async def requires_technical_analysis(context: RunContextWrapper[EnterpriseContext], input_data: Any) -> bool:
    """Determine if input requires technical analysis"""
    technical_keywords = ["code", "programming",
                          "algorithm", "database", "api", "technical"]
    input_text = str(input_data).lower()
    return any(keyword in input_text for keyword in technical_keywords)


async def demo_advanced_handoffs():
    """Demonstrate advanced handoff patterns with descriptions"""
    print("=" * 80)
    print("DEMO 3: Advanced Handoffs with Intelligent Routing")
    print("=" * 80)

    # Specialized agents with detailed descriptions
    financial_agent = Agent(
        name="FinancialAnalyst",
        instructions="You are a financial analyst specializing in market analysis, investment strategies, and financial planning.",
        handoff_description="Expert in financial analysis, market trends, investment advice, and portfolio management. Use for all finance-related queries.",
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    technical_agent = Agent(
        name="TechnicalSpecialist",
        instructions="You are a technical specialist expert in programming, databases, APIs, and system architecture.",
        handoff_description="Expert in programming, system design, database optimization, and technical problem-solving. Use for all technical queries.",
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    # Router agent with intelligent handoffs (FIXED)
    router_agent = Agent(
        name="IntelligentRouter",
        instructions="""You are an intelligent routing agent. Analyze incoming requests and delegate to appropriate specialists.
        
        Available specialists:
        - FinancialAnalyst: For financial, investment, and market-related queries
        - TechnicalSpecialist: For programming, database, and technical queries
        
        If the query doesn't clearly fit a specialty, handle it yourself.""",
        handoffs=[
            SpecializedHandoff(
                financial_agent, requires_financial_analysis, "Financial Analysis"),
            SpecializedHandoff(
                technical_agent, requires_technical_analysis, "Technical Analysis")
        ],
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    test_queries = [
        "What's the best investment strategy for a tech portfolio?",
        "How do I optimize a PostgreSQL database for high-traffic applications?",
        "What's the weather like today?",  # Should stay with router
        "Analyze the recent stock market volatility and its impact on retirement planning"
    ]

    context = EnterpriseContext()

    for i, query in enumerate(test_queries, 1):
        print(f"\n🔄 Test {i}: {query}")
        try:
            result = await Runner.run(router_agent, query, context=context)
            print(f"✅ Response: {result.final_output[:150]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

# =============================================================================
# DEMO 4: Dynamic System Prompt Generation
# =============================================================================


async def dynamic_instructions_with_context(context: RunContextWrapper[EnterpriseContext], agent: Agent) -> str:
    """Generate dynamic instructions based on context state"""
    base_instructions = f"You are {agent.name}, an AI assistant."

    # Add security context
    security_level = "high" if context.context.security.risk_score > 0.5 else "standard"
    security_instructions = f"\n\nSecurity Level: {security_level}. "

    if security_level == "high":
        security_instructions += "Be extra cautious with sensitive information. Require additional verification for sensitive operations."

    # Add task-specific instructions
    task_instructions = f"\n\nCurrent task type: {context.context.task_type.value}. "

    if context.context.task_type == TaskType.SENSITIVE:
        task_instructions += "This is a sensitive task. Follow all compliance protocols and maintain detailed audit logs."
    elif context.context.task_type == TaskType.CREATIVE:
        task_instructions += "Be creative and innovative in your responses while maintaining accuracy."
    elif context.context.task_type == TaskType.ANALYSIS:
        task_instructions += "Provide thorough, data-driven analysis with clear reasoning."

    # Add user context
    user_instructions = f"\n\nUser: {context.context.security.user_id} (Role: {context.context.security.role})"
    user_instructions += f"\nPermissions: {', '.join(context.context.security.permissions)}"

    # Add compliance requirements
    compliance_instructions = f"\n\nCompliance Level: {context.context.compliance_level}"
    if context.context.compliance_level == "high":
        compliance_instructions += "\nEnsure all responses meet regulatory requirements. Include appropriate disclaimers."

    return base_instructions + security_instructions + task_instructions + user_instructions + compliance_instructions


async def demo_dynamic_system_prompts():
    """Demonstrate dynamic system prompt generation"""
    print("=" * 80)
    print("DEMO 4: Dynamic System Prompt Generation")
    print("=" * 80)

    # Create agent with dynamic instructions
    adaptive_agent = Agent(
        name="AdaptiveAssistant",
        instructions=dynamic_instructions_with_context,
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    # Test different context scenarios
    scenarios = [
        {
            "name": "Low Risk Standard User",
            "context": EnterpriseContext(
                security=SecurityContext(
                    user_id="john_doe", role="user", permissions=["read"]),
                task_type=TaskType.RESEARCH,
                compliance_level="standard"
            )
        },
        {
            "name": "High Risk Admin User",
            "context": EnterpriseContext(
                security=SecurityContext(
                    user_id="admin_user",
                    role="admin",
                    permissions=["admin", "read", "write", "delete"],
                    risk_score=0.8
                ),
                task_type=TaskType.SENSITIVE,
                compliance_level="high"
            )
        },
        {
            "name": "Creative Task Analyst",
            "context": EnterpriseContext(
                security=SecurityContext(
                    user_id="creative_analyst", role="analyst", permissions=["read", "analyze"]),
                task_type=TaskType.CREATIVE,
                compliance_level="standard"
            )
        }
    ]

    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")

        # Get the generated system prompt
        context_wrapper = RunContextWrapper(scenario['context'])
        system_prompt = await adaptive_agent.get_system_prompt(context_wrapper)

        print(f"🤖 Generated System Prompt:")
        if system_prompt:
            print(f"   {system_prompt[:200]}...")
        else:
            print("   No system prompt generated")

        # Test with a query
        try:
            result = await Runner.run(
                adaptive_agent,
                "Provide analysis on market trends",
                context=scenario['context']
            )
            print(f"✅ Response: {result.final_output[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

# =============================================================================
# DEMO 5: Production Error Handling & Edge Cases
# =============================================================================


async def demo_error_handling():
    """Demonstrate comprehensive error handling patterns"""
    print("=" * 80)
    print("DEMO 5: Production Error Handling & Edge Cases")
    print("=" * 80)

    context = EnterpriseContext()

    # Agent with error handling
    resilient_agent = Agent(
        name="ResilientAgent",
        instructions="You are a resilient agent. Handle errors gracefully and provide helpful feedback to users.",
        hooks=ProductionAgentHooks(),
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    test_scenarios = [
        "Explain how to handle errors gracefully in production systems",
        "What are best practices for agent error recovery?",
        "How do you implement circuit breaker patterns?",
    ]

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔄 Test {i}: {scenario}")
        try:
            result = await Runner.run(
                resilient_agent,
                scenario,
                context=context
            )
            print(f"✅ Success: {result.final_output[:150]}...")
        except Exception as e:
            print(f"❌ Failed: {type(e).__name__}: {e}")

        print(f"📊 Current risk score: {context.security.risk_score}")

# =============================================================================
# MAIN EXECUTION - COMPLETE DEEP DIVE
# =============================================================================


async def main():
    """Execute complete agent deep dive demonstration"""
    print("🎯 AGENT DEEP DIVE - COMPLETE MASTERY")
    print("=" * 100)
    print("Comprehensive coverage of ALL advanced Agent concepts")
    print("=" * 100)

    await demo_guardrails()
    await demo_agent_hooks()
    await demo_advanced_handoffs()
    await demo_dynamic_system_prompts()
    await demo_error_handling()

    print("\n" + "=" * 100)
    print("🎓 EXPERT-LEVEL MASTERY ACHIEVED")
    print("=" * 100)
    print("""
    ✅ COMPLETE AGENT CONCEPT COVERAGE:
    
    1. 🔒 Security & Compliance Guardrails
       - Input validation and threat detection
       - Output compliance and data leakage prevention
       - Permission-based access control
    
    2. 📊 Lifecycle Event Monitoring
       - Agent execution tracking
       - Comprehensive audit trails
       - Error handling and recovery
    
    3. 🔄 Intelligent Agent Handoffs
       - Conditional routing logic
       - Specialized agent descriptions
       - Dynamic delegation patterns
    
    4. 🤖 Dynamic System Prompt Generation
       - Context-aware instructions
       - Security-level adaptation
       - Task-specific customization
    
    5. 🛡️  Production Error Handling
       - Graceful failure recovery
       - Comprehensive audit trails
       - Risk assessment and mitigation
    
    🚀 READY FOR EXPERT QUIZ AND PRODUCTION DEPLOYMENT!
    """)

if __name__ == "__main__":
    asyncio.run(main())
