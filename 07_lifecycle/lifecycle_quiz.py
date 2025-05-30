"""
Lifecycle Management Quiz - CLI Assessment

This quiz tests your understanding of the advanced lifecycle concepts you've mastered
in the 07_lifecycle directory. It covers RunHooks, AgentHooks, combined patterns,
and production lifecycle management.

Topics Covered:
- RunHooks vs AgentHooks patterns
- Event tracking and monitoring
- Performance optimization patterns
- Multi-tenant monitoring systems
- SLA compliance and alerting
- Production observability patterns

Run this quiz to validate your expertise before moving to the next phase!
"""

import asyncio
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# ============================================================================
# Quiz Infrastructure
# ============================================================================


@dataclass
class Question:
    """Quiz question model"""
    id: str
    question: str
    options: List[str]
    correct_answer: int  # Index of correct option
    explanation: str
    difficulty: str  # "basic", "intermediate", "advanced", "expert"
    category: str


@dataclass
class QuizResult:
    """Quiz result tracking"""
    total_questions: int = 0
    correct_answers: int = 0
    by_category: Dict[str, Dict[str, int]] = field(default_factory=dict)
    by_difficulty: Dict[str, Dict[str, int]] = field(default_factory=dict)
    incorrect_questions: List[Question] = field(default_factory=list)
    time_taken: float = 0.0


