# Input Filters Example
# https://openai.github.io/openai-agents-python/handoffs/

import asyncio
from agents import Agent, Runner, handoff, function_tool
from agents.extensions import handoff_filters
from agents.handoffs import HandoffInputData


# =============================================================================
# CUSTOM INPUT FILTER FUNCTIONS
# =============================================================================

def remove_sensitive_info(input_data: HandoffInputData) -> HandoffInputData:
    """Custom filter to remove sensitive information from conversation history."""

    def clean_message(text: str) -> str:
        """Remove sensitive patterns from text."""
        import re

        # Remove credit card numbers (basic pattern)
        text = re.sub(
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CREDIT_CARD_REDACTED]', text)

        # Remove SSN patterns
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]', text)

        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                      '[PHONE_REDACTED]', text)

        # Remove email addresses
        text = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)

        return text

    # Process conversation history
    if isinstance(input_data.input_history, str):
        cleaned_history = clean_message(input_data.input_history)
    else:
        # For tuple of items, would need to process each item
        # This is a simplified version
        cleaned_history = input_data.input_history

    return HandoffInputData(
        input_history=cleaned_history,
        pre_handoff_items=input_data.pre_handoff_items,
        new_items=input_data.new_items
    )


def summarize_conversation(input_data: HandoffInputData) -> HandoffInputData:
    """Custom filter to provide a summary instead of full conversation history."""

    # In a real implementation, you might use an LLM to summarize
    # Here we'll create a simple summary
    summary = """
    CONVERSATION SUMMARY:
    - Customer contacted support with an issue
    - Initial troubleshooting was attempted
    - Issue requires specialist attention
    - Customer information and context preserved
    - Transferring to appropriate specialist
    """

    return HandoffInputData(
        input_history=summary.strip(),
        pre_handoff_items=input_data.pre_handoff_items,
        new_items=input_data.new_items
    )


def privacy_focused_filter(input_data: HandoffInputData) -> HandoffInputData:
    """Filter that removes all previous conversation for privacy."""

    privacy_message = """
    PRIVACY PROTECTED HANDOFF:
    - Previous conversation history removed for privacy
    - Customer context maintained through structured handoff data
    - Specialist agent should gather necessary information directly
    """

    return HandoffInputData(
        input_history=privacy_message.strip(),
        pre_handoff_items=(),  # Remove previous items
        new_items=input_data.new_items
    )


# =============================================================================
# DEMO TOOLS FOR TESTING
# =============================================================================

@function_tool
def get_customer_info(customer_id: str) -> str:
    """Simulate getting customer information."""
    return f"Customer {customer_id}: Premium member since 2020, last contact 2 days ago"


@function_tool
def log_interaction(interaction_type: str, details: str) -> str:
    """Simulate logging customer interactions."""
    return f"Logged {interaction_type}: {details}"


