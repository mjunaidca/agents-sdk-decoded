# Real-World Handoff Patterns Example
# https://openai.github.io/openai-agents-python/handoffs/

import asyncio
from typing import Optional, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from agents import Agent, Runner, handoff, function_tool, RunContextWrapper
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions


# =============================================================================
# INDUSTRY-SPECIFIC MODELS AND ENUMS
# =============================================================================

class IndustryType(str, Enum):
    """Different industry verticals"""
    ECOMMERCE = "ecommerce"
    HEALTHCARE = "healthcare"
    FINANCIAL = "financial"
    SAAS = "saas"
    TELECOM = "telecom"


class ComplianceLevel(str, Enum):
    """Compliance and security levels"""
    STANDARD = "standard"
    HIPAA = "hipaa"  # Healthcare
    PCI_DSS = "pci_dss"  # Payment processing
    SOX = "sox"  # Financial
    GDPR = "gdpr"  # Data privacy


class CustomerSegment(str, Enum):
    """Customer segments for different industries"""
    CONSUMER = "consumer"
    SMB = "small_medium_business"
    ENTERPRISE = "enterprise"
    HEALTHCARE_PROVIDER = "healthcare_provider"
    FINANCIAL_INSTITUTION = "financial_institution"


class HandoffContext(BaseModel):
    """Rich context for industry-specific handoffs"""
    industry: IndustryType
    compliance_requirements: List[ComplianceLevel] = Field(
        default_factory=list)
    customer_segment: CustomerSegment
    urgency_level: int = Field(ge=1, le=5, description="1=low, 5=critical")
    business_impact: Optional[str] = None
    regulatory_considerations: List[str] = Field(default_factory=list)
    previous_interactions: List[str] = Field(default_factory=list)


# =============================================================================
# INDUSTRY-SPECIFIC SIMULATION TOOLS
# =============================================================================

@function_tool
def check_compliance_requirements(industry: str, issue_type: str) -> str:
    """Check what compliance requirements apply to this handoff."""
    compliance_map = {
        "healthcare": ["HIPAA", "GDPR"],
        "financial": ["SOX", "PCI_DSS", "GDPR"],
        "ecommerce": ["PCI_DSS", "GDPR"],
        "saas": ["GDPR", "SOC2"],
        "telecom": ["GDPR", "TCPA"]
    }

    requirements = compliance_map.get(industry, ["STANDARD"])
    return f"Compliance requirements for {industry}: {', '.join(requirements)}"


@function_tool
def escalate_to_compliance_officer(issue_details: str, compliance_type: str) -> str:
    """Escalate to compliance officer for regulatory issues."""
    return f"COMPLIANCE ESCALATION: {compliance_type} issue - {issue_details}"


@function_tool
def create_audit_trail(agent_name: str, action: str, customer_data: str) -> str:
    """Create audit trail for compliance tracking."""
    timestamp = datetime.now().isoformat()
    return f"AUDIT: {timestamp} - {agent_name} performed {action} - Customer: {customer_data}"


@function_tool
def check_business_hours(timezone: str = "UTC") -> str:
    """Check if escalation is within business hours."""
    now = datetime.now()
    # Simplified business hours check
    if 9 <= now.hour <= 17:
        return "Within business hours - full staff available"
    else:
        return "Outside business hours - limited staff, emergency protocols active"


@function_tool
def calculate_sla_deadline(customer_segment: str, issue_type: str) -> str:
    """Calculate SLA deadline based on customer segment and issue type."""
    sla_matrix = {
        ("enterprise", "critical"): "1 hour",
        ("enterprise", "high"): "4 hours",
        ("smb", "critical"): "2 hours",
        ("smb", "high"): "8 hours",
        ("consumer", "critical"): "4 hours",
        ("consumer", "high"): "24 hours"
    }

    deadline = sla_matrix.get((customer_segment, issue_type), "48 hours")
    return f"SLA deadline: {deadline} from now"


# =============================================================================
# INDUSTRY-SPECIFIC AGENTS
# =============================================================================