class LifecycleQuiz:
    """Interactive CLI quiz for lifecycle management concepts"""

    def __init__(self):
        self.questions = self._load_questions()
        self.result = QuizResult()

    def _load_questions(self) -> List[Question]:
        """Load all quiz questions"""
        return [
            # ============================================================================
            # Basic RunHooks Questions
            # ============================================================================
            Question(
                id="rh_001",
                question="What is the primary purpose of RunHooks in the OpenAI Agents SDK?",
                options=[
                    "To handle individual agent lifecycle events",
                    "To monitor and respond to global run-level events and transitions",
                    "To manage tool execution within agents",
                    "To configure agent model parameters"
                ],
                correct_answer=1,
                explanation="RunHooks are designed to monitor and respond to global run-level events, providing observability and control over the entire execution flow.",
                difficulty="basic",
                category="RunHooks Fundamentals"
            ),

            Question(
                id="rh_002",
                question="Which RunHook method is called when an agent handoff occurs?",
                options=[
                    "on_run_step_done()",
                    "on_agent_handoff()",
                    "on_tool_call_done()",
                    "on_run_done()"
                ],
                correct_answer=1,
                explanation="The on_agent_handoff() method is specifically called when control is transferred from one agent to another.",
                difficulty="basic",
                category="RunHooks Fundamentals"
            ),

            Question(
                id="rh_003",
                question="In performance monitoring with RunHooks, what should you track to optimize response times?",
                options=[
                    "Only tool execution time",
                    "Only LLM inference time",
                    "Total run time, step duration, tool calls, and handoff latency",
                    "Only memory usage"
                ],
                correct_answer=2,
                explanation="Comprehensive performance monitoring requires tracking multiple metrics including total run time, individual step durations, tool execution times, and handoff latency.",
                difficulty="intermediate",
                category="Performance Monitoring"
            ),

            # ============================================================================
            # AgentHooks Questions
            # ============================================================================
            Question(
                id="ah_001",
                question="How do AgentHooks differ from RunHooks in scope and purpose?",
                options=[
                    "AgentHooks monitor global events, RunHooks monitor individual agents",
                    "AgentHooks monitor individual agent behavior, RunHooks monitor global run events",
                    "They are identical in functionality",
                    "AgentHooks only work with streaming responses"
                ],
                correct_answer=1,
                explanation="AgentHooks focus on individual agent-level events and behavior, while RunHooks monitor global run-level events across all agents.",
                difficulty="intermediate",
                category="AgentHooks Fundamentals"
            ),

            Question(
                id="ah_002",
                question="Which pattern enables an agent to learn and improve from its past interactions?",
                options=[
                    "Static configuration patterns",
                    "LearningAgentHooks with performance tracking and adaptive optimization",
                    "Basic logging hooks",
                    "Tool validation hooks"
                ],
                correct_answer=1,
                explanation="LearningAgentHooks implement adaptive patterns that track performance metrics and automatically adjust agent behavior based on past interactions.",
                difficulty="advanced",
                category="Adaptive Learning"
            ),

            Question(
                id="ah_003",
                question="In agent quality assessment, what metrics should LearningAgentHooks track for continuous improvement?",
                options=[
                    "Only response time",
                    "Response quality scores, user satisfaction, error rates, and performance trends",
                    "Only memory usage",
                    "Only token consumption"
                ],
                correct_answer=1,
                explanation="Comprehensive quality assessment requires tracking multiple dimensions: response quality, user satisfaction, error rates, and performance trends over time.",
                difficulty="advanced",
                category="Quality Assessment"
            ),

            # ============================================================================
            # Combined Patterns Questions
            # ============================================================================
            Question(
                id="cp_001",
                question="What is the main advantage of using an Event Bus architecture for lifecycle management?",
                options=[
                    "Reduced memory usage",
                    "Centralized event processing with loose coupling between components",
                    "Faster execution speed",
                    "Simpler code structure"
                ],
                correct_answer=1,
                explanation="Event Bus architecture enables centralized event processing while maintaining loose coupling, allowing multiple systems to observe and react to lifecycle events independently.",
                difficulty="intermediate",
                category="Event Architecture"
            ),

            Question(
                id="cp_002",
                question="In multi-level event correlation, what enables tracking complex workflows across multiple agents?",
                options=[
                    "Simple event logging",
                    "Correlation IDs, event chains, and workflow context tracking",
                    "Agent naming conventions",
                    "Tool function names"
                ],
                correct_answer=1,
                explanation="Multi-level correlation uses correlation IDs to link related events, event chains to track sequences, and workflow context to understand cross-agent interactions.",
                difficulty="advanced",
                category="Event Correlation"
            ),

            Question(
                id="cp_003",
                question="What pattern enables real-time alerting when agent performance degrades?",
                options=[
                    "Batch processing logs",
                    "Real-time event streaming with threshold monitoring and alert generation",
                    "Manual log review",
                    "Daily report generation"
                ],
                correct_answer=1,
                explanation="Real-time alerting requires event streaming that continuously monitors performance metrics against thresholds and generates immediate alerts when violations occur.",
                difficulty="advanced",
                category="Real-time Monitoring"
            ),

            # ============================================================================
            # Production Patterns Questions
            # ============================================================================
            Question(
                id="pp_001",
                question="In production SLA compliance monitoring, what should trigger a CRITICAL alert?",
                options=[
                    "Any performance deviation",
                    "SLA violations exceeding 50% of threshold with sustained impact",
                    "Single slow response",
                    "Agent restart events"
                ],
                correct_answer=1,
                explanation="CRITICAL alerts should be reserved for significant SLA violations (typically >50% threshold breach) with sustained impact to avoid alert fatigue.",
                difficulty="advanced",
                category="SLA Management"
            ),

            Question(
                id="pp_002",
                question="How should multi-tenant monitoring isolate metrics and alerts between different clients?",
                options=[
                    "Use a single shared dashboard",
                    "Tenant-specific hooks, isolated metrics stores, and tenant-scoped alerting",
                    "Manual separation in reports",
                    "Different agent models per tenant"
                ],
                correct_answer=1,
                explanation="Multi-tenant isolation requires tenant-specific hooks, separate metrics stores, and scoped alerting to ensure data privacy and relevant notifications.",
                difficulty="expert",
                category="Multi-tenant Architecture"
            ),

            Question(
                id="pp_003",
                question="What is the recommended approach for automated escalation in production monitoring?",
                options=[
                    "Immediate escalation for all alerts",
                    "Severity-based escalation with time delays and automatic resolution detection",
                    "Manual escalation only",
                    "Email-only notifications"
                ],
                correct_answer=1,
                explanation="Effective escalation uses severity levels, appropriate time delays for each level, and automatic resolution detection to reduce noise and ensure appropriate response.",
                difficulty="expert",
                category="Alert Escalation"
            ),

            # ============================================================================
            # Advanced Concepts Questions
            # ============================================================================
            Question(
                id="ac_001",
                question="In enterprise observability, what combination provides comprehensive monitoring coverage?",
                options=[
                    "Logs only",
                    "Metrics, logs, traces, and distributed correlation with real-time dashboards",
                    "Metrics and logs only",
                    "Manual monitoring only"
                ],
                correct_answer=1,
                explanation="Enterprise observability requires the full stack: metrics for quantitative data, logs for detailed events, traces for request flows, and correlation for understanding complex interactions.",
                difficulty="expert",
                category="Enterprise Observability"
            ),

            Question(
                id="ac_002",
                question="How should capacity planning use lifecycle data to predict scaling needs?",
                options=[
                    "Based on current usage only",
                    "Historical trend analysis, load pattern recognition, and predictive modeling",
                    "Manual estimation",
                    "Fixed scaling schedules"
                ],
                correct_answer=1,
                explanation="Effective capacity planning analyzes historical trends, recognizes load patterns, and uses predictive models to anticipate scaling needs before they become critical.",
                difficulty="expert",
                category="Capacity Planning"
            ),

            Question(
                id="ac_003",
                question="What pattern enables automated optimization based on lifecycle data?",
                options=[
                    "Manual tuning",
                    "Feedback loops with performance analysis and adaptive configuration updates",
                    "Static configurations",
                    "Random parameter changes"
                ],
                correct_answer=1,
                explanation="Automated optimization requires feedback loops that analyze performance data and automatically adjust configurations based on observed patterns and outcomes.",
                difficulty="expert",
                category="Automated Optimization"
            ),

            # ============================================================================
            # Integration and Best Practices
            # ============================================================================
            Question(
                id="bp_001",
                question="What is the recommended pattern for combining RunHooks and AgentHooks in production?",
                options=[
                    "Use only RunHooks",
                    "Hierarchical monitoring with RunHooks for global oversight and AgentHooks for detailed behavior",
                    "Use only AgentHooks",
                    "Alternate between them randomly"
                ],
                correct_answer=1,
                explanation="Best practice is hierarchical monitoring: RunHooks provide global oversight and coordination, while AgentHooks provide detailed behavioral insights for individual agents.",
                difficulty="advanced",
                category="Integration Patterns"
            ),

            Question(
                id="bp_002",
                question="How should lifecycle hooks handle errors to maintain system stability?",
                options=[
                    "Crash the application on any hook error",
                    "Graceful error handling with logging, fallback mechanisms, and isolated execution",
                    "Ignore all hook errors",
                    "Retry infinitely"
                ],
                correct_answer=1,
                explanation="Lifecycle hooks should implement graceful error handling with proper logging, fallback mechanisms, and isolated execution to prevent hook errors from affecting the main application flow.",
                difficulty="intermediate",
                category="Error Handling"
            ),

            Question(
                id="bp_003",
                question="What is the key principle for designing scalable lifecycle monitoring systems?",
                options=[
                    "Centralize everything in one component",
                    "Stateless, event-driven design with distributed processing and horizontal scaling",
                    "Use only local monitoring",
                    "Manual monitoring approaches"
                ],
                correct_answer=1,
                explanation="Scalable monitoring systems must be stateless and event-driven, enabling distributed processing and horizontal scaling to handle large agent populations.",
                difficulty="expert",
                category="Scalability Design"
            )
        ]

    def run_quiz(self, num_questions: Optional[int] = None, difficulty_filter: Optional[str] = None) -> QuizResult:
        """Run the interactive quiz"""
        print("🧠 OpenAI Agents SDK - Lifecycle Management Quiz")
        print("=" * 60)
        print("Testing your expertise in advanced lifecycle patterns!\n")

        # Filter and select questions
        available_questions = self.questions
        if difficulty_filter:
            available_questions = [
                q for q in available_questions if q.difficulty == difficulty_filter]

        if num_questions:
            available_questions = random.sample(
                available_questions, min(num_questions, len(available_questions)))
        else:
            available_questions = random.sample(
                available_questions, min(15, len(available_questions)))

        print(f"📝 Quiz Overview:")
        print(f"   Questions: {len(available_questions)}")
        print(f"   Difficulty: {difficulty_filter or 'Mixed'}")
        print(f"   Topics: RunHooks, AgentHooks, Production Patterns, Enterprise Observability")
        print("\n" + "=" * 60 + "\n")

        start_time = time.time()

        for i, question in enumerate(available_questions, 1):
            self._ask_question(i, question, len(available_questions))

        self.result.time_taken = time.time() - start_time
        self._show_results()
        return self.result

    def _ask_question(self, question_num: int, question: Question, total: int):
        """Ask a single question and process the answer"""
        print(
            f"Question {question_num}/{total} [{question.difficulty.upper()}] - {question.category}")
        print(f"📋 {question.question}\n")

        for i, option in enumerate(question.options):
            print(f"   {i + 1}. {option}")

        while True:
            try:
                print(f"\n💭 Your answer (1-{len(question.options)}): ", end="")
                user_answer = int(input()) - 1

                if 0 <= user_answer < len(question.options):
                    break
                else:
                    print(
                        f"❌ Please enter a number between 1 and {len(question.options)}")
            except ValueError:
                print(
                    f"❌ Please enter a valid number between 1 and {len(question.options)}")

        # Track results
        self.result.total_questions += 1

        # Initialize category tracking
        if question.category not in self.result.by_category:
            self.result.by_category[question.category] = {
                "correct": 0, "total": 0}
        if question.difficulty not in self.result.by_difficulty:
            self.result.by_difficulty[question.difficulty] = {
                "correct": 0, "total": 0}

        self.result.by_category[question.category]["total"] += 1
        self.result.by_difficulty[question.difficulty]["total"] += 1

        if user_answer == question.correct_answer:
            print("✅ Correct!")
            self.result.correct_answers += 1
            self.result.by_category[question.category]["correct"] += 1
            self.result.by_difficulty[question.difficulty]["correct"] += 1
        else:
            print(
                f"❌ Incorrect. The correct answer was: {question.options[question.correct_answer]}")
            self.result.incorrect_questions.append(question)

        print(f"\n💡 Explanation: {question.explanation}")
        print("\n" + "-" * 60 + "\n")

    def _show_results(self):
        """Display comprehensive quiz results"""
        score_percentage = (self.result.correct_answers /
                            self.result.total_questions) * 100

        print("🎯 QUIZ RESULTS")
        print("=" * 60)
        print(
            f"📊 Overall Score: {self.result.correct_answers}/{self.result.total_questions} ({score_percentage:.1f}%)")
        print(f"⏱️  Time Taken: {self.result.time_taken:.1f} seconds")
        print(
            f"⚡ Average Time per Question: {self.result.time_taken / self.result.total_questions:.1f} seconds")

        # Performance assessment
        if score_percentage >= 90:
            print("🏆 EXPERT LEVEL - Outstanding mastery of lifecycle concepts!")
        elif score_percentage >= 80:
            print("🥇 ADVANCED LEVEL - Strong understanding with minor gaps")
        elif score_percentage >= 70:
            print("🥈 INTERMEDIATE LEVEL - Good foundation, some concepts need review")
        elif score_percentage >= 60:
            print("🥉 BASIC LEVEL - Understanding established, significant review needed")
        else:
            print("📚 LEARNING PHASE - Recommend reviewing lifecycle documentation")

        print("\n📈 Performance by Category:")
        print("-" * 40)
        for category, stats in self.result.by_category.items():
            cat_score = (stats["correct"] / stats["total"]) * 100
            print(
                f"   {category}: {stats['correct']}/{stats['total']} ({cat_score:.1f}%)")

        print("\n🎚️  Performance by Difficulty:")
        print("-" * 40)
        for difficulty, stats in self.result.by_difficulty.items():
            diff_score = (stats["correct"] / stats["total"]) * 100
            print(
                f"   {difficulty.title()}: {stats['correct']}/{stats['total']} ({diff_score:.1f}%)")

        if self.result.incorrect_questions:
            print(
                f"\n🔍 Review Recommendations ({len(self.result.incorrect_questions)} topics):")
            print("-" * 50)
            for question in self.result.incorrect_questions:
                print(f"   • {question.category}: {question.question[:60]}...")

        print("\n🎓 Next Steps:")
        print("-" * 20)
        if score_percentage >= 80:
            print("   ✅ Ready for Phase 4: Expert Level (Agent Orchestration)")
            print("   ✅ Strong foundation in lifecycle management")
            print("   ✅ Prepared for production deployment patterns")
        elif score_percentage >= 70:
            print("   📖 Consider reviewing advanced lifecycle patterns")
            print("   💡 Focus on production monitoring and multi-tenant concepts")
            print("   ⚡ Ready for Phase 4 with some additional study")
        else:
            print("   📚 Recommend reviewing 07_lifecycle examples")
            print("   🔄 Retake quiz after additional study")
            print("   💭 Focus on fundamental RunHooks and AgentHooks patterns")

        print("\n" + "=" * 60)


