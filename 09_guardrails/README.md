# 09_guardrails - OpenAI Agents SDK Guardrails

This directory contains comprehensive examples of guardrails in the OpenAI Agents SDK. Guardrails are powerful mechanisms that run in parallel to your agents to provide safety, validation, and quality control.

## 📖 Core Concepts

### What are Guardrails?

Guardrails are checks that run **in parallel** to your agents to:

-   ✅ Validate user input before it reaches the agent
-   ✅ Check agent output before it's returned to users
-   ✅ Implement safety and policy enforcement
-   ✅ Provide quality control and monitoring

### Types of Guardrails

1. **Input Guardrails** - Check user input before agent processing
2. **Output Guardrails** - Check agent responses before returning to users

### Key Components

-   **`@input_guardrail`** - Decorator for input validation functions
-   **`@output_guardrail`** - Decorator for output validation functions
-   **`GuardrailFunctionOutput`** - Result object with `output_info` and `tripwire_triggered`
-   **Tripwires** - When `tripwire_triggered=True`, execution is halted
-   **Exceptions** - `InputGuardrailTripwireTriggered` and `OutputGuardrailTripwireTriggered`

## 📁 File Structure

```
09_guardrails/
├── 01_basic_input_guardrail.py      # Basic input validation examples
├── 02_basic_output_guardrail.py     # Basic output validation examples
├── 03_guardrail_exceptions.py       # Exception handling when guardrails trigger
├── 04_agent_based_guardrails.py     # Advanced agent-based guardrails
├── 05_guardrails_quiz.py            # Interactive quiz to test your understanding
└── README.md                        # This comprehensive guide
```

## 🚀 Examples Breakdown

### 1. Basic Input Guardrails (`01_basic_input_guardrail.py`)

**Purpose**: Demonstrates simple input validation guardrails

**Key Features**:

-   Content filtering (banned words)
-   Message length validation
-   Named guardrails using decorator parameters
-   Both sync and async guardrail functions

**Example Guardrail**:

```python
@input_guardrail
def content_filter_guardrail(context: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    # Extract and check user message
    user_message = input if isinstance(input, str) else str(input[-1]) if input else ""

    banned_words = ["spam", "hack", "virus"]
    found_banned = [word for word in banned_words if word.lower() in user_message.lower()]

    if found_banned:
        return GuardrailFunctionOutput(
            output_info={"banned_words_found": found_banned},
            tripwire_triggered=True  # Halt execution
        )

    return GuardrailFunctionOutput(
        output_info={"status": "clean"},
        tripwire_triggered=False  # Allow execution
    )
```

### 2. Basic Output Guardrails (`02_basic_output_guardrail.py`)

**Purpose**: Demonstrates output validation and filtering

**Key Features**:

-   Response safety checking
-   Response length validation
-   Async guardrail implementation
-   Politeness checking

**Example Guardrail**:

```python
@output_guardrail
def response_safety_guardrail(context: RunContextWrapper, agent: Agent, agent_output) -> GuardrailFunctionOutput:
    response_text = str(agent_output) if agent_output else ""

    unsafe_patterns = ["password", "secret", "confidential"]
    found_unsafe = [pattern for pattern in unsafe_patterns if pattern.lower() in response_text.lower()]

    if found_unsafe:
        return GuardrailFunctionOutput(
            output_info={"unsafe_patterns_found": found_unsafe},
            tripwire_triggered=True  # Block response
        )

    return GuardrailFunctionOutput(
        output_info={"status": "safe"},
        tripwire_triggered=False  # Allow response
    )
```

### 3. Exception Handling (`03_guardrail_exceptions.py`)

**Purpose**: Shows proper exception handling when guardrails trigger

**Key Features**:

-   `InputGuardrailTripwireTriggered` exception handling
-   `OutputGuardrailTripwireTriggered` exception handling
-   Comprehensive error handling patterns
-   User-friendly error messages

**Example Exception Handling**:

```python
try:
    result = await Runner.run(agent, user_input)
    print(f"Success: {result.final_output}")

except InputGuardrailTripwireTriggered as e:
    print(f"Input blocked: {e.guardrail_result.output.output_info}")

except OutputGuardrailTripwireTriggered as e:
    print(f"Output blocked: {e.guardrail_result.output.output_info}")
```

### 4. Agent-Based Guardrails (`04_agent_based_guardrails.py`)

**Purpose**: Advanced guardrails using dedicated agents for validation

**Key Features**:

-   Math homework detection using a guardrail agent
-   Content moderation with structured outputs
-   Response quality checking
-   Performance comparison with simple guardrails

**Example Agent-Based Guardrail**:

```python
# Guardrail agent with structured output
math_homework_agent = Agent(
    name="MathHomeworkDetector",
    instructions="Detect if users are asking for math homework help...",
    output_type=MathHomeworkOutput,  # Pydantic model
)

@input_guardrail(name="math_homework_detector")
async def math_homework_guardrail(context, agent, input) -> GuardrailFunctionOutput:
    # Run the guardrail agent
    result = await Runner.run(math_homework_agent, input, context=context.context)
    detection = result.final_output_as(MathHomeworkOutput)

    # Trigger based on confidence score
    should_trigger = detection.is_math_homework and detection.confidence_score > 0.7

    return GuardrailFunctionOutput(
        output_info={"detection_result": detection.model_dump()},
        tripwire_triggered=should_trigger
    )
```

## ⚙️ Function Signatures

### Input Guardrail Function

```python
def input_guardrail_function(
    context: RunContextWrapper,           # Runtime context
    agent: Agent,                        # The agent being guarded
    input: str | list[TResponseInputItem] # User input
) -> GuardrailFunctionOutput:            # Return with tripwire status
```

### Output Guardrail Function

```python
def output_guardrail_function(
    context: RunContextWrapper,  # Runtime context
    agent: Agent,               # The agent that generated output
    agent_output: Any           # The agent's output
) -> GuardrailFunctionOutput:   # Return with tripwire status
```

## 🎯 Best Practices

### 1. Guardrail Design

-   **Keep guardrails focused** - Each guardrail should check one specific thing
-   **Use appropriate thresholds** - Don't make guardrails too sensitive
-   **Provide informative output_info** - Help with debugging and monitoring
-   **Consider performance** - Agent-based guardrails add latency

### 2. Exception Handling

-   **Always handle guardrail exceptions** - Users need friendly error messages
-   **Log guardrail triggers** - Important for monitoring and debugging
-   **Consider fallback strategies** - What happens when guardrails trigger?

### 3. Testing

-   **Test positive and negative cases** - Ensure guardrails work correctly
-   **Test edge cases** - Empty inputs, very long inputs, etc.
-   **Monitor guardrail performance** - Track trigger rates and false positives

### 4. Async vs Sync

-   **Use async for I/O operations** - External API calls, database queries
-   **Use sync for simple checks** - String validation, length checks
-   **Mix both as needed** - Guardrails can be sync or async independently

## 🔧 Running the Examples

Each example is self-contained and can be run independently:

```bash
# Basic input guardrails
python decoded/09_guardrails/01_basic_input_guardrail.py

# Basic output guardrails
python decoded/09_guardrails/02_basic_output_guardrail.py

# Exception handling
python decoded/09_guardrails/03_guardrail_exceptions.py

# Agent-based guardrails (requires OpenAI API key)
python decoded/09_guardrails/04_agent_based_guardrails.py

# Test your understanding with the interactive quiz
python decoded/09_guardrails/05_guardrails_quiz.py
```

## 🚨 Important Notes

### Input Guardrails

-   Only run for the **first agent** in a handoff chain
-   Receive the same input passed to the agent
-   Trigger `InputGuardrailTripwireTriggered` exception when tripwire is triggered

### Output Guardrails

-   Only run for the **last agent** in a handoff chain
-   Receive the final agent output
-   Trigger `OutputGuardrailTripwireTriggered` exception when tripwire is triggered

### Performance Considerations

-   **Simple guardrails** - Milliseconds overhead
-   **Agent-based guardrails** - Seconds overhead (additional LLM calls)
-   **Multiple guardrails** - Run in parallel, but total time is sum of slowest
-   **Cost implications** - Agent-based guardrails use additional API calls

## 🎓 Key Takeaways

1. **Guardrails provide essential safety** - Use them for production applications
2. **Input and output guardrails serve different purposes** - Plan accordingly
3. **Exception handling is crucial** - Always handle guardrail triggers gracefully
4. **Agent-based guardrails are powerful** - But consider performance implications
5. **Test thoroughly** - Guardrails are part of your application's reliability

## 🔗 Related SDK Documentation

-   [Guardrails API Reference](https://openai.github.io/openai-agents-python/ref/guardrail/)
-   [Guardrails Guide](https://openai.github.io/openai-agents-python/guardrails/)
-   [Exception Handling](https://openai.github.io/openai-agents-python/ref/exceptions/)

## 📈 Next Steps

After understanding guardrails, consider exploring:

-   **Context Management** - How to maintain state across guardrails
-   **Orchestrating Multiple Agents** - Guardrails in multi-agent workflows
-   **Tracing** - Monitoring and debugging guardrail execution
-   **Voice Agents** - Guardrails for speech-based interactions