# E-COMMERCE AGENTS
def create_ecommerce_order_agent():
    return Agent(
        name="E-commerce Order Specialist",
        instructions=prompt_with_handoff_instructions("""
        You are an e-commerce order specialist. You handle:
        - Order status inquiries and tracking
        - Shipping and delivery issues
        - Order modifications and cancellations
        - Return and refund processing
        - Inventory and availability questions
        
        For payment issues, transfer to Payment Security.
        For complex disputes, escalate to Customer Advocacy.
        Always maintain PCI compliance when handling payment data.
        """),
        tools=[create_audit_trail, calculate_sla_deadline]
    )


def create_payment_security_agent():
    return Agent(
        name="Payment Security Specialist",
        instructions=prompt_with_handoff_instructions("""
        You are a payment security specialist. You handle:
        - Payment processing issues
        - Fraud investigation and prevention
        - Chargeback disputes
        - PCI compliance matters
        - Account security concerns
        
        CRITICAL: Never store or log payment details.
        For regulatory issues, escalate to Compliance Officer.
        Maintain strict audit trails for all payment interactions.
        """),
        tools=[create_audit_trail, escalate_to_compliance_officer,
               check_compliance_requirements]
    )


# HEALTHCARE AGENTS
def create_healthcare_patient_services():
    return Agent(
        name="Patient Services Representative",
        instructions=prompt_with_handoff_instructions("""
        You are a patient services representative. You handle:
        - Appointment scheduling and rescheduling
        - Insurance verification and billing
        - General medical questions (non-diagnostic)
        - Portal access and technical support
        - Patient advocacy and concerns
        
        HIPAA COMPLIANCE CRITICAL:
        - Never discuss specific medical information without verification
        - Maintain strict patient privacy standards
        - Document all interactions in HIPAA-compliant manner
        
        For clinical questions, transfer to Clinical Support.
        For privacy concerns, escalate to Privacy Officer.
        """),
        tools=[create_audit_trail, check_compliance_requirements]
    )


def create_clinical_support_agent():
    return Agent(
        name="Clinical Support Specialist",
        instructions=prompt_with_handoff_instructions("""
        You are a clinical support specialist (typically a nurse). You handle:
        - Clinical questions and concerns
        - Medication and treatment questions
        - Symptom assessment and triage
        - Care coordination between providers
        - Clinical documentation support
        
        CRITICAL REQUIREMENTS:
        - Maintain HIPAA compliance at all times
        - Stay within scope of practice
        - Document all clinical interactions
        - Escalate urgent medical situations appropriately
        
        For emergencies, immediately escalate to Emergency Protocol.
        For complex cases, escalate to Physician Review.
        """),
        tools=[create_audit_trail, escalate_to_compliance_officer]
    )


# FINANCIAL SERVICES AGENTS
def create_financial_account_services():
    return Agent(
        name="Financial Account Services",
        instructions=prompt_with_handoff_instructions("""
        You are a financial account services representative. You handle:
        - Account balance and transaction inquiries
        - General banking questions
        - Card activation and basic services
        - Account maintenance requests
        - Service questions and support
        
        COMPLIANCE REQUIREMENTS:
        - Verify customer identity before discussing accounts
        - Maintain SOX compliance for all interactions
        - Follow KYC (Know Your Customer) procedures
        - Document all account interactions
        
        For fraud concerns, immediately transfer to Fraud Investigation.
        For investment questions, transfer to Investment Advisory.
        For complex compliance issues, escalate to Compliance Officer.
        """),
        tools=[create_audit_trail, check_compliance_requirements]
    )


def create_fraud_investigation_agent():
    return Agent(
        name="Fraud Investigation Specialist",
        instructions=prompt_with_handoff_instructions("""
        You are a fraud investigation specialist. You handle:
        - Suspected fraudulent transactions
        - Account security breaches
        - Identity theft reports
        - Disputed charges investigation
        - Risk assessment and mitigation
        
        CRITICAL SECURITY PROTOCOLS:
        - Verify customer identity through multiple factors
        - Immediate account protection measures
        - Coordinate with law enforcement when required
        - Maintain strict confidentiality
        - Document everything for legal compliance
        
        For regulatory reporting requirements, escalate to Compliance Officer.
        For law enforcement coordination, escalate to Legal Department.
        """),
        tools=[create_audit_trail,
               escalate_to_compliance_officer, check_business_hours]
    )


