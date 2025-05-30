"""
04_tracing_quiz.py

Interactive quiz for testing understanding of OpenAI Agents SDK tracing concepts.
Covers basic tracing, custom tracing, advanced patterns, and production considerations.

Key Topics Tested:
- Default tracing behavior and configuration
- Traces vs spans understanding
- Custom tracing and span creation
- Tracing processors and external integrations
- Performance monitoring and alerting
- Compliance and audit trails
- Production tracing architectures

Run this to test your knowledge!
"""

import asyncio
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class QuizQuestion:
    """Represents a single quiz question."""
    question: str
    options: Dict[str, str]
    correct_answer: str
    explanation: str
    category: str
    difficulty: str

# ================== QUIZ QUESTIONS ==================


QUIZ_QUESTIONS = [
    # Basic Tracing Questions
    QuizQuestion(
        question="What is the default tracing behavior in the OpenAI Agents SDK?",
        options={
            "a": "Tracing is disabled by default",
            "b": "Tracing is enabled by default",
            "c": "Tracing must be manually configured",
            "d": "Tracing only works in production"
        },
        correct_answer="b",
        explanation="Tracing is enabled by default in the OpenAI Agents SDK, automatically capturing comprehensive data about agent runs.",
        category="Basic Tracing",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="What is the relationship between traces and spans?",
        options={
            "a": "Traces and spans are the same thing",
            "b": "Spans contain multiple traces",
            "c": "Traces contain multiple spans",
            "d": "Traces and spans are independent"
        },
        correct_answer="c",
        explanation="Traces represent complete workflows and contain multiple spans, which represent individual operations within the trace.",
        category="Basic Tracing",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="Which function is used to get the current trace context?",
        options={
            "a": "get_trace()",
            "b": "current_trace()",
            "c": "get_current_trace()",
            "d": "trace_context()"
        },
        correct_answer="c",
        explanation="get_current_trace() returns the current trace object, allowing tools and functions to access trace context information.",
        category="Basic Tracing",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="What is the correct format for a trace ID?",
        options={
            "a": "Any string format",
            "b": "trace_<32_alphanumeric>",
            "c": "UUID format",
            "d": "Numeric ID"
        },
        correct_answer="b",
        explanation="Trace IDs must follow the format trace_<32_alphanumeric>, which can be generated using gen_trace_id().",
        category="Basic Tracing",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="Which built-in span type captures LLM API calls?",
        options={
            "a": "Agent span",
            "b": "Function span",
            "c": "Generation span",
            "d": "Handoff span"
        },
        correct_answer="c",
        explanation="Generation spans wrap LLM API calls, capturing input prompts, output responses, and model parameters.",
        category="Basic Tracing",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="How do you disable tracing globally?",
        options={
            "a": "set_tracing_disabled(True)",
            "b": "OPENAI_AGENTS_DISABLE_TRACING=1",
            "c": "Both a and b are correct",
            "d": "delete_tracing()"
        },
        correct_answer="c",
        explanation="You can disable tracing globally either programmatically with set_tracing_disabled(True) or via environment variable OPENAI_AGENTS_DISABLE_TRACING=1.",
        category="Basic Tracing",
        difficulty="Intermediate"
    ),

    # Custom Tracing Questions
    QuizQuestion(
        question="What is the recommended way to create custom traces?",
        options={
            "a": "trace.start() and trace.finish()",
            "b": "with trace('WorkflowName'): context manager",
            "c": "new_trace() function",
            "d": "create_trace() method"
        },
        correct_answer="b",
        explanation="The context manager approach (with trace('WorkflowName'):) is recommended as it automatically handles trace start and finish.",
        category="Custom Tracing",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="Which function creates custom spans for fine-grained tracking?",
        options={
            "a": "create_span()",
            "b": "new_span()",
            "c": "custom_span()",
            "d": "add_span()"
        },
        correct_answer="c",
        explanation="custom_span() is used to create custom spans with optional metadata for fine-grained operation tracking.",
        category="Custom Tracing",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="What type of data can be stored in trace metadata?",
        options={
            "a": "Only strings",
            "b": "Only numbers and strings",
            "c": "Any JSON-serializable data",
            "d": "Only predefined metadata fields"
        },
        correct_answer="c",
        explanation="Trace metadata can store any JSON-serializable data, including nested objects, arrays, and complex structures.",
        category="Custom Tracing",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="What is the purpose of group_id in RunConfig?",
        options={
            "a": "To identify individual traces",
            "b": "To group related traces together",
            "c": "To set trace priority",
            "d": "To control trace sampling"
        },
        correct_answer="b",
        explanation="group_id links multiple related traces together, useful for tracking multi-step workflows or user sessions.",
        category="Custom Tracing",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="When should you create custom spans?",
        options={
            "a": "For every function call",
            "b": "For significant operations (typically >10ms)",
            "c": "Only for error handling",
            "d": "Never, use default spans only"
        },
        correct_answer="b",
        explanation="Create custom spans for significant operations that warrant separate tracking, typically those taking >10ms or having business importance.",
        category="Custom Tracing",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What is a best practice for span naming?",
        options={
            "a": "Use short generic names like 'process'",
            "b": "Use clear, descriptive names like 'ProcessPayment'",
            "c": "Use random names for security",
            "d": "Use numeric IDs only"
        },
        correct_answer="b",
        explanation="Use clear, descriptive names that indicate the operation type and purpose, following consistent naming conventions.",
        category="Custom Tracing",
        difficulty="Intermediate"
    ),

    # Advanced Tracing Questions
    QuizQuestion(
        question="What is the purpose of TracingProcessor?",
        options={
            "a": "To process trace data and export to external systems",
            "b": "To create new traces",
            "c": "To delete old traces",
            "d": "To compress trace data"
        },
        correct_answer="a",
        explanation="TracingProcessor provides an interface to process trace and span data, enabling custom logging, metrics collection, and external system integration.",
        category="Advanced Tracing",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Which TracingProcessor method is called when a trace starts?",
        options={
            "a": "on_start()",
            "b": "trace_started()",
            "c": "on_trace_start()",
            "d": "start_trace()"
        },
        correct_answer="c",
        explanation="on_trace_start(trace) is called when a trace begins, allowing processors to initialize tracking or logging.",
        category="Advanced Tracing",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="How do you add a custom processor to the tracing system?",
        options={
            "a": "register_processor()",
            "b": "add_trace_processor()",
            "c": "install_processor()",
            "d": "set_processor()"
        },
        correct_answer="b",
        explanation="add_trace_processor() adds a custom processor to the existing list of processors, allowing multiple processors to run simultaneously.",
        category="Advanced Tracing",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What does set_trace_processors() do?",
        options={
            "a": "Adds processors to the existing list",
            "b": "Replaces all existing processors",
            "c": "Creates a backup of processors",
            "d": "Disables all processors"
        },
        correct_answer="b",
        explanation="set_trace_processors() replaces the entire list of processors, potentially removing default OpenAI backend export if not included.",
        category="Advanced Tracing",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Which external systems can benefit from tracing integration?",
        options={
            "a": "Only monitoring platforms like DataDog",
            "b": "Only logging systems like Elastic",
            "c": "Monitoring, logging, analytics, and observability platforms",
            "d": "Only OpenAI's own systems"
        },
        correct_answer="c",
        explanation="Tracing can integrate with various external systems including monitoring platforms, logging systems, analytics tools, and observability platforms.",
        category="Advanced Tracing",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="What is the benefit of hierarchical custom spans?",
        options={
            "a": "Faster execution",
            "b": "Organized tracking of complex workflows with sub-operations",
            "c": "Reduced memory usage",
            "d": "Better security"
        },
        correct_answer="b",
        explanation="Hierarchical spans provide organized tracking of complex workflows, showing parent-child relationships between operations and sub-operations.",
        category="Advanced Tracing",
        difficulty="Advanced"
    ),

    # Performance and Monitoring Questions
    QuizQuestion(
        question="What should you monitor for performance bottlenecks?",
        options={
            "a": "Only response times",
            "b": "Only error rates",
            "c": "Response times, error rates, and resource utilization",
            "d": "Only token usage"
        },
        correct_answer="c",
        explanation="Comprehensive performance monitoring includes response times, error rates, resource utilization, and throughput metrics.",
        category="Performance Monitoring",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What is a recommended approach for high-latency alerting?",
        options={
            "a": "Alert on every slow operation",
            "b": "Set reasonable thresholds and track patterns",
            "c": "Never alert on latency",
            "d": "Only alert in production"
        },
        correct_answer="b",
        explanation="Set reasonable latency thresholds based on your SLAs and track patterns rather than alerting on every individual slow operation.",
        category="Performance Monitoring",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Which percentiles are commonly used for performance analysis?",
        options={
            "a": "Only average (P50)",
            "b": "P50, P95, P99",
            "c": "Only maximum values",
            "d": "P25, P75 only"
        },
        correct_answer="b",
        explanation="P50 (median), P95, and P99 percentiles provide insights into typical performance and tail latencies.",
        category="Performance Monitoring",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What is sampling in tracing?",
        options={
            "a": "Recording every single trace",
            "b": "Recording only a percentage of traces to reduce overhead",
            "c": "Recording only error traces",
            "d": "Recording traces randomly"
        },
        correct_answer="b",
        explanation="Sampling records only a percentage of traces to reduce storage costs and processing overhead while maintaining visibility.",
        category="Performance Monitoring",
        difficulty="Advanced"
    ),

    # Production and Compliance Questions
    QuizQuestion(
        question="Which environment variables protect sensitive data in tracing?",
        options={
            "a": "OPENAI_AGENTS_DISABLE_TRACING only",
            "b": "OPENAI_AGENTS_DONT_LOG_MODEL_DATA and OPENAI_AGENTS_DONT_LOG_TOOL_DATA",
            "c": "OPENAI_AGENTS_SECURE_MODE only",
            "d": "No environment variables needed"
        },
        correct_answer="b",
        explanation="These environment variables disable logging of potentially sensitive LLM inputs/outputs and tool data in production environments.",
        category="Production Configuration",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="What is a circuit breaker pattern in tracing?",
        options={
            "a": "A way to delete traces",
            "b": "A resilience pattern that stops tracing when external systems fail",
            "c": "A security feature",
            "d": "A compression technique"
        },
        correct_answer="b",
        explanation="Circuit breaker patterns prevent cascading failures by temporarily disabling tracing exports when external systems are unavailable.",
        category="Production Configuration",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Which compliance regulations might require audit trails?",
        options={
            "a": "Only GDPR",
            "b": "Only HIPAA",
            "c": "GDPR, HIPAA, SOX, PCI DSS, SOC 2",
            "d": "No regulations require audit trails"
        },
        correct_answer="c",
        explanation="Multiple regulations including GDPR, HIPAA, SOX, PCI DSS, and SOC 2 may require comprehensive audit trails for compliance.",
        category="Compliance",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What should be included in compliance audit trails?",
        options={
            "a": "Only error information",
            "b": "Only user identification",
            "c": "Timestamps, user context, operations performed, and regulatory context",
            "d": "Only system performance data"
        },
        correct_answer="c",
        explanation="Comprehensive audit trails include timestamps, user context, operations performed, and relevant regulatory context for compliance requirements.",
        category="Compliance",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What is the recommended sampling rate for high-volume production systems?",
        options={
            "a": "100% (sample everything)",
            "b": "0% (sample nothing)",
            "c": "1-10% depending on volume and requirements",
            "d": "50% always"
        },
        correct_answer="c",
        explanation="High-volume systems typically use 1-10% sampling to balance observability needs with storage costs and performance impact.",
        category="Production Configuration",
        difficulty="Advanced"
    ),

    # Practical Scenarios
    QuizQuestion(
        question="You need to debug a slow agent workflow. What tracing approach is best?",
        options={
            "a": "Disable tracing to improve performance",
            "b": "Enable verbose logging and use custom spans for bottleneck identification",
            "c": "Only look at error logs",
            "d": "Use default tracing without modifications"
        },
        correct_answer="b",
        explanation="Enable verbose logging and add custom spans around suspected bottlenecks to identify performance issues in the workflow.",
        category="Practical Scenarios",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Your traces are missing important business context. What should you do?",
        options={
            "a": "Ignore the missing context",
            "b": "Add rich metadata to traces and spans",
            "c": "Create more traces",
            "d": "Disable metadata to reduce overhead"
        },
        correct_answer="b",
        explanation="Add rich metadata containing business context, user information, and operational details to make traces more useful for analysis.",
        category="Practical Scenarios",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="You want to track user journeys across multiple agent interactions. What's the best approach?",
        options={
            "a": "Use the same trace_id for all interactions",
            "b": "Use group_id to link related traces",
            "c": "Create separate unlinked traces",
            "d": "Don't track user journeys"
        },
        correct_answer="b",
        explanation="Use group_id in RunConfig to link related traces together while maintaining separate trace_ids for individual interactions.",
        category="Practical Scenarios",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Your external tracing system is down. What's the best practice?",
        options={
            "a": "Stop all agent operations",
            "b": "Disable tracing completely",
            "c": "Use fallback processors or circuit breaker patterns",
            "d": "Retry indefinitely"
        },
        correct_answer="c",
        explanation="Implement fallback processors or circuit breaker patterns to maintain system operation when external tracing systems are unavailable.",
        category="Practical Scenarios",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="You need to analyze agent performance trends over time. What should you implement?",
        options={
            "a": "Manual log analysis only",
            "b": "Custom processors that collect and aggregate performance metrics",
            "c": "Increase logging verbosity",
            "d": "Use only default tracing"
        },
        correct_answer="b",
        explanation="Implement custom processors that collect, aggregate, and analyze performance metrics over time for trend analysis.",
        category="Practical Scenarios",
        difficulty="Advanced"
    ),

    # Error Handling and Edge Cases
    QuizQuestion(
        question="What happens if you don't use context managers for custom traces?",
        options={
            "a": "Nothing, it works the same",
            "b": "Risk of traces not being properly finished",
            "c": "Better performance",
            "d": "Automatic error handling"
        },
        correct_answer="b",
        explanation="Without context managers, traces may not be properly finished if exceptions occur, leading to incomplete trace data.",
        category="Error Handling",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="How should errors be handled in custom tracing processors?",
        options={
            "a": "Let errors crash the application",
            "b": "Ignore all errors silently",
            "c": "Implement graceful error handling and fallback mechanisms",
            "d": "Disable the processor on any error"
        },
        correct_answer="c",
        explanation="Implement graceful error handling in processors to prevent tracing issues from affecting the main application functionality.",
        category="Error Handling",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What should you do if trace export is failing frequently?",
        options={
            "a": "Ignore the failures",
            "b": "Implement retry logic with exponential backoff",
            "c": "Disable tracing permanently",
            "d": "Increase export frequency"
        },
        correct_answer="b",
        explanation="Implement retry logic with exponential backoff and consider circuit breaker patterns to handle temporary export failures gracefully.",
        category="Error Handling",
        difficulty="Advanced"
    ),

    # Integration and Architecture
    QuizQuestion(
        question="In a microservices architecture, how should you correlate traces across services?",
        options={
            "a": "Use separate trace systems for each service",
            "b": "Use consistent trace_id or group_id across services",
            "c": "Don't correlate traces across services",
            "d": "Use only timestamps for correlation"
        },
        correct_answer="b",
        explanation="Use consistent trace_id or group_id across services to enable end-to-end tracing and correlation in distributed systems.",
        category="Integration",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What is the best practice for tracing in development vs production?",
        options={
            "a": "Use identical tracing configuration",
            "b": "Disable tracing in development",
            "c": "Use verbose tracing in development, optimized tracing in production",
            "d": "Use tracing only in production"
        },
        correct_answer="c",
        explanation="Use verbose tracing with detailed metadata in development for debugging, and optimized tracing with sampling and sensitive data protection in production.",
        category="Integration",
        difficulty="Advanced"
    )
]

