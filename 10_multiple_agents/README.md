# 10_multiple_agents - OpenAI Agents SDK Multi-Agent Orchestration

This directory contains comprehensive examples of multi-agent orchestration patterns in the OpenAI Agents SDK. Learn how to coordinate multiple AI agents to solve complex tasks through intelligent planning and systematic execution.

## 📖 Core Concepts

### What is Multi-Agent Orchestration?

Multi-agent orchestration refers to coordinating the flow of agents in your application - determining which agents run, in what order, and how they decide what happens next. This enables you to build sophisticated AI systems that can handle complex, multi-faceted tasks.

### Two Main Orchestration Approaches

Based on the [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/multi_agent/), there are two primary orchestration strategies:

1. **🤖 LLM Orchestration** - Intelligence-driven decision making
2. **⚙️ Code Orchestration** - Deterministic programmatic control

## 📁 File Structure

```
10_multiple_agents/
├── 01_llm_orchestrated_agents.py       # LLM intelligence-driven orchestration
├── 02_code_orchestrated_agents.py      # Deterministic code-driven orchestration
├── 03_hybrid_orchestration.py          # Adaptive hybrid approach
├── 04_multiple_agents_quiz.py          # Interactive quiz to test understanding
└── README.md                           # This comprehensive guide
```

## 🤖 LLM Orchestration (Intelligence-Driven)

### Overview

LLM orchestration allows agents to autonomously plan, reason, and decide on execution steps using AI intelligence. The LLM acts as an intelligent coordinator that can adapt to changing requirements.

### Key Features

-   **Autonomous Planning**: LLM decides which tools to use and when
-   **Dynamic Handoffs**: Intelligent delegation to specialized agents
-   **Adaptive Reasoning**: Handles ambiguous and open-ended tasks
-   **Self-Correction**: Can critique and improve its own work

### Best For

-   ✅ Open-ended and creative tasks
-   ✅ Strategic planning and complex reasoning
-   ✅ Tasks requiring domain expertise judgment
-   ✅ Scenarios with ambiguous requirements

### Example Pattern

```python
# Autonomous research orchestrator
research_orchestrator = Agent(
    name="ResearchOrchestrator",
    instructions="""
    You are an intelligent research orchestrator. Plan and execute
    complex research tasks autonomously using available tools and
    delegating to specialized agents.
    """,
    tools=[web_search, file_search, execute_code],
    handoffs=[
        Handoff(target=writing_agent),
        Handoff(target=planning_agent),
        Handoff(target=data_analyst_agent)
    ]
)

# Let the LLM autonomously orchestrate
result = await Runner.run(research_orchestrator, complex_task, max_turns=8)
```

### Key Tactics for LLM Orchestration

1. **Invest in good prompts** - Clearly explain available tools and capabilities
2. **Monitor and iterate** - Track where things go wrong and improve prompts
3. **Enable introspection** - Let agents critique and improve their own work
4. **Use specialized agents** - Domain experts > general-purpose agents
5. **Implement evals** - Measure and improve agent performance over time

## ⚙️ Code Orchestration (Deterministic)

### Overview

Code orchestration uses programmatic logic to control agent flow, providing deterministic, predictable execution with better performance and cost control.

### Key Features

-   **Structured Outputs**: Use Pydantic models for decision making
-   **Sequential Chaining**: Transform output of one agent into input of next
-   **Parallel Execution**: Run independent tasks concurrently with `asyncio.gather`
-   **Iterative Loops**: Quality-driven improvement with evaluator agents

### Best For

-   ✅ Predictable, well-defined workflows
-   ✅ Performance and cost-critical applications
-   ✅ Tasks that can be decomposed systematically
-   ✅ High-volume processing scenarios

### Example Patterns

#### 1. Structured Routing

```python
# Classify task to route to appropriate specialist
classification_result = await Runner.run(task_classifier, task)
classification = classification_result.final_output_as(TaskClassification)

# Route based on classification
if classification.category == TaskCategory.RESEARCH:
    agent = research_agent
elif classification.category == TaskCategory.WRITING:
    agent = writing_agent
# ... etc

result = await Runner.run(agent, task)
```

