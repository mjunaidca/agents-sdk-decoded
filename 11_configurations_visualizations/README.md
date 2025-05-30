# Configuration and Visualization Guide

Welcome to the **Configuration and Visualization** module of the OpenAI Agents SDK educational series! This module covers essential topics for configuring and visualizing your agent systems.

## 📚 Module Overview

This module teaches you how to:

-   Configure the SDK for different environments
-   Set up tracing and logging
-   Visualize agent architectures
-   Optimize for production deployments
-   Implement security best practices

## 📁 Module Contents

### 1. Basic Configuration (`01_basic_configuration.py`)

Learn the fundamentals of SDK configuration:

**Key Topics:**

-   ✅ API key management with environment variables
-   ✅ Custom OpenAI client configuration
-   ✅ Tracing setup and control
-   ✅ Debug logging configuration
-   ✅ Environment variable usage

**Example Usage:**

```python
from agents import set_default_openai_client, enable_verbose_stdout_logging
from openai import AsyncOpenAI

# Configure custom client
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0,
    max_retries=3
)
set_default_openai_client(client)

# Enable verbose logging for development
enable_verbose_stdout_logging()
```

### 2. Agent Visualization (`02_agent_visualization.py`)

Master agent architecture visualization:

**Key Topics:**

-   🎨 Installing Graphviz dependencies
-   🎨 Creating simple agent visualizations
-   🎨 Multi-agent system diagrams
-   🎨 Complex hierarchical architectures
-   🎨 Saving and exporting graphs

**Example Usage:**

```python
from agents.extensions.visualization import draw_graph

# Create and visualize an agent
agent = Agent(
    name="WeatherAgent",
    instructions="Provide weather information",
    tools=[get_weather_tool]
)

# Generate visualization
graph = draw_graph(agent)

# Save as PNG
draw_graph(agent, filename="weather_agent")
```

**Visualization Elements:**

-   🟦 **Blue ellipses**: Start and end points
-   🟨 **Yellow rectangles**: AI agents
-   🟩 **Green ellipses**: Tools/functions
-   ➡️ **Solid arrows**: Agent handoffs
-   ⚫ **Dotted arrows**: Tool access

### 3. Advanced Configuration (`03_advanced_configuration.py`)

Deep dive into production-ready configuration:

**Key Topics:**

-   ⚙️ RunConfig for execution control
-   ⚙️ Custom tracing and spans
-   ⚙️ Model provider customization
-   ⚙️ Environment-specific profiles
-   ⚙️ Security and compliance settings

**Example Usage:**

```python
from agents import RunConfig, trace, custom_span

# Advanced RunConfig
config = RunConfig(
    workflow_name="ProductionWorkflow",
    trace_id=gen_trace_id(),
    group_id="user_session_123",
    trace_metadata={
        "environment": "production",
        "user_id": "user_456",
        "version": "2.1.0"
    }
)

# Custom tracing
with trace("MainWorkflow", trace_id=trace_id):
    with custom_span("DataProcessing"):
        # Your processing logic
        pass
```

### 4. Interactive Quiz (`04_configurations_visualizations_quiz.py`)

Test your knowledge with 30+ questions covering:

**Quiz Categories:**

-   📋 Basic Configuration (API keys, clients, logging)
-   📋 Visualization (Graphviz, graph elements, saving)
-   📋 RunConfig (execution control, tracing options)
-   📋 Advanced Configuration (spans, model settings)
-   📋 Production Configuration (security, performance)
-   📋 Practical Scenarios (debugging, optimization)

**Quiz Modes:**

-   🎯 Quick Quiz (10 questions)
-   🎯 Category-specific quizzes
-   🎯 Difficulty-based quizzes (Beginner/Intermediate/Advanced)
-   🎯 Full comprehensive quiz

## 🔧 Configuration Concepts

### API Key Management

