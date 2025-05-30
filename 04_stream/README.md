# 04_stream - OpenAI Agents SDK Streaming Mastery

This directory provides comprehensive coverage of streaming responses with the OpenAI Agents SDK, focusing on real-time user feedback and production-ready streaming patterns.

## 📁 Directory Contents

### Core Files

#### 01_basic_streaming.py

**Introduction to Streaming Concepts**

-   Basic `Runner.run_streamed()` usage
-   Understanding `stream_events()` iteration
-   Comparing regular vs streaming execution
-   Core streaming workflow patterns

**Key Concepts:**

-   RunResultStreaming object
-   Event-driven response processing
-   Real-time vs batch execution

#### 02_raw_response_events.py

**Token-by-Token Streaming**

-   Raw response event processing
-   `ResponseTextDeltaEvent` handling
-   Token-level text streaming
-   Performance timing analysis

**Key Concepts:**

-   `event.type == "raw_response_event"`
-   `isinstance(event.data, ResponseTextDeltaEvent)`
-   `event.data.delta` for text tokens
-   Real-time text reconstruction

#### 03_run_item_events.py

**Higher-Level Event Processing**

-   `run_item_stream_event` handling
-   `agent_updated_stream_event` for handoffs
-   Tool call and output tracking
-   Message output processing

**Key Concepts:**

-   Structured event types
-   `tool_call_item` and `tool_call_output_item`
-   `message_output_item` processing
-   `ItemHelpers.text_message_output()`

#### 04_streaming_with_handoffs.py

**Agent Transitions in Streaming**

-   Seamless handoff streaming
-   Agent transition tracking
-   Multi-agent workflow streaming
-   Complex handoff pattern analysis

**Key Concepts:**

-   `event.new_agent` access
-   Handoff transparency in streaming
-   Agent workflow coordination
-   Real-time agent switching

#### 05_streaming_patterns.py

**Production Streaming Patterns**

-   UI-friendly streaming implementation
-   Buffered streaming for smooth output
-   Error handling and fallback strategies
-   Performance monitoring and metrics
-   Multi-stream coordination
-   Stream cancellation patterns

**Key Concepts:**

-   Production-ready patterns
-   User experience optimization
-   Error resilience
-   Performance measurement

#### 06_streaming_quiz.py

**Comprehensive Assessment**

-   50 expert-level questions across 3 difficulty levels
-   5 categories covering all streaming aspects
-   Performance tracking and analysis
-   Personalized study recommendations

**Categories:**

-   Basic Streaming Concepts
-   Raw Response Events
-   Run Item Events & Agent Events
-   Streaming with Tools & Handoffs
-   Production Patterns & Best Practices

## 🎯 Learning Objectives

### Beginner Level

-   [ ] Understand the difference between regular and streaming execution
-   [ ] Use `Runner.run_streamed()` and `stream_events()`
-   [ ] Process raw response events for token-by-token streaming
-   [ ] Handle basic event types and their properties
-   [ ] Know when to use streaming vs regular execution

### Intermediate Level

-   [ ] Implement production-ready streaming patterns
-   [ ] Handle errors and implement fallback strategies
-   [ ] Optimize streaming performance and measure metrics
-   [ ] Process complex event types and tool interactions
-   [ ] Coordinate multiple concurrent streams

### Advanced Level

-   [ ] Design enterprise-scale streaming architectures
-   [ ] Implement custom streaming event processors
-   [ ] Optimize for high-concurrency scenarios
-   [ ] Build resilient streaming systems with circuit breakers
-   [ ] Implement comprehensive observability

## 🔧 Core Streaming Concepts

### Basic Streaming Flow

```python
# Start streaming
result = Runner.run_streamed(agent, user_input)

# Process events
async for event in result.stream_events():
    if event.type == "raw_response_event":
        # Handle token-level events
        if isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    elif event.type == "run_item_stream_event":
        # Handle higher-level events
        if event.item.type == "tool_call_item":
            print("Tool called...")

    elif event.type == "agent_updated_stream_event":
        # Handle agent transitions
        print(f"Agent changed to: {event.new_agent.name}")

# Access final result
final_output = result.final_output
```

### Event Type Hierarchy

```
StreamEvent
├── raw_response_event
│   └── ResponseTextDeltaEvent (text tokens)
├── run_item_stream_event
│   ├── tool_call_item (tool invocation)
│   ├── tool_call_output_item (tool results)
│   └── message_output_item (final messages)
└── agent_updated_stream_event (handoffs)
```

### Production Patterns

#### UI-Friendly Streaming

```python
class StreamingUI:
    def __init__(self):
        self.current_text = ""
        self.status = "idle"

    def process_event(self, event):
        if event.type == "raw_response_event":
            self.add_text_chunk(event.data.delta)
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                self.show_progress("Processing...")
```

#### Error Handling

