"""
05_guardrails_quiz.py

Interactive quiz to test understanding of OpenAI Agents SDK Guardrails.
Covers input guardrails, output guardrails, exceptions, and agent-based guardrails.
"""

import asyncio
import random
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class QuizQuestion:
    question: str
    options: List[str]
    correct_answer: int  # Index of correct option (0-based)
    explanation: str
    category: str
    difficulty: str  # "Beginner", "Intermediate", "Advanced"
    points: int


class GuardrailsQuiz:
    def __init__(self):
        self.questions = self._create_questions()
        self.score = 0
        self.total_questions = 0

    def _create_questions(self) -> List[QuizQuestion]:
        """Create all quiz questions organized by difficulty and category."""
        return [
            # === BEGINNER LEVEL ===
            QuizQuestion(
                "What are guardrails in the OpenAI Agents SDK?",
                [
                    "Security measures that prevent unauthorized access",
                    "Checks that run in parallel to agents for validation and safety",
                    "Methods to optimize agent performance",
                    "Tools for debugging agent responses"
                ],
                1, "Guardrails are checks that run in parallel to agents to provide safety, validation, and quality control.",
                "Basics", "Beginner", 1
            ),

            QuizQuestion(
                "Which decorator is used to create input guardrails?",
                ["@input_guard", "@guardrail_input",
                    "@input_guardrail", "@validate_input"],
                2, "@input_guardrail decorator is used to create input validation guardrails.",
                "Basics", "Beginner", 1
            ),

            QuizQuestion(
                "What does tripwire_triggered=True mean in GuardrailFunctionOutput?",
                [
                    "The guardrail passed validation",
                    "The guardrail failed and execution should be halted",
                    "The guardrail needs more information",
                    "The guardrail should run again"
                ],
                1, "When tripwire_triggered=True, the guardrail has failed validation and agent execution will be halted.",
                "Basics", "Beginner", 1
            ),

            QuizQuestion(
                "When do input guardrails run?",
                [
                    "After the agent generates a response",
                    "Before user input reaches the agent",
                    "During agent processing",
                    "Only when errors occur"
                ],
                1, "Input guardrails run before user input reaches the agent for processing.",
                "Input Guardrails", "Beginner", 1
            ),

            QuizQuestion(
                "When do output guardrails run?",
                [
                    "Before the agent starts processing",
                    "During agent processing",
                    "After the agent generates output but before it's returned",
                    "Only when the user requests validation"
                ],
                2, "Output guardrails run after the agent generates output but before it's returned to the user.",
                "Output Guardrails", "Beginner", 1
            ),

            QuizQuestion(
                "Which exception is raised when an input guardrail tripwire is triggered?",
                [
                    "GuardrailException",
                    "InputGuardrailTripwireTriggered",
                    "ValidationError",
                    "TripwireException"
                ],
                1, "InputGuardrailTripwireTriggered exception is raised when an input guardrail tripwire is triggered.",
                "Exceptions", "Beginner", 1
            ),

            # === INTERMEDIATE LEVEL ===
            QuizQuestion(
                "What is the correct function signature for an input guardrail?",
                [
                    "def guardrail(input: str) -> bool",
                    "def guardrail(context: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput",
                    "def guardrail(agent: Agent, input: str) -> dict",
                    "async def guardrail(input: Any) -> GuardrailFunctionOutput"
                ],
                1, "Input guardrails must accept context, agent, and input parameters and return GuardrailFunctionOutput.",
                "Implementation", "Intermediate", 2
            ),

            QuizQuestion(
                "What information can you include in the output_info field of GuardrailFunctionOutput?",
                [
                    "Only boolean values",
                    "Only error messages",
                    "Any information about the guardrail's output and checks performed",
                    "Only structured data with predefined schema"
                ],
                2, "output_info can contain any information about the guardrail's output, checks performed, and granular results.",
                "Implementation", "Intermediate", 2
            ),

            QuizQuestion(
                "In a handoff chain, input guardrails run for which agent?",
                [
                    "All agents in the chain",
                    "Only the first agent",
                    "Only the last agent",
                    "The agent with the highest priority"
                ],
                1, "Input guardrails only run for the first agent in a handoff chain since they check user input.",
                "Handoffs", "Intermediate", 2
            ),

            QuizQuestion(
                "In a handoff chain, output guardrails run for which agent?",
                [
                    "All agents in the chain",
                    "Only the first agent",
                    "Only the last agent",
                    "The agent that generates the most output"
                ],
                2, "Output guardrails only run for the last agent in a handoff chain since they check the final output.",
                "Handoffs", "Intermediate", 2
            ),

            QuizQuestion(
                "Can guardrails be both sync and async?",
                [
                    "No, only sync functions are supported",
                    "No, only async functions are supported",
                    "Yes, both sync and async functions are supported",
                    "Only async for input guardrails, sync for output guardrails"
                ],
                2, "Guardrails can be either sync or async functions. The SDK handles both types appropriately.",
                "Implementation", "Intermediate", 2
            ),

            QuizQuestion(
                "What happens when multiple guardrails are configured and one triggers?",
                [
                    "All guardrails continue running",
                    "Execution stops immediately when the first guardrail triggers",
                    "The agent runs with a warning",
                    "Only the last guardrail result is considered"
                ],
                1, "When any guardrail triggers a tripwire, execution stops immediately and an exception is raised.",
                "Multiple Guardrails", "Intermediate", 2
            ),

            # === ADVANCED LEVEL ===
            QuizQuestion(
                "What is the main advantage of agent-based guardrails over simple guardrails?",
                [
                    "They run faster",
                    "They use less memory",
                    "They provide more sophisticated reasoning and context understanding",
                    "They don't require exception handling"
                ],
                2, "Agent-based guardrails use LLM reasoning for more sophisticated validation and context understanding.",
                "Agent-Based", "Advanced", 3
            ),

            QuizQuestion(
                "What is a major performance consideration with agent-based guardrails?",
                [
                    "They use more CPU",
                    "They require more memory",
                    "They add significant latency due to additional LLM calls",
                    "They can't run in parallel"
                ],
                2, "Agent-based guardrails add significant latency because they make additional LLM API calls for validation.",
                "Performance", "Advanced", 3
            ),

            QuizQuestion(
                "How can you implement a confidence threshold in agent-based guardrails?",
                [
                    "Set tripwire_triggered based on the guardrail agent's confidence score",
                    "Use multiple guardrail agents and vote",
                    "Only run guardrails if confidence is high",
                    "Confidence thresholds are not supported"
                ],
                0, "You can implement confidence thresholds by setting tripwire_triggered based on the guardrail agent's confidence score.",
                "Agent-Based", "Advanced", 3
            ),

            QuizQuestion(
                "What should you do when a guardrail exception is caught in production?",
                [
                    "Re-raise the exception to the user",
                    "Ignore the exception and continue",
                    "Log the event and provide a user-friendly error message",
                    "Retry the operation without guardrails"
                ],
                2, "In production, log guardrail triggers for monitoring and provide user-friendly error messages.",
                "Production", "Advanced", 3
            ),

            QuizQuestion(
                "Which approach is better for high-performance scenarios?",
                [
                    "Always use agent-based guardrails for accuracy",
                    "Use simple rule-based guardrails for speed",
                    "Disable guardrails completely",
                    "Use only output guardrails"
                ],
                1, "For high-performance scenarios, simple rule-based guardrails provide speed with minimal latency overhead.",
                "Performance", "Advanced", 3
            ),

            # === PRACTICAL SCENARIOS ===
            QuizQuestion(
                "You need to block math homework requests. Which approach would you use?",
                [
                    "Simple keyword matching guardrail",
                    "Agent-based guardrail with confidence scoring",
                    "Only output validation",
                    "Manual review process"
                ],
                1, "For complex intent detection like math homework, agent-based guardrails with confidence scoring provide better accuracy.",
                "Practical", "Intermediate", 2
            ),

            QuizQuestion(
                "For a content moderation system, where should you place guardrails?",
                [
                    "Only input guardrails",
                    "Only output guardrails",
                    "Both input and output guardrails",
                    "External service only"
                ],
                2, "Content moderation benefits from both input guardrails (filtering inappropriate questions) and output guardrails (ensuring appropriate responses).",
                "Practical", "Intermediate", 2
            ),

            QuizQuestion(
                "What's the best way to handle false positives in guardrails?",
                [
                    "Disable the guardrail",
                    "Lower the sensitivity threshold and monitor performance",
                    "Ignore false positives",
                    "Only use manual review"
                ],
                1, "Handle false positives by adjusting sensitivity thresholds and monitoring performance metrics.",
                "Practical", "Advanced", 3
            ),

            QuizQuestion(
                "How would you implement a guardrail that checks response length?",
                [
                    "Count characters and compare to max_length threshold",
                    "Use an agent to evaluate if response is too long",
                    "Only check word count",
                    "Let the UI handle length limits"
                ],
                0, "Response length checking is best implemented as a simple character/token count comparison for performance.",
                "Implementation", "Beginner", 1
            ),

            QuizQuestion(
                "What information should you log when a guardrail triggers?",
                [
                    "Only the guardrail name",
                    "Only the user input",
                    "Guardrail name, trigger reason, input/output content, and timestamp",
                    "No logging needed"
                ],
                2, "Log comprehensive information including guardrail name, trigger reason, content, and timestamp for debugging and monitoring.",
                "Monitoring", "Intermediate", 2
            )
        ]

    def get_questions_by_difficulty(self, difficulty: str) -> List[QuizQuestion]:
        """Get questions filtered by difficulty level."""
        return [q for q in self.questions if q.difficulty == difficulty]

    def get_questions_by_category(self, category: str) -> List[QuizQuestion]:
        """Get questions filtered by category."""
        return [q for q in self.questions if q.category == category]

    def run_quiz(self, mode: str = "mixed", num_questions: int = 10):
        """Run the quiz in different modes."""
        available_questions = self.questions.copy()

        if mode == "beginner":
            available_questions = self.get_questions_by_difficulty("Beginner")
        elif mode == "intermediate":
            available_questions = self.get_questions_by_difficulty(
                "Intermediate")
        elif mode == "advanced":
            available_questions = self.get_questions_by_difficulty("Advanced")

        # Randomly select questions
        selected_questions = random.sample(
            available_questions,
            min(num_questions, len(available_questions))
        )

        print(f"\n🧠 OpenAI Agents SDK - Guardrails Quiz 🧠")
        print(f"Mode: {mode.title()}")
        print(f"Questions: {len(selected_questions)}")
        print("=" * 50)

        for i, question in enumerate(selected_questions, 1):
            self._ask_question(i, question)

        self._show_final_results(selected_questions)

    def _ask_question(self, question_num: int, question: QuizQuestion):
        """Ask a single question and handle the response."""
        print(
            f"\nQuestion {question_num}: [{question.difficulty}] ({question.points} points)")
        print(f"Category: {question.category}")
        print(f"\n{question.question}")

        for i, option in enumerate(question.options):
            print(f"{i + 1}. {option}")

        while True:
            try:
                user_answer = input(
                    f"\nYour answer (1-{len(question.options)}): ").strip()
                answer_index = int(user_answer) - 1

                if 0 <= answer_index < len(question.options):
                    break
                else:
                    print(
                        f"Please enter a number between 1 and {len(question.options)}")
            except ValueError:
                print("Please enter a valid number")

        self.total_questions += 1

        if answer_index == question.correct_answer:
            print("✅ Correct!")
            self.score += question.points
        else:
            print(
                f"❌ Incorrect. The correct answer was: {question.options[question.correct_answer]}")

        print(f"\nExplanation: {question.explanation}")
        input("\nPress Enter to continue...")

    def _show_final_results(self, questions: List[QuizQuestion]):
        """Show final quiz results and performance analysis."""
        max_possible_score = sum(q.points for q in questions)
        percentage = (self.score / max_possible_score) * \
            100 if max_possible_score > 0 else 0

        print("\n" + "=" * 50)
        print("🎯 QUIZ RESULTS 🎯")
        print("=" * 50)
        print(
            f"Score: {self.score}/{max_possible_score} points ({percentage:.1f}%)")
        print(f"Questions answered: {self.total_questions}")

        # Performance categories
        if percentage >= 90:
            grade = "🏆 Excellent! You have mastered guardrails!"
        elif percentage >= 80:
            grade = "🥇 Great! You have a strong understanding of guardrails."
        elif percentage >= 70:
            grade = "🥈 Good! Review the areas where you missed questions."
        elif percentage >= 60:
            grade = "🥉 Fair. Consider reviewing the documentation and examples."
        else:
            grade = "📚 Study needed. Review the guardrails examples and documentation."

        print(f"\nGrade: {grade}")

        # Category performance analysis
        self._show_category_analysis(questions)

        print("\n📚 Study Resources:")
        print("• Review 01_basic_input_guardrail.py for input validation")
        print("• Study 02_basic_output_guardrail.py for output validation")
        print("• Practice 03_guardrail_exceptions.py for exception handling")
        print("• Explore 04_agent_based_guardrails.py for advanced patterns")
        print("• Read the README.md for comprehensive concepts")

    def _show_category_analysis(self, questions: List[QuizQuestion]):
        """Show performance analysis by category."""
        categories = {}

        for question in questions:
            category = question.category
            if category not in categories:
                categories[category] = {
                    "total": 0, "correct": 0, "points": 0, "max_points": 0}

            categories[category]["total"] += 1
            categories[category]["max_points"] += question.points

        # This is a simplified analysis - in a real implementation,
        # you'd track which questions were answered correctly
        print(f"\n📊 Category Breakdown:")
        for category, stats in categories.items():
            print(
                f"• {category}: {stats['total']} questions ({stats['max_points']} points)")


