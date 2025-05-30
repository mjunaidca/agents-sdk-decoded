# Complex Multi-Agent Orchestration Example
# https://openai.github.io/openai-agents-python/handoffs/

import asyncio
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from agents import Agent, Runner, handoff, function_tool, RunContextWrapper
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions


# =============================================================================
# BUSINESS LOGIC AND DATA MODELS
# =============================================================================

class CustomerTier(str, Enum):
    """Customer service tier levels"""
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    VIP = "vip"


class IssueComplexity(str, Enum):
    """Issue complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    CRITICAL = "critical"


class HandoffContext(BaseModel):
    """Context data passed between agents"""
    customer_tier: CustomerTier
    issue_complexity: IssueComplexity
    escalation_count: int = 0
    previous_agents: list[str] = Field(default_factory=list)
    resolution_attempts: list[str] = Field(default_factory=list)
    customer_satisfaction: Optional[str] = None


# =============================================================================
# SIMULATION TOOLS
# =============================================================================

@function_tool
def lookup_customer_tier(customer_id: str) -> str:
    """Look up customer service tier."""
    # Simulate customer lookup
    tiers = {
        "cust_001": "vip",
        "cust_002": "enterprise",
        "cust_003": "premium",
        "cust_004": "basic"
    }
    return tiers.get(customer_id, "basic")


@function_tool
def log_agent_interaction(agent_name: str, action: str, customer_id: str) -> str:
    """Log agent interactions for audit trail."""
    return f"LOGGED: {agent_name} performed {action} for customer {customer_id}"


@function_tool
def check_issue_complexity(issue_description: str) -> str:
    """Analyze and categorize issue complexity."""
    # Simple keyword-based complexity analysis
    if any(word in issue_description.lower() for word in ["api", "integration", "database", "security"]):
        return "complex"
    elif any(word in issue_description.lower() for word in ["urgent", "critical", "down", "outage"]):
        return "critical"
    elif any(word in issue_description.lower() for word in ["billing", "refund", "payment"]):
        return "moderate"
    else:
        return "simple"


@function_tool
def escalate_to_engineering(issue_details: str, customer_tier: str) -> str:
    """Escalate technical issues to engineering team."""
    return f"Engineering escalation created for {customer_tier} customer: {issue_details}"


@function_tool
def create_priority_ticket(issue: str, priority: str) -> str:
    """Create high-priority support ticket."""
    return f"Priority ticket created: {priority} - {issue}"


# =============================================================================
# SPECIALIZED AGENT NETWORK
# =============================================================================

# Level 1: Frontline Support Agents
def create_frontline_agent():
    return Agent(
        name="Frontline Support",
        instructions=prompt_with_handoff_instructions("""
        You are a frontline customer support agent. Your responsibilities:
        1. Initial customer contact and issue identification
        2. Basic troubleshooting and simple issue resolution
        3. Customer tier identification and appropriate routing
        4. Issue complexity assessment
        
        You should handle simple issues directly but transfer complex ones to specialists.
        Always check customer tier to ensure appropriate service level.
        """),
        tools=[lookup_customer_tier,
               log_agent_interaction, check_issue_complexity]
    )


# Level 2: Specialized Support Agents
def create_billing_specialist():
    return Agent(
        name="Billing Specialist",
        instructions=prompt_with_handoff_instructions("""
        You are a billing and payments specialist. You handle:
        - Payment processing issues
        - Invoice disputes and corrections
        - Subscription management
        - Billing policy questions
        
        For complex billing issues or VIP customers, you may escalate to Account Management.
        For technical billing system issues, transfer to Technical Support.
        """),
        tools=[log_agent_interaction, create_priority_ticket]
    )


def create_technical_specialist():
    return Agent(
        name="Technical Specialist",
        instructions=prompt_with_handoff_instructions("""
        You are a technical support specialist. You provide:
        - Software troubleshooting
        - API and integration support
        - System configuration help
        - Performance optimization
        
        For critical technical issues or when you need engineering involvement, 
        escalate to Senior Technical Support or Engineering.
        """),
        tools=[log_agent_interaction,
               escalate_to_engineering, create_priority_ticket]
    )


def create_account_specialist():
    return Agent(
        name="Account Specialist",
        instructions=prompt_with_handoff_instructions("""
        You are an account management specialist. You handle:
        - Account configuration changes
        - Service upgrades and downgrades
        - Contract modifications
        - Premium customer requests
        
        You work closely with Sales for upgrades and with Customer Success for retention.
        """),
        tools=[log_agent_interaction, create_priority_ticket]
    )


# Level 3: Senior/Management Level
def create_senior_technical():
    return Agent(
        name="Senior Technical Support",
        instructions=prompt_with_handoff_instructions("""
        You are senior technical support handling complex technical issues:
        - System architecture problems
        - Critical performance issues
        - Security concerns
        - Engineering escalations
        
        You have authority to engage engineering directly and make technical decisions.
        For business-critical issues, you may need to involve Customer Success Management.
        """),
        tools=[log_agent_interaction,
               escalate_to_engineering, create_priority_ticket]
    )


def create_customer_success_manager():
    return Agent(
        name="Customer Success Manager",
        instructions=prompt_with_handoff_instructions("""
        You are a Customer Success Manager handling high-value customer relationships:
        - VIP and Enterprise customer issues
        - Complex multi-department problems
        - Contract and business relationship issues
        - Customer retention and satisfaction
        
        You have broad authority to make decisions and coordinate across departments.
        You're the final escalation point for most customer issues.
        """),
        tools=[log_agent_interaction, create_priority_ticket]
    )


def create_sales_agent():
    return Agent(
        name="Sales Representative",
        instructions=prompt_with_handoff_instructions("""
        You are a sales representative focused on:
        - Upgrade opportunities and upselling
        - New feature demonstrations
        - Contract renewals and expansions
        - Competitive analysis and positioning
        
        Work with Account Specialists for existing customer changes
        and Customer Success for retention issues.
        """),
        tools=[log_agent_interaction]
    )


# =============================================================================
# ORCHESTRATION CALLBACKS
# =============================================================================

async def on_tier_based_routing(ctx: RunContextWrapper[None], handoff_data: HandoffContext):
    """Route based on customer tier and issue complexity."""
    print(f"🎯 SMART ROUTING:")
    print(f"   Customer Tier: {handoff_data.customer_tier}")
    print(f"   Issue Complexity: {handoff_data.issue_complexity}")
    print(f"   Escalation Count: {handoff_data.escalation_count}")
    print(f"   Previous Agents: {', '.join(handoff_data.previous_agents)}")


async def on_escalation_tracking(ctx: RunContextWrapper[None], handoff_data: HandoffContext):
    """Track escalations and maintain context."""
    handoff_data.escalation_count += 1
    if ctx.agent:
        handoff_data.previous_agents.append(ctx.agent.name)

    print(f"📈 ESCALATION TRACKING:")
    print(f"   Escalation #{handoff_data.escalation_count}")
    print(f"   Agent Chain: {' → '.join(handoff_data.previous_agents)}")


async def main():
    """Demonstrate complex multi-agent orchestration."""

    # Create the agent network
    frontline = create_frontline_agent()
    billing = create_billing_specialist()
    technical = create_technical_specialist()
    account = create_account_specialist()
    senior_tech = create_senior_technical()
    cs_manager = create_customer_success_manager()
    sales = create_sales_agent()

    # Create the main orchestrator with complex handoff logic
    orchestrator = Agent(
        name="AI Customer Service Orchestrator",
        instructions=prompt_with_handoff_instructions("""
        You are an intelligent customer service orchestrator. Your role is to:
        1. Analyze customer requests and determine optimal routing
        2. Consider customer tier, issue complexity, and business context
        3. Route to the most appropriate specialist
        4. Handle escalations intelligently
        
        Routing Guidelines:
        - Simple issues: Handle directly or route to appropriate specialist
        - VIP/Enterprise customers: Expedited routing, consider Account Specialist
        - Technical issues: Technical Specialist → Senior Technical → Engineering
        - Billing issues: Billing Specialist → Account Specialist (if needed)
        - Complex/Critical: May require Customer Success Manager involvement
        - Sales opportunities: Route to Sales Representative
        
        Always maintain context and explain routing decisions to customers.
        """),
        tools=[lookup_customer_tier,
               check_issue_complexity, log_agent_interaction],
        handoffs=[
            # Direct specialist routing
            handoff(
                agent=frontline,
                tool_name_override="route_to_frontline",
                tool_description_override="Route to frontline support for initial handling"
            ),

            handoff(
                agent=billing,
                tool_name_override="route_to_billing",
                tool_description_override="Route to billing specialist for payment and invoice issues"
            ),

            handoff(
                agent=technical,
                tool_name_override="route_to_technical",
                tool_description_override="Route to technical specialist for software and system issues"
            ),

            handoff(
                agent=account,
                tool_name_override="route_to_account",
                tool_description_override="Route to account specialist for account management issues"
            ),

            # Escalation routing
            handoff(
                agent=senior_tech,
                tool_name_override="escalate_to_senior_tech",
                tool_description_override="Escalate complex technical issues to senior technical support"
            ),

            handoff(
                agent=cs_manager,
                tool_name_override="escalate_to_cs_manager",
                tool_description_override="Escalate to Customer Success Manager for high-value or complex issues"
            ),

            handoff(
                agent=sales,
                tool_name_override="route_to_sales",
                tool_description_override="Route to sales for upgrade opportunities and new feature discussions"
            )
        ]
    )

    print("=== Complex Multi-Agent Customer Service Orchestration ===")
    print()
    print("Agent Network:")
    print("Level 1 (Frontline): Frontline Support")
    print("Level 2 (Specialists): Billing, Technical, Account")
    print("Level 3 (Senior/Mgmt): Senior Technical, Customer Success Manager, Sales")
    print()

    # Test Case 1: VIP customer with critical technical issue
    print("=== Test 1: VIP Customer - Critical Technical Issue ===")
    result1 = await Runner.run(
        orchestrator,
        input="""Customer ID: cust_001
        Issue: Our production API is completely down. We're losing $10,000 per hour. 
        This is a critical business emergency that needs immediate engineering attention.
        We're a major enterprise client and expect immediate escalation."""
    )
    print(f"Result: {result1.final_output}")
    print()

    # Test Case 2: Basic customer with billing question
    print("=== Test 2: Basic Customer - Simple Billing Question ===")
    result2 = await Runner.run(
        orchestrator,
        input="""Customer ID: cust_004
        Issue: I don't understand why my bill went up this month. 
        Can someone explain the charges?"""
    )
    print(f"Result: {result2.final_output}")
    print()

    # Test Case 3: Premium customer interested in upgrades
    print("=== Test 3: Premium Customer - Upgrade Interest ===")
    result3 = await Runner.run(
        orchestrator,
        input="""Customer ID: cust_003
        Issue: We're growing fast and think we might need to upgrade our plan. 
        Can you tell me about enterprise features and pricing?"""
    )
    print(f"Result: {result3.final_output}")
    print()

    # Test Case 4: Enterprise customer with complex account issue
    print("=== Test 4: Enterprise Customer - Complex Account Issue ===")
    result4 = await Runner.run(
        orchestrator,
        input="""Customer ID: cust_002
        Issue: We need to restructure our account to support multiple subsidiaries, 
        each with different billing and access controls. This involves contract changes 
        and custom configuration."""
    )
    print(f"Result: {result4.final_output}")
    print()

    # Test Case 5: Mixed technical and billing issue requiring coordination
    print("=== Test 5: Mixed Issue - Technical + Billing Coordination ===")
    result5 = await Runner.run(
        orchestrator,
        input="""Customer ID: cust_001
        Issue: We were charged for API usage during yesterday's outage when your service 
        was down. This is both a billing dispute and indicates a technical problem with 
        your usage tracking system."""
    )
    print(f"Result: {result5.final_output}")
    print()

    # Demonstrate orchestration benefits
    print("=== Benefits of Complex Orchestration ===")
    benefits = """
    Complex Multi-Agent Orchestration provides:
    
    1. Intelligent Routing:
       - Customer tier-based prioritization
       - Issue complexity analysis
       - Optimal specialist selection
    
    2. Escalation Management:
       - Structured escalation paths
       - Context preservation across handoffs
       - Escalation tracking and analytics
    
    3. Business Logic Integration:
       - Customer value consideration
       - SLA adherence based on tier
       - Revenue impact assessment
    
    4. Cross-Department Coordination:
       - Technical + Business issue handling
       - Sales opportunity identification
       - Account management integration
    
    5. Scalability and Efficiency:
       - Reduces human coordination overhead
       - Ensures consistent service quality
       - Optimizes specialist utilization
    
    This pattern is ideal for enterprise customer service systems where
    multiple departments must coordinate to resolve complex customer issues.
    """
    print(benefits)


if __name__ == "__main__":
    asyncio.run(main())
