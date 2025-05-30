"""
04_configurations_visualizations_quiz.py

Interactive quiz for testing understanding of OpenAI Agents SDK configuration and visualization.
Covers basic configuration, advanced settings, visualization concepts, and production best practices.

Key Topics Tested:
- API keys and client configuration
- Tracing and logging setup
- RunConfig options
- Agent visualization
- Production configurations
- Security and performance settings

Run this to test your knowledge!
"""

import asyncio
import random
from typing import List, Dict, Any
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
    # Basic Configuration Questions
    QuizQuestion(
        question="What is the recommended way to store API keys for the OpenAI Agents SDK?",
        options={
            "a": "Hardcode them directly in the Python files",
            "b": "Store them in environment variables",
            "c": "Put them in a configuration file in the project repository",
            "d": "Pass them as command line arguments"
        },
        correct_answer="b",
        explanation="Environment variables are the recommended approach for storing API keys as they keep sensitive data out of code and allow for environment-specific configuration.",
        category="Basic Configuration",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="Which function is used to set a custom OpenAI client as the default for the SDK?",
        options={
            "a": "configure_openai_client()",
            "b": "set_default_openai_client()",
            "c": "update_openai_client()",
            "d": "initialize_client()"
        },
        correct_answer="b",
        explanation="set_default_openai_client() is the correct function to set a custom OpenAI client as the default for the entire SDK.",
        category="Basic Configuration",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="What happens when you call enable_verbose_stdout_logging()?",
        options={
            "a": "Only error messages are shown",
            "b": "All logging is disabled",
            "c": "Detailed debugging information is output to stdout",
            "d": "Logs are redirected to a file"
        },
        correct_answer="c",
        explanation="enable_verbose_stdout_logging() enables detailed debugging information to be output to stdout, which is useful during development.",
        category="Basic Configuration",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="Which environment variable disables LLM input/output logging?",
        options={
            "a": "OPENAI_AGENTS_DISABLE_LOGGING",
            "b": "OPENAI_AGENTS_DONT_LOG_MODEL_DATA",
            "c": "OPENAI_AGENTS_NO_MODEL_LOGS",
            "d": "OPENAI_DISABLE_TRACING"
        },
        correct_answer="b",
        explanation="OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1 disables logging of LLM input and output data, useful for privacy and compliance.",
        category="Basic Configuration",
        difficulty="Intermediate"
    ),

    # Visualization Questions
    QuizQuestion(
        question="What Python package is required for agent visualization?",
        options={
            "a": "matplotlib",
            "b": "plotly",
            "c": "graphviz",
            "d": "networkx"
        },
        correct_answer="c",
        explanation="Graphviz is required for agent visualization. Install with pip install 'openai-agents[viz]' and the system graphviz package.",
        category="Visualization",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="In agent visualizations, what do yellow rectangles represent?",
        options={
            "a": "Tools",
            "b": "Agents",
            "c": "Handoffs",
            "d": "Inputs"
        },
        correct_answer="b",
        explanation="Yellow rectangles represent AI agents in the visualization, while green ellipses represent tools and blue ellipses represent start/end points.",
        category="Visualization",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="What do dotted arrows represent in agent visualizations?",
        options={
            "a": "Agent handoffs",
            "b": "Data flow",
            "c": "Tool access (bidirectional)",
            "d": "Error paths"
        },
        correct_answer="c",
        explanation="Dotted arrows represent tool access, showing the bidirectional relationship between agents and the tools they can use.",
        category="Visualization",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="Which function generates an agent visualization graph?",
        options={
            "a": "create_graph()",
            "b": "visualize_agent()",
            "c": "draw_graph()",
            "d": "generate_visualization()"
        },
        correct_answer="c",
        explanation="draw_graph() from agents.extensions.visualization is the function used to generate agent visualization graphs.",
        category="Visualization",
        difficulty="Beginner"
    ),

    QuizQuestion(
        question="How do you save an agent visualization as a PNG file?",
        options={
            "a": "draw_graph(agent).save('filename.png')",
            "b": "draw_graph(agent, filename='graph')",
            "c": "draw_graph(agent, output='png')",
            "d": "export_graph(agent, 'filename')"
        },
        correct_answer="b",
        explanation="draw_graph(agent, filename='graph') saves the visualization as 'graph.png' in the current directory.",
        category="Visualization",
        difficulty="Intermediate"
    ),

    # RunConfig Questions
    QuizQuestion(
        question="What is the primary purpose of RunConfig?",
        options={
            "a": "To configure the OpenAI model parameters",
            "b": "To control agent execution settings and tracing",
            "c": "To set up tool configurations",
            "d": "To manage handoff behavior"
        },
        correct_answer="b",
        explanation="RunConfig is used to control agent execution settings, including tracing configuration, workflow names, and global guardrails.",
        category="RunConfig",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="Which RunConfig parameter groups related traces together?",
        options={
            "a": "trace_id",
            "b": "workflow_name",
            "c": "group_id",
            "d": "session_id"
        },
        correct_answer="c",
        explanation="group_id in RunConfig is used to group related traces together, useful for organizing traces from related operations.",
        category="RunConfig",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="What type of data can be stored in RunConfig.trace_metadata?",
        options={
            "a": "Only strings",
            "b": "Only numbers and strings",
            "c": "Any JSON-serializable data",
            "d": "Only predefined metadata fields"
        },
        correct_answer="c",
        explanation="trace_metadata can store any JSON-serializable data, allowing you to include custom information like user context, environment details, etc.",
        category="RunConfig",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="How do you disable tracing for a specific agent run?",
        options={
            "a": "Set max_turns=0 in RunConfig",
            "b": "Set tracing_disabled=True in RunConfig",
            "c": "Use set_tracing_disabled(True) globally",
            "d": "Both b and c are correct"
        },
        correct_answer="d",
        explanation="You can disable tracing either globally with set_tracing_disabled(True) or for a specific run with RunConfig(tracing_disabled=True).",
        category="RunConfig",
        difficulty="Advanced"
    ),

    # Advanced Configuration Questions
    QuizQuestion(
        question="What is the purpose of custom spans in tracing?",
        options={
            "a": "To replace agent spans entirely",
            "b": "To add fine-grained timing and metadata to specific operations",
            "c": "To disable certain parts of tracing",
            "d": "To change the trace format"
        },
        correct_answer="b",
        explanation="Custom spans allow you to add fine-grained timing and metadata to specific operations within your workflow, improving observability.",
        category="Advanced Configuration",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Which parameter in OpenAIChatCompletionsModel controls response randomness?",
        options={
            "a": "randomness",
            "b": "temperature",
            "c": "variance",
            "d": "creativity"
        },
        correct_answer="b",
        explanation="temperature controls the randomness of the model's responses. Higher values (0.8-1.0) make responses more creative, lower values (0.1-0.3) make them more deterministic.",
        category="Advanced Configuration",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="What is the recommended temperature setting for production chatbots?",
        options={
            "a": "0.0 (completely deterministic)",
            "b": "0.3-0.7 (balanced)",
            "c": "0.8-1.0 (highly creative)",
            "d": "1.5+ (maximum creativity)"
        },
        correct_answer="b",
        explanation="0.3-0.7 provides a good balance between consistency and natural variation for production chatbots. 0.0 can be too robotic, while high values can be unpredictable.",
        category="Advanced Configuration",
        difficulty="Advanced"
    ),

    # Production Configuration Questions
    QuizQuestion(
        question="In production environments, you should:",
        options={
            "a": "Enable verbose logging for better debugging",
            "b": "Disable sensitive data logging and use appropriate log levels",
            "c": "Set temperature to maximum for creative responses",
            "d": "Use unlimited max_turns for complex tasks"
        },
        correct_answer="b",
        explanation="Production environments should have disabled sensitive data logging (OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1) and appropriate log levels (ERROR/WARN) to protect privacy and reduce noise.",
        category="Production Configuration",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="What is a recommended max_turns setting for production?",
        options={
            "a": "1-2 (minimal interaction)",
            "b": "5-8 (controlled interaction)",
            "c": "10-15 (extended interaction)",
            "d": "Unlimited (no restrictions)"
        },
        correct_answer="b",
        explanation="5-8 max_turns provides a good balance for production, allowing sufficient interaction while preventing infinite loops and controlling costs.",
        category="Production Configuration",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Which timeout setting is recommended for production API calls?",
        options={
            "a": "5-10 seconds",
            "b": "15-30 seconds",
            "c": "60+ seconds",
            "d": "No timeout"
        },
        correct_answer="b",
        explanation="15-30 seconds provides enough time for complex LLM operations while preventing hanging connections in production environments.",
        category="Production Configuration",
        difficulty="Advanced"
    ),

    # Security Questions
    QuizQuestion(
        question="What is the security risk of logging model data in production?",
        options={
            "a": "Increased storage costs",
            "b": "Slower performance",
            "c": "Exposure of sensitive user inputs and AI responses",
            "d": "Higher API usage"
        },
        correct_answer="c",
        explanation="Logging model data can expose sensitive user inputs and AI responses, creating privacy and compliance risks in production systems.",
        category="Security",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="Best practice for API key management in container deployments:",
        options={
            "a": "Embed keys in Docker images",
            "b": "Use environment variables or secret management systems",
            "c": "Store keys in configuration files",
            "d": "Pass keys as command line arguments"
        },
        correct_answer="b",
        explanation="Use environment variables or dedicated secret management systems (like Kubernetes secrets) to avoid embedding sensitive data in images or code.",
        category="Security",
        difficulty="Advanced"
    ),

    # Practical Scenarios
    QuizQuestion(
        question="You need to trace related operations across multiple agent runs. What should you use?",
        options={
            "a": "Same trace_id for all runs",
            "b": "Same group_id in RunConfig",
            "c": "Same workflow_name",
            "d": "Custom metadata tags"
        },
        correct_answer="b",
        explanation="group_id in RunConfig is specifically designed to group related traces together, making it easy to analyze related operations.",
        category="Practical Scenarios",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="Your agent visualization shows many disconnected components. This likely indicates:",
        options={
            "a": "Optimal architecture",
            "b": "Missing handoff relationships or poor organization",
            "c": "Too many tools",
            "d": "Correct security isolation"
        },
        correct_answer="b",
        explanation="Disconnected components in visualizations often indicate missing handoff relationships or poor architectural organization that should be reviewed.",
        category="Practical Scenarios",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="To debug agent execution issues, you should first:",
        options={
            "a": "Increase max_turns",
            "b": "Enable verbose logging and check traces",
            "c": "Reduce temperature",
            "d": "Add more tools"
        },
        correct_answer="b",
        explanation="Enable verbose logging and examine traces to understand the execution flow, errors, and decision points before making other changes.",
        category="Practical Scenarios",
        difficulty="Intermediate"
    ),

    QuizQuestion(
        question="You want to A/B test different agent configurations. What's the best approach?",
        options={
            "a": "Use different trace_metadata to tag experiments",
            "b": "Use separate API keys",
            "c": "Change workflow_name for each variant",
            "d": "Disable tracing for tests"
        },
        correct_answer="a",
        explanation="Use trace_metadata to tag different experiment variants, allowing you to analyze and compare results effectively.",
        category="Practical Scenarios",
        difficulty="Advanced"
    ),

    # Performance and Monitoring
    QuizQuestion(
        question="To monitor agent performance in production, you should track:",
        options={
            "a": "Only error rates",
            "b": "Response times, token usage, error rates, and user satisfaction",
            "c": "Only token costs",
            "d": "Only completion rates"
        },
        correct_answer="b",
        explanation="Comprehensive monitoring should include response times, token usage (cost), error rates, and user satisfaction metrics for a complete picture.",
        category="Performance and Monitoring",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What indicates you might need to optimize your agent architecture?",
        options={
            "a": "High handoff depth and long execution times",
            "b": "Too many successful completions",
            "c": "Low token usage",
            "d": "Few tool calls"
        },
        correct_answer="a",
        explanation="High handoff depth and long execution times suggest inefficient architecture that could benefit from optimization or redesign.",
        category="Performance and Monitoring",
        difficulty="Advanced"
    ),

    # Error Handling
    QuizQuestion(
        question="When configuring retry policies, you should consider:",
        options={
            "a": "Only the number of retries",
            "b": "Retry count, backoff strategy, and error types",
            "c": "Only the timeout duration",
            "d": "Only the API rate limits"
        },
        correct_answer="b",
        explanation="Effective retry policies consider retry count, backoff strategy (exponential, linear), and which error types should trigger retries.",
        category="Error Handling",
        difficulty="Advanced"
    ),

    QuizQuestion(
        question="What's the recommended approach for handling configuration validation errors?",
        options={
            "a": "Ignore them and continue",
            "b": "Log warnings but proceed",
            "c": "Fail fast with clear error messages",
            "d": "Use default values silently"
        },
        correct_answer="c",
        explanation="Fail fast with clear error messages helps identify configuration issues early and prevents runtime failures with unclear causes.",
        category="Error Handling",
        difficulty="Intermediate"
    )
]