# SAAS SUPPORT AGENTS
def create_saas_technical_support():
    return Agent(
        name="SaaS Technical Support",
        instructions=prompt_with_handoff_instructions("""
        You are a SaaS technical support specialist. You handle:
        - Software functionality questions
        - Integration and API support
        - Performance and reliability issues
        - User training and best practices
        - Configuration and setup assistance
        
        For billing questions, transfer to Account Management.
        For enterprise customizations, escalate to Solutions Engineering.
        For critical outages, immediately escalate to Engineering.
        
        Always consider customer's business impact when prioritizing issues.
        """),
        tools=[create_audit_trail, calculate_sla_deadline, check_business_hours]
    )


def create_solutions_engineering():
    return Agent(
        name="Solutions Engineering",
        instructions=prompt_with_handoff_instructions("""
        You are a solutions engineer handling complex technical requirements:
        - Enterprise integration planning
        - Custom solution architecture
        - Performance optimization consulting
        - Security and compliance consulting
        - Technical escalation resolution
        
        Work closely with Customer Success for business alignment.
        Coordinate with Product Engineering for feature requests.
        Maintain technical documentation for complex solutions.
        """),
        tools=[create_audit_trail, escalate_to_compliance_officer]
    )


# =============================================================================
# INDUSTRY-SPECIFIC HANDOFF CALLBACKS
# =============================================================================

async def on_compliance_handoff(ctx: RunContextWrapper[None], handoff_data: HandoffContext):
    """Handle compliance-aware handoffs."""
    print(f"🔒 COMPLIANCE-AWARE HANDOFF:")
    print(f"   Industry: {handoff_data.industry}")
    print(
        f"   Compliance Requirements: {', '.join(handoff_data.compliance_requirements)}")
    print(f"   Customer Segment: {handoff_data.customer_segment}")
    print(f"   Urgency Level: {handoff_data.urgency_level}/5")

    if handoff_data.regulatory_considerations:
        print(
            f"   Regulatory Considerations: {', '.join(handoff_data.regulatory_considerations)}")


async def on_sla_tracking_handoff(ctx: RunContextWrapper[None], handoff_data: HandoffContext):
    """Track SLA requirements during handoffs."""
    print(f"⏱️ SLA TRACKING:")
    print(f"   Customer Segment: {handoff_data.customer_segment}")
    print(f"   Business Impact: {handoff_data.business_impact or 'Standard'}")
    print(f"   Urgency: {handoff_data.urgency_level}/5")

    # Calculate SLA based on context
    if handoff_data.urgency_level >= 4:
        print(f"   ⚠️ HIGH PRIORITY - Escalated SLA timeframes apply")


