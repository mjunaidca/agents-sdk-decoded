# Recommended Prompts for Handoffs Example
# https://openai.github.io/openai-agents-python/handoffs/

import asyncio
from agents import Agent, Runner, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX, prompt_with_handoff_instructions


async def main():
    """Demonstrate recommended prompt patterns for better handoff understanding."""

    # Method 1: Using RECOMMENDED_PROMPT_PREFIX directly
    billing_agent_manual = Agent(
        name="Billing Agent (Manual Prompt)",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
        
        You are a billing specialist who helps customers with:
        - Invoice questions and disputes
        - Payment processing issues
        - Account balance inquiries
        - Subscription management
        - Billing policy explanations
        
        Always be professional and thorough when resolving billing matters.
        If you cannot resolve an issue, you may transfer the customer to:
        - Management for policy exceptions
        - Technical support for system-related billing issues
        - Collections for overdue account matters
        """
    )

    # Method 2: Using prompt_with_handoff_instructions helper
    refund_agent_helper = Agent(
        name="Refund Agent (Helper Method)",
        instructions=prompt_with_handoff_instructions("""
        You are a refund processing specialist. Your responsibilities include:
        - Evaluating refund requests against company policy
        - Processing approved refunds through the system
        - Explaining refund policies to customers
        - Handling disputed charges and chargebacks
        - Coordinating with billing for complex refund cases
        
        Be empathetic but firm about policy requirements.
        Ensure all refunds comply with legal and company guidelines.
        """)
    )

    # Create specialized agents with recommended prompts
    technical_agent = Agent(
        name="Technical Support",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
        
        You are a technical support specialist providing:
        - Software troubleshooting and bug resolution
        - System configuration assistance  
        - Integration support and API guidance
        - Performance optimization recommendations
        - Security and compliance technical advice
        
        Provide detailed, step-by-step technical solutions.
        Document all technical interactions for knowledge base updates.
        """)

    escalation_agent = Agent(
        name="Customer Success Manager",
        instructions=prompt_with_handoff_instructions("""
        You are a Customer Success Manager handling escalated issues:
        - Complex account problems requiring management authority
        - Customer retention and satisfaction concerns
        - Contract negotiations and custom arrangements
        - Multi-department coordination for resolution
        - Policy exception approvals within guidelines
        
        Focus on preserving customer relationships while protecting company interests.
        You have authority to make exceptions within defined limits.
        """)
    )

    # Create triage agent with recommended prompts and handoffs
    triage_agent = Agent(
        name="Customer Service Triage",
        instructions=prompt_with_handoff_instructions("""
        You are a customer service triage agent responsible for:
        1. Understanding customer needs through active listening
        2. Providing initial support and basic troubleshooting
        3. Routing customers to the most appropriate specialist
        4. Setting clear expectations about the transfer process
        
        Available specialist teams:
        - Billing Agent: Invoice questions, payments, account balance issues
        - Refund Agent: Return requests, refund processing, disputed charges  
        - Technical Support: Software issues, system problems, integration help
        - Customer Success Manager: Complex issues requiring management attention
        
        Guidelines for transfers:
        - Always explain WHY you're transferring the customer
        - Summarize the issue for the receiving agent
        - Set expectations about what the specialist can help with
        - Ensure the customer feels heard and understood before transferring
        """),
        handoffs=[
            handoff(
                agent=billing_agent_manual,
                tool_name_override="transfer_to_billing",
                tool_description_override="Transfer to billing specialist for payment and invoice issues"
            ),
            handoff(
                agent=refund_agent_helper,
                tool_name_override="transfer_to_refunds",
                tool_description_override="Transfer to refund specialist for return and refund requests"
            ),
            handoff(
                agent=technical_agent,
                tool_name_override="transfer_to_technical",
                tool_description_override="Transfer to technical support for software and system issues"
            ),
            handoff(
                agent=escalation_agent,
                tool_name_override="escalate_to_manager",
                tool_description_override="Escalate complex issues to Customer Success Manager"
            )
        ]
    )

    print("=== Recommended Prompts for Better Handoffs ===")
    print()

    # Demonstrate the recommended prompt content
    print("=== Recommended Prompt Prefix Content ===")
    print(f"RECOMMENDED_PROMPT_PREFIX:\n{RECOMMENDED_PROMPT_PREFIX}")
    print()

    # Test Case 1: Billing issue with proper explanation
    print("=== Test 1: Billing Issue (Should explain transfer) ===")
    result1 = await Runner.run(
        triage_agent,
        input="I received a charge on my credit card that I don't recognize. It's for $99.99 from your company but I didn't make any purchases recently."
    )
    print(f"Result: {result1.final_output}")
    print()

    # Test Case 2: Refund request with context
    print("=== Test 2: Refund Request (Should set expectations) ===")
    result2 = await Runner.run(
        triage_agent,
        input="I want to return a product I bought last month. It doesn't work as advertised and I'd like my money back."
    )
    print(f"Result: {result2.final_output}")
    print()

    # Test Case 3: Technical issue requiring specialist
    print("=== Test 3: Technical Issue (Should summarize for specialist) ===")
    result3 = await Runner.run(
        triage_agent,
        input="Your API keeps returning 500 errors when I try to upload files. I've checked my API key and it's valid. This is blocking my production deployment."
    )
    print(f"Result: {result3.final_output}")
    print()

    # Test Case 4: Complex issue requiring escalation
    print("=== Test 4: Complex Escalation (Should provide context) ===")
    result4 = await Runner.run(
        triage_agent,
        input="""This is extremely frustrating. I've been a customer for 3 years and this is the worst 
        service I've experienced. Your system deleted my data, billing charged me during a service outage, 
        and now I'm told there's no backup. I want to speak to someone with actual authority to fix this 
        disaster and compensate me for the business I've lost."""
    )
    print(f"Result: {result4.final_output}")
    print()

    # Test Case 5: Ambiguous request that needs clarification
    print("=== Test 5: Ambiguous Request (Should gather info before transfer) ===")
    result5 = await Runner.run(
        triage_agent,
        input="Hi, I need help with my account."
    )
    print(f"Result: {result5.final_output}")
    print()

    # Show the difference between agents with and without recommended prompts
    print("=== Comparison: With vs Without Recommended Prompts ===")

    # Agent without recommended prompts
    basic_agent = Agent(
        name="Basic Agent",
        instructions="You help customers and can transfer them to specialists.",
        handoffs=[billing_agent_manual]
    )

    print("Agent WITHOUT recommended prompts:")
    result_basic = await Runner.run(
        basic_agent,
        input="I have a billing problem and need help."
    )
    print(f"Basic Result: {result_basic.final_output}")
    print()

    print("Agent WITH recommended prompts (from above):")
    result_recommended = await Runner.run(
        triage_agent,
        input="I have a billing problem and need help."
    )
    print(f"Recommended Result: {result_recommended.final_output}")
    print()

    # Explain the benefits
    print("=== Benefits of Recommended Prompts ===")
    benefits = """
    The recommended prompts help LLMs understand handoffs better by:
    
    1. Transfer Context:
       - Explains WHY transfers are happening
       - Sets customer expectations appropriately
       - Provides context to receiving agents
    
    2. Better Decision Making:
       - Helps LLM understand when to transfer vs handle directly
       - Improves specialist selection accuracy
       - Reduces inappropriate transfers
    
    3. Professional Communication:
       - Maintains consistent tone during transfers
       - Ensures customers feel heard and understood
       - Provides smooth transition experience
    
    4. Conversation Flow:
       - Maintains context across agent boundaries
       - Summarizes key points for specialists
       - Reduces need for customers to repeat information
    
    5. Usage Options:
       - RECOMMENDED_PROMPT_PREFIX: Manual inclusion in instructions
       - prompt_with_handoff_instructions(): Automatic helper function
       - Both approaches ensure consistent handoff behavior
    
    Best Practice: Always use recommended prompts for agents that perform handoffs
    to ensure optimal LLM understanding and customer experience.
    """
    print(benefits)


if __name__ == "__main__":
    asyncio.run(main())
