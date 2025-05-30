"""
04_multiple_agents_quiz.py

Interactive quiz to test understanding of Multi-Agent Orchestration in the OpenAI Agents SDK.
Covers LLM orchestration, code orchestration, hybrid patterns, and best practices.
"""

import asyncio
import random
from typing import List
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


class MultiAgentQuiz:
    def __init__(self):
        self.questions = self._create_questions()
        self.score = 0
        self.total_questions = 0

    def _create_questions(self) -> List[QuizQuestion]:
        """Create all quiz questions organized by difficulty and category."""
        return [
            # === BEGINNER LEVEL ===
            QuizQuestion(
                "What are the two main approaches to orchestrating multiple agents?",
                [
                    "Sequential and parallel execution",
                    "LLM orchestration and code orchestration",
                    "Sync and async processing",
                    "Local and remote agents"
                ],
                1, "The two main approaches are LLM orchestration (letting LLM make decisions) and code orchestration (deterministic code control).",
                "Orchestration Basics", "Beginner", 1
            ),

            QuizQuestion(
                "What is the main advantage of LLM orchestration?",
                [
                    "It's faster and more efficient",
                    "It uses intelligence to handle open-ended and ambiguous tasks",
                    "It's more predictable and deterministic",
                    "It costs less to operate"
                ],
                1, "LLM orchestration leverages AI intelligence to plan, reason, and handle open-ended tasks that require creativity and adaptability.",
                "LLM Orchestration", "Beginner", 1
            ),

            QuizQuestion(
                "What is the main advantage of code orchestration?",
                [
                    "It can handle more creative tasks",
                    "It provides more deterministic, predictable, and cost-effective execution",
                    "It requires less configuration",
                    "It works better with complex reasoning"
                ],
                1, "Code orchestration provides deterministic, predictable execution with better performance and cost control.",
                "Code Orchestration", "Beginner", 1
            ),

            QuizQuestion(
                "Which Python feature is commonly used for parallel agent execution?",
                ["threading.Thread", "multiprocessing.Process",
                    "asyncio.gather", "concurrent.futures"],
                2, "asyncio.gather is used to run multiple agents in parallel asynchronously.",
                "Parallel Execution", "Beginner", 1
            ),

            QuizQuestion(
                "What are handoffs in multi-agent systems?",
                [
                    "Transferring data between databases",
                    "Delegating tasks from one agent to specialized agents",
                    "Switching between sync and async execution",
                    "Moving agents between different servers"
                ],
                1, "Handoffs allow agents to delegate tasks to other specialized agents for domain-specific work.",
                "Handoffs", "Beginner", 1
            ),

            QuizQuestion(
                "What is agent chaining?",
                [
                    "Connecting agents physically with cables",
                    "Running multiple agents at the same time",
                    "Transforming output of one agent into input of the next sequentially",
                    "Creating backup copies of agents"
                ],
                2, "Agent chaining involves sequential execution where the output of one agent becomes the input for the next agent.",
                "Chaining", "Beginner", 1
            ),

            # === INTERMEDIATE LEVEL ===
            QuizQuestion(
                "When should you use LLM orchestration over code orchestration?",
                [
                    "Always, it's more advanced",
                    "For open-ended, creative, or strategic tasks requiring reasoning",
                    "For simple, predictable operations",
                    "When you need maximum performance"
                ],
                1, "LLM orchestration is best for open-ended, creative, or strategic tasks that require reasoning and adaptability.",
                "Strategy Selection", "Intermediate", 2
            ),

            QuizQuestion(
                "What is structured output used for in code orchestration?",
                [
                    "Creating better documentation",
                    "Improving agent performance",
                    "Making deterministic routing decisions based on agent classifications",
                    "Reducing memory usage"
                ],
                2, "Structured outputs enable deterministic routing decisions by providing classification and analysis data that code can process.",
                "Structured Outputs", "Intermediate", 2
            ),

            QuizQuestion(
                "Which pattern uses a while loop with an evaluator agent?",
                [
                    "Parallel execution pattern",
                    "Sequential chaining pattern",
                    "Iterative improvement pattern",
                    "Structured routing pattern"
                ],
                2, "The iterative improvement pattern uses a while loop with an evaluator agent to continuously improve output until quality criteria are met.",
                "Patterns", "Intermediate", 2
            ),

            QuizQuestion(
                "What's a key consideration when running agents in parallel?",
                [
                    "All agents must be identical",
                    "Tasks should be independent and not depend on each other's results",
                    "Only one agent can run at a time",
                    "Parallel execution is always slower"
                ],
                1, "For parallel execution, tasks should be independent so they can run concurrently without dependencies.",
                "Parallel Execution", "Intermediate", 2
            ),

            QuizQuestion(
                "How do you implement task classification for routing?",
                [
                    "Use random selection",
                    "Always use the same agent",
                    "Use an agent with structured output to classify tasks into categories",
                    "Let users choose the agent manually"
                ],
                2, "Task classification uses an agent with structured output (like Pydantic models) to classify tasks into categories for routing decisions.",
                "Task Routing", "Intermediate", 2
            ),

            QuizQuestion(
                "What's the benefit of specialized agents over general-purpose agents?",
                [
                    "They use less memory",
                    "They excel in specific domains and provide higher quality results",
                    "They're easier to configure",
                    "They run faster"
                ],
                1, "Specialized agents excel in specific domains and typically provide higher quality results than general-purpose agents.",
                "Specialization", "Intermediate", 2
            ),

            # === ADVANCED LEVEL ===
            QuizQuestion(
                "What is hybrid orchestration?",
                [
                    "Using both sync and async agents",
                    "Combining LLM intelligence with code control for adaptive execution",
                    "Running agents on multiple servers",
                    "Using both cloud and local agents"
                ],
                1, "Hybrid orchestration combines LLM intelligence for creative decisions with code control for deterministic operations.",
                "Hybrid Patterns", "Advanced", 3
            ),

            QuizQuestion(
                "How should you handle failures in multi-agent orchestration?",
                [
                    "Ignore failures and continue",
                    "Always restart from the beginning",
                    "Implement fallback strategies and graceful degradation",
                    "Stop all agents immediately"
                ],
                2, "Implement fallback strategies and graceful degradation to handle failures without losing all progress.",
                "Error Handling", "Advanced", 3
            ),

            QuizQuestion(
                "What's the best approach for monitoring multi-agent workflows?",
                [
                    "Only log final results",
                    "Implement comprehensive logging, tracing, and performance metrics",
                    "Monitor only failed executions",
                    "Use random sampling for monitoring"
                ],
                1, "Comprehensive logging, tracing, and performance metrics are essential for monitoring complex multi-agent workflows.",
                "Monitoring", "Advanced", 3
            ),

            QuizQuestion(
                "When implementing iterative improvement, what prevents infinite loops?",
                [
                    "The agents eventually stop working",
                    "Maximum iteration limits and quality thresholds",
                    "Network timeouts",
                    "Random stopping conditions"
                ],
                1, "Maximum iteration limits and quality thresholds prevent infinite loops in iterative improvement patterns.",
                "Iterative Patterns", "Advanced", 3
            ),

            QuizQuestion(
                "What's a key performance consideration for large-scale multi-agent systems?",
                [
                    "Using only the fastest agents",
                    "Managing token usage, API costs, and latency optimization",
                    "Running everything sequentially",
                    "Using only free models"
                ],
                1, "Large-scale systems must carefully manage token usage, API costs, and optimize for latency to be cost-effective and performant.",
                "Performance", "Advanced", 3
            ),

            QuizQuestion(
                "How do you implement dynamic agent configuration in orchestration?",
                [
                    "Hard-code all configurations",
                    "Use reflection and runtime modification of agent properties like handoffs",
                    "Restart the entire system",
                    "Create new agents for each task"
                ],
                1, "Dynamic configuration involves runtime modification of agent properties like handoffs and tools based on task requirements.",
                "Dynamic Configuration", "Advanced", 3
            ),

            # === PRACTICAL SCENARIOS ===
            QuizQuestion(
                "You need to process 100 research tasks that are independent. Which pattern should you use?",
                [
                    "Sequential chaining",
                    "Parallel execution with asyncio.gather",
                    "Iterative improvement",
                    "Single agent processing"
                ],
                1, "Independent tasks benefit from parallel execution using asyncio.gather for speed and efficiency.",
                "Practical Application", "Intermediate", 2
            ),

            QuizQuestion(
                "For a creative writing task requiring research, planning, writing, and editing, which approach is best?",
                [
                    "Single agent handling everything",
                    "Sequential chaining through specialized agents",
                    "Parallel execution of all steps",
                    "Random agent selection"
                ],
                1, "Creative tasks with dependencies benefit from sequential chaining through specialized agents (research -> planning -> writing -> editing).",
                "Practical Application", "Intermediate", 2
            ),

            QuizQuestion(
                "How would you handle a task that's sometimes creative and sometimes routine?",
                [
                    "Always use LLM orchestration",
                    "Always use code orchestration",
                    "Use hybrid orchestration with task analysis for adaptive routing",
                    "Use random selection"
                ],
                2, "Variable tasks benefit from hybrid orchestration with task analysis to adaptively choose the best approach.",
                "Practical Application", "Advanced", 3
            ),

            QuizQuestion(
                "For a customer support system handling diverse queries, what's the best orchestration strategy?",
                [
                    "Single general-purpose agent",
                    "Task classification with routing to specialized agents",
                    "Random agent assignment",
                    "Always escalate to humans"
                ],
                1, "Customer support benefits from task classification to route queries to appropriate specialized agents (technical, billing, general, etc.).",
                "Practical Application", "Advanced", 3
            ),

            # === BEST PRACTICES ===
            QuizQuestion(
                "What's important when designing prompts for orchestrator agents?",
                [
                    "Keep them as short as possible",
                    "Make them clear about available tools, handoffs, and decision-making process",
                    "Use only technical language",
                    "Avoid mentioning specific capabilities"
                ],
                1, "Orchestrator prompts should clearly explain available tools, handoffs, and decision-making processes for effective autonomous operation.",
                "Best Practices", "Intermediate", 2
            ),

            QuizQuestion(
                "How should you test multi-agent orchestration systems?",
                [
                    "Only test individual agents",
                    "Test end-to-end workflows with various scenarios and edge cases",
                    "Only test successful scenarios",
                    "Testing is not necessary"
                ],
                1, "Test complete end-to-end workflows with various scenarios, edge cases, and failure conditions to ensure robustness.",
                "Testing", "Advanced", 3
            ),

            QuizQuestion(
                "What's crucial for maintaining multi-agent systems in production?",
                [
                    "Never change anything once deployed",
                    "Continuous monitoring, evaluation, and iterative improvement based on real usage",
                    "Only monitor failures",
                    "Use static configurations always"
                ],
                1, "Production systems require continuous monitoring, evaluation, and iterative improvement based on real usage patterns and feedback.",
                "Production", "Advanced", 3
            ),

            QuizQuestion(
                "When should you consider breaking down a single complex agent into multiple agents?",
                [
                    "Never, single agents are always better",
                    "When the agent handles multiple distinct domains or the task is too complex",
                    "Only for simple tasks",
                    "Random timing"
                ],
                1, "Break down agents when they handle multiple distinct domains or when tasks become too complex for effective single-agent handling.",
                "Architecture", "Advanced", 3
            ),

            # === COMPARISON QUESTIONS ===
            QuizQuestion(
                "Compare: asyncio.gather vs sequential execution for independent tasks.",
                [
                    "Sequential is always faster",
                    "asyncio.gather enables parallel execution for faster completion",
                    "No difference in performance",
                    "asyncio.gather is only for dependent tasks"
                ],
                1, "asyncio.gather enables parallel execution of independent tasks, significantly reducing total execution time.",
                "Performance Comparison", "Intermediate", 2
            ),

            QuizQuestion(
                "What's the trade-off between LLM and code orchestration in terms of cost?",
                [
                    "Both cost the same",
                    "LLM orchestration typically costs more due to additional reasoning calls",
                    "Code orchestration always costs more",
                    "Cost doesn't matter in orchestration"
                ],
                1, "LLM orchestration typically costs more due to additional API calls for reasoning and decision-making, while code orchestration has more predictable costs.",
                "Cost Analysis", "Advanced", 3
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

        print(f"\n🤖 OpenAI Agents SDK - Multi-Agent Orchestration Quiz 🤖")
        print(f"Mode: {mode.title()}")
        print(f"Questions: {len(selected_questions)}")
        print("=" * 60)

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

        print("\n" + "=" * 60)
        print("🎯 QUIZ RESULTS 🎯")
        print("=" * 60)
        print(
            f"Score: {self.score}/{max_possible_score} points ({percentage:.1f}%)")
        print(f"Questions answered: {self.total_questions}")

        # Performance categories
        if percentage >= 90:
            grade = "🏆 Excellent! You have mastered multi-agent orchestration!"
        elif percentage >= 80:
            grade = "🥇 Great! You have a strong understanding of orchestration patterns."
        elif percentage >= 70:
            grade = "🥈 Good! Review the areas where you missed questions."
        elif percentage >= 60:
            grade = "🥉 Fair. Consider reviewing the documentation and examples."
        else:
            grade = "📚 Study needed. Review the multi-agent orchestration examples."

        print(f"\nGrade: {grade}")

        # Category performance analysis
        self._show_category_analysis(questions)

        print("\n📚 Study Resources:")
        print("• Review 01_llm_orchestrated_agents.py for LLM intelligence patterns")
        print("• Study 02_code_orchestrated_agents.py for deterministic patterns")
        print("• Explore 03_hybrid_orchestration.py for adaptive strategies")
        print("• Practice with different orchestration patterns in your projects")
        print("• Read the OpenAI documentation on multi-agent patterns")

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

    def _run_custom_questions(self, questions: List[QuizQuestion], mode_name: str):
        """Run quiz with custom question set."""
        print(f"\n🤖 OpenAI Agents SDK - Multi-Agent Orchestration Quiz 🤖")
        print(f"Mode: {mode_name}")
        print(f"Questions: {len(questions)}")
        print("=" * 60)

        for i, question in enumerate(questions, 1):
            self._ask_question(i, question)

        self._show_final_results(questions)


def run_custom_quiz():
    """Run a customized quiz based on user preferences."""
    quiz = MultiAgentQuiz()

    print("🎮 Welcome to the Multi-Agent Orchestration Quiz! 🎮")
    print("\nSelect quiz mode:")
    print("1. Mixed (all difficulty levels)")
    print("2. Beginner only")
    print("3. Intermediate only")
    print("4. Advanced only")
    print("5. Quick test (5 questions)")
    print("6. Full test (20 questions)")
    print("7. LLM Orchestration focus")
    print("8. Code Orchestration focus")
    print("9. Practical Applications focus")

    while True:
        try:
            choice = input("\nEnter your choice (1-9): ").strip()

            if choice == "1":
                quiz.run_quiz("mixed", 12)
                break
            elif choice == "2":
                quiz.run_quiz("beginner", 8)
                break
            elif choice == "3":
                quiz.run_quiz("intermediate", 8)
                break
            elif choice == "4":
                quiz.run_quiz("advanced", 8)
                break
            elif choice == "5":
                quiz.run_quiz("mixed", 5)
                break
            elif choice == "6":
                quiz.run_quiz("mixed", 20)
                break
            elif choice == "7":
                # Filter by LLM orchestration related categories
                llm_questions = []
                for q in quiz.questions:
                    if q.category in ["LLM Orchestration", "Handoffs", "Orchestration Basics"]:
                        llm_questions.append(q)
                selected = random.sample(
                    llm_questions, min(8, len(llm_questions)))
                quiz._run_custom_questions(selected, "LLM Orchestration Focus")
                break
            elif choice == "8":
                # Filter by code orchestration
                code_questions = []
                for q in quiz.questions:
                    if q.category in ["Code Orchestration", "Structured Outputs", "Parallel Execution", "Patterns"]:
                        code_questions.append(q)
                selected = random.sample(
                    code_questions, min(8, len(code_questions)))
                quiz._run_custom_questions(
                    selected, "Code Orchestration Focus")
                break
            elif choice == "9":
                # Filter by practical applications
                practical_questions = []
                for q in quiz.questions:
                    if q.category in ["Practical Application", "Best Practices", "Testing", "Production"]:
                        practical_questions.append(q)
                selected = random.sample(
                    practical_questions, min(8, len(practical_questions)))
                quiz._run_custom_questions(
                    selected, "Practical Applications Focus")
                break
            else:
                print("Please enter a number between 1 and 9")
        except KeyboardInterrupt:
            print("\n\nQuiz cancelled. Study well! 📚")
            return


async def main():
    """Main function to run the multi-agent orchestration quiz."""
    run_custom_quiz()

if __name__ == "__main__":
    asyncio.run(main())