#### 2. Sequential Chaining

```python
# Chain: Plan -> Research -> Write -> Evaluate
plan = await Runner.run(planner, task)
research = await Runner.run(researcher, plan.final_output)
content = await Runner.run(writer, research.final_output)
evaluation = await Runner.run(evaluator, content.final_output)
```

#### 3. Parallel Execution

```python
# Run multiple independent tasks in parallel
research_tasks = [
    research_task("Healthcare AI", "Research AI in healthcare"),
    research_task("Finance AI", "Research AI in finance"),
    research_task("Education AI", "Research AI in education")
]

results = await asyncio.gather(*research_tasks)
```

#### 4. Iterative Improvement

```python
# Keep improving until quality threshold is met
current_content = initial_content
for iteration in range(max_iterations):
    assessment = await Runner.run(evaluator, current_content)
    if assessment.quality_score >= threshold:
        break
    current_content = await Runner.run(improver, current_content)
```

## 🔀 Hybrid Orchestration (Best of Both Worlds)

### Overview

Hybrid orchestration intelligently combines LLM decision-making with code control, adapting the approach based on task characteristics for optimal results.

### Key Features

-   **Adaptive Strategy Selection**: Choose approach based on task analysis
-   **Phased Execution**: LLM planning + code execution + LLM synthesis
-   **Fallback Mechanisms**: Graceful degradation when primary strategy fails
-   **Dynamic Configuration**: Runtime modification of agent capabilities

### Example Architecture

```python
class HybridOrchestrator:
    async def orchestrate_task(self, task: str):
        # 1. Analyze task to determine best approach
        analysis = await self.analyze_task(task)

        # 2. Execute with optimal strategy
        if analysis.orchestration_strategy.mode == OrchestrationMode.LLM_DRIVEN:
            return await self.execute_llm_driven(task, analysis)
        elif analysis.orchestration_strategy.mode == OrchestrationMode.CODE_DRIVEN:
            return await self.execute_code_driven(task, analysis)
        else:  # HYBRID
            return await self.execute_hybrid(task, analysis)
```

## 🎯 Orchestration Patterns Deep Dive

### Pattern 1: Autonomous Research System

**Use Case**: Complex research projects requiring multiple data sources and expertise

```python
# LLM autonomously plans research strategy
# Uses tools: web_search, file_search, code_execution
# Delegates to: writing_specialist, planning_specialist, data_analyst
```

### Pattern 2: Content Creation Pipeline

**Use Case**: Systematic content creation with quality control

```python
# Sequential chain: Planning -> Research -> Writing -> Quality Check
# Each step feeds into the next with structured handoffs
```

### Pattern 3: Parallel Processing System

**Use Case**: High-volume independent task processing

```python
# Multiple research agents working simultaneously
# Final synthesis of all results into comprehensive report
```

### Pattern 4: Iterative Quality Improvement

**Use Case**: Content that must meet specific quality standards

```python
# Writer creates content -> Evaluator assesses -> Writer improves
# Continues until quality threshold is met or max iterations reached
```

## 🚀 Best Practices

### 1. Orchestration Design

-   **Choose the right approach** for your specific use case
-   **Hybrid strategies** often provide the best balance
-   **Specialized agents** typically outperform general-purpose ones
-   **Design for failure** with fallback strategies

### 2. Performance Optimization

-   **Use parallel execution** for independent tasks
-   **Implement caching** for repeated operations
-   **Monitor token usage** and API costs
-   **Set appropriate timeouts** and retry policies

### 3. Quality Assurance

-   **Implement comprehensive testing** for all orchestration paths
-   **Use structured outputs** for deterministic decision making
-   **Add quality evaluation steps** in your workflows
-   **Monitor real-world performance** and iterate

### 4. Production Readiness

-   **Implement proper logging** and observability
-   **Add circuit breakers** for external dependencies
-   **Design for scalability** with stateless agents
-   **Use configuration management** for different environments

## 📊 Performance Comparison

