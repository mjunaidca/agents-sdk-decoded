"""
05_results_expert_quiz.py

Comprehensive expert-level quiz covering RunResult and RunResultStreaming.

Categories:
- RunResult Basics & Attributes
- RunResultStreaming & Events  
- Advanced Usage Patterns
- Performance & Optimization
- Error Handling & Edge Cases
- Production Patterns

Total: 80 questions across 4 difficulty levels
"""

import random
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


class ResultsExpertQuiz:
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
                "What attribute of RunResult contains the final response from the agent?",
                ["final_output", "last_response", "result_text", "output_content"],
                0, "final_output contains the final response text from the agent execution.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "Which method converts RunResult to input format for the next conversation turn?",
                ["to_input_list()", "get_inputs()", "convert_to_input()",
                 "next_turn_input()"],
                0, "to_input_list() returns conversation history in format suitable for next turn.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What does RunResult.last_agent contain?",
                ["Agent name string", "Agent object that handled the final response",
                    "Agent ID", "Agent configuration"],
                1, "last_agent contains the actual Agent object that produced the final response.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "How do you check if a RunResultStreaming has completed?",
                ["is_finished", "is_complete", "has_ended", "stream_done"],
                1, "is_complete property indicates whether the streaming execution has finished.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What method is used to iterate through streaming events?",
                ["get_events()", "stream_events()",
                 "iterate_stream()", "event_iterator()"],
                1, "stream_events() returns an async iterator for processing streaming events.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What does RunResult.new_items contain?",
                ["Only new text responses", "All items generated during the run",
                    "Tool outputs only", "Error messages"],
                1, "new_items contains all items (messages, tool calls, outputs) generated during execution.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "Which is the correct way to run an agent with streaming?",
                ["Runner.stream()", "Runner.run_streamed()",
                 "Runner.run(stream=True)", "Agent.run_stream()"],
                1, "Runner.run_streamed() is the method to execute agents with streaming responses.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What type of object does Runner.run() return?",
                ["RunResult", "AgentResult", "ExecutionResult", "ResponseResult"],
                0, "Runner.run() returns a RunResult object containing execution results.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What type of object does Runner.run_streamed() return?",
                ["RunResult", "RunResultStreaming", "StreamResult", "AsyncResult"],
                1, "Runner.run_streamed() returns a RunResultStreaming object for streaming execution.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "How do you access the original input in a RunResult?",
                ["result.input", "result.original_input",
                    "result.user_input", "result.request"],
                0, "result.input contains the original input that was passed to the agent.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What happens when you access final_output on an incomplete RunResultStreaming?",
                ["Returns empty string", "Raises an exception",
                    "Returns None", "Blocks until complete"],
                1, "Accessing final_output on incomplete streaming raises an exception.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "Which attribute tells you how many items were generated during execution?",
                ["len(result.items)", "len(result.new_items)",
                 "result.item_count", "result.total_items"],
                1, "len(result.new_items) gives the count of items generated during execution.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What is the primary advantage of streaming responses?",
                ["Faster execution", "Lower memory usage",
                    "Real-time user feedback", "Better error handling"],
                2, "Streaming provides real-time feedback, allowing users to see responses as they're generated.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "Can you call to_input_list() on a RunResultStreaming before it completes?",
                ["Yes, always", "No, never",
                    "Only after first event", "Depends on the agent"],
                1, "to_input_list() should only be called after streaming completes.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What format does to_input_list() typically return?",
                ["List of strings", "List of dictionaries",
                    "List of Agent objects", "List of Message objects"],
                1, "to_input_list() typically returns a list of dictionaries compatible with OpenAI API format.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "Which property indicates the agent that produced the final response?",
                ["current_agent", "last_agent", "final_agent", "response_agent"],
                1, "last_agent indicates which agent produced the final response.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "How do you detect text content in streaming events?",
                ["Check event.text", "Check hasattr(event, 'text_delta')",
                 "Check event.content", "Check event.message"],
                1, "Check hasattr(event, 'text_delta') to detect text content in streaming events.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What should you do after streaming completes to get the final result?",
                ["Call get_result()", "Access final_output",
                 "Call finalize()", "Access result_text"],
                1, "Access final_output property after streaming completes to get the final result.",
                "RunResultStreaming Basics", "Beginner", 1
            ),
            QuizQuestion(
                "Can RunResult be used for multi-turn conversations?",
                ["No, single turn only", "Yes, using to_input_list()",
                 "Only with special configuration", "Depends on the agent"],
                1, "Yes, RunResult.to_input_list() enables multi-turn conversations by providing conversation history.",
                "RunResult Basics", "Beginner", 1
            ),
            QuizQuestion(
                "What happens to new_items when agents use tools?",
                ["Only final response included", "Tool calls and outputs included",
                    "Tools ignored", "Separate tool_items list"],
                1, "new_items includes tool calls, tool outputs, and all other items generated during execution.",
                "RunResult Basics", "Beginner", 1
            )
        ]

        # INTERMEDIATE LEVEL (25 questions, 2 points each)
        intermediate_questions = [
            QuizQuestion(
                "When using handoffs, which agent appears in RunResult.last_agent?",
                ["The original agent", "The agent that received the handoff",
                    "Both agents", "The coordinator agent"],
                1, "last_agent contains the agent that actually handled the final response after handoff.",
                "Advanced Usage", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the best practice for handling streaming events with unknown types?",
                ["Ignore them", "Use try-catch blocks",
                    "Check hasattr() for expected attributes", "Convert to string"],
                2, "Use hasattr() to safely check for expected attributes on streaming events.",
                "RunResultStreaming Advanced", "Intermediate", 2
            ),
            QuizQuestion(
                "How should you handle memory efficiency in long streaming sessions?",
                ["Store all events", "Process events immediately and discard",
                    "Batch events", "Use compression"],
                1, "Process streaming events immediately and discard to maintain memory efficiency.",
                "Performance & Optimization", "Intermediate", 2
            ),
            QuizQuestion(
                "What information is preserved in to_input_list() for tool usage?",
                ["Tool names only", "Tool calls and their outputs",
                    "Tool descriptions", "Tool configurations"],
                1, "to_input_list() preserves tool calls and their outputs for conversation continuity.",
                "Advanced Usage", "Intermediate", 2
            ),
            QuizQuestion(
                "Which pattern is recommended for error handling in streaming?",
                ["Catch all exceptions", "Handle specific event types",
                    "Use try-catch around stream_events()", "Ignore errors"],
                2, "Use try-catch around the entire stream_events() iteration for proper error handling.",
                "Error Handling", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you measure streaming performance effectively?",
                ["Total execution time only", "Time to first chunk and total time",
                    "Event count only", "Memory usage only"],
                1, "Measure both time to first chunk (user experience) and total execution time.",
                "Performance & Optimization", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the relationship between RunResult.input and to_input_list()?",
                ["They're identical", "input is original, to_input_list() includes conversation",
                 "No relationship", "to_input_list() is compressed input"],
                1, "input is the original request, to_input_list() includes full conversation history.",
                "Advanced Usage", "Intermediate", 2
            ),
            QuizQuestion(
                "When should you prefer streaming over regular execution?",
                ["Always", "For long responses", "For short responses", "Never"],
                1, "Prefer streaming for long responses where real-time feedback improves user experience.",
                "Performance & Optimization", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you handle partial results in streaming scenarios?",
                ["Wait for completion", "Process incrementally",
                    "Ignore partial data", "Buffer everything"],
                1, "Process streaming data incrementally to provide real-time user feedback.",
                "RunResultStreaming Advanced", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the correct way to combine multiple streaming sessions?",
                ["Merge final_outputs", "Chain to_input_list() results",
                 "Use separate agents", "Not possible"],
                1, "Chain to_input_list() results to maintain conversation context across sessions.",
                "Advanced Usage", "Intermediate", 2
            ),
            QuizQuestion(
                "How should you validate streaming event consistency?",
                ["Compare event count", "Reconstruct text and compare with final_output",
                    "Check timestamps", "Validate JSON"],
                1, "Reconstruct text from streaming events and compare with final_output for consistency.",
                "RunResultStreaming Advanced", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the impact of tool usage on streaming performance?",
                ["No impact", "Increases latency due to tool execution",
                    "Decreases latency", "Depends on tool type"],
                1, "Tool usage increases latency as tools must execute before streaming can continue.",
                "Performance & Optimization", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you handle streaming timeouts effectively?",
                ["Increase timeout", "Use asyncio.wait_for()", "Ignore timeouts",
                 "Retry automatically"],
                1, "Use asyncio.wait_for() to implement proper timeout handling for streaming operations.",
                "Error Handling", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the best practice for logging streaming events?",
                ["Log all events", "Log errors only",
                    "Log selectively based on event type", "No logging"],
                2, "Log selectively based on event type to balance debugging needs with performance.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you implement backpressure in streaming scenarios?",
                ["Ignore it", "Use asyncio queues",
                    "Buffer events", "Slow down generation"],
                1, "Use asyncio queues to implement proper backpressure handling in streaming.",
                "Performance & Optimization", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the correct approach for streaming event filtering?",
                ["Filter at source", "Filter during iteration",
                    "Filter after completion", "No filtering needed"],
                1, "Filter events during iteration to process only relevant events efficiently.",
                "RunResultStreaming Advanced", "Intermediate", 2
            ),
            QuizQuestion(
                "How should you handle streaming interruptions?",
                ["Restart from beginning", "Resume from last event",
                    "Use partial results", "Fail completely"],
                2, "Use partial results when streaming is interrupted to provide best user experience.",
                "Error Handling", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the recommended pattern for streaming event aggregation?",
                ["Store all events", "Aggregate incrementally",
                    "Aggregate at end", "No aggregation"],
                1, "Aggregate streaming events incrementally to maintain memory efficiency.",
                "Performance & Optimization", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you ensure thread safety in streaming scenarios?",
                ["Use locks", "Use asyncio primitives",
                    "Single-threaded only", "No safety needed"],
                1, "Use asyncio primitives for proper concurrency control in streaming scenarios.",
                "Production Patterns", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the impact of handoffs on streaming continuity?",
                ["Breaks streaming", "Seamless continuation",
                    "Requires restart", "Depends on agents"],
                1, "Handoffs provide seamless streaming continuation with the new agent.",
                "Advanced Usage", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you optimize memory usage for large streaming responses?",
                ["Increase memory", "Process and discard events",
                    "Compress events", "Use disk storage"],
                1, "Process and discard streaming events immediately to optimize memory usage.",
                "Performance & Optimization", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the correct way to handle streaming event ordering?",
                ["Events are always ordered", "Manual ordering required",
                    "Use timestamps", "Order doesn't matter"],
                0, "Streaming events are guaranteed to be delivered in order by the SDK.",
                "RunResultStreaming Advanced", "Intermediate", 2
            ),
            QuizQuestion(
                "How should you implement streaming event caching?",
                ["Cache all events", "Cache selectively",
                    "No caching", "Cache final result only"],
                1, "Cache streaming events selectively based on application requirements.",
                "Performance & Optimization", "Intermediate", 2
            ),
            QuizQuestion(
                "What's the best practice for streaming error recovery?",
                ["Retry immediately", "Exponential backoff",
                    "Fail fast", "Ignore errors"],
                1, "Use exponential backoff for streaming error recovery to avoid overwhelming the system.",
                "Error Handling", "Intermediate", 2
            ),
            QuizQuestion(
                "How do you implement streaming event validation?",
                ["Validate all events", "Validate critical events only",
                    "No validation", "Validate at end"],
                1, "Validate critical streaming events only to balance safety with performance.",
                "Production Patterns", "Intermediate", 2
            )
        ]

        # ADVANCED LEVEL (25 questions, 3 points each)
        advanced_questions = [
            QuizQuestion(
                "How do you implement custom streaming event processors for complex workflows?",
                ["Subclass StreamEvent", "Create event handler classes",
                    "Use decorators", "Modify SDK source"],
                1, "Create dedicated event handler classes for complex streaming workflow processing.",
                "RunResultStreaming Advanced", "Advanced", 3
            ),
            QuizQuestion(
                "What's the optimal strategy for handling streaming in distributed systems?",
                ["Single node processing", "Event streaming with message queues",
                    "Shared memory", "Database coordination"],
                1, "Use event streaming with message queues for distributed streaming processing.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result persistence for audit trails?",
                ["Store final result only", "Stream events to persistent storage",
                    "Periodic snapshots", "No persistence"],
                1, "Stream events directly to persistent storage for complete audit trails.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the correct approach for streaming result versioning?",
                ["Version final results", "Version event streams",
                    "Version agents", "No versioning"],
                1, "Version event streams to maintain complete execution history and enable replay.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result compression for large responses?",
                ["Compress final output", "Compress event stream",
                    "Compress individual events", "No compression"],
                1, "Compress the entire event stream for optimal compression ratio and performance.",
                "Performance & Optimization", "Advanced", 3
            ),
            QuizQuestion(
                "What's the best practice for streaming result monitoring in production?",
                ["Monitor final results", "Monitor streaming metrics",
                    "Monitor agent performance", "All of the above"],
                3, "Monitor all aspects: final results, streaming metrics, and agent performance.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result replay for debugging?",
                ["Store final results", "Store event streams with metadata",
                    "Store agent states", "Use logging"],
                1, "Store complete event streams with metadata to enable accurate replay for debugging.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the optimal pattern for streaming result aggregation across multiple agents?",
                ["Merge final outputs", "Aggregate event streams",
                    "Use coordinator agent", "Sequential processing"],
                1, "Aggregate event streams from multiple agents for comprehensive result processing.",
                "Advanced Usage", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result security for sensitive data?",
                ["Encrypt final results", "Encrypt event streams",
                    "Use secure channels", "All of the above"],
                3, "Implement comprehensive security: encrypt streams, use secure channels, protect results.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the correct approach for streaming result load balancing?",
                ["Round-robin agents", "Event-based distribution",
                    "Content-aware routing", "Random distribution"],
                2, "Use content-aware routing to distribute streaming workload based on request characteristics.",
                "Performance & Optimization", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result circuit breakers?",
                ["Monitor final results", "Monitor streaming health",
                    "Monitor agent availability", "All metrics"],
                3, "Monitor all metrics: results, streaming health, and agent availability for circuit breakers.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the best practice for streaming result rate limiting?",
                ["Limit requests", "Limit events",
                    "Limit bandwidth", "Adaptive limiting"],
                3, "Use adaptive rate limiting based on system capacity and streaming performance.",
                "Performance & Optimization", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result failover mechanisms?",
                ["Agent failover", "Stream failover",
                    "Result failover", "Multi-level failover"],
                3, "Implement multi-level failover: agent, stream, and result level redundancy.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the optimal strategy for streaming result caching in CDNs?",
                ["Cache final results", "Cache event patterns",
                    "Cache agent responses", "Dynamic caching"],
                3, "Use dynamic caching strategies based on content type and access patterns.",
                "Performance & Optimization", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result analytics for business intelligence?",
                ["Analyze final outputs", "Analyze event patterns",
                    "Analyze agent behavior", "Comprehensive analytics"],
                3, "Implement comprehensive analytics covering outputs, events, and agent behavior.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the correct approach for streaming result schema evolution?",
                ["Version schemas", "Backward compatibility",
                    "Migration strategies", "All approaches"],
                3, "Use all approaches: schema versioning, backward compatibility, and migration strategies.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result compliance for regulations?",
                ["Data retention", "Audit logging",
                    "Access controls", "Comprehensive compliance"],
                3, "Implement comprehensive compliance: retention, logging, access controls, and monitoring.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the best practice for streaming result testing in CI/CD?",
                ["Test final results", "Test streaming behavior",
                    "Test performance", "Comprehensive testing"],
                3, "Implement comprehensive testing: results, streaming behavior, and performance.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result observability?",
                ["Metrics only", "Logs only", "Traces only",
                    "Full observability stack"],
                3, "Implement full observability: metrics, logs, traces, and distributed tracing.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the optimal pattern for streaming result data lineage?",
                ["Track final results", "Track event lineage",
                    "Track agent lineage", "End-to-end lineage"],
                3, "Implement end-to-end data lineage tracking from input through events to final results.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result disaster recovery?",
                ["Backup results", "Backup streams",
                    "Backup agents", "Comprehensive DR"],
                3, "Implement comprehensive disaster recovery for results, streams, and agent infrastructure.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the correct approach for streaming result capacity planning?",
                ["Plan for peak", "Plan for average",
                    "Dynamic scaling", "Predictive scaling"],
                3, "Use predictive scaling based on historical patterns and real-time metrics.",
                "Performance & Optimization", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result multi-tenancy?",
                ["Separate agents", "Separate streams",
                    "Separate infrastructure", "Logical separation"],
                3, "Use logical separation with proper isolation at all levels for multi-tenancy.",
                "Production Patterns", "Advanced", 3
            ),
            QuizQuestion(
                "What's the best practice for streaming result cost optimization?",
                ["Optimize compute", "Optimize storage",
                    "Optimize network", "Holistic optimization"],
                3, "Use holistic optimization across compute, storage, and network resources.",
                "Performance & Optimization", "Advanced", 3
            ),
            QuizQuestion(
                "How do you implement streaming result governance frameworks?",
                ["Technical governance", "Business governance",
                    "Data governance", "Comprehensive governance"],
                3, "Implement comprehensive governance covering technical, business, and data aspects.",
                "Production Patterns", "Advanced", 3
            )
        ]

        # EXPERT LEVEL (10 questions, 4 points each)
        expert_questions = [
            QuizQuestion(
                "Design a streaming result architecture for 1M+ concurrent users with sub-100ms latency.",
                ["Single region deployment", "Multi-region with edge caching",
                    "Microservices architecture", "Event-driven distributed system"],
                3, "Event-driven distributed system with edge processing and intelligent routing.",
                "Production Patterns", "Expert", 4
            ),
            QuizQuestion(
                "Implement streaming result consistency in eventually consistent distributed systems.",
                ["Strong consistency", "Eventual consistency",
                    "Vector clocks", "Consensus algorithms"],
                2, "Use vector clocks to track causality and maintain consistency in distributed streaming.",
                "Production Patterns", "Expert", 4
            ),
            QuizQuestion(
                "Optimize streaming result performance for GPU-accelerated inference workloads.",
                ["CPU optimization", "Memory optimization",
                    "GPU pipeline optimization", "Hybrid optimization"],
                2, "Optimize GPU pipelines with batching, memory management, and async processing.",
                "Performance & Optimization", "Expert", 4
            ),
            QuizQuestion(
                "Design streaming result security for zero-trust environments.",
                ["Perimeter security", "Identity-based security",
                    "Zero-trust architecture", "Encryption only"],
                2, "Implement zero-trust architecture with identity verification at every layer.",
                "Production Patterns", "Expert", 4
            ),
            QuizQuestion(
                "Implement streaming result ML model versioning and A/B testing.",
                ["Simple versioning", "Canary deployments",
                    "Feature flags", "Comprehensive ML ops"],
                3, "Use comprehensive ML ops with versioning, canary deployments, and feature flags.",
                "Production Patterns", "Expert", 4
            ),
            QuizQuestion(
                "Design streaming result data mesh architecture for enterprise scale.",
                ["Centralized data", "Federated data",
                    "Data mesh principles", "Hybrid approach"],
                2, "Apply data mesh principles with domain ownership and federated governance.",
                "Production Patterns", "Expert", 4
            ),
            QuizQuestion(
                "Optimize streaming result carbon footprint for sustainable AI.",
                ["Efficient algorithms", "Green infrastructure",
                    "Carbon-aware scheduling", "Holistic sustainability"],
                3, "Implement holistic sustainability: efficient algorithms, green infrastructure, carbon-aware scheduling.",
                "Performance & Optimization", "Expert", 4
            ),
            QuizQuestion(
                "Implement streaming result quantum-safe cryptography for future security.",
                ["Current encryption", "Post-quantum algorithms",
                    "Hybrid approach", "Quantum key distribution"],
                2, "Use post-quantum cryptographic algorithms for future-proof security.",
                "Production Patterns", "Expert", 4
            ),
            QuizQuestion(
                "Design streaming result edge computing architecture for IoT integration.",
                ["Cloud-only", "Edge-only", "Hybrid edge-cloud", "Federated edge"],
                3, "Use federated edge architecture with intelligent workload distribution.",
                "Production Patterns", "Expert", 4
            ),
            QuizQuestion(
                "Implement streaming result autonomous healing for self-managing systems.",
                ["Manual intervention", "Automated recovery",
                    "Predictive healing", "Autonomous systems"],
                3, "Develop autonomous systems with predictive healing and self-optimization.",
                "Production Patterns", "Expert", 4
            )
        ]

        # Combine all questions
        questions.extend(beginner_questions)
        questions.extend(intermediate_questions)
        questions.extend(advanced_questions)
        questions.extend(expert_questions)

        return questions

    def run_quiz(self, mode: str = "full") -> None:
        """Run the quiz in different modes."""
        print("🧠 OpenAI Agents SDK - RunResult & Streaming Expert Quiz")
        print("=" * 60)

        if mode == "full":
            selected_questions = self.questions
        elif mode == "quick":
            selected_questions = random.sample(self.questions, 20)
        elif mode == "beginner":
            selected_questions = [
                q for q in self.questions if q.difficulty == "Beginner"]
        elif mode == "intermediate":
            selected_questions = [
                q for q in self.questions if q.difficulty == "Intermediate"]
        elif mode == "advanced":
            selected_questions = [
                q for q in self.questions if q.difficulty == "Advanced"]
        elif mode == "expert":
            selected_questions = [
                q for q in self.questions if q.difficulty == "Expert"]
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
        print("🎯 QUIZ RESULTS")
        print("=" * 60)

        print(
            f"📊 Overall Score: {self.score}/{self.total_points} ({percentage:.1f}%)")
        print(f"⏱️  Time Taken: {elapsed_time:.1f} seconds")

        # Mastery level
        if percentage >= 95:
            level = "🏆 EXPERT LEVEL"
            message = "Outstanding! You have mastery-level understanding of RunResult and streaming."
        elif percentage >= 85:
            level = "🥇 ADVANCED"
            message = "Excellent! You have strong understanding with minor gaps."
        elif percentage >= 75:
            level = "🥈 INTERMEDIATE"
            message = "Good! You understand the basics but need to study advanced concepts."
        elif percentage >= 60:
            level = "🥉 BEGINNER+"
            message = "Fair understanding. Focus on fundamentals and practice more."
        else:
            level = "📚 NEEDS STUDY"
            message = "Significant gaps identified. Recommend thorough review of materials."

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
            print("Focus on these areas:")
            for category in weak_categories:
                if "Basics" in category:
                    print(
                        f"  • {category}: Review fundamental concepts and basic usage patterns")
                elif "Advanced" in category:
                    print(
                        f"  • {category}: Study complex scenarios and optimization techniques")
                elif "Production" in category:
                    print(
                        f"  • {category}: Learn enterprise patterns and best practices")
                elif "Performance" in category:
                    print(
                        f"  • {category}: Focus on optimization and monitoring strategies")
                else:
                    print(
                        f"  • {category}: Review core concepts and practical applications")
        else:
            print("  🎉 Excellent performance across all categories!")

        print(f"\n🔗 Additional Resources:")
        print("  • OpenAI Agents SDK Documentation: https://openai.github.io/openai-agents-python/")
        print(
            "  • Results Reference: https://openai.github.io/openai-agents-python/results/")
        print(
            "  • Streaming Guide: https://openai.github.io/openai-agents-python/streaming/")


def main():
    """Main function to run the quiz."""
    quiz = ResultsExpertQuiz()

    print("Select quiz mode:")
    print("1. Full Quiz (80 questions)")
    print("2. Quick Assessment (20 questions)")
    print("3. Beginner Level Only")
    print("4. Intermediate Level Only")
    print("5. Advanced Level Only")
    print("6. Expert Level Only")

    while True:
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            modes = {
                "1": "full",
                "2": "quick",
                "3": "beginner",
                "4": "intermediate",
                "5": "advanced",
                "6": "expert"
            }

            if choice in modes:
                quiz.run_quiz(modes[choice])
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
        except KeyboardInterrupt:
            print("\n\n👋 Quiz cancelled. Good luck with your studies!")
            break


if __name__ == "__main__":
    main()