```python
# ✅ Recommended: Environment variables
os.environ["OPENAI_API_KEY"] = "your-key-here"

# ✅ Programmatic setting (if needed)
set_default_openai_key("your-key-here")

# ❌ Avoid: Hardcoding in source code
```

### Environment-Specific Configuration

```python
config_profiles = {
    "development": {
        "tracing_enabled": True,
        "verbose_logging": True,
        "timeout": 30.0,
        "max_turns": 10
    },
    "production": {
        "tracing_enabled": True,
        "verbose_logging": False,
        "timeout": 15.0,
        "max_turns": 5
    }
}
```

### Security Settings

```python
# Disable sensitive data logging in production
os.environ["OPENAI_AGENTS_DONT_LOG_MODEL_DATA"] = "1"
os.environ["OPENAI_AGENTS_DONT_LOG_TOOL_DATA"] = "1"
```

## 🎨 Visualization Concepts

### Installation Requirements

```bash
# Install visualization dependencies
pip install "openai-agents[viz]"

# Install system Graphviz (macOS)
brew install graphviz

# Install system Graphviz (Ubuntu)
apt-get install graphviz
```

### Understanding Visualizations

**Graph Elements:**

-   **Start Node**: Entry point (`__start__`)
-   **Agent Nodes**: Yellow rectangles with agent names
-   **Tool Nodes**: Green ellipses with tool names
-   **End Node**: Termination point (`__end__`)

**Connection Types:**

-   **Solid arrows**: Agent handoffs (control flow)
-   **Dotted arrows**: Tool access (bidirectional)

**Architecture Patterns:**

-   **Linear**: Simple chain of agent → tool → output
-   **Hub & Spoke**: Central agent with multiple tools
-   **Hierarchical**: Multi-level agent delegation
-   **Network**: Complex interconnected systems

### Visualization Best Practices

1. **📏 Use descriptive agent names** for clarity
2. **🔧 Group related tools** with appropriate agents
3. **🏗️ Design hierarchical structures** for complex systems
4. **📊 Generate visualizations** during system design
5. **🔄 Update visualizations** when architecture changes
6. **📚 Include in documentation** for team understanding

## ⚙️ Advanced Configuration

### RunConfig Options

```python
RunConfig(
    workflow_name="MyWorkflow",     # Workflow identifier
    trace_id=gen_trace_id(),        # Unique trace ID
    group_id="session_123",         # Group related traces
    trace_metadata={                # Custom metadata
        "user_id": "user_456",
        "experiment": "A/B_test_v1"
    },
    tracing_disabled=False,         # Enable/disable tracing
    input_guardrails=[...],         # Global input guardrails
    output_guardrails=[...]         # Global output guardrails
)
```

### Custom Tracing

```python
# Manual trace management
with trace("CustomWorkflow", trace_id=trace_id):
    # Custom spans for fine-grained tracking
    with custom_span("DataPrep", metadata={"step": "prepare"}):
        # Data preparation logic
        pass

    with custom_span("AgentExecution", metadata={"step": "execute"}):
        # Agent execution logic
        pass
```

### Model Configuration

```python
from agents import OpenAIChatCompletionsModel

# Custom model settings
model = OpenAIChatCompletionsModel(
    openai_client=custom_client,
    model="gpt-4o-mini",
    temperature=0.7,           # Control randomness
    max_tokens=1000,           # Limit response length
    top_p=0.9,                 # Nucleus sampling
    frequency_penalty=0.1,     # Reduce repetition
    presence_penalty=0.1       # Encourage diversity
)
```

## 🚀 Production Configuration

### Environment Detection

```python
environment = os.getenv("ENVIRONMENT", "development")

if environment == "production":
    # Production settings
    set_tracing_disabled(False)  # Keep tracing for monitoring
    os.environ["OPENAI_AGENTS_DONT_LOG_MODEL_DATA"] = "1"
    timeout = 15.0
    max_turns = 5
elif environment == "development":
    # Development settings
    enable_verbose_stdout_logging()
    timeout = 30.0
    max_turns = 10
```