# ================== QUIZ ENGINE ==================


class ConfigurationVisualizationQuiz:
    """Interactive quiz engine for configuration and visualization concepts."""

    def __init__(self):
        self.questions = QUIZ_QUESTIONS.copy()
        self.score = 0
        self.answers = []
        self.categories = {}

    def shuffle_questions(self):
        """Shuffle questions for randomized quiz experience."""
        random.shuffle(self.questions)

    def run_quiz(self, num_questions: int = None, difficulty: str = None, category: str = None):
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

        print(f"🧪 Configuration & Visualization Quiz")
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
                "🏆 Excellent! You have mastery of configuration and visualization concepts.")
        elif percentage >= 80:
            print("🥈 Great job! You understand most concepts well.")
        elif percentage >= 70:
            print("🥉 Good work! Some areas could use more review.")
        elif percentage >= 60:
            print("📚 Fair performance. Consider reviewing the documentation.")
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
                if "Basic Configuration" in category:
                    print(
                        "     • 01_basic_configuration.py - API keys, clients, logging")
                elif "Visualization" in category:
                    print("     • 02_agent_visualization.py - Graphviz, drawing graphs")
                elif "RunConfig" in category:
                    print("     • 03_advanced_configuration.py - RunConfig options")
                elif "Advanced Configuration" in category:
                    print("     • 03_advanced_configuration.py - Tracing, model config")
                elif "Production" in category:
                    print("     • 03_advanced_configuration.py - Production patterns")
                elif "Security" in category:
                    print("     • Security best practices and environment variables")

        print("\n🔗 Additional Resources:")
        print("   • https://openai.github.io/openai-agents-python/config/")
        print("   • https://openai.github.io/openai-agents-python/visualization/")
        print("   • Review the decoded/11_configurations_visualizations/ examples")

# ================== QUIZ MODES ==================


def quick_quiz():
    """Run a quick 10-question quiz."""
    quiz = ConfigurationVisualizationQuiz()
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
            quiz = ConfigurationVisualizationQuiz()
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
            quiz = ConfigurationVisualizationQuiz()
            quiz.shuffle_questions()
            quiz.run_quiz(difficulty=selected_difficulty)
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Please enter a valid number")


def full_quiz():
    """Run the complete quiz with all questions."""
    quiz = ConfigurationVisualizationQuiz()
    quiz.shuffle_questions()
    quiz.run_quiz()

# ================== MAIN EXECUTION ==================


def main():
    """Main quiz interface."""
    print("🎓 OpenAI Agents SDK - Configuration & Visualization Quiz 🎓")
    print("\nTest your knowledge of SDK configuration and agent visualization!")
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
