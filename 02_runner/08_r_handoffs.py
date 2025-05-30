"""
08_runner_and_handoffs_loop.py

Focuses on the Runner's role in handling handoffs within the agent loop.

- Runner processing a handoff instruction from an agent.
- Runner updating the current agent and input for the new target agent.
- Runner re-running the loop with the new agent.
- Illustrating the role of `handoff_description`.

Based on: https://openai.github.io/openai-agents-python/running_agents/#the-agent-loop
And general handoff concepts.
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, Handoff

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# --- Agents for Handoff Demo ---

# Specialist Agent 1: Customer Support for Technical Issues
tech_support_agent = Agent(
    name="TechSupportAgent",
    instructions="You are a technical support specialist. Help users with technical problems related to our software.",
    model=OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=provider),
    handoff_description="For technical software issues, error messages, and bug reports."
)

# Specialist Agent 2: Customer Support for Billing Inquiries
billing_support_agent = Agent(
    name="BillingSupportAgent",
    instructions="You are a billing support specialist. Help users with questions about invoices, payments, and subscriptions.",
    model=OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=provider),
    handoff_description="For billing questions, invoice clarification, payment issues, and subscription management."
)

router_agent = Agent(
    name="SupportRouterAgent",
    instructions=(
        "You are a customer support router. Analyze the user's query and decide if it needs to be handled "
        "by a technical specialist or a billing specialist. Then, handoff to the appropriate agent. "
        "If unsure, ask clarifying questions. Provide the specialist agent's handoff_description in your reasoning if you handoff."
        "\n\nAvailable Specialists:"
        f"\n- {tech_support_agent.name}: {tech_support_agent.handoff_description}"
        f"\n- {billing_support_agent.name}: {billing_support_agent.handoff_description}"
    ),
    model=OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=provider),
    # The LLM will choose based on instructions. The Handoff objects here allow the mechanism.
    handoffs=[
        tech_support_agent,
        billing_support_agent
    ]
)


async def demo_runner_facilitating_handoff(user_query: str, expected_handler_name: str):
    print(
        f"\n--- Demo: Runner facilitating handoff for query: '{user_query}' ---")
    print(f"Input: {user_query}")

    result = await Runner.run(
        starting_agent=router_agent,
        input=user_query
    )

    print(f"Final Output: {result.final_output}")
    
    print(f"Last Agent: {result.last_agent}")
    
    print(f"History: {result.to_input_list()}")


async def main():
    print("--- Running 08_runner_and_handoffs_loop.py ---")

    await demo_runner_facilitating_handoff(
        user_query="I'm getting a 'null pointer exception' when I try to save my work.",
        expected_handler_name=tech_support_agent.name
    )

    await demo_runner_facilitating_handoff(
        user_query="I think I was overcharged on my last invoice. Can you check?",
        expected_handler_name=billing_support_agent.name
    )

    await demo_runner_facilitating_handoff(
        user_query="What's the weather like today?",  # Query not for tech or billing
        expected_handler_name=router_agent.name  # Router should handle it or ask
    )

    print("\n--- Finished 08_runner_and_handoffs_loop.py ---")

if __name__ == "__main__":
    asyncio.run(main())
