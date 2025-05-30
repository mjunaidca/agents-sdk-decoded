# Basic Handoffs Example
# https://openai.github.io/openai-agents-python/handoffs/

import asyncio
from agents import Agent, Runner


async def main():
    """Demonstrate basic handoffs between specialized agents."""

    # Create specialized agents
    billing_agent = Agent(
        name="Billing Agent",
        instructions="""You are a billing specialist. You help customers with:
        - Invoice questions
        - Payment issues
        - Billing history
        - Account balance inquiries
        
        Provide clear, helpful responses about billing matters."""
    )

    refund_agent = Agent(
        name="Refund Agent",
        instructions="""You are a refund specialist. You help customers with:
        - Refund requests
        - Return policies
        - Processing refunds
        - Refund status checks
        
        Be empathetic and helpful when processing refund requests."""
    )

    support_agent = Agent(
        name="Support Agent",
        instructions="""You are a general support specialist. You help with:
        - Account issues
        - Technical problems
        - General questions
        - Product information
        
        Provide comprehensive support for general inquiries."""
    )

    # Create triage agent with handoffs to specialized agents
    triage_agent = Agent(
        name="Triage Agent",
        instructions="""You are a customer service triage agent. Your job is to:
        1. Understand the customer's request
        2. Determine which specialist can best help them
        3. Transfer them to the appropriate agent
        
        Available specialists:
        - Billing Agent: For all billing, payment, and invoice questions
        - Refund Agent: For refund requests and return-related issues  
        - Support Agent: For general support, technical issues, and product questions
        
        Always explain why you're transferring them to help set expectations.""",
        handoffs=[billing_agent, refund_agent,
                  support_agent]  # Direct agent references
    )

    print("=== Customer Service Triage System ===")
    print("Available agents:", [agent.name for agent in triage_agent.handoffs])
    print()

    # Test Case 1: Billing question
    print("=== Test 1: Billing Question ===")
    result1 = await Runner.run(
        triage_agent,
        input="Hi, I have a question about my last invoice. It seems like I was charged twice for the same service."
    )
    print(f"Triage Result: {result1.final_output}")
    print()

    # Test Case 2: Refund request
    print("=== Test 2: Refund Request ===")
    result2 = await Runner.run(
        triage_agent,
        input="I'd like to return a product I bought last week and get a refund. The item doesn't work as expected."
    )
    print(f"Triage Result: {result2.final_output}")
    print()

    # Test Case 3: General support
    print("=== Test 3: General Support ===")
    result3 = await Runner.run(
        triage_agent,
        input="I'm having trouble logging into my account. It keeps saying my password is wrong but I'm sure it's correct."
    )
    print(f"Triage Result: {result3.final_output}")
    print()

    # Test Case 4: Ambiguous request
    print("=== Test 4: Ambiguous Request ===")
    result4 = await Runner.run(
        triage_agent,
        input="Hello, I need help with my account."
    )
    print(f"Triage Result: {result4.final_output}")
    print()

    # Demonstrate available handoff tools
    print("=== Available Handoff Tools ===")
    if hasattr(triage_agent, '_handoff_tools'):
        for tool in triage_agent._handoff_tools:
            print(f"Tool: {tool.name}")
            print(f"Description: {tool.description}")
            print()
    else:
        print("Handoff tools are generated automatically by the SDK")
        print("Expected tools:")
        print("- transfer_to_billing_agent")
        print("- transfer_to_refund_agent")
        print("- transfer_to_support_agent")


if __name__ == "__main__":
    asyncio.run(main())
