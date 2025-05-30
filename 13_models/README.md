# 🤖 OpenAI Agents SDK - Models Module

This module provides comprehensive education on model configuration, selection, and optimization within the OpenAI Agents SDK. Each lesson is focused on a single concept to enable expert-level assessment.

## 🎯 Overview

The OpenAI Agents SDK supports multiple model types and providers. This module breaks down model management into **focused, digestible concepts** - each file covers exactly one topic for optimal learning and testing by experienced engineers.

**Focused Structure**: 6 targeted modules (5 learning + 1 quiz) instead of monolithic documentation, perfect for preparing for expert-level assessments and deep technical questioning.

## 📚 Module Structure

### 🏗️ Foundation Modules (1-3)

**Essential concepts for model configuration and usage**

#### 01_default_models.py

-   **Focus**: OpenAI model types and their differences
-   **Key Topics**: OpenAIResponsesModel vs OpenAIChatCompletionsModel comparison
-   **Learning Goals**: Understand model selection trade-offs and migration patterns
-   **Expert Questions**: Architecture decisions, performance optimization, cost management

#### 02_litellm_integration.py

-   **Focus**: LiteLLM extension for 100+ model providers
-   **Key Topics**: Provider setup, model configuration, limitations
-   **Learning Goals**: Multi-provider integration and universal model interface
-   **Expert Questions**: Provider selection strategies, fallback mechanisms, cost optimization

#### 03_model_configuration.py

-   **Focus**: ModelSettings parameters and optimization
-   **Key Topics**: Temperature, max_tokens, penalties, tool_choice, client-level configuration
-   **Learning Goals**: Fine-tuning model behavior for specific use cases
-   **Expert Questions**: Parameter trade-offs, production optimization, use-case matching

### 🚀 Advanced Modules (4-5)

**Advanced patterns for production deployment**

#### 04_model_mixing.py

-   **Focus**: Multi-model architectures and cost optimization
-   **Key Topics**: Triage-specialist patterns, provider mixing, dynamic selection
-   **Learning Goals**: Cost-effective multi-model workflows and performance optimization
-   **Expert Questions**: Architecture scalability, monitoring strategies, fallback implementation

#### 05_provider_integration.py

-   **Focus**: Provider integration and multi-provider workflows
-   **Key Topics**: LiteLLM setup, custom providers, environment configuration
-   **Learning Goals**: Production-ready provider management and deployment patterns
-   **Expert Questions**: Provider selection criteria, failover strategies, environment management

### 🧪 Assessment Module (6)

**Comprehensive technical evaluation**

#### 06_models_quiz.py

-   **Focus**: Test understanding of concepts from modules 01-05
-   **Key Topics**: Model types, ModelSettings, LiteLLM, custom providers, multi-model workflows, cost optimization, production best practices
-   **Learning Goals**: Validate mastery of the OpenAI Agents SDK Models module
-   **Expert Questions**: Scenario-based problem solving, architecture design, troubleshooting

## 🎯 Learning Objectives

By completing this module, you will master:

### Foundation Skills

-   ✅ Model type selection and migration strategies
-   ✅ LiteLLM integration for multiple providers (OpenAI, Anthropic, Google, Mistral)
-   ✅ ModelSettings optimization for different use cases
-   ✅ Client-level configuration and timeout management

### Advanced Skills

-   ✅ Multi-model architectures for cost optimization (60-80% savings)
-   ✅ Provider mixing and specialization strategies
-   ✅ Dynamic model selection based on request complexity
-   ✅ Production deployment and environment management

### Expert-Level Mastery

-   ✅ Cost optimization through intelligent model selection
-   ✅ Performance monitoring and optimization strategies
-   ✅ Reliability through failover and degradation patterns
-   ✅ Scalable multi-provider architecture design
-   ✅ Comprehensive knowledge validation through interactive quiz

## 🌐 Provider Ecosystem Coverage

### Direct OpenAI Support

-   **Models**: gpt-4o, gpt-4o-mini, gpt-3.5-turbo
-   **Features**: Native tool use, structured outputs, function calling
-   **Best For**: General AI tasks, proven reliability

### LiteLLM Integration (100+ Models)

-   **Anthropic**: claude-3-5-sonnet, claude-3-haiku (reasoning, safety)
-   **Google**: gemini-2.5-flash, gemini-1.5-pro (speed, multimodal)
-   **Mistral**: mistral-large, mistral-small (European compliance)
-   **Cohere**: command-r-plus, command-r (enterprise features)