# ================== QUIZ ENGINE ==================


class TracingQuiz:
    """Interactive quiz engine for tracing concepts."""

    def __init__(self):
        self.questions = QUIZ_QUESTIONS.copy()
        self.score = 0
        self.answers = []
        self.categories = {}

    def shuffle_questions(self):
        """Shuffle questions for randomized quiz experience."""
        random.shuffle(self.questions)

    def run_quiz(self, num_questions: Optional[int] = None, difficulty: Optional[str] = None, category: Optional[str] = None):
        """Run the interactive quiz."""
        # Filter questions based on criteria
        filtered_questions = self.questions

        if difficulty:
            filtered_questions = [
                q for q in filtered_questions if q.difficulty.lower() == difficulty.lower()]

        if category:
            filtered_questions = [
                q for q in filtered_questions if category.lower() in q.category.lower()]

        if not filtered_questions:
            print("❌ No questions match the specified criteria.")
            return

        # Limit number of questions
        if num_questions:
            filtered_questions = filtered_questions[:num_questions]

        print(f"📊 Tracing Concepts Quiz")
        print(f"📚 Questions: {len(filtered_questions)}")
        if difficulty:
            print(f"🎯 Difficulty: {difficulty}")
        if category:
            print(f"📂 Category: {category}")
        print("="*60)

        for i, question in enumerate(filtered_questions, 1):
            self.ask_question(i, question)

        self.show_results()

    def ask_question(self, number: int, question: QuizQuestion):
        """Ask a single question and process the answer."""
        print(
            f"\n❓ Question {number}: [{question.category} - {question.difficulty}]")
        print(f"{question.question}")
        print()

        # Display options
        for key, value in question.options.items():
            print(f"   {key.upper()}) {value}")

        # Get user answer
        while True:
            answer = input("\n👉 Your answer (a/b/c/d): ").strip().lower()
            if answer in ['a', 'b', 'c', 'd']:
                break
            print("❌ Please enter a, b, c, or d")

        # Check answer
        is_correct = answer == question.correct_answer.lower()
        if is_correct:
            print("✅ Correct!")
            self.score += 1
        else:
            print(
                f"❌ Incorrect. The correct answer is {question.correct_answer.upper()}")

        print(f"💡 Explanation: {question.explanation}")

        # Track by category
        if question.category not in self.categories:
            self.categories[question.category] = {"correct": 0, "total": 0}

        self.categories[question.category]["total"] += 1
        if is_correct:
            self.categories[question.category]["correct"] += 1

        self.answers.append({
            "question": question.question,
            "your_answer": answer,
            "correct_answer": question.correct_answer,
            "is_correct": is_correct,
            "category": question.category,
            "difficulty": question.difficulty
        })

    def show_results(self):
        """Display quiz results and analysis."""
        total_questions = len(self.answers)
        percentage = (self.score / total_questions *
                      100) if total_questions > 0 else 0

        print("\n" + "="*60)
        print("📊 QUIZ RESULTS")
        print("="*60)
        print(
            f"🎯 Final Score: {self.score}/{total_questions} ({percentage:.1f}%)")

        # Performance rating
        if percentage >= 90:
            print(
                "🏆 Excellent! You have mastery of tracing concepts.")
        elif percentage >= 80:
            print("🥈 Great job! You understand most tracing concepts well.")
        elif percentage >= 70:
            print("🥉 Good work! Some areas could use more review.")
        elif percentage >= 60:
            print("📚 Fair performance. Consider reviewing the tracing documentation.")
        else:
            print("📖 Keep studying! Review the examples and documentation.")

        # Category breakdown
        if self.categories:
            print("\n📈 Performance by Category:")
            for category, stats in self.categories.items():
                cat_percentage = (
                    stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
                print(
                    f"   {category}: {stats['correct']}/{stats['total']} ({cat_percentage:.1f}%)")

        # Difficulty analysis
        difficulty_stats = {}
        for answer in self.answers:
            diff = answer["difficulty"]
            if diff not in difficulty_stats:
                difficulty_stats[diff] = {"correct": 0, "total": 0}
            difficulty_stats[diff]["total"] += 1
            if answer["is_correct"]:
                difficulty_stats[diff]["correct"] += 1

        if difficulty_stats:
            print("\n📊 Performance by Difficulty:")
            for difficulty, stats in difficulty_stats.items():
                diff_percentage = (
                    stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
                print(
                    f"   {difficulty}: {stats['correct']}/{stats['total']} ({diff_percentage:.1f}%)")

        # Study recommendations
        self.show_study_recommendations()

    def show_study_recommendations(self):
        """Provide personalized study recommendations."""
        print("\n💡 Study Recommendations:")

        # Identify weak categories
        weak_categories = []
        for category, stats in self.categories.items():
            if stats["total"] > 0:
                percentage = stats["correct"] / stats["total"] * 100
                if percentage < 70:
                    weak_categories.append(category)

        if weak_categories:
            print("   📚 Review these topics:")
            for category in weak_categories:
                if "Basic Tracing" in category:
                    print(
                        "     • 01_basic_tracing.py - Default behavior, traces vs spans")
                elif "Custom Tracing" in category:
                    print(
                        "     • 02_custom_tracing.py - Custom traces, spans, metadata")
                elif "Advanced Tracing" in category or "Performance" in category or "Production" in category:
                    print(
                        "     • 03_advanced_tracing.py - Processors, integrations, production")
                elif "Compliance" in category:
                    print("     • 03_advanced_tracing.py - Compliance and audit trails")

        print("\n🔗 Additional Resources:")
        print("   • https://openai.github.io/openai-agents-python/tracing/")
        print("   • https://openai.github.io/openai-agents-python/ref/tracing/")
        print("   • Review the decoded/12_tracing/ examples")

# ================== QUIZ MODES ==================


def quick_quiz():
    """Run a quick 10-question quiz."""
    quiz = TracingQuiz()
    quiz.shuffle_questions()
    quiz.run_quiz(num_questions=10)


def category_quiz():
    """Run a quiz focused on a specific category."""
    categories = list(set(q.category for q in QUIZ_QUESTIONS))

    print("📂 Available Categories:")
    for i, category in enumerate(categories, 1):
        print(f"   {i}. {category}")

    try:
        choice = int(input("\n👉 Choose a category (number): ")) - 1
        if 0 <= choice < len(categories):
            selected_category = categories[choice]
            quiz = TracingQuiz()
            quiz.shuffle_questions()
            quiz.run_quiz(category=selected_category)
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Please enter a valid number")


def difficulty_quiz():
    """Run a quiz focused on a specific difficulty level."""
    difficulties = ["Beginner", "Intermediate", "Advanced"]

    print("🎯 Available Difficulty Levels:")
    for i, difficulty in enumerate(difficulties, 1):
        print(f"   {i}. {difficulty}")

    try:
        choice = int(input("\n👉 Choose difficulty (number): ")) - 1
        if 0 <= choice < len(difficulties):
            selected_difficulty = difficulties[choice]
            quiz = TracingQuiz()
            quiz.shuffle_questions()
            quiz.run_quiz(difficulty=selected_difficulty)
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Please enter a valid number")


def full_quiz():
    """Run the complete quiz with all questions."""
    quiz = TracingQuiz()
    quiz.shuffle_questions()
    quiz.run_quiz()

# ================== MAIN EXECUTION ==================


def main():
    """Main quiz interface."""
    print("📊 OpenAI Agents SDK - Tracing Concepts Quiz 📊")
    print("\nTest your knowledge of SDK tracing capabilities!")
    print("\n📚 Quiz Options:")
    print("   1. Quick Quiz (10 questions)")
    print("   2. Category-Specific Quiz")
    print("   3. Difficulty-Based Quiz")
    print("   4. Full Quiz (All questions)")
    print("   5. Exit")

    while True:
        try:
            choice = input("\n👉 Choose an option (1-5): ").strip()

            if choice == "1":
                quick_quiz()
                break
            elif choice == "2":
                category_quiz()
                break
            elif choice == "3":
                difficulty_quiz()
                break
            elif choice == "4":
                full_quiz()
                break
            elif choice == "5":
                print("👋 Happy learning!")
                break
            else:
                print("❌ Please choose 1, 2, 3, 4, or 5")

        except KeyboardInterrupt:
            print("\n\n👋 Quiz interrupted. Happy learning!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