def run_custom_quiz():
    """Run a customized quiz based on user preferences."""
    quiz = GuardrailsQuiz()

    print("🎮 Welcome to the OpenAI Agents SDK Guardrails Quiz! 🎮")
    print("\nSelect quiz mode:")
    print("1. Mixed (all difficulty levels)")
    print("2. Beginner only")
    print("3. Intermediate only")
    print("4. Advanced only")
    print("5. Quick test (5 questions)")
    print("6. Full test (20 questions)")

    while True:
        try:
            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == "1":
                quiz.run_quiz("mixed", 10)
                break
            elif choice == "2":
                quiz.run_quiz("beginner", 8)
                break
            elif choice == "3":
                quiz.run_quiz("intermediate", 8)
                break
            elif choice == "4":
                quiz.run_quiz("advanced", 6)
                break
            elif choice == "5":
                quiz.run_quiz("mixed", 5)
                break
            elif choice == "6":
                quiz.run_quiz("mixed", 20)
                break
            else:
                print("Please enter a number between 1 and 6")
        except KeyboardInterrupt:
            print("\n\nQuiz cancelled. Study well! 📚")
            return


async def main():
    """Main function to run the guardrails quiz."""
    run_custom_quiz()

if __name__ == "__main__":
    asyncio.run(main())