### Custom Providers

-   **Azure OpenAI**: Enterprise deployment
-   **Together.ai**: Open source models
-   **Hugging Face**: Research and experimental models
-   **Self-hosted**: On-premises deployment

## 💰 Cost Optimization Strategies

### Triage-Specialist Pattern

-   **Concept**: Fast, cheap model for routing + powerful model for processing
-   **Savings**: 60-80% cost reduction on typical workloads
-   **Implementation**: gpt-3.5-turbo for triage → gpt-4o for complex tasks

### Provider Cost Comparison

-   **OpenAI gpt-4o**: $15/$3 per 1M tokens (input/output)
-   **Anthropic Claude**: $3/$15 per 1M tokens
-   **Google Gemini**: $1.25/$5 per 1M tokens
-   **Mistral Large**: $4/$12 per 1M tokens

### Dynamic Selection

-   **Simple tasks**: Use gpt-3.5-turbo or gemini-flash
-   **Complex reasoning**: Use claude-3-5-sonnet
-   **Tool integration**: Use gpt-4o
-   **Real-time**: Use gemini-flash

## ⚙️ Configuration Patterns

### ModelSettings Parameters

```python
ModelSettings(
    temperature=0.7,        # Creativity control (0.0-2.0)
    max_tokens=1000,        # Response length limit
    top_p=0.9,             # Vocabulary focus
    frequency_penalty=0.1,  # Repetition reduction
    presence_penalty=0.1,   # Topic diversity
    tool_choice="auto",     # Tool usage control
    parallel_tool_calls=True # Tool execution
)
```

### Client-Level Configuration

```python
client = AsyncOpenAI(
    api_key="your_key",
    timeout=30.0,          # Network timeout
    max_retries=3,         # Retry attempts
    base_url="custom_url"  # Custom provider
)
```

## 🏗️ Architecture Patterns

### Multi-Model Workflow

```python
# Specialized agents for different tasks
triage_agent = Agent(model="gpt-3.5-turbo")      # Fast routing
reasoning_agent = Agent(model="claude-3-5-sonnet") # Complex analysis
speed_agent = Agent(model="gemini-flash")        # Real-time responses
tool_agent = Agent(model="gpt-4o")               # Tool integration
```

### Provider Failover

```python
# Graceful degradation across providers
providers = ["openai", "anthropic", "gemini"]
for provider in providers:
    try:
        return await run_with_provider(provider, request)
    except Exception:
        continue  # Try next provider
```

## 📊 Production Considerations

### Monitoring Metrics

-   **Cost**: $/request by model, monthly spend by provider
-   **Performance**: Response latency, throughput, success rate
-   **Quality**: User satisfaction, task completion rate
-   **Usage**: Token consumption, rate limit utilization

### Reliability Patterns

-   **Failover**: Automatic provider switching on errors
-   **Rate Limiting**: Graceful handling of API limits
-   **Caching**: Response caching for improved performance
-   **Health Checks**: Provider availability monitoring

## 🧪 Testing Your Knowledge

Each module is designed to enable deep technical questioning by experienced engineers:

### Foundation Questions

-   Model selection criteria and trade-offs
-   Provider integration strategies
-   Configuration optimization techniques

### Advanced Questions

-   Multi-model architecture design
-   Cost optimization implementation
-   Performance monitoring strategies

### Expert Questions

-   Scalability patterns for 10M+ requests
-   Reliability engineering for production
-   DACA framework integration patterns

## 🎯 Next Steps

After mastering this module:

1.  **Apply to DACA Framework**: Integrate with Dapr for planet-scale deployment
2.  **Production Deployment**: Implement monitoring and optimization
3.  **Advanced Patterns**: Explore custom model fine-tuning and specialized providers

## 📖 Documentation References

