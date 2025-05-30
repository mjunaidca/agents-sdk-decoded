# Tools Examples - OpenAI Agents SDK

This directory contains comprehensive examples demonstrating the three main types of tools in the OpenAI Agents SDK, based on the official documentation at [https://openai.github.io/openai-agents-python/tools/](https://openai.github.io/openai-agents-python/tools/).

## Overview

Tools let agents take actions: things like fetching data, running code, calling external APIs, and even using a computer. The Agent SDK supports three classes of tools:

1. **Hosted Tools** - Run on LLM servers alongside AI models (e.g., WebSearchTool, CodeInterpreterTool)
2. **Function Tools** - Use any Python function as a tool with automatic schema generation
3. **Agents as Tools** - Use agents as tools for orchestration without handoffs

## Examples

### Basic Examples

#### 1. Basic Function Tools (`01_basic_function_tools.py`)

-   `@function_tool` decorator usage
-   TypedDict for parameters
-   Automatic schema generation from docstrings
-   Simple function-to-tool conversion

#### 2. Hosted Tools (`02_hosted_tools.py`)

-   WebSearchTool configuration
-   Error handling for hosted tools
-   Basic hosted tool integration

#### 3. Custom Function Tools (`03_custom_function_tools.py`)

-   Manual FunctionTool creation
-   Pydantic models for structured data
-   Custom validation and processing
-   RunContextWrapper usage

#### 4. Agents as Tools (`04_agents_as_tools.py`)

-   Using Agent.as_tool() method
-   Multi-agent orchestration patterns
-   Specialized agent delegation
-   Agent composition strategies

#### 5. Error Handling (`05_error_handling.py`)

-   Tool failure scenarios
-   Custom error handling
-   Graceful degradation patterns
-   Error propagation to LLM

#### 6. Context-Aware Tools (`06_context_aware_tools.py`)

-   RunContextWrapper usage
-   Context-dependent behavior
-   State sharing between tools
-   Application context integration

### Advanced Examples (Quiz-Focused)

#### 7. Tool Choice Control (`07_tool_choice_control.py`) ⭐ **Quiz Critical**

-   `ModelSettings.tool_choice` parameter
-   Values: "auto", "required", "none", specific tool names
-   `reset_tool_choice` behavior
-   `parallel_tool_calls` vs sequential execution
-   Agent.clone() method for configuration

#### 8. Sync vs Async Execution (`08_sync_vs_async.py`) ⭐ **Quiz Critical**

-   `Runner.run()` vs `Runner.run_sync()`
-   Concurrent execution patterns with `asyncio.gather()`
-   Performance comparisons
-   Error handling in sync vs async contexts
-   Threading and execution context

#### 9. Complete Hosted Tools (`09_complete_hosted_tools.py`) ⭐ **Quiz Critical**

-   All hosted tools: WebSearchTool, FileSearchTool, CodeInterpreterTool, ComputerTool, LocalShellTool, ImageGenerationTool, HostedMCPTool
-   Proper configuration for each tool type
-   Security considerations and best practices
-   Multi-tool agent patterns

#### 10. Advanced Pydantic Integration (`10_advanced_pydantic_integration.py`) ⭐ **Quiz Critical**

-   Complex Pydantic models with validation
-   `strict_json_schema` mode
-   Enums, constraints, and cross-field validation
-   Manual FunctionTool creation with custom schemas
-   Structured error handling and responses

## Key Concepts for Quiz Preparation

### Tool Choice Parameter

```python
from agents import ModelSettings

# Auto (default) - LLM decides
agent.clone(model_settings=ModelSettings(tool_choice="auto"))

# Required - LLM must use a tool
agent.clone(model_settings=ModelSettings(tool_choice="required"))

# None - LLM cannot use tools
agent.clone(model_settings=ModelSettings(tool_choice="none"))

# Specific tool - Force specific tool usage
agent.clone(model_settings=ModelSettings(tool_choice="my_tool"))
```

### Runner Execution Methods

```python
# Asynchronous (preferred)
result = await Runner.run(agent, "message")

# Synchronous (blocking)
result = Runner.run_sync(agent, "message")

# Concurrent execution
results = await asyncio.gather(
    Runner.run(agent1, "task1"),
    Runner.run(agent2, "task2")
)
```

### Tool Behavior Control

```python
# Default behavior - LLM processes tool results
agent = Agent(tool_use_behavior="run_llm_again")

# Stop after first tool call
agent = Agent(tool_use_behavior="stop_on_first_tool")

# Custom tool behavior function
agent = Agent(tool_use_behavior=custom_function)
```

### Agent Configuration and Cloning

```python
# Create base agent
base_agent = Agent(name="Base", tools=[tool1, tool2])

# Clone with modifications
specialized_agent = base_agent.clone(
    instructions="New instructions",
    model_settings=ModelSettings(tool_choice="required"),
    reset_tool_choice=False
)
```

### Pydantic Integration Patterns

```python
# Strict schema for better validation
tool = FunctionTool(
    name="my_tool",
    params_json_schema=MyModel.model_json_schema(),
    strict_json_schema=True  # Enable strict mode
)

# Complex validation with Pydantic
class MyModel(BaseModel):
    field: str = Field(..., description="Required field")

    @validator('field')
    def validate_field(cls, v):
        # Custom validation logic
        return v
```

## Running the Examples

Each example can be run independently:

```bash
cd decoded/05_tools

# Basic examples
python 01_basic_function_tools.py
python 02_hosted_tools.py
python 03_custom_function_tools.py
python 04_agents_as_tools.py
python 05_error_handling.py
python 06_context_aware_tools.py

# Advanced examples (quiz-focused)
python 07_tool_choice_control.py
python 08_sync_vs_async.py
python 09_complete_hosted_tools.py
python 10_advanced_pydantic_integration.py
```

## Quiz Preparation Checklist

Based on the quiz requirements focusing on "niche SDK features", ensure you understand:

-   ✅ **tool_choice parameter** - All values and behaviors
-   ✅ **Runner.run_sync vs Runner.run** - Execution patterns
-   ✅ **ModelSettings configuration** - Complete parameter set
-   ✅ **Agent.clone() method** - Configuration inheritance
-   ✅ **reset_tool_choice behavior** - Tool loop prevention
-   ✅ **parallel_tool_calls setting** - Concurrent vs sequential
-   ✅ **All hosted tools** - Configuration and capabilities
-   ✅ **Pydantic validation** - Strict schemas and custom validation
-   ✅ **FunctionTool manual creation** - Schema control
-   ✅ **Tool behavior patterns** - stop_on_first_tool, custom functions
-   ✅ **Error handling patterns** - Tool failures and recovery
-   ✅ **Context-aware tools** - RunContextWrapper usage

## Advanced Topics

### Tool Execution Flow

1. LLM generates response with tool calls
2. Tools execute (parallel or sequential based on settings)
3. Results processed based on `tool_use_behavior`
4. LLM receives results and continues or stops

### Performance Considerations

-   Async execution for I/O-bound operations
-   Parallel tool calls for independent operations
-   Sequential for dependent operations
-   Tool choice optimization for efficiency

### Security and Validation

-   Input validation with Pydantic
-   Output sanitization
-   Error handling and graceful degradation
-   Rate limiting and resource management

This comprehensive collection covers all the specialized SDK features that would appear in an advanced OpenAI Agents SDK quiz.
