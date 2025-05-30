"""
06_streaming_quiz.py

Comprehensive quiz covering OpenAI Agents SDK streaming concepts.

Categories:
- Basic Streaming Concepts
- Raw Response Events
- Run Item Events & Agent Events
- Streaming with Tools & Handoffs
- Production Patterns & Best Practices

Total: 50 questions across 3 difficulty levels
"""

import random
import time
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class QuizQuestion:
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    category: str
    difficulty: str
    points: int


class StreamingQuiz:
    def __init__(self):
        self.questions = self._create_questions()
        self.score = 0
        self.total_points = 0
        self.category_scores: Dict[str, Dict[str, int]] = {}
        self.start_time = None

    def _create_questions(self) -> List[QuizQuestion]:
        """Create all quiz questions organized by difficulty and category."""
        questions = []

        # BEGINNER LEVEL (20 questions, 1 point each)
        beginner_questions = [
            QuizQuestion(
                "Which method is used to start streaming execution?",
                ["Runner.run()", "Runner.run_streamed()",
                 "Agent.stream()", "Runner.stream()"],
                1, "Runner.run_streamed() is the method to start streaming execution.",
                "Basic Streaming", "Beginner", 1
            ),
            QuizQuestion(
                "What method do you call to iterate through streaming events?",
                ["get_events()", "stream_events()",
                 "iterate_events()", "event_stream()"],
                1, "stream_events() returns an async iterator for processing streaming events.",
                "Basic Streaming", "Beginner", 1
            ),
            QuizQuestion(
                "What type of object does Runner.run_streamed() return?",
                ["RunResult", "RunResultStreaming", "StreamResult", "AsyncResult"],
                1, "Runner.run_streamed() returns a RunResultStreaming object.",
                "Basic Streaming", "Beginner", 1
            ),
            QuizQuestion(
                "How do you identify raw response events in the stream?",
                ["event.type == 'raw'", "event.type == 'raw_response_event'",
                    "event.is_raw", "event.raw == True"],
                1, "Raw response events have event.type == 'raw_response_event'.",
                "Raw Response Events", "Beginner", 1
            ),
            QuizQuestion(
                "What class contains individual text tokens in raw response events?",
                ["TextDelta", "ResponseTextDeltaEvent", "TokenEvent", "TextChunk"],
                1, "ResponseTextDeltaEvent contains individual text tokens in event.data.delta.",
                "Raw Response Events", "Beginner", 1
            ),
            QuizQuestion(
                "How do you access the text content from a ResponseTextDeltaEvent?",
                ["event.text", "event.data.delta", "event.content", "event.token"],
                1, "Use event.data.delta to access the text content from ResponseTextDeltaEvent.",
                "Raw Response Events", "Beginner", 1
            ),
            QuizQuestion(
                "What event type indicates an agent change during handoffs?",
                ["agent_change_event", "agent_updated_stream_event",
                    "handoff_event", "agent_switch_event"],
                1, "agent_updated_stream_event indicates when the current agent changes.",
                "Agent Events", "Beginner", 1
            ),
            QuizQuestion(
                "How do you access the new agent in an agent update event?",
                ["event.agent", "event.new_agent",
                    "event.current_agent", "event.updated_agent"],
                1, "Use event.new_agent to access the new agent in agent update events.",
                "Agent Events", "Beginner", 1
            ),
            QuizQuestion(
                "What event type provides higher-level item updates?",
                ["item_event", "run_item_stream_event",
                    "stream_item_event", "item_update_event"],
                1, "run_item_stream_event provides higher-level item updates like tool calls and messages.",
                "Run Item Events", "Beginner", 1
            ),
            QuizQuestion(
                "What item type indicates a tool was called?",
                ["tool_item", "tool_call_item",
                    "function_call_item", "tool_execution_item"],
                1, "tool_call_item indicates that a tool was called.",
                "Run Item Events", "Beginner", 1
            ),
            QuizQuestion(
                "What item type contains tool execution results?",
                ["tool_result_item", "tool_call_output_item",
                    "tool_response_item", "function_output_item"],
                1, "tool_call_output_item contains the results of tool execution.",
                "Run Item Events", "Beginner", 1
            ),
            QuizQuestion(
                "What item type contains final message content?",
                ["text_item", "message_output_item",
                    "response_item", "content_item"],
                1, "message_output_item contains the final message content from the agent.",
                "Run Item Events", "Beginner", 1
            ),
            QuizQuestion(
                "How do you extract text from a message_output_item?",
                ["item.text",
                    "ItemHelpers.text_message_output(item)", "item.content", "item.message"],
                1, "Use ItemHelpers.text_message_output(item) to extract text from message items.",
                "Run Item Events", "Beginner", 1
            ),
            QuizQuestion(
                "What is the main advantage of streaming responses?",
                ["Faster execution", "Lower memory usage",
                    "Real-time user feedback", "Better error handling"],
                2, "Streaming provides real-time user feedback as responses are generated.",
                "Basic Streaming", "Beginner", 1
            ),
            QuizQuestion(
                "Can you access final_output before streaming completes?",
                ["Yes, always", "No, it raises an exception",
                    "Yes, but it's empty", "Depends on the agent"],
                1, "Accessing final_output before streaming completes raises an exception.",
                "Basic Streaming", "Beginner", 1
            ),
            QuizQuestion(
                "What happens to handoffs in streaming mode?",
                ["They're disabled", "They work seamlessly",
                    "They require special handling", "They cause errors"],
                1, "Handoffs work seamlessly in streaming mode with agent_updated_stream_event notifications.",
                "Streaming with Handoffs", "Beginner", 1
            ),
            QuizQuestion(
                "How do you check if streaming has completed?",
                ["result.is_done", "result.is_complete",
                    "result.finished", "result.completed"],
                1, "Use result.is_complete to check if streaming has finished.",
                "Basic Streaming", "Beginner", 1
            ),
            QuizQuestion(
                "What should you do to ignore raw events and focus on high-level events?",
                ["Filter by event.level", "Check event.type != 'raw_response_event'",
                    "Use event.is_high_level", "Call filter_events()"],
                1, "Check event.type != 'raw_response_event' to ignore raw events.",
                "Production Patterns", "Beginner", 1
            ),
            QuizQuestion(
                "What's the typical pattern for token-by-token streaming?",
                ["Process all events", "Process only raw_response_event with ResponseTextDeltaEvent",
                    "Process only text events", "Process message events"],
                1, "Process raw_response_event with isinstance(event.data, ResponseTextDeltaEvent) for token-by-token streaming.",
                "Raw Response Events", "Beginner", 1
            ),
            QuizQuestion(
                "When should you prefer streaming over regular execution?",
                ["Always", "For long responses", "For short responses", "Never"],
                1, "Prefer streaming for long responses where real-time feedback improves user experience.",
                "Production Patterns", "Beginner", 1
            )
        ]

        # INTERMEDIATE LEVEL (20 questions, 2 points each)
        intermediate_questions = [
            QuizQuestion(
                "How do you implement buffered streaming for word-by-word output?",
                ["Buffer all text then output", "Buffer until space character, then output words",
                    "Use built-in buffering", "Buffer by sentence"],
                1, "Buffer text until space character, then output complete words for smoother display.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the best practice for error handling in streaming?",
                ["Ignore errors", "Catch all exceptions around stream_events()",
                 "Handle each event separately", "Use try-catch per event"],
                1, "Use try-catch around the entire stream_events() iteration for proper error handling.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you measure streaming performance effectively?",
                ["Total time only", "Time to first chunk and total time",
                    "Event count only", "Memory usage only"],
                1, "Measure both time to first chunk (user experience) and total execution time.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the correct way to handle streaming timeouts?",
                ["Increase timeout", "Use asyncio.wait_for()", "Ignore timeouts",
                 "Retry automatically"],
                1, "Use asyncio.wait_for() to implement proper timeout handling for streaming operations.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you implement stream cancellation?",
                ["Call cancel() method", "Break from the async for loop",
                 "Use stop() method", "Raise exception"],
                1, "Break from the async for loop to implement stream cancellation.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the recommended approach for UI progress updates?",
                ["Use raw events only", "Use run_item_stream_event for progress indicators",
                    "Use agent events only", "Poll for status"],
                1, "Use run_item_stream_event to provide meaningful progress indicators to users.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you validate streaming consistency?",
                ["Count events", "Reconstruct text from deltas and compare with final_output",
                    "Check timestamps", "Validate JSON"],
                1, "Reconstruct text from streaming deltas and compare with final_output for consistency.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the impact of tool usage on streaming?",
                ["No impact", "Increases latency due to tool execution",
                    "Decreases latency", "Breaks streaming"],
                1, "Tool usage increases latency as tools must execute before streaming can continue.",
                "Streaming with Tools", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you handle multiple concurrent streams?",
                ["Process sequentially", "Use asyncio.gather() for concurrent processing",
                 "Use threading", "Not possible"],
                1, "Use asyncio.gather() to process multiple streams concurrently.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the correct pattern for streaming event filtering?",
                ["Filter at source", "Filter during iteration based on event.type",
                    "Filter after completion", "No filtering needed"],
                1, "Filter events during iteration based on event.type to process only relevant events.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you implement fallback for streaming failures?",
                ["Retry streaming", "Use Runner.run() as fallback",
                 "Return error", "Cache previous result"],
                1, "Use Runner.run() as fallback when streaming fails to ensure user gets a response.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the best practice for logging streaming events?",
                ["Log all events", "Log errors only",
                    "Log selectively based on event type and importance", "No logging"],
                2, "Log selectively based on event type and importance to balance debugging with performance.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you track agent transitions in complex handoff scenarios?",
                ["Count agent_updated_stream_event occurrences",
                    "Store agent names in sequence", "Use event timestamps", "All of the above"],
                3, "Use all approaches: count events, store sequence, and track timestamps for complete analysis.",
                "Streaming with Handoffs", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the recommended memory management for long streams?",
                ["Store all events", "Process events immediately and discard",
                    "Batch events", "Use compression"],
                1, "Process streaming events immediately and discard to maintain memory efficiency.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you implement streaming rate limiting?",
                ["Limit requests", "Add delays between event processing",
                    "Limit bandwidth", "Use backpressure"],
                3, "Use backpressure mechanisms to implement proper streaming rate limiting.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the correct approach for streaming event aggregation?",
                ["Store all events", "Aggregate incrementally during streaming",
                    "Aggregate at end", "No aggregation"],
                1, "Aggregate streaming events incrementally to maintain memory efficiency and real-time updates.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you handle streaming in distributed systems?",
                ["Single node only", "Event streaming with message queues",
                    "Shared memory", "Database coordination"],
                1, "Use event streaming with message queues for distributed streaming processing.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the impact of network latency on streaming?",
                ["No impact", "Affects time to first chunk",
                    "Breaks streaming", "Requires buffering"],
                1, "Network latency primarily affects time to first chunk, impacting perceived performance.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you implement streaming event replay for debugging?",
                ["Store final results", "Store complete event streams with metadata",
                    "Store agent states", "Use logging only"],
                1, "Store complete event streams with metadata to enable accurate replay for debugging.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the best practice for streaming event validation?",
                ["Validate all events", "Validate critical events only",
                    "No validation", "Validate at end"],
                1, "Validate critical streaming events only to balance safety with performance.",
                "Production Patterns", "Intermediate", 2
            )
        ]

        # ADVANCED LEVEL (10 questions, 3 points each)
        advanced_questions = [
            QuizQuestion(
                "How do you implement custom streaming event processors for complex workflows?",
                ["Subclass StreamEvent", "Create event handler classes with type-specific processing",
                    "Use decorators", "Modify SDK source"],
                1, "Create dedicated event handler classes with type-specific processing for complex workflows.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the optimal strategy for streaming in high-concurrency scenarios?",
                ["Single-threaded processing", "Event-driven architecture with async processing",
                    "Thread pools", "Process pools"],
                1, "Use event-driven architecture with async processing for optimal high-concurrency streaming.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result persistence for audit trails?",
                ["Store final results only", "Stream events directly to persistent storage",
                    "Periodic snapshots", "Memory-only"],
                1, "Stream events directly to persistent storage for complete audit trails and replay capability.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the correct approach for streaming result compression?",
                ["Compress final output", "Compress event stream in real-time",
                    "Compress individual events", "No compression"],
                1, "Compress the event stream in real-time for optimal performance and storage efficiency.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming circuit breakers for resilience?",
                ["Monitor final results", "Monitor streaming health metrics in real-time",
                    "Monitor agent availability", "All metrics combined"],
                3, "Monitor all metrics: streaming health, agent availability, and results for comprehensive circuit breaking.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the best practice for streaming in microservices architecture?",
                ["Direct streaming", "Event sourcing with streaming projections",
                    "Synchronous calls", "Batch processing"],
                1, "Use event sourcing with streaming projections for microservices architecture.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming load balancing across multiple agents?",
                ["Round-robin", "Content-aware routing with streaming metrics",
                    "Random distribution", "Static assignment"],
                1, "Use content-aware routing combined with streaming performance metrics for optimal load balancing.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the optimal pattern for streaming result caching?",
                ["Cache final results", "Cache event patterns and stream signatures",
                    "Cache agent responses", "No caching"],
                1, "Cache event patterns and stream signatures for intelligent streaming result caching.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming observability for production systems?",
                ["Metrics only", "Logs only", "Traces only",
                    "Full observability with metrics, logs, traces, and distributed tracing"],
                3, "Implement full observability stack with metrics, logs, traces, and distributed tracing for streaming.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the correct approach for streaming security in zero-trust environments?",
                ["Encrypt final results", "End-to-end encryption with identity verification at every streaming hop",
                    "Use HTTPS only", "Token-based auth"],
                1, "Implement end-to-end encryption with identity verification at every streaming hop for zero-trust security.",
                "Production Patterns", "Advanced", 3
            )
        ]

        # Combine all questions
        questions.extend(beginner_questions)
        questions.extend(intermediate_questions)
        questions.extend(advanced_questions)

        return questions

    def run_quiz(self, mode: str = "full") -> None:
        """Run the quiz in different modes."""
        print("🌊 OpenAI Agents SDK - Streaming Expert Quiz")
        print("=" * 60)

        if mode == "full":
            selected_questions = self.questions
        elif mode == "quick":
            selected_questions = random.sample(self.questions, 15)
        elif mode == "beginner":
            selected_questions = [
                q for q in self.questions if q.difficulty == "Beginner"]
        elif mode == "intermediate":
            selected_questions = [
                q for q in self.questions if q.difficulty == "Intermediate"]
        elif mode == "advanced":
            selected_questions = [
                q for q in self.questions if q.difficulty == "Advanced"]
        else:
            selected_questions = self.questions

        self.start_time = time.time()

        for i, question in enumerate(selected_questions, 1):
            self._ask_question(i, question, len(selected_questions))

        self._show_results()

    def _ask_question(self, num: int, question: QuizQuestion, total: int) -> None:
        """Ask a single question and process the answer."""
        print(
            f"\n📝 Question {num}/{total} [{question.difficulty}] ({question.points} points)")
        print(f"Category: {question.category}")
        print(f"\n{question.question}")

        for i, option in enumerate(question.options):
            print(f"  {i + 1}. {option}")

        while True:
            try:
                answer = input(
                    f"\nYour answer (1-{len(question.options)}): ").strip()
                answer_idx = int(answer) - 1

                if 0 <= answer_idx < len(question.options):
                    break
                else:
                    print("❌ Invalid option. Please try again.")
            except ValueError:
                print("❌ Please enter a number.")

        # Update scores
        self.total_points += question.points
        if answer_idx == question.correct_answer:
            self.score += question.points
            print("✅ Correct!")
        else:
            print(
                f"❌ Incorrect. The correct answer is: {question.options[question.correct_answer]}")

        print(f"💡 Explanation: {question.explanation}")

        # Update category scores
        if question.category not in self.category_scores:
            self.category_scores[question.category] = {"earned": 0, "total": 0}

        self.category_scores[question.category]["total"] += question.points
        if answer_idx == question.correct_answer:
            self.category_scores[question.category]["earned"] += question.points

    def _show_results(self) -> None:
        """Display comprehensive quiz results."""
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        percentage = (self.score / self.total_points *
                      100) if self.total_points > 0 else 0

        print("\n" + "=" * 60)
        print("🎯 STREAMING QUIZ RESULTS")
        print("=" * 60)

        print(
            f"📊 Overall Score: {self.score}/{self.total_points} ({percentage:.1f}%)")
        print(f"⏱️  Time Taken: {elapsed_time:.1f} seconds")

        # Mastery level
        if percentage >= 95:
            level = "🏆 STREAMING EXPERT"
            message = "Outstanding! You have mastery-level understanding of streaming concepts."
        elif percentage >= 85:
            level = "🥇 ADVANCED STREAMER"
            message = "Excellent! You understand streaming with minor gaps."
        elif percentage >= 75:
            level = "🥈 INTERMEDIATE STREAMER"
            message = "Good! You understand basics but need advanced streaming practice."
        elif percentage >= 60:
            level = "🥉 BEGINNER STREAMER"
            message = "Fair understanding. Focus on streaming fundamentals."
        else:
            level = "📚 NEEDS STREAMING STUDY"
            message = "Significant gaps. Recommend thorough review of streaming concepts."

        print(f"\n🎖️  Mastery Level: {level}")
        print(f"💬 {message}")

        # Category breakdown
        print(f"\n📈 Category Performance:")
        for category, scores in self.category_scores.items():
            cat_percentage = (
                scores["earned"] / scores["total"] * 100) if scores["total"] > 0 else 0
            print(
                f"  {category}: {scores['earned']}/{scores['total']} ({cat_percentage:.1f}%)")

        # Study recommendations
        print(f"\n📚 Study Recommendations:")
        weak_categories = [cat for cat, scores in self.category_scores.items()
                           if (scores["earned"] / scores["total"] * 100) < 70]

        if weak_categories:
            print("Focus on these streaming areas:")
            for category in weak_categories:
                if "Basic" in category:
                    print(
                        f"  • {category}: Review fundamental streaming concepts")
                elif "Raw Response" in category:
                    print(
                        f"  • {category}: Practice token-by-token streaming patterns")
                elif "Run Item" in category:
                    print(f"  • {category}: Study high-level event processing")
                elif "Production" in category:
                    print(
                        f"  • {category}: Learn production streaming patterns")
                else:
                    print(
                        f"  • {category}: Review core concepts and practical applications")
        else:
            print("  🎉 Excellent performance across all streaming categories!")

        print(f"\n🔗 Streaming Resources:")
        print(
            "  • Streaming Guide: https://openai.github.io/openai-agents-python/streaming/")
        print("  • Practice with: 01_basic_streaming.py through 05_streaming_patterns.py")
        print("  • Advanced patterns: Focus on production streaming scenarios")


def main():
    """Main function to run the quiz."""
    quiz = StreamingQuiz()

    print("Select streaming quiz mode:")
    print("1. Full Quiz (50 questions)")
    print("2. Quick Assessment (15 questions)")
    print("3. Beginner Level Only")
    print("4. Intermediate Level Only")
    print("5. Advanced Level Only")

    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            modes = {
                "1": "full",
                "2": "quick",
                "3": "beginner",
                "4": "intermediate",
                "5": "advanced"
            }

            if choice in modes:
                quiz.run_quiz(modes[choice])
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
        except KeyboardInterrupt:
            print("\n\n👋 Quiz cancelled. Good luck with your streaming studies!")
            break


if __name__ == "__main__":
    main()