| Aspect             | LLM Orchestration | Code Orchestration | Hybrid   |
| ------------------ | ----------------- | ------------------ | -------- |
| **Flexibility**    | ⭐⭐⭐⭐⭐        | ⭐⭐               | ⭐⭐⭐⭐ |
| **Predictability** | ⭐⭐              | ⭐⭐⭐⭐⭐         | ⭐⭐⭐⭐ |
| **Cost**           | ⭐⭐              | ⭐⭐⭐⭐⭐         | ⭐⭐⭐   |
| **Speed**          | ⭐⭐              | ⭐⭐⭐⭐⭐         | ⭐⭐⭐   |
| **Creativity**     | ⭐⭐⭐⭐⭐        | ⭐⭐               | ⭐⭐⭐⭐ |
| **Reliability**    | ⭐⭐⭐            | ⭐⭐⭐⭐⭐         | ⭐⭐⭐⭐ |

## 🔧 Running the Examples

Each example is self-contained and demonstrates different orchestration patterns:

```bash
# LLM-driven orchestration with autonomous planning
python decoded/10_multiple_agents/01_llm_orchestrated_agents.py

# Code-driven orchestration with deterministic control
python decoded/10_multiple_agents/02_code_orchestrated_agents.py

# Hybrid orchestration with adaptive strategies
python decoded/10_multiple_agents/03_hybrid_orchestration.py

# Test your understanding with the interactive quiz
python decoded/10_multiple_agents/04_multiple_agents_quiz.py
```

## 🧠 When to Use Each Approach

### Choose LLM Orchestration When:

-   Tasks are **open-ended** or **creative**
-   Requirements are **ambiguous** or **evolving**
-   You need **strategic thinking** and **reasoning**
-   **Quality** is more important than **speed/cost**
-   You want **autonomous adaptation** to new scenarios

### Choose Code Orchestration When:

-   Tasks are **well-defined** and **predictable**
-   You need **consistent performance** and **cost control**
-   **Speed** and **efficiency** are priorities
-   You can **decompose** the problem systematically
-   You need **high reliability** and **auditability**

### Choose Hybrid Orchestration When:

-   Tasks have **varying complexity** and **requirements**
-   You want **adaptability** with **performance control**
-   Different phases need **different approaches**
-   You need **fallback strategies** for robustness
-   You want to **optimize** for multiple criteria

## 🔗 Related Concepts

This builds on previous concepts from the decoded series:

-   **Agents** (`01_agent/`) - Individual agent creation and configuration
-   **Runners** (`02_runner/`) - Executing agents and handling results
-   **Tools** (`05_tools/`) - Equipping agents with capabilities
-   **Handoffs** (`06_hands_off/`) - Agent-to-agent task delegation
-   **Guardrails** (`09_guardrails/`) - Safety and validation in orchestration

## 📈 Advanced Topics

After mastering basic orchestration, explore:

-   **Context Management** - Maintaining state across agent interactions
-   **Tracing and Monitoring** - Observability in complex workflows
-   **Voice Agents** - Orchestrating speech-based agent interactions
-   **DACA Framework** - Scalable agent infrastructure patterns

## 🎓 Key Takeaways

1. **Two main approaches**: LLM orchestration (intelligence) vs Code orchestration (determinism)
2. **Hybrid strategies** often provide optimal balance of flexibility and control
3. **Specialized agents** typically outperform general-purpose solutions
4. **Parallel execution** can dramatically improve performance for independent tasks
5. **Quality evaluation loops** enable iterative improvement
6. **Proper monitoring and fallbacks** are essential for production systems
7. **Choose approach based on task characteristics** and requirements

## 📚 Additional Resources

-   [OpenAI Agents SDK Multi-Agent Documentation](https://openai.github.io/openai-agents-python/multi_agent/)
-   [Agent Patterns Examples](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns)
-   [Handoffs Documentation](https://openai.github.io/openai-agents-python/handoffs/)
-   [Context Management Guide](https://openai.github.io/openai-agents-python/context_management/)

---

_This guide provides comprehensive coverage of multi-agent orchestration patterns. Practice with the examples, take the quiz, and experiment with different approaches to master these powerful coordination strategies!_ 🚀