```python
try:
    result = Runner.run_streamed(agent, input)
    async for event in result.stream_events():
        # Process events
        pass
except Exception as e:
    # Fallback to regular execution
    fallback_result = await Runner.run(agent, input)
```

#### Performance Monitoring

```python
start_time = time.time()
first_chunk_time = None
chunk_count = 0

async for event in result.stream_events():
    if event.type == "raw_response_event":
        if first_chunk_time is None:
            first_chunk_time = time.time() - start_time
        chunk_count += 1

# Analyze metrics
total_time = time.time() - start_time
print(f"Time to first chunk: {first_chunk_time:.3f}s")
print(f"Total time: {total_time:.3f}s")
```

## 📊 When to Use Streaming

### ✅ Use Streaming For:

-   Long responses (>2 seconds generation time)
-   Interactive applications requiring real-time feedback
-   Progressive data processing scenarios
-   User experience optimization
-   Complex multi-step workflows

### ❌ Avoid Streaming For:

-   Short, quick responses (<1 second)
-   Batch processing scenarios
-   Simple request-response patterns
-   Resource-constrained environments

## 🏗️ Production Considerations

### Performance Optimization

-   **Time to First Chunk**: Critical for user experience
-   **Memory Management**: Process events immediately, don't store all
-   **Concurrency**: Use `asyncio.gather()` for multiple streams
-   **Buffering**: Implement word-level buffering for smooth output

### Error Resilience

-   **Timeout Handling**: Use `asyncio.wait_for()`
-   **Fallback Strategy**: Regular execution as backup
-   **Circuit Breakers**: Monitor streaming health
-   **Graceful Degradation**: Partial results on interruption

### Monitoring and Observability

-   **Metrics**: Track latency, throughput, error rates
-   **Logging**: Selective event logging for debugging
-   **Tracing**: Distributed tracing for complex workflows
-   **Alerting**: Real-time monitoring of streaming health

## 🧪 Testing Strategies

### Unit Testing

```python
async def test_streaming_events():
    result = Runner.run_streamed(agent, "test input")
    events = []

    async for event in result.stream_events():
        events.append(event.type)

    assert "raw_response_event" in events
    assert result.is_complete
```

### Integration Testing

```python
async def test_streaming_consistency():
    result = Runner.run_streamed(agent, input)
    collected_text = ""

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            collected_text += event.data.delta

    assert collected_text == result.final_output
```

### Performance Testing

```python
async def test_streaming_performance():
    start_time = time.time()
    result = Runner.run_streamed(agent, input)

    first_chunk_time = None
    async for event in result.stream_events():
        if event.type == "raw_response_event" and first_chunk_time is None:
            first_chunk_time = time.time() - start_time
            break

    assert first_chunk_time < 1.0  # First chunk within 1 second
```

## 📚 Study Path

### Phase 1: Fundamentals (Files 01-02)

1. Run `01_basic_streaming.py` and understand basic concepts
2. Study `02_raw_response_events.py` for token-level processing
3. Practice with different agent configurations
4. Take beginner-level quiz questions

### Phase 2: Advanced Processing (Files 03-04)

1. Explore `03_run_item_events.py` for structured events
2. Study `04_streaming_with_handoffs.py` for agent transitions
3. Implement your own event processing patterns
4. Take intermediate-level quiz questions

### Phase 3: Production Patterns (File 05)

1. Master `05_streaming_patterns.py` for real-world scenarios
2. Implement production-ready streaming systems
3. Practice error handling and performance optimization
4. Take advanced-level quiz questions

### Phase 4: Mastery Assessment

1. Complete the full expert quiz (`06_streaming_quiz.py`)
2. Achieve 85%+ score across all categories
3. Implement custom streaming solutions
4. Design enterprise-scale streaming architectures

## 🔗 Related Documentation

-   [OpenAI Agents SDK Streaming Guide](https://openai.github.io/openai-agents-python/streaming/)
-   [Runner Documentation](https://openai.github.io/openai-agents-python/running_agents/)
-   [Results Documentation](https://openai.github.io/openai-agents-python/results/)
-   [Performance Best Practices](https://openai.github.io/openai-agents-python/performance/)

## 🎓 Certification Readiness

After completing this directory, you should be able to:

-   ✅ Explain the difference between streaming and regular execution
-   ✅ Implement token-by-token streaming with raw events
-   ✅ Process structured events for UI updates
-   ✅ Handle agent handoffs in streaming scenarios
-   ✅ Design production-ready streaming systems
-   ✅ Optimize streaming performance and handle errors
-   ✅ Monitor and observe streaming applications

**Quiz Target**: 90%+ overall score with 85%+ in each category for expert-level certification readiness.

## 🚀 Next Steps

After mastering streaming concepts:

1. Explore advanced Runner patterns in `02_runner`
2. Study result handling in `03_results`
3. Learn tool integration patterns
4. Practice with complex multi-agent workflows
5. Build production streaming applications