-   [OpenAI Agents SDK Models](https://openai.github.io/openai-agents-python/models/)
-   [LiteLLM Extension](https://openai.github.io/openai-agents-python/ref/extensions/litellm/)
-   [ModelSettings Reference](https://openai.github.io/openai-agents-python/ref/model_settings/)
-   [Provider Examples](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers)

## 🚀 Quick Start

### Default OpenAI Models

```python
from agents import Agent, Runner

# Uses OpenAIResponsesModel by default (recommended)
agent = Agent(name="MyAgent", instructions="You help with tasks")
result = await Runner.run(agent, "Hello world", max_turns=2)
```

### LiteLLM Integration (100+ Models)

```bash
# Install LiteLLM support
pip install "openai-agents[litellm]"
```

```python
# Use any model with litellm/ prefix
claude_agent = Agent(
    model="litellm/anthropic/claude-3-5-sonnet-20240620",
    instructions="You are powered by Claude"
)
```

### Model Configuration

```python
from agents import ModelSettings

# Configure model behavior
agent = Agent(
    name="ConfiguredAgent",
    model_settings=ModelSettings(
        temperature=0.7,      # Balanced creativity
        max_tokens=500,       # Response length limit
        top_p=0.9,           # Vocabulary diversity
    )
)
```

## 📈 Learning Path

**Structured progression for expert-level mastery:**

1.  **Foundation** (Modules 1-3): Core model concepts and configuration
2.  **Advanced Integration** (Modules 4-5): Multi-model architectures and troubleshooting
3.  **Expert Assessment** (Module 6): Comprehensive technical evaluation via interactive quiz

Each learning module is **~300-500 lines** and covers **exactly one concept** comprehensively. The quiz module provides a final assessment.

## 🎯 Why This Structure?

### 🎓 Expert-Level Learning

-   **Focused modules**: One concept per file for deep understanding
-   **Practical examples**: Real-world configuration patterns
-   **Progressive complexity**: Foundation → Advanced → Expert assessment
-   **Technical depth**: Suitable for senior engineer evaluation

### 🧪 Assessment Readiness

-   **Unit-testable knowledge**: Each concept can be questioned independently
-   **Scenario-based learning**: Practical problem-solving approach
-   **Architecture patterns**: Production-ready design principles
-   **Troubleshooting expertise**: Common issues and solutions

### 🏗️ Production Benefits

-   **Configuration reference**: Quick access to specific patterns
-   **Best practices**: Battle-tested approaches
-   **Cost optimization**: Model selection strategies
-   **Performance tuning**: Configuration optimization

## 🤖 Model Types Comparison

| Feature                | ResponsesModel  | ChatCompletionsModel  | LiteLLM Models |
| ---------------------- | --------------- | --------------------- | -------------- |
| **API**                | Responses API   | Chat Completions API  | Various        |
| **Providers**          | OpenAI only     | OpenAI + compatible   | 100+ providers |
| **Features**           | Advanced ✓✓     | Standard ✓            | Variable       |
| **Structured Outputs** | Advanced ✓✓     | Basic ✓               | Variable       |
| **Compatibility**      | OpenAI specific | Universal ✓✓          | Universal ✓✓   |
| **Stability**          | New (evolving)  | Very stable ✓✓        | Beta           |
| **Recommendation**     | New projects    | Legacy/multi-provider | Diverse models |

## 🔧 ModelSettings Parameters

### Core Parameters

-   **temperature** (0.0-2.0): Creativity vs consistency control
-   **max_tokens**: Response length limit (not total context)
-   **top_p** (0.0-1.0): Vocabulary diversity control

### Advanced Parameters

-   **frequency_penalty** (-2.0 to 2.0): Reduce word repetition
-   **presence_penalty** (-2.0 to 2.0): Encourage topic diversity
-   **tool_choice**: 'auto', 'required', 'none', or specific tool name
-   **parallel_tool_calls**: Enable parallel tool execution

### Use Case Configurations

```python
# Code generation
ModelSettings(temperature=0.1, max_tokens=1000, tool_choice="auto")

# Creative writing
ModelSettings(temperature=0.8, presence_penalty=0.4, max_tokens=2000)

# Data extraction
ModelSettings(temperature=0.0, max_tokens=100, top_p=0.1, tool_choice="none")

# Real-time chat (client-level timeout)
ModelSettings(temperature=0.7, max_tokens=300)
```

## 🌐 Supported Providers (via LiteLLM)

### Major Providers

-   **OpenAI**: gpt-4o, gpt-3.5-turbo, o1-preview
-   **Anthropic**: claude-3-5-sonnet, claude-3-haiku
-   **Google**: gemini-2.5-flash, gemini-pro
-   **Cohere**: command-r-plus, command-light
-   **Meta**: llama-2-70b, llama-3-8b
-   **Mistral**: mistral-large, mistral-7b

### Enterprise Providers

-   **Azure OpenAI**: azure/gpt-4, azure/gpt-35-turbo
-   **AWS Bedrock**: bedrock/claude-3, bedrock/llama2
-   **Google Vertex**: vertex_ai/gemini-pro

## 🛠️ Configuration Best Practices

### Development

-   Start with default settings and adjust incrementally
-   Test configuration changes with real use cases
-   Use temperature 0.0-0.2 for deterministic tasks
-   Use temperature 0.6-0.8 for creative tasks

### Production

-   Set appropriate client-level timeouts for your use case
-   Monitor token usage for cost optimization
-   Implement fallback models for reliability
-   Use environment variables for API keys

### Performance

-   Lower max_tokens for faster responses
-   Consider model capabilities vs cost trade-offs
-   Implement caching for repeated queries

## 🔒 Security & Cost Management

### API Key Management

```bash
# Environment variables (recommended)
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
export GOOGLE_API_KEY="your_google_key"
```

### Cost Optimization

-   Use smaller/faster models for simple tasks (Triage-Specialist pattern)
-   Set appropriate max_tokens limits
-   Monitor usage across providers (LiteLLM helps)
-   Implement request caching where appropriate

## 🚨 Common Issues & Solutions

### LiteLLM Integration

-   **Issue**: ModuleNotFoundError
-   **Solution**: `pip install "openai-agents[litellm]"` or `pip install litellm`

### API Compatibility

-   **Issue**: 404 errors with non-OpenAI providers via default client
-   **Solution**: Use `litellm/` prefix or configure a custom `AsyncOpenAI` client with correct `base_url`.

### Structured Outputs

-   **Issue**: JSON schema not supported by some models/providers.
-   **Solution**: Use providers with full JSON schema support (e.g., OpenAI) or implement robust parsing for text-based structured data.

## 📖 Integration with DACA Framework

This Models module aligns with **DACA (Dapr Agentic Cloud Ascent)** principles:

-   **Model Diversity**: Support for 100+ models enables provider flexibility and specialization.
-   **Cost Efficiency**: Smart model selection (Triage-Specialist), configuration optimization, and multi-provider cost comparison.
-   **Scalability**: Different models for different use cases and scales, supporting 10M+ concurrent agents.
-   **Open Core**: LiteLLM integration provides vendor neutrality and access to open-source models.

## 🧪 Expert Assessment Readiness

The modular structure enables **expert-level technical questioning**:

-   **Architecture Decisions**: When to use which model type (ResponsesModel, ChatCompletionsModel) and why. Provider selection trade-offs.
-   **Performance Optimization**: Configuration tuning (ModelSettings, client-level) for specific use cases (e.g., low latency vs. high accuracy).
-   **Cost Management**: Model selection strategies (Triage-Specialist, dynamic selection) for different scenarios. Budgeting with diverse providers.
-   **Troubleshooting**: Debugging configuration issues, provider API errors, LiteLLM integration problems.
-   **Scalability**: Designing multi-model architectures. Implementing robust fallback and monitoring strategies for production systems.

Perfect for assessments designed by experienced engineers testing both theoretical knowledge and practical application skills in the context of building large-scale agentic systems.

## 📖 Additional Resources

-   **Official Documentation**: https://openai.github.io/openai-agents-python/models/
-   **LiteLLM Documentation**: https://openai.github.io/openai-agents-python/ref/extensions/litellm/
-   **Provider Compatibility**: Check LiteLLM provider documentation and individual provider API docs.
-   **DACA Framework**: Production patterns for agentic systems (conceptual).

## 🤝 Contributing

This educational module emphasizes:

-   **Focused learning**: One concept per module
-   **Expert assessment**: Deep technical questioning capability
-   **Production readiness**: Real-world applicable patterns
-   **Progressive complexity**: Foundation to advanced mastery, culminating in a quiz.

---

_Part of the OpenAI Agents SDK Educational Series - Optimized for Expert-Level Technical Assessment_

## Quick Start Commands

```bash
# Run foundation modules
python 01_default_models.py
python 02_litellm_integration.py
python 03_model_configuration.py

# Run advanced modules
python 04_model_mixing.py
python 05_provider_integration.py

# Take the quiz!
python 06_models_quiz.py
```

Each module demonstrates concepts with practical examples and can be run independently for focused learning.
