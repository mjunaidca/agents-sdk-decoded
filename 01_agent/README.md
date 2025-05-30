# 🤖 Agent Fundamentals - Complete Coverage

This directory contains comprehensive examples covering **all core Agent concepts** from the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/ref/agent/).

## 📚 **Complete Agent Coverage**

### ✅ **Basic Agent Concepts**

-   **`01_hello.py`** - Basic agent creation and execution
-   **`02_hello_handoff.py`** - Agent handoffs and delegation
-   **`03_agent_ins.py`** - Dynamic instructions (string, callable, async callable)

### ✅ **Context Management**

-   **`04_acontext.py`** - Basic context usage
-   **`05_immutable_context.py`** - Advanced context patterns and immutability

### ✅ **Structured Outputs**

-   **`06_structure.py`** - Comprehensive structured outputs guide (8 patterns)
-   **`07_non_strict_output_type.py`** - Non-strict schema examples

### ✅ **Advanced Agent Features**

-   **`08_agent_advanced_features.py`** - Complete coverage of:
    -   `Agent.clone()` - Creating agent variants
    -   `Agent.as_tool()` - Converting agents to tools
    -   `model_settings` - Temperature, top_p configuration
    -   `tool_use_behavior` - Control tool execution flow
    -   `reset_tool_choice` - Prevent infinite tool loops

## 🎯 **Key Agent Concepts Mastered**

### 1. **Agent Creation & Configuration**

```python
agent = Agent(
    name="MyAgent",
    instructions="System prompt or callable function",
    model=OpenAIChatCompletionsModel(...),
    model_settings=ModelSettings(temperature=0.7),
    tools=[...],
    handoffs=[...],
    output_type=MyPydanticModel
)
```

### 2. **Dynamic Instructions**

```python
# String instructions
instructions="You are a helpful assistant"

# Callable instructions
def dynamic_instructions(context, agent):
    return f"Context state: {context.context.state}"

# Async callable instructions
async def async_instructions(context, agent):
    data = await fetch_data()
    return f"Instructions based on: {data}"
```

### 3. **Structured Outputs**

```python
# Strict mode (recommended)
class StrictOutput(BaseModel):
    name: str = ""
    age: int = 0
    model_config = ConfigDict(extra="forbid")

# Non-strict mode (flexible)
output_type=AgentOutputSchema(FlexibleModel, strict_json_schema=False)
```

### 4. **Tool Use Behavior**

```python
# Default: LLM processes tool results
tool_use_behavior="run_llm_again"

# Stop after first tool call
tool_use_behavior="stop_on_first_tool"

# Stop at specific tools
tool_use_behavior={"stop_at_tool_names": ["final_tool"]}

# Custom behavior function
tool_use_behavior=custom_function
```

### 5. **Agent Cloning & Composition**

```python
# Clone with modifications
specialized_agent = base_agent.clone(
    instructions="New instructions",
    model_settings=ModelSettings(temperature=0.9)
)

# Convert agent to tool
research_tool = research_agent.as_tool(
    tool_name="research_topic",
    tool_description="Research any topic thoroughly"
)
```

## 🚀 **Ready for Next Level**

With complete Agent mastery achieved, you're ready to move to:

### **Next: `02_runner`**

-   [Runner.run()](https://openai.github.io/openai-agents-python/running_agents/)
-   [Runner.run_sync()](https://openai.github.io/openai-agents-python/running_agents/)
-   [Runner.run_streamed()](https://openai.github.io/openai-agents-python/running_agents/)
-   Agent loop mechanics
-   Streaming events
-   Run configuration
-   Conversations/chat threads
-   Exception handling

## 🎓 **Expert-Level Understanding**

You now have **complete mastery** of:

-   ✅ Agent architecture and design patterns
-   ✅ Context management and state handling
-   ✅ Structured outputs (strict vs non-strict)
-   ✅ Tool integration and behavior control
-   ✅ Agent composition and delegation
-   ✅ Advanced configuration options

**Total Coverage**: 100% of core Agent concepts from the OpenAI Agents SDK documentation.