### Security Checklist

-   ✅ Store API keys in environment variables or secret managers
-   ✅ Disable sensitive data logging in production
-   ✅ Use appropriate timeout and retry settings
-   ✅ Implement proper error handling
-   ✅ Monitor API usage and costs
-   ✅ Use least-privilege access patterns

### Performance Optimization

-   ⚡ Set appropriate `max_turns` limits (5-8 for production)
-   ⚡ Configure reasonable timeouts (15-30 seconds)
-   ⚡ Use connection pooling for high throughput
-   ⚡ Implement circuit breakers for external dependencies
-   ⚡ Monitor response times and error rates

## 🛠️ Practical Examples

### Debugging Configuration Issues

```python
# Enable verbose logging
enable_verbose_stdout_logging()

# Check environment variables
required_vars = ["OPENAI_API_KEY"]
for var in required_vars:
    if not os.getenv(var):
        print(f"❌ Missing environment variable: {var}")

# Test basic configuration
try:
    result = await Runner.run(test_agent, "Hello", max_turns=2)
    print("✅ Configuration working")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

### Architecture Analysis with Visualization

```python
# Generate visualization
graph = draw_graph(main_agent)

# Analyze architecture
def analyze_architecture(agent):
    handoff_count = len(agent.handoffs)
    tool_count = len(agent.tools)

    print(f"Architecture Analysis:")
    print(f"- Handoffs: {handoff_count}")
    print(f"- Tools: {tool_count}")

    if handoff_count > 5:
        print("⚠️ Consider reducing handoff complexity")
    if tool_count > 10:
        print("⚠️ Consider grouping related tools")
```

### A/B Testing Configuration

```python
# Tag experiments with metadata
def run_experiment(variant: str, user_id: str):
    config = RunConfig(
        workflow_name=f"Experiment_{variant}",
        trace_metadata={
            "experiment": "homepage_agent_v2",
            "variant": variant,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
    )

    return await Runner.run(agent, input_text, run_config=config)
```

## 📊 Monitoring and Observability

### Key Metrics to Track

-   **Response Times**: Latency distribution
-   **Token Usage**: Cost monitoring
-   **Error Rates**: Success/failure ratios
-   **User Satisfaction**: Quality metrics
-   **System Health**: Availability and performance

### Trace Analysis

```python
# Use metadata for filtering and analysis
with trace("UserSession", metadata={
    "user_id": "user_123",
    "session_id": "session_456",
    "feature_flags": ["new_ui", "enhanced_agent"]
}):
    # Your workflow logic
    pass
```

## 🎯 Learning Path

### Beginner (Start Here)

1. **Basic Configuration**: API keys, environment variables
2. **Simple Visualization**: Single agent with tools
3. **Basic Tracing**: Understanding trace output

### Intermediate

1. **RunConfig**: Workflow control and metadata
2. **Multi-Agent Visualization**: Complex systems
3. **Environment Profiles**: Development vs. production

### Advanced

1. **Custom Tracing**: Spans and detailed monitoring
2. **Production Optimization**: Performance and security
3. **Architecture Analysis**: Using visualizations for optimization

## 🔗 Additional Resources

-   **Official Documentation**: [Configuration Guide](https://openai.github.io/openai-agents-python/config/)
-   **Visualization Guide**: [Agent Visualization](https://openai.github.io/openai-agents-python/visualization/)
-   **Best Practices**: Review production configuration examples
-   **Community**: Share your configurations and visualizations

## 🤝 Contributing

Have ideas for improving this module? Found issues or want to add examples?

-   Review the existing examples for patterns
-   Add practical scenarios and use cases
-   Improve documentation and explanations
-   Share your production configuration patterns

---

**Next Steps**: Ready to test your knowledge? Run the interactive quiz with `python 04_configurations_visualizations_quiz.py` to reinforce these concepts!
