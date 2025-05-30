# Error Handling in Handoffs Example
# https://openai.github.io/openai-agents-python/handoffs/

import asyncio
from typing import Optional
from pydantic import BaseModel
from agents import Agent, Runner, handoff, function_tool, RunContextWrapper
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions



customer_service_agent = Agent(
    name="Customer Service",
    instructions="You are a customer service agent. You are responsible for helping customers with their issues.",
)

billing_agent = Agent(
    name="Billing",
    instructions="You are a billing agent. You are responsible for helping customers with their billing issues.",
    model="gpt-4o-min"
)




async def main():
    """Demonstrate comprehensive error handling in handoffs."""

    # Create main agent with error-handling handoffs
    main_agent = Agent(
        name="Error-Handling Customer Service",
        instructions=prompt_with_handoff_instructions("""
        You are a customer service agent with advanced error handling capabilities.
        
        When transferring customers:
        1. Always validate the transfer requirements first
        2. Check agent availability before attempting handoff
        3. If errors occur, implement recovery strategies
        4. Keep customers informed about any service issues
        5. Use fallback agents when primary agents are unavailable
        
        Error handling priorities:
        1. Customer experience comes first
        2. Transparent communication about issues
        3. Quick recovery and alternative solutions
        4. Learning from errors to prevent recurrence
        """),
        handoffs=[
            customer_service_agent,
            handoff(
                agent=billing_agent,
            )
            
        ]
    )

    print("=== Error Handling in Handoffs ===")
    print()

    # Test Case 1: Successful handoff with validation
    print("=== Test 1: Successful Handoff ===")
    try:
        result1 = await Runner.run(
            main_agent,
            input="Customer ID: valid_customer. I have a billing issue that needs specialist help. Ask why portal for billing is down"
        )
        print(f"Result: {result1.final_output}")
        print(f"Result: {result1.last_agent}")
    except Exception as e:
        print(f"Error in test case 1: {str(e)}")
    print()

    # Test Case 2: Handoff with validation error
    # print("=== Test 2: Validation Error ===")
    # try:
    #     result2 = await Runner.run(
    #         main_agent,
    #         input="Customer ID: invalid_customer. I need technical help but my account seems to have issues."
    #     )
    #     print(f"Result: {result2.final_output}")
    #     print(f"Result: {result2.last_agent}")
    # except Exception as e:
    #     print(f"Error in test case 2: {str(e)}")
    # print()


if __name__ == "__main__":
    asyncio.run(main())