def main():
    """Run the lifecycle management quiz"""
    quiz = LifecycleQuiz()

    print("Welcome to the Lifecycle Management Expertise Quiz!")
    print("This will test your understanding of the concepts from 07_lifecycle\n")

    while True:
        print("Quiz Options:")
        print("1. Full Quiz (15 random questions)")
        print("2. Quick Quiz (8 questions)")
        print("3. Basic Level Only")
        print("4. Advanced Level Only")
        print("5. Expert Level Only")
        print("6. Exit")

        try:
            choice = input("\nSelect option (1-6): ").strip()

            if choice == "1":
                quiz.run_quiz()
                break
            elif choice == "2":
                quiz.run_quiz(num_questions=8)
                break
            elif choice == "3":
                quiz.run_quiz(difficulty_filter="basic")
                break
            elif choice == "4":
                quiz.run_quiz(difficulty_filter="advanced")
                break
            elif choice == "5":
                quiz.run_quiz(difficulty_filter="expert")
                break
            elif choice == "6":
                print("👋 Thanks for using the Lifecycle Management Quiz!")
                break
            else:
                print("❌ Please select a valid option (1-6)")
        except KeyboardInterrupt:
            print("\n\n👋 Quiz interrupted. Thanks for participating!")
            break


if __name__ == "__main__":
    main()
