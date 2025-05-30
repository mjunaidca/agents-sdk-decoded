# Handoff Function with Customization Example
# https://openai.github.io/openai-agents-python/handoffs/

import asyncio

from pydantic import BaseModel
from agents import Agent, Runner, handoff, RunContextWrapper


class EscalationData(BaseModel):
    reason: str
async def main():
    """Demonstrate the handoff() function with various customizations."""

    # Create specialized agents
    escalation_agent = Agent(
        name="Escalation Agent",
        instructions="""You are a senior customer service representative. You handle:
        - Complex issues that require manager attention
        - Complaints and difficult situations
        - Policy exceptions and special cases
        
        Always be professional and work to resolve issues definitively."""
    )

    technical_agent = Agent(
        name="Technical Agent",
        instructions="""You are a technical support specialist. You help with:
        - Software troubleshooting
        - System configuration
        - Technical documentation
        - Bug reports and feature requests
        
        Provide detailed technical assistance and solutions."""
    )

    sales_agent = Agent(
        name="Sales Agent",
        instructions="""You are a sales representative. You help with:
        - Product information and demos
        - Pricing and quotes
        - Upgrade recommendations
        - New customer onboarding
        
        Be helpful and focus on matching customer needs to solutions."""
    )

    # Callback functions for handoffs
    def on_escalation_handoff(ctx: RunContextWrapper[None]):
        """Called when escalating to manager."""
        print("🚨 ESCALATION: Issue escalated to senior representative")
        print(
            f"Session context: Agent={ctx}")
        # In real implementation, you might:
        # - Log escalation to database
        # - Send notification to managers
        # - Update customer service metrics

    
    def on_technical_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
        """Called when transferring to technical support."""
        print("🔧 TECHNICAL: Transferring to technical support team")
        print(
            f"Session context: Agent={ctx}")
        print(f"Input data: {input_data}")
        # In real implementation, you might:
        # - Create technical support ticket
        # - Gather system information
        # - Prepare diagnostic data

    def on_sales_handoff(ctx: RunContextWrapper[None]):
        """Called when transferring to sales team."""
        print("💰 SALES: Connecting with sales representative")
        print(
            f"Session context: Agent={ctx}")
        # In real implementation, you might:
        # - Update lead tracking system
        # - Prepare customer profile
        # - Set sales context

    # Create main agent with customized handoffs
    main_agent = Agent(
        name="Customer Service Agent",
        instructions="""You are a frontline customer service agent. You help customers with various issues.
        
        When you need to transfer customers, use these guidelines:
        - Use 'escalate_to_manager' for complaints, complex issues, or when policy exceptions are needed
        - Use 'get_technical_help' for software problems, bugs, or technical configuration issues  
        - Use 'connect_with_sales' for product questions, upgrades, or purchasing decisions
        
        Always explain to the customer why you're transferring them and what to expect.""",
        handoffs=[
            # Direct agent reference (basic handoff)
            escalation_agent,

            # Customized handoff with callback and custom tool name
            handoff(
                agent=technical_agent,
                tool_name_override="get_technical_help",
                tool_description_override="Transfer customer to technical support for software and system issues",
                on_handoff=on_technical_handoff,
                input_type=EscalationData
            ),

            # Customized handoff with different tool name and callback
            handoff(
                agent=sales_agent,
                tool_name_override="connect_with_sales",
                tool_description_override="Connect customer with sales team for product information and purchases",
                on_handoff=on_sales_handoff
            ),

            # Custom escalation handoff
            handoff(
                agent=escalation_agent,
                tool_name_override="escalate_to_manager",
                tool_description_override="Escalate complex issues or complaints to senior customer service",
                on_handoff=on_escalation_handoff
            )
        ]
    )

    print("=== Advanced Customer Service System ===")
    print("Available handoff tools:")
    print("- transfer_to_escalation_agent (default)")
    print("- get_technical_help (custom)")
    print("- connect_with_sales (custom)")
    print("- escalate_to_manager (custom)")
    print()

    # Test Case 1: Technical issue
    print("=== Test 1: Technical Issue ===")
    result1 = await Runner.run(
        main_agent,
        input="My software keeps crashing when I try to export data. I've tried restarting but it doesn't help."
    )
    print(f"Result: {result1.final_output}")
    print()

    # Test Case 2: Sales inquiry
    print("=== Test 2: Sales Inquiry ===")
    result2 = await Runner.run(
        main_agent,
        input="I'm interested in upgrading my plan. Can you tell me about the premium features and pricing?"
    )
    print(f"Result: {result2.final_output}")
    print()

    # Test Case 3: Complaint requiring escalation
    print("=== Test 3: Complaint Requiring Escalation ===")
    result3 = await Runner.run(
        main_agent,
        input="This is unacceptable! I've been charged for a service I cancelled three months ago. I want to speak to a manager immediately!"
    )
    print(f"Result: {result3.final_output}")
    print()

    # Test Case 4: Complex technical issue that might need escalation
    print("=== Test 4: Complex Issue ===")
    result4 = await Runner.run(
        main_agent,
        input="I've been having issues with data corruption in your system. This has affected my business operations and I may need compensation."
    )
    print(f"Result: {result4.final_output}")
    print()

    # Demonstrate handoff customization benefits
    print("=== Handoff Customization Benefits ===")
    benefits = """
    1. Custom Tool Names:
       - 'get_technical_help' is more descriptive than 'transfer_to_technical_agent'
       - Better LLM understanding of when to use each handoff
    
    2. Custom Descriptions:
       - Provide specific guidance on when to use each handoff
       - Help LLM make better transfer decisions
    
    3. Callbacks (on_handoff):
       - Execute custom logic when handoffs occur
       - Log events, update systems, send notifications
       - Prepare context for receiving agent
    
    4. Multiple Handoffs to Same Agent:
       - Different contexts (escalation vs normal transfer)
       - Different triggers and behaviors
       - Flexible routing based on situation
    """
    print(benefits)


if __name__ == "__main__":
    asyncio.run(main())