async def main():
    """Demonstrate real-world industry-specific handoff patterns."""

    print("=== Real-World Industry Handoff Patterns ===")
    print()

    # =============================================================================
    # E-COMMERCE SCENARIO
    # =============================================================================

    print("=== E-COMMERCE CUSTOMER SERVICE ===")

    # Create e-commerce agents
    order_agent = create_ecommerce_order_agent()
    payment_agent = create_payment_security_agent()

    ecommerce_orchestrator = Agent(
        name="E-commerce Customer Service",
        instructions=prompt_with_handoff_instructions("""
        You are an e-commerce customer service representative. Route customers based on:
        - Order-related issues → Order Specialist
        - Payment/fraud concerns → Payment Security (PCI compliance required)
        - Compliance issues → Escalate to Compliance Officer
        
        Always consider PCI and GDPR compliance requirements.
        Prioritize based on customer segment and business impact.
        """),
        tools=[check_compliance_requirements,
               calculate_sla_deadline, create_audit_trail],
        handoffs=[
            handoff(
                agent=order_agent,
                tool_name_override="transfer_to_order_specialist",
                tool_description_override="Transfer to order specialist for order-related issues",
                on_handoff=on_sla_tracking_handoff,
                input_type=HandoffContext
            ),
            handoff(
                agent=payment_agent,
                tool_name_override="escalate_to_payment_security",
                tool_description_override="Escalate to payment security for fraud/payment issues",
                on_handoff=on_compliance_handoff,
                input_type=HandoffContext
            )
        ]
    )

    # Test e-commerce scenario
    result_ecommerce = await Runner.run(
        ecommerce_orchestrator,
        input="""I'm an enterprise customer and there's a suspicious charge on my company credit card 
        for $5,000 that I didn't authorize. This is urgent as it could be fraud affecting our business operations."""
    )
    print(f"E-commerce Result: {result_ecommerce.final_output}")
    print()

    # =============================================================================
    # HEALTHCARE SCENARIO
    # =============================================================================

    print("=== HEALTHCARE PATIENT SERVICES ===")

    # Create healthcare agents
    patient_services = create_healthcare_patient_services()
    clinical_support = create_clinical_support_agent()

    healthcare_orchestrator = Agent(
        name="Healthcare Patient Support",
        instructions=prompt_with_handoff_instructions("""
        You are a healthcare patient support coordinator. HIPAA compliance is CRITICAL.
        
        Route patients based on:
        - Administrative questions → Patient Services
        - Clinical questions → Clinical Support (nurse-level)
        - Emergency situations → Immediate Emergency Protocol
        - Privacy concerns → Privacy Officer escalation
        
        NEVER discuss specific medical information without proper verification.
        Maintain audit trails for all patient interactions.
        """),
        tools=[check_compliance_requirements, create_audit_trail],
        handoffs=[
            handoff(
                agent=patient_services,
                tool_name_override="transfer_to_patient_services",
                tool_description_override="Transfer to patient services for administrative support",
                on_handoff=on_compliance_handoff,
                input_type=HandoffContext
            ),
            handoff(
                agent=clinical_support,
                tool_name_override="transfer_to_clinical_support",
                tool_description_override="Transfer to clinical support for medical questions",
                on_handoff=on_compliance_handoff,
                input_type=HandoffContext
            )
        ]
    )

    # Test healthcare scenario
    result_healthcare = await Runner.run(
        healthcare_orchestrator,
        input="""I'm concerned about some side effects I'm experiencing from my new medication. 
        I'd like to speak with someone who can help me understand if this is normal and what I should do."""
    )
    print(f"Healthcare Result: {result_healthcare.final_output}")
    print()

    # =============================================================================
    # FINANCIAL SERVICES SCENARIO
    # =============================================================================

    print("=== FINANCIAL SERVICES ===")

    # Create financial agents
    account_services = create_financial_account_services()
    fraud_investigation = create_fraud_investigation_agent()

    financial_orchestrator = Agent(
        name="Financial Services Support",
        instructions=prompt_with_handoff_instructions("""
        You are a financial services support coordinator. Regulatory compliance is mandatory.
        
        Route customers based on:
        - General account questions → Account Services
        - Fraud/security concerns → Fraud Investigation (immediate)
        - Investment questions → Investment Advisory
        - Compliance issues → Compliance Officer
        
        ALWAYS verify customer identity before account discussions.
        Maintain SOX compliance and audit trails.
        Prioritize fraud and security issues immediately.
        """),
        tools=[check_compliance_requirements,
               create_audit_trail, check_business_hours],
        handoffs=[
            handoff(
                agent=account_services,
                tool_name_override="transfer_to_account_services",
                tool_description_override="Transfer to account services for general banking support",
                on_handoff=on_compliance_handoff,
                input_type=HandoffContext
            ),
            handoff(
                agent=fraud_investigation,
                tool_name_override="escalate_to_fraud_investigation",
                tool_description_override="IMMEDIATE escalation to fraud investigation",
                on_handoff=on_compliance_handoff,
                input_type=HandoffContext
            )
        ]
    )

    # Test financial services scenario
    result_financial = await Runner.run(
        financial_orchestrator,
        input="""I noticed several unauthorized transactions on my business account totaling $50,000. 
        These transactions occurred overnight and I definitely did not authorize them. This is a major emergency."""
    )
    print(f"Financial Result: {result_financial.final_output}")
    print()

    # =============================================================================
    # SAAS SUPPORT SCENARIO
    # =============================================================================

    print("=== SAAS TECHNICAL SUPPORT ===")

    # Create SaaS agents
    tech_support = create_saas_technical_support()
    solutions_eng = create_solutions_engineering()

    saas_orchestrator = Agent(
        name="SaaS Customer Success",
        instructions=prompt_with_handoff_instructions("""
        You are a SaaS customer success coordinator. Focus on business outcomes.
        
        Route customers based on:
        - Technical issues → Technical Support
        - Complex integrations → Solutions Engineering
        - Billing/account changes → Account Management
        - Feature requests → Product Management
        
        Consider customer segment (Consumer/SMB/Enterprise) for SLA prioritization.
        Track business impact and urgency for proper escalation.
        """),
        tools=[calculate_sla_deadline, check_business_hours, create_audit_trail],
        handoffs=[
            handoff(
                agent=tech_support,
                tool_name_override="transfer_to_technical_support",
                tool_description_override="Transfer to technical support for software issues",
                on_handoff=on_sla_tracking_handoff,
                input_type=HandoffContext
            ),
            handoff(
                agent=solutions_eng,
                tool_name_override="escalate_to_solutions_engineering",
                tool_description_override="Escalate to solutions engineering for complex technical requirements",
                on_handoff=on_sla_tracking_handoff,
                input_type=HandoffContext
            )
        ]
    )

    # Test SaaS scenario
    result_saas = await Runner.run(
        saas_orchestrator,
        input="""We're an enterprise customer and our API integration is failing in production. 
        This is affecting our customer-facing application and we're losing revenue. We need immediate 
        engineering support to diagnose and fix this critical issue."""
    )
    print(f"SaaS Result: {result_saas.final_output}")
    print()

    # =============================================================================
    # INDUSTRY PATTERNS SUMMARY
    # =============================================================================

    print("=== Industry-Specific Handoff Patterns Summary ===")
    patterns = """
    Real-World Handoff Considerations by Industry:
    
    🛒 E-COMMERCE:
    - PCI DSS compliance for payment data
    - Customer segment-based SLA (Consumer/SMB/Enterprise)
    - Fraud detection and prevention priority
    - Integration with order management systems
    - Business impact assessment for downtime
    
    🏥 HEALTHCARE: 
    - HIPAA compliance mandatory for all interactions
    - Clinical vs administrative routing
    - Emergency protocol for urgent medical situations
    - Scope of practice boundaries for different roles
    - Comprehensive audit trails for legal protection
    
    💰 FINANCIAL SERVICES:
    - SOX compliance and regulatory reporting
    - Multi-factor authentication requirements
    - Fraud investigation immediate escalation
    - KYC (Know Your Customer) procedures
    - Business hours considerations for escalations
    
    💻 SAAS/TECHNOLOGY:
    - SLA based on customer tier and business impact
    - Technical complexity routing (L1/L2/L3 support)
    - Integration and customization requirements
    - Performance and reliability monitoring
    - Feature request and product feedback loops
    
    🔑 UNIVERSAL BEST PRACTICES:
    - Industry-specific compliance awareness
    - Customer segment-appropriate service levels
    - Business impact and urgency assessment
    - Comprehensive audit trails and documentation
    - Escalation paths that respect business hours
    - Error handling with regulatory considerations
    - Context preservation across specialist handoffs
    - Performance monitoring and SLA tracking
    
    These patterns demonstrate how handoffs must adapt to:
    - Regulatory and compliance requirements
    - Industry-specific customer expectations
    - Business context and impact assessment
    - Specialized knowledge and skill requirements
    - Risk management and escalation protocols
    """
    print(patterns)


if __name__ == "__main__":
    asyncio.run(main())
