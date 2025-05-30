# Handoff Inputs with Pydantic Models Example
# https://openai.github.io/openai-agents-python/handoffs/

import asyncio
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from agents import Agent, Runner, handoff, RunContextWrapper


# =============================================================================
# PYDANTIC MODELS FOR HANDOFF INPUTS
# =============================================================================

class IssueType(str, Enum):
    """Types of customer service issues"""
    BILLING = "billing"
    TECHNICAL = "technical"
    REFUND = "refund"
    GENERAL = "general"
    COMPLAINT = "complaint"


class Priority(str, Enum):
    """Issue priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class EscalationData(BaseModel):
    """Data passed when escalating to manager"""
    reason: str = Field(..., description="Reason for escalation")
    issue_type: IssueType = Field(...,
                                  description="Type of issue being escalated")
    priority: Priority = Field(
        default=Priority.MEDIUM, description="Priority level")
    customer_sentiment: str = Field(...,
                                    description="Customer's emotional state")
    attempted_solutions: List[str] = Field(
        default_factory=list, description="Solutions already attempted")


class TechnicalHandoffData(BaseModel):
    """Data passed when transferring to technical support"""
    problem_description: str = Field(...,
                                     description="Detailed problem description")
    error_messages: Optional[str] = Field(
        None, description="Any error messages encountered")
    system_info: Optional[str] = Field(
        None, description="Relevant system information")
    urgency: Priority = Field(default=Priority.MEDIUM,
                              description="Technical urgency level")
    troubleshooting_done: List[str] = Field(
        default_factory=list, description="Troubleshooting steps already performed")


class SalesHandoffData(BaseModel):
    """Data passed when transferring to sales"""
    interest_area: str = Field(...,
                               description="What the customer is interested in")
    budget_range: Optional[str] = Field(
        None, description="Customer's budget range if mentioned")
    timeline: Optional[str] = Field(
        None, description="Customer's timeline for purchase")
    current_plan: Optional[str] = Field(
        None, description="Customer's current plan or service level")
    specific_questions: List[str] = Field(
        default_factory=list, description="Specific questions customer has")


class RefundRequestData(BaseModel):
    """Data passed when processing refund requests"""
    item_or_service: str = Field(...,
                                 description="What the customer wants to refund")
    purchase_date: Optional[str] = Field(
        None, description="When the purchase was made")
    reason_for_refund: str = Field(...,
                                   description="Why the customer wants a refund")
    order_number: Optional[str] = Field(
        None, description="Order or invoice number if provided")
    refund_amount: Optional[str] = Field(
        None, description="Expected refund amount if mentioned")


# =============================================================================
# CALLBACK FUNCTIONS WITH INPUT DATA
# =============================================================================

async def on_escalation_with_data(ctx: RunContextWrapper[None], input_data: EscalationData):
    """Handle escalation with structured data"""
    print(f"🚨 ESCALATION ALERT:")
    print(f"   Reason: {input_data.reason}")
    print(f"   Issue Type: {input_data.issue_type.value}")
    print(f"   Priority: {input_data.priority.value}")
    print(f"   Customer Sentiment: {input_data.customer_sentiment}")
    print(f"   Attempted Solutions: {', '.join(input_data.attempted_solutions) if input_data.attempted_solutions else 'None'}")

    # In real implementation:
    # - Create escalation ticket in system
    # - Send notification to managers
    # - Update customer priority flags
    # - Log escalation metrics


async def on_technical_with_data(ctx: RunContextWrapper[None], input_data: TechnicalHandoffData):
    """Handle technical transfer with structured data"""
    print(f"🔧 TECHNICAL HANDOFF:")
    print(f"   Problem: {input_data.problem_description}")
    print(f"   Urgency: {input_data.urgency.value}")
    print(f"   Error Messages: {input_data.error_messages or 'None provided'}")
    print(f"   System Info: {input_data.system_info or 'None provided'}")
    print(f"   Previous Troubleshooting: {', '.join(input_data.troubleshooting_done) if input_data.troubleshooting_done else 'None'}")

    # In real implementation:
    # - Create technical support ticket
    # - Attach diagnostic data
    # - Set priority flags
    # - Prepare technical context


async def on_sales_with_data(ctx: RunContextWrapper[None], input_data: SalesHandoffData):
    """Handle sales transfer with structured data"""
    print(f"💰 SALES HANDOFF:")
    print(f"   Interest: {input_data.interest_area}")
    print(f"   Budget: {input_data.budget_range or 'Not specified'}")
    print(f"   Timeline: {input_data.timeline or 'Not specified'}")
    print(f"   Current Plan: {input_data.current_plan or 'Unknown'}")
    print(f"   Questions: {', '.join(input_data.specific_questions) if input_data.specific_questions else 'General inquiry'}")

    # In real implementation:
    # - Update CRM with lead data
    # - Set sales context
    # - Prepare customer profile
    # - Schedule follow-up if needed


async def on_refund_with_data(ctx: RunContextWrapper[None], input_data: RefundRequestData):
    """Handle refund request with structured data"""
    print(f"💸 REFUND REQUEST:")
    print(f"   Item/Service: {input_data.item_or_service}")
    print(f"   Purchase Date: {input_data.purchase_date or 'Not provided'}")
    print(f"   Reason: {input_data.reason_for_refund}")
    print(f"   Order Number: {input_data.order_number or 'Not provided'}")
    print(f"   Expected Amount: {input_data.refund_amount or 'Not specified'}")

    # In real implementation:
    # - Look up order in system
    # - Check refund eligibility
    # - Prepare refund processing
    # - Update customer account


async def main():
    """Demonstrate handoffs with structured input data."""

    # Create specialized agents
    escalation_agent = Agent(
        name="Manager",
        instructions="You are a customer service manager. Handle escalated issues with authority and care."
    )

    technical_agent = Agent(
        name="Technical Support",
        instructions="You are a technical support specialist. Solve technical problems with expertise."
    )

    sales_agent = Agent(
        name="Sales Representative",
        instructions="You are a sales representative. Help customers find the right solutions."
    )

    refund_agent = Agent(
        name="Refund Specialist",
        instructions="You are a refund specialist. Process refund requests fairly and efficiently."
    )

    # Create main agent with handoffs that expect input data
    main_agent = Agent(
        name="Customer Service Agent",
        instructions="""You are a customer service agent. When you need to transfer customers, 
        provide detailed information about their situation using the structured handoff inputs.
        
        For escalations: Include reason, issue type, priority, customer sentiment, and attempted solutions.
        For technical issues: Include problem description, error messages, system info, urgency, and troubleshooting done.
        For sales inquiries: Include interest area, budget, timeline, current plan, and specific questions.
        For refund requests: Include item/service, purchase date, reason, order number, and expected amount.
        
        Extract as much relevant information as possible from the conversation to populate these fields.""",
        handoffs=[
            handoff(
                agent=escalation_agent,
                tool_name_override="escalate_to_manager",
                tool_description_override="Escalate complex issues to manager with detailed context",
                on_handoff=on_escalation_with_data,
                input_type=EscalationData
            ),

            handoff(
                agent=technical_agent,
                tool_name_override="transfer_to_technical",
                tool_description_override="Transfer to technical support with problem details",
                on_handoff=on_technical_with_data,
                input_type=TechnicalHandoffData
            ),

            handoff(
                agent=sales_agent,
                tool_name_override="connect_with_sales",
                tool_description_override="Connect with sales team with customer interest data",
                on_handoff=on_sales_with_data,
                input_type=SalesHandoffData
            ),

            handoff(
                agent=refund_agent,
                tool_name_override="process_refund_request",
                tool_description_override="Transfer to refund specialist with request details",
                on_handoff=on_refund_with_data,
                input_type=RefundRequestData
            )
        ]
    )

    print("=== Customer Service with Structured Handoffs ===")
    print()

    # Test Case 1: Escalation with detailed context
    print("=== Test 1: Escalation with Context ===")
    result1 = await Runner.run(
        main_agent,
        input="""I am extremely frustrated! I've been trying to resolve a billing issue for three weeks. 
        I've called twice, sent two emails, and even tried the online chat. Each time I'm told someone 
        will call me back within 24 hours, but no one ever does. This is a billing error where I'm being 
        charged $500 for a service I never signed up for. I want to speak to a manager RIGHT NOW!"""
    )
    print(f"Result: {result1.final_output}")
    print()

    # Test Case 2: Technical issue with details
    print("=== Test 2: Technical Issue with Details ===")
    result2 = await Runner.run(
        main_agent,
        input="""My application keeps crashing when I try to upload files larger than 10MB. I get an error 
        message that says "Memory allocation failed - Error Code: 0x80070057". I'm running Windows 11 with 
        16GB RAM. I've already tried restarting the application, clearing the cache, and running as administrator. 
        This is urgent because I have a project deadline tomorrow."""
    )
    print(f"Result: {result2.final_output}")
    print()

    # Test Case 3: Sales inquiry with specific needs
    print("=== Test 3: Sales Inquiry with Specific Needs ===")
    result3 = await Runner.run(
        main_agent,
        input="""I'm currently on your Basic plan but I'm interested in upgrading to get more storage and 
        better performance. My budget is around $50-100 per month. I need this by the end of next month 
        when my current contract expires. I have specific questions about the API rate limits, backup 
        options, and whether I can get a custom domain. Can you connect me with sales?"""
    )
    print(f"Result: {result3.final_output}")
    print()

    # Test Case 4: Refund request with details
    print("=== Test 4: Refund Request with Details ===")
    result4 = await Runner.run(
        main_agent,
        input="""I need to request a refund for the Premium subscription I purchased on January 15th. 
        Order number is ORD-2024-001234. I'm requesting a refund because the features don't work as 
        advertised - specifically the AI analysis feature that was the main reason I upgraded. 
        I paid $299 for the annual plan and would like a full refund."""
    )
    print(f"Result: {result4.final_output}")
    print()

    # Demonstrate the value of structured inputs
    print("=== Benefits of Structured Handoff Inputs ===")
    benefits = """
    1. Data Consistency:
       - Ensures all relevant information is captured
       - Standardizes data format across handoffs
       - Reduces information loss during transfers
    
    2. Validation:
       - Pydantic models validate input data
       - Catch missing or invalid information early
       - Ensure data quality for receiving agents
    
    3. Processing Automation:
       - Callbacks can automatically process structured data
       - Create tickets, update systems, send notifications
       - Prepare context for receiving agents
    
    4. Analytics and Reporting:
       - Structured data enables better analytics
       - Track escalation reasons, issue types, priorities
       - Measure handoff effectiveness and outcomes
    
    5. Agent Context:
       - Receiving agents get rich, structured context
       - Better understanding of customer situation
       - More effective problem resolution
    """
    print(benefits)


if __name__ == "__main__":
    asyncio.run(main())
