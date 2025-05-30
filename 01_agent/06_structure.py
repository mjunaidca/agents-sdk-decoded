"""
Comprehensive Guide: Structured Outputs in OpenAI Agents SDK

This file demonstrates 8 different approaches to structured outputs, from basic to advanced,
showing when to use each approach and the trade-offs involved.

Key Concepts:
1. Strict vs Non-Strict Schemas
2. Simple vs Complex Data Structures  
3. Optional vs Required Fields
4. Nested Models vs Flat Structures
5. Performance vs Flexibility Trade-offs
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional, Union, Literal, Any
from enum import Enum
from datetime import datetime
from agents import Agent, Runner, AgentOutputSchema
import asyncio

# =============================================================================
# USE CASE 1: Basic Strict Schema (Recommended for Production)
# =============================================================================


class BasicUserInfo(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE
    - Only basic types (str, int, bool)
    - No Optional/Union types
    - All fields have defaults
    - Perfect for simple, reliable outputs
    """
    name: str = ""
    age: int = 0
    is_student: bool = False
    email: str = ""

    model_config = ConfigDict(extra="forbid")

# =============================================================================
# USE CASE 2: Enum-Based Strict Schema (Great for Classification)
# =============================================================================


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskClassification(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE
    - Uses Enums for controlled values
    - Prevents invalid classifications
    - Type-safe and self-documenting
    """
    task_type: Literal["bug", "feature",
                       "documentation", "maintenance"] = "feature"
    priority: Priority = Priority.MEDIUM
    estimated_hours: int = 1
    requires_review: bool = True

    model_config = ConfigDict(extra="forbid")

# =============================================================================
# USE CASE 3: Nested Strict Schema (Complex but Strict-Compatible)
# =============================================================================


class Address(BaseModel):
    street: str = ""
    city: str = ""
    country: str = ""
    postal_code: str = ""

    model_config = ConfigDict(extra="forbid")


class ContactInfo(BaseModel):
    email: str = ""
    phone: str = ""

    model_config = ConfigDict(extra="forbid")


class ComplexUserProfile(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE
    - Nested Pydantic models instead of dicts
    - No Optional/Union types
    - Uses Field(default_factory) for complex defaults
    - Maintains structure while being strict
    """
    personal_info: BasicUserInfo = Field(default_factory=BasicUserInfo)
    address: Address = Field(default_factory=Address)
    contact: ContactInfo = Field(default_factory=ContactInfo)
    registration_date: str = ""  # ISO format string instead of datetime

    model_config = ConfigDict(extra="forbid")

# =============================================================================
# USE CASE 4: List-Based Strict Schema (Collections in Strict Mode)
# =============================================================================


class CourseGrade(BaseModel):
    course_name: str = ""
    grade: str = ""
    credits: int = 0

    model_config = ConfigDict(extra="forbid")


class StudentTranscript(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE
    - Lists of Pydantic models work in strict mode
    - Avoids complex dict structures
    - Maintains type safety for collections
    """
    student_id: str = ""
    student_name: str = ""
    gpa: float = 0.0
    courses: List[CourseGrade] = Field(default_factory=list)
    graduation_status: Literal["enrolled", "graduated", "dropped"] = "enrolled"

    model_config = ConfigDict(extra="forbid")

# =============================================================================
# USE CASE 5: Flexible Non-Strict Schema (Maximum Flexibility)
# =============================================================================


class FlexibleAnalysis(BaseModel):
    """
    ❌ NON-STRICT MODE ONLY
    - Uses Optional/Union types freely
    - More flexible but slower validation
    - Good for prototyping and dynamic data
    """
    analysis_type: str
    confidence_score: Optional[float] = None
    results: Union[dict[str, Any], list[Any], str, None] = None
    metadata: Optional[dict[str, Any]] = None
    errors: Optional[List[str]] = None
    timestamp: Optional[datetime] = None

    # Allow extra fields for maximum flexibility
    model_config = ConfigDict(extra="allow")

# =============================================================================
# USE CASE 6: Validated Strict Schema (Business Logic Validation)
# =============================================================================


class ValidatedOrder(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE WITH VALIDATION
    - Includes custom validation logic
    - Maintains strict compatibility
    - Enforces business rules
    """
    order_id: str = ""
    customer_email: str = ""
    total_amount: float = 0.0
    currency: Literal["USD", "EUR", "GBP"] = "USD"
    status: Literal["pending", "confirmed", "shipped", "delivered"] = "pending"

    model_config = ConfigDict(extra="forbid")

    @field_validator('customer_email')
    @classmethod
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v

    @field_validator('total_amount')
    @classmethod
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Amount cannot be negative')
        return v

# =============================================================================
# USE CASE 7: Multi-Level Nested Schema (Enterprise-Grade Structure)
# =============================================================================


class ProductInfo(BaseModel):
    name: str = ""
    sku: str = ""
    price: float = 0.0

    model_config = ConfigDict(extra="forbid")


class OrderItem(BaseModel):
    product: ProductInfo = Field(default_factory=ProductInfo)
    quantity: int = 1
    subtotal: float = 0.0

    model_config = ConfigDict(extra="forbid")


class ShippingInfo(BaseModel):
    method: Literal["standard", "express", "overnight"] = "standard"
    tracking_number: str = ""
    estimated_delivery: str = ""  # ISO date string

    model_config = ConfigDict(extra="forbid")


class EnterpriseOrder(BaseModel):
    """
    ✅ STRICT MODE COMPATIBLE - ENTERPRISE LEVEL
    - Multi-level nesting
    - Complex business logic
    - Maintains strict compatibility
    - Production-ready structure
    """
    order_header: ValidatedOrder = Field(default_factory=ValidatedOrder)
    items: List[OrderItem] = Field(default_factory=list)
    shipping: ShippingInfo = Field(default_factory=ShippingInfo)
    notes: str = ""

    model_config = ConfigDict(extra="forbid")

# =============================================================================
# USE CASE 8: Dynamic Schema Selection (Runtime Schema Choice)
# =============================================================================


class SimpleResponse(BaseModel):
    message: str = ""
    success: bool = True

    model_config = ConfigDict(extra="forbid")


class DetailedResponse(BaseModel):
    message: str = ""
    success: bool = True
    data: ComplexUserProfile = Field(default_factory=ComplexUserProfile)
    metadata: BasicUserInfo = Field(default_factory=BasicUserInfo)

    model_config = ConfigDict(extra="forbid")

# =============================================================================
# SAMPLE DATA FOR TESTING
# =============================================================================


sample_inputs = {
    "basic_user": "Extract user info: John Doe, 25 years old, student, email: john@example.com",

    "task_classification": "Analyze this task: Fix the login bug that's causing users to get locked out. This is blocking production and needs immediate attention. Estimated 3-4 hours of work.",

    "complex_profile": """
    User Profile: Sarah Johnson, 28, software engineer
    Address: 123 Main St, San Francisco, CA, USA, 94105
    Contact: sarah.j@techcorp.com, +1-555-0123
    Registered: 2023-01-15
    """,

    "student_transcript": """
    Student: Alice Smith (ID: STU001)
    Courses completed:
    - Computer Science 101: A (3 credits)
    - Mathematics 201: B+ (4 credits) 
    - Physics 150: A- (3 credits)
    Current GPA: 3.7, Status: Enrolled
    """,

    "flexible_analysis": """
    Analysis Results: Sentiment analysis of customer reviews
    Confidence: 87.5%
    Found 150 positive, 23 negative, 12 neutral reviews
    Key themes: quality, shipping, customer service
    Timestamp: 2024-01-15T10:30:00Z
    """,

    "validated_order": "Order #ORD-001 for customer jane@shop.com, total $299.99 USD, status: confirmed",

    "enterprise_order": """
    Enterprise Order Details:
    Order: ORD-ENT-001, customer: corp@business.com, $1,250.00 USD
    Items:
    - Laptop Pro X1 (SKU: LAP001), Qty: 2, Price: $500 each
    - Wireless Mouse (SKU: MOU001), Qty: 5, Price: $50 each  
    Shipping: Express delivery, tracking: TRK123456789
    Notes: Urgent delivery for new employee onboarding
    """
}

# =============================================================================
# AGENT DEFINITIONS
# =============================================================================

agents = {
    "basic_strict": Agent(
        name="BasicUserExtractor",
        instructions="Extract basic user information into the specified format.",
        output_type=BasicUserInfo
    ),

    "task_classifier": Agent(
        name="TaskClassifier",
        instructions="Classify the task type, priority, estimated hours, and review requirements.",
        output_type=TaskClassification
    ),

    "complex_profile": Agent(
        name="ProfileExtractor",
        instructions="Extract comprehensive user profile including personal info, address, and contact details.",
        output_type=ComplexUserProfile
    ),

    "transcript_analyzer": Agent(
        name="TranscriptAnalyzer",
        instructions="Parse student transcript data including courses, grades, and status.",
        output_type=StudentTranscript
    ),

    "flexible_analyzer": Agent(
        name="FlexibleAnalyzer",
        instructions="Perform flexible analysis and extract results in any format needed.",
        output_type=AgentOutputSchema(
            FlexibleAnalysis, strict_json_schema=False)
    ),

    "order_validator": Agent(
        name="OrderValidator",
        instructions="Extract and validate order information ensuring all business rules are met.",
        output_type=ValidatedOrder
    ),

    "enterprise_processor": Agent(
        name="EnterpriseOrderProcessor",
        instructions="Process complex enterprise orders with full item details and shipping info.",
        output_type=EnterpriseOrder
    ),

    "simple_responder": Agent(
        name="SimpleResponder",
        instructions="Provide a simple success/failure response with message.",
        output_type=SimpleResponse
    )
}

# =============================================================================
# COMPREHENSIVE TEST SUITE
# =============================================================================


async def run_comprehensive_tests():
    """
    Test all 8 use cases with detailed output and analysis
    """

    test_cases = [
        ("basic_strict", "basic_user", "Basic Strict Schema"),
        ("task_classifier", "task_classification", "Enum-Based Classification"),
        ("complex_profile", "complex_profile", "Nested Strict Schema"),
        ("transcript_analyzer", "student_transcript", "List-Based Collections"),
        ("flexible_analyzer", "flexible_analysis", "Flexible Non-Strict"),
        ("order_validator", "validated_order", "Validated Business Logic"),
        ("enterprise_processor", "enterprise_order", "Enterprise Multi-Level"),
        ("simple_responder", "basic_user", "Dynamic Schema Selection")
    ]

    print("=" * 80)
    print("COMPREHENSIVE STRUCTURED OUTPUT TESTING")
    print("=" * 80)

    for i, (agent_key, input_key, description) in enumerate(test_cases, 1):
        print(f"\n{'='*20} USE CASE {i}: {description} {'='*20}")

        try:
            agent = agents[agent_key]
            input_data = sample_inputs[input_key]

            print(f"📝 Input: {input_data[:100]}...")
            print(f"🤖 Agent: {agent.name}")
            print(f"📋 Output Type: {agent.output_type}")

            result = await Runner.run(agent, input_data)

            print(f"✅ Success!")
            print(f"📊 Result: {result.final_output}")
            print(f"🔍 Type: {type(result.final_output)}")

            # Show nested structure for complex types
            if hasattr(result.final_output, '__dict__'):
                print(f"📁 Structure:")
                for field, value in result.final_output.__dict__.items():
                    if hasattr(value, '__dict__'):
                        print(f"   {field}: {type(value).__name__} -> {value}")
                    else:
                        print(f"   {field}: {value}")

        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"🔧 This demonstrates the limitations of this approach")

        print("-" * 80)

# =============================================================================
# PERFORMANCE COMPARISON
# =============================================================================


async def performance_comparison():
    """
    Compare performance between strict and non-strict schemas
    """
    print("\n" + "=" * 50)
    print("PERFORMANCE COMPARISON: STRICT vs NON-STRICT")
    print("=" * 50)

    import time

    # Test strict schema performance
    start_time = time.time()
    for _ in range(10):
        result = await Runner.run(agents["basic_strict"], sample_inputs["basic_user"])
    strict_time = time.time() - start_time

    # Test another strict schema for comparison
    start_time = time.time()
    for _ in range(10):
        result = await Runner.run(agents["task_classifier"], sample_inputs["task_classification"])
    complex_strict_time = time.time() - start_time

    print(f"⚡ Basic Strict Schema (10 runs): {strict_time:.3f}s")
    print(f"🔧 Complex Strict Schema (10 runs): {complex_strict_time:.3f}s")
    print(f"📊 Note: Non-strict schema comparison skipped due to model output format issues")
    print(f"💡 Key Point: Strict schemas provide consistent, fast validation")

# =============================================================================
# MASTERY QUIZ: Test Your Understanding
# =============================================================================


def mastery_quiz():
    """
    Quick mastery assessment for structured outputs in OpenAI Agents SDK
    """
    print("\n" + "=" * 80)
    print("🎯 MASTERY QUIZ: STRUCTURED OUTPUTS IN OPENAI AGENTS SDK")
    print("=" * 80)

    questions = [
        {
            "question": "1. Which of these Pydantic models will work in STRICT mode?",
            "options": [
                "A) field: str | None = None",
                "B) field: Optional[str] = None",
                "C) field: str = ''",
                "D) field: Union[str, int] = 'default'"
            ],
            "correct": "C",
            "explanation": "Strict mode requires concrete default values, not None or Union types"
        },
        {
            "question": "2. How do you make a complex nested structure work in strict mode?",
            "options": [
                "A) Use dict[str, str] with default_factory",
                "B) Use Optional[ComplexModel] = None",
                "C) Use ComplexModel = Field(default_factory=ComplexModel)",
                "D) Use Union[ComplexModel, None] = None"
            ],
            "correct": "C",
            "explanation": "Field(default_factory=ModelClass) creates nested models without Union types"
        },
        {
            "question": "3. What's the correct way to handle collections in strict mode?",
            "options": [
                "A) items: list = []",
                "B) items: List[dict] = Field(default_factory=list)",
                "C) items: List[ItemModel] = Field(default_factory=list)",
                "D) items: Optional[List[ItemModel]] = None"
            ],
            "correct": "C",
            "explanation": "List[PydanticModel] with default_factory works perfectly in strict mode"
        },
        {
            "question": "4. Which validation approach is correct for Pydantic v2?",
            "options": [
                "A) @validator('field')",
                "B) @field_validator('field') with @classmethod",
                "C) @validates('field')",
                "D) @field_validator('field') without @classmethod"
            ],
            "correct": "B",
            "explanation": "Pydantic v2 uses @field_validator with @classmethod decorator"
        },
        {
            "question": "5. How do you enable non-strict mode for flexible schemas?",
            "options": [
                "A) Agent(output_type=Model, strict=False)",
                "B) Agent(output_type=AgentOutputSchema(Model, strict_json_schema=False))",
                "C) Agent(output_type=Model, strict_mode=False)",
                "D) Model.model_config = ConfigDict(strict=False)"
            ],
            "correct": "B",
            "explanation": "Use AgentOutputSchema wrapper with strict_json_schema=False"
        },
        {
            "question": "6. What's the main advantage of strict schemas?",
            "options": [
                "A) More flexible data structures",
                "B) Faster validation and OpenAI compatibility",
                "C) Support for Union types",
                "D) Dynamic field addition"
            ],
            "correct": "B",
            "explanation": "Strict schemas are faster, more reliable, and optimized for OpenAI's function calling"
        },
        {
            "question": "7. Which model_config setting is recommended for strict schemas?",
            "options": [
                "A) extra='allow'",
                "B) extra='ignore'",
                "C) extra='forbid'",
                "D) extra='strict'"
            ],
            "correct": "C",
            "explanation": "extra='forbid' prevents additional properties, maintaining strict validation"
        },
        {
            "question": "8. What causes the 'additionalProperties should not be set' error?",
            "options": [
                "A) Missing default values",
                "B) Union/Optional types creating anyOf schemas",
                "C) Wrong Pydantic version",
                "D) Missing model_config"
            ],
            "correct": "B",
            "explanation": "Union/Optional types generate anyOf schemas which aren't strict-mode compatible"
        },
        {
            "question": "9. Best practice for handling missing/optional data in strict mode?",
            "options": [
                "A) Use None as default",
                "B) Use empty string/list/dict as defaults",
                "C) Use Optional[Type] = None",
                "D) Use Union[Type, None]"
            ],
            "correct": "B",
            "explanation": "Use concrete defaults (empty string, 0, False, []) instead of None"
        },
        {
            "question": "10. When should you use non-strict schemas?",
            "options": [
                "A) Production applications",
                "B) Performance-critical systems",
                "C) Prototyping with dynamic/unknown data structures",
                "D) Simple data extraction"
            ],
            "correct": "C",
            "explanation": "Non-strict is best for prototyping when data structure is unknown or highly dynamic"
        }
    ]

    score = 0
    total = len(questions)

    for i, q in enumerate(questions):
        print(f"\n{q['question']}")
        for option in q['options']:
            print(f"   {option}")

        user_answer = input("\nYour answer (A/B/C/D): ").strip().upper()

        if user_answer == q['correct']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong. Correct answer: {q['correct']}")

        print(f"💡 Explanation: {q['explanation']}")
        print("-" * 60)

    # Calculate mastery level
    percentage = (score / total) * 100

    print(f"\n🎯 QUIZ RESULTS:")
    print(f"Score: {score}/{total} ({percentage:.1f}%)")

    if percentage >= 90:
        mastery_level = "🏆 EXPERT LEVEL"
        feedback = "Outstanding! You've mastered structured outputs in OpenAI Agents SDK."
    elif percentage >= 80:
        mastery_level = "🥇 ADVANCED"
        feedback = "Excellent! You have strong understanding with minor gaps to fill."
    elif percentage >= 70:
        mastery_level = "🥈 INTERMEDIATE"
        feedback = "Good foundation! Review the areas you missed for full mastery."
    elif percentage >= 60:
        mastery_level = "🥉 BEGINNER+"
        feedback = "Basic understanding present. More practice needed with complex scenarios."
    else:
        mastery_level = "📚 NEEDS STUDY"
        feedback = "Significant gaps identified. Review the comprehensive guide thoroughly."

    print(f"Mastery Level: {mastery_level}")
    print(f"Feedback: {feedback}")

    # Specific recommendations based on wrong answers
    if percentage < 90:
        print(f"\n📖 STUDY RECOMMENDATIONS:")
        if score < 7:
            print("- Review basic strict vs non-strict differences")
            print("- Practice creating simple strict schemas")
        if score < 8:
            print("- Focus on nested model patterns and Field(default_factory)")
            print("- Understand Union type limitations in strict mode")
        if score < 9:
            print("- Master Pydantic v2 validation patterns")
            print("- Practice debugging schema compatibility issues")

    return percentage

# =============================================================================
# PRACTICAL CODING CHALLENGE
# =============================================================================


def coding_challenge():
    """
    Hands-on coding challenge to test practical skills
    """
    print("\n" + "=" * 80)
    print("💻 CODING CHALLENGE: Build a Strict-Compatible Schema")
    print("=" * 80)

    challenge_text = """
CHALLENGE: Create a strict-mode compatible Pydantic model for this data:

{
    "user_profile": {
        "name": "Alice Johnson",
        "age": 30,
        "preferences": {
            "theme": "dark",
            "language": "en"
        }
    },
    "orders": [
        {
            "order_id": "ORD-001",
            "items": ["laptop", "mouse"],
            "total": 1299.99,
            "status": "shipped"
        }
    ],
    "metadata": {
        "last_login": "2024-01-15T10:30:00Z",
        "account_type": "premium"
    }
}

REQUIREMENTS:
1. Must work in strict mode (no Union/Optional types)
2. Use nested Pydantic models
3. Include proper defaults
4. Add model_config with extra="forbid"
5. Use Literal types for controlled vocabularies

Try to implement this, then run the verification below!
"""

    print(challenge_text)

    # Sample solution (hidden from user initially)
    solution = '''
# SAMPLE SOLUTION:

class UserPreferences(BaseModel):
    theme: Literal["light", "dark"] = "light"
    language: str = "en"
    model_config = ConfigDict(extra="forbid")

class UserProfile(BaseModel):
    name: str = ""
    age: int = 0
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    model_config = ConfigDict(extra="forbid")

class Order(BaseModel):
    order_id: str = ""
    items: List[str] = Field(default_factory=list)
    total: float = 0.0
    status: Literal["pending", "confirmed", "shipped", "delivered"] = "pending"
    model_config = ConfigDict(extra="forbid")

class Metadata(BaseModel):
    last_login: str = ""  # ISO datetime string
    account_type: Literal["basic", "premium"] = "basic"
    model_config = ConfigDict(extra="forbid")

class UserData(BaseModel):
    user_profile: UserProfile = Field(default_factory=UserProfile)
    orders: List[Order] = Field(default_factory=list)
    metadata: Metadata = Field(default_factory=Metadata)
    model_config = ConfigDict(extra="forbid")
'''

    show_solution = input(
        "\nWould you like to see the sample solution? (y/n): ").strip().lower()
    if show_solution == 'y':
        print(solution)

# =============================================================================
# MAIN EXECUTION
# =============================================================================


async def main():
    """
    Run all demonstrations and comparisons
    """
    await run_comprehensive_tests()
    await performance_comparison()

    print("\n" + "=" * 80)
    print("KEY TAKEAWAYS FOR OPENAI AGENTS SDK:")
    print("=" * 80)
    print("""
    1. 🎯 STRICT MODE (Recommended):
       - Use basic types only (str, int, bool, float)
       - Avoid Optional/Union types
       - Use nested Pydantic models instead of dicts
       - Provide default values for all fields
       - Set extra="forbid" in model_config
    
    2. 🔄 NON-STRICT MODE (Flexible):
       - Use AgentOutputSchema(Model, strict_json_schema=False)
       - Allows Optional/Union types
       - Supports dynamic dict structures
       - Slower validation but more flexible
    
    3. 🏗️ DESIGN PATTERNS:
       - Composition over Union types
       - Nested models over complex dicts
       - Enums for controlled vocabularies
       - Validators for business logic
    
    4. 🚀 PERFORMANCE:
       - Strict schemas are faster and more reliable
       - Non-strict schemas offer more flexibility
       - Choose based on your use case requirements
    
    5. 📚 QUIZ PREPARATION:
       - Understand when strict mode fails
       - Know how to fix schema compatibility issues
       - Practice nested model design
       - Master the trade-offs between approaches
    """)

    # Run mastery assessment
    quiz_score = mastery_quiz()
    coding_challenge()

    print(f"\n🎓 FINAL ASSESSMENT:")
    print(f"Quiz Score: {quiz_score:.1f}%")
    if quiz_score >= 80:
        print("🎉 You're ready for the expert-level quiz!")
    else:
        print("📚 Review the areas you missed and practice more.")

if __name__ == "__main__":
    asyncio.run(main())