async def main():
    """Demonstrate various input filters for handoffs."""

    # Create specialized agents
    billing_agent = Agent(
        name="Billing Specialist",
        instructions="""You are a billing specialist. Help customers with billing issues.
        You receive filtered conversation history based on privacy and security needs.""",
        tools=[get_customer_info, log_interaction]
    )

    privacy_agent = Agent(
        name="Privacy Specialist",
        instructions="""You are a privacy specialist. Handle sensitive data requests.
        You receive minimal conversation history to protect customer privacy."""
    )

    technical_agent = Agent(
        name="Technical Support",
        instructions="""You are technical support. The conversation history has been 
        cleaned to remove sensitive information while preserving technical details."""
    )

    summary_agent = Agent(
        name="Senior Support",
        instructions="""You are senior support. You receive conversation summaries 
        instead of full transcripts to focus on key issues efficiently."""
    )

    # Create main agent with different filter strategies
    main_agent = Agent(
        name="Customer Service Agent",
        instructions="""You are a frontline customer service agent. Help customers 
        and transfer them to specialists when needed. Be aware that different 
        specialists receive different levels of conversation history based on their needs.""",
        tools=[get_customer_info, log_interaction],
        handoffs=[
            # No filter - full conversation history
            billing_agent,

            # Built-in filter - remove all tools from history
            handoff(
                agent=technical_agent,
                tool_name_override="transfer_to_technical_clean",
                tool_description_override="Transfer to technical support with clean conversation (no tool calls)",
                input_filter=handoff_filters.remove_all_tools
            ),

            # Custom filter - remove sensitive information
            handoff(
                agent=billing_agent,
                tool_name_override="transfer_to_billing_secure",
                tool_description_override="Transfer to billing with sensitive info removed",
                input_filter=remove_sensitive_info
            ),

            # Custom filter - conversation summary only
            handoff(
                agent=summary_agent,
                tool_name_override="escalate_with_summary",
                tool_description_override="Escalate to senior support with conversation summary",
                input_filter=summarize_conversation
            ),

            # Custom filter - privacy focused (minimal history)
            handoff(
                agent=privacy_agent,
                tool_name_override="transfer_to_privacy",
                tool_description_override="Transfer to privacy specialist with minimal conversation history",
                input_filter=privacy_focused_filter
            )
        ]
    )

    print("=== Input Filters for Handoffs ===")
    print("Available handoff options:")
    print("- transfer_to_billing_specialist (full history)")
    print("- transfer_to_technical_clean (no tool calls)")
    print("- transfer_to_billing_secure (sensitive info removed)")
    print("- escalate_with_summary (summary only)")
    print("- transfer_to_privacy (minimal history)")
    print()

    # Test Case 1: Normal handoff with full history
    print("=== Test 1: Standard Handoff (Full History) ===")
    result1 = await Runner.run(
        main_agent,
        input="Hi, I'm having issues with my billing. My credit card 1234-5678-9012-3456 was charged twice."
    )
    print(f"Result: {result1.final_output}")
    print()

    # Test Case 2: Technical handoff with tool calls removed
    print("=== Test 2: Technical Handoff (Tools Removed) ===")
    # First, create a conversation with tool usage
    result2a = await Runner.run(
        main_agent,
        input="Let me check my customer information first, then I need technical help with login issues."
    )

    # Then transfer to technical (this would remove tool calls from history)
    result2b = await Runner.run(
        main_agent,
        input="Please transfer me to technical support for the login issue."
    )
    print(f"Result: {result2b.final_output}")
    print()

    # Test Case 3: Billing handoff with sensitive info removed
    print("=== Test 3: Secure Billing Handoff (Sensitive Info Removed) ===")
    result3 = await Runner.run(
        main_agent,
        input="""I need help with billing. My details are:
        - SSN: 123-45-6789
        - Phone: 555-123-4567
        - Email: john.doe@example.com
        - Credit Card: 4532-1234-5678-9012
        
        I was charged incorrectly. Please transfer me to billing securely."""
    )
    print(f"Result: {result3.final_output}")
    print()

    # Test Case 4: Escalation with summary
    print("=== Test 4: Senior Support Escalation (Summary Only) ===")
    result4 = await Runner.run(
        main_agent,
        input="""This is a complex issue. I've been dealing with billing problems, tried technical solutions,
        spoke with multiple agents, and nothing is resolved. I need to escalate this to senior support
        but they don't need the full conversation - just a summary of the key issues."""
    )
    print(f"Result: {result4.final_output}")
    print()

    # Test Case 5: Privacy specialist with minimal history
    print("=== Test 5: Privacy Transfer (Minimal History) ===")
    result5 = await Runner.run(
        main_agent,
        input="""I need to speak with someone about data privacy and GDPR compliance. This is sensitive
        and I don't want my full conversation history shared. Please transfer me to your privacy specialist."""
    )
    print(f"Result: {result5.final_output}")
    print()

    # Demonstrate built-in filters
    print("=== Available Built-in Filters ===")
    builtin_info = """
    Built-in filters from agents.extensions.handoff_filters:
    
    1. remove_all_tools:
       - Removes all tool calls and tool outputs from conversation history
       - Useful when tools contain sensitive data or are not relevant to receiving agent
       - Preserves regular conversation messages
    
    2. Custom Filter Function Signature:
       def my_filter(input_data: HandoffInputData) -> HandoffInputData:
           # Process input_data.input_history (str or tuple)
           # Process input_data.pre_handoff_items (tuple of RunItem)
           # Process input_data.new_items (tuple of RunItem) 
           return HandoffInputData(...)
    
    3. Common Custom Filter Patterns:
       - Sensitive data removal (PII, credentials, etc.)
       - Conversation summarization for efficiency
       - Tool call filtering for specific tool types
       - Message type filtering (keep only user messages)
       - Privacy-focused minimal history transfer
       - Language translation for international handoffs
    """
    print(builtin_info)


if __name__ == "__main__":
    asyncio.run(main())
