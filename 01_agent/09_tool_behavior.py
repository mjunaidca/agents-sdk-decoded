"""
🛠️ TOOL USE BEHAVIOR - COMPREHENSIVE DEEP DIVE
Complete mastery of tool_use_behavior configuration in OpenAI Agents SDK

This comprehensive guide covers all four tool_use_behavior modes:
1. "run_llm_again" (default) - LLM processes tool results
2. "stop_on_first_tool" - First tool output becomes final output
3. StopAtTools (list) - Stop when specific tools are called
4. Custom ToolsToFinalOutputFunction - Advanced control logic

Key Concepts:
- Tool execution flow control
- When to use each behavior mode
- Performance implications
- Production patterns and best practices
- Error handling in different modes
- Combining with other Agent features
"""

from dataclasses import field
import asyncio
import os
from dataclasses import dataclass
from typing import Any, List, Dict

from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from agents.agent import ToolsToFinalOutputResult, StopAtTools
from agents.run_context import RunContextWrapper

load_dotenv(find_dotenv())

provider = AsyncOpenAI(base_url="https://api.openai.com/v1",
                       api_key=os.getenv("OPENAI_API_KEY"))

# =============================================================================
# CONTEXT FOR TOOL BEHAVIOR DEMOS
# =============================================================================


@dataclass
class ToolBehaviorContext:
    execution_log: List[str] = field(default_factory=list)
    tool_results: Dict[str, Any] = field(default_factory=dict)
    processing_mode: str = "default"

# =============================================================================
# DEMO TOOLS FOR BEHAVIOR TESTING
# =============================================================================


@function_tool
async def fetch_data(context: RunContextWrapper[ToolBehaviorContext], source: str) -> str:
    """Fetch data from a specified source"""
    context.context.execution_log.append(
        f"TOOL: fetch_data called with source={source}")

    # Simulate data fetching
    data = {
        "database": "User records: 1000 active users, 500 premium subscribers",
        "api": "Weather: 72°F, sunny, 10% chance of rain",
        "file": "Config: debug=true, max_connections=100, timeout=30s"
    }

    result = data.get(source, f"No data available for source: {source}")
    context.context.tool_results["fetch_data"] = result
    return result


@function_tool
async def process_data(context: RunContextWrapper[ToolBehaviorContext], data: str, operation: str) -> str:
    """Process data with specified operation"""
    context.context.execution_log.append(
        f"TOOL: process_data called with operation={operation}")

    # Simulate data processing
    if operation == "summarize":
        result = f"Summary: {data[:50]}... (processed)"
    elif operation == "analyze":
        result = f"Analysis: Key metrics extracted from {len(data)} characters"
    elif operation == "transform":
        result = f"Transformed: {data.upper()[:30]}..."
    else:
        result = f"Unknown operation: {operation}"

    context.context.tool_results["process_data"] = result
    return result


@function_tool
async def save_result(context: RunContextWrapper[ToolBehaviorContext], data: str, format: str = "json") -> str:
    """Save processed data in specified format"""
    context.context.execution_log.append(
        f"TOOL: save_result called with format={format}")

    result = f"Data saved successfully in {format} format. Size: {len(data)} bytes"
    context.context.tool_results["save_result"] = result
    return result


@function_tool
async def generate_report(context: RunContextWrapper[ToolBehaviorContext], data: str, report_type: str = "summary") -> str:
    """Generate a report from processed data"""
    context.context.execution_log.append(
        f"TOOL: generate_report called with type={report_type}")

    result = f"📊 {report_type.upper()} REPORT\n" \
        f"Data processed: {len(data)} characters\n" \
        f"Generated at: {asyncio.get_event_loop().time()}\n" \
        f"Status: Complete"

    context.context.tool_results["generate_report"] = result
    return result


@function_tool
async def send_notification(context: RunContextWrapper[ToolBehaviorContext], message: str, recipient: str) -> str:
    """Send notification to specified recipient"""
    context.context.execution_log.append(
        f"TOOL: send_notification called to {recipient}")

    result = f"✉️ Notification sent to {recipient}: {message[:50]}..."
    context.context.tool_results["send_notification"] = result
    return result

# =============================================================================
# DEMO 1: Default Behavior - "run_llm_again"
# =============================================================================


async def demo_run_llm_again():
    """Demonstrate default tool_use_behavior: run_llm_again"""
    print("=" * 80)
    print("DEMO 1: Default Behavior - 'run_llm_again'")
    print("=" * 80)

    context = ToolBehaviorContext()

    # Agent with default behavior (run_llm_again)
    default_agent = Agent(
        name="DefaultAgent",
        instructions="""You are a data processing agent. When asked to process data:
        1. First fetch the data from the specified source
        2. Process the data as requested
        3. Provide a summary of what was accomplished
        
        Always explain what you did and provide insights about the results.""",
        tools=[fetch_data, process_data, save_result],
        # tool_use_behavior="run_llm_again" is the default
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    print("🔄 Testing default behavior: LLM processes tool results")
    print("Query: 'Fetch data from database and summarize it'")

    try:
        result = await Runner.run(
            default_agent,
            "Fetch data from database and summarize it",
            context=context
        )

        print(f"\n✅ Final Output: {result.final_output}")
        print(f"\n📊 Execution Log:")
        for i, log in enumerate(context.execution_log, 1):
            print(f"   {i}. {log}")

        print(f"\n🔧 Tool Results:")
        for tool, tool_result in context.tool_results.items():
            print(f"   {tool}: {tool_result[:60]}...")

    except Exception as e:
        print(f"❌ Error: {e}")

# =============================================================================
# DEMO 2: Stop on First Tool - Direct Tool Output
# =============================================================================


async def demo_stop_on_first_tool():
    """Demonstrate tool_use_behavior: stop_on_first_tool"""
    print("\n" + "=" * 80)
    print("DEMO 2: Stop on First Tool - Direct Tool Output")
    print("=" * 80)

    context = ToolBehaviorContext()

    # Agent that stops on first tool call
    direct_agent = Agent(
        name="DirectAgent",
        instructions="You are a direct data fetcher. Use tools to get exactly what the user requests.",
        tools=[fetch_data, process_data, generate_report],
        tool_use_behavior="stop_on_first_tool",  # Stop after first tool
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    print("⏹️  Testing stop_on_first_tool: First tool output becomes final result")
    print("Query: 'Get weather data from API'")

    try:
        result = await Runner.run(
            direct_agent,
            "Get weather data from API",
            context=context
        )

        print(f"\n✅ Final Output (Direct Tool Result): {result.final_output}")
        print(f"\n📊 Execution Log:")
        for i, log in enumerate(context.execution_log, 1):
            print(f"   {i}. {log}")

        print(f"\n💡 Note: LLM did not process the tool result - direct output used")

    except Exception as e:
        print(f"❌ Error: {e}")

# =============================================================================
# DEMO 3: Stop at Specific Tools - Selective Control
# =============================================================================


async def demo_stop_at_tools():
    """Demonstrate tool_use_behavior: StopAtTools"""
    print("\n" + "=" * 80)
    print("DEMO 3: Stop at Specific Tools - Selective Control")
    print("=" * 80)

    context = ToolBehaviorContext()

    # Agent that stops when specific tools are called
    selective_agent = Agent(
        name="SelectiveAgent",
        instructions="""You are a data pipeline agent. Process data through multiple steps:
        1. Fetch data from source
        2. Process the data
        3. Save results or generate reports
        
        When you save results or generate reports, that should be the final step.""",
        tools=[fetch_data, process_data, save_result, generate_report],
        tool_use_behavior=StopAtTools(stop_at_tool_names=[
            "save_result", "generate_report"]),
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    print("🎯 Testing StopAtTools: Stop when save_result or generate_report is called")
    print("Query: 'Fetch database data, analyze it, and generate a report'")

    try:
        result = await Runner.run(
            selective_agent,
            "Fetch database data, analyze it, and generate a report",
            context=context
        )

        print(f"\n✅ Final Output: {result.final_output}")
        print(f"\n📊 Execution Log:")
        for i, log in enumerate(context.execution_log, 1):
            print(f"   {i}. {log}")

        print(
            f"\n🎯 Stopped at: {[tool for tool in ['save_result', 'generate_report'] if tool in context.tool_results]}")

    except Exception as e:
        print(f"❌ Error: {e}")

# =============================================================================
# DEMO 4: Custom Tool Behavior Function - Advanced Control
# =============================================================================


async def custom_tool_behavior(context: RunContextWrapper, tool_results: List[Any]) -> ToolsToFinalOutputResult:
    """Custom function to determine when to stop tool execution"""

    # Log the custom behavior execution
    context.context.execution_log.append(
        f"CUSTOM: Evaluating {len(tool_results)} tool results")

    # Get the last tool result
    if not tool_results:
        return ToolsToFinalOutputResult(is_final_output=False)

    last_result = tool_results[-1]
    result_text = str(last_result.result) if hasattr(
        last_result, 'result') else str(last_result)

    # Custom logic: Stop if we have a report or if we've processed data
    stop_conditions = [
        "REPORT" in result_text.upper(),
        "saved successfully" in result_text.lower(),
        len(tool_results) >= 3,  # Stop after 3 tool calls
        "error" in result_text.lower()
    ]

    should_stop = any(stop_conditions)

    if should_stop:
        # Create custom final output
        summary = f"🎯 CUSTOM BEHAVIOR SUMMARY\n"
        summary += f"Processed {len(tool_results)} tool calls\n"
        summary += f"Final result: {result_text[:100]}..."

        context.context.execution_log.append(
            "CUSTOM: Stopping execution with custom output")
        return ToolsToFinalOutputResult(is_final_output=True, final_output=summary)
    else:
        context.context.execution_log.append("CUSTOM: Continuing execution")
        return ToolsToFinalOutputResult(is_final_output=False)


async def demo_custom_tool_behavior():
    """Demonstrate custom tool_use_behavior function"""
    print("\n" + "=" * 80)
    print("DEMO 4: Custom Tool Behavior Function - Advanced Control")
    print("=" * 80)

    context = ToolBehaviorContext()

    # Agent with custom tool behavior function
    custom_agent = Agent(
        name="CustomAgent",
        instructions="""You are an intelligent data processor. Use tools to complete complex workflows.
        The system will automatically determine when to stop based on custom logic.""",
        tools=[fetch_data, process_data, save_result,
               generate_report, send_notification],
        tool_use_behavior=custom_tool_behavior,
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    print("🧠 Testing custom tool behavior: Advanced stopping logic")
    print("Query: 'Create a complete data processing workflow'")

    try:
        result = await Runner.run(
            custom_agent,
            "Fetch data from database, process it, generate a report, and notify the team",
            context=context
        )

        print(f"\n✅ Final Output: {result.final_output}")
        print(f"\n📊 Execution Log:")
        for i, log in enumerate(context.execution_log, 1):
            print(f"   {i}. {log}")

        print(f"\n🔧 Tool Results Collected:")
        for tool, tool_result in context.tool_results.items():
            print(f"   {tool}: {tool_result[:60]}...")

    except Exception as e:
        print(f"❌ Error: {e}")

# =============================================================================
# DEMO 5: Behavior Comparison - Performance Analysis
# =============================================================================


async def demo_behavior_comparison():
    """Compare different tool_use_behavior modes"""
    print("\n" + "=" * 80)
    print("DEMO 5: Behavior Comparison - Performance Analysis")
    print("=" * 80)

    behaviors: List[tuple[str, Any]] = [
        ("run_llm_again", "run_llm_again"),
        ("stop_on_first_tool", "stop_on_first_tool"),
        ("stop_at_tools", StopAtTools(stop_at_tool_names=["fetch_data"])),
    ]

    results = {}

    for name, behavior in behaviors:
        print(f"\n🔄 Testing {name}...")

        context = ToolBehaviorContext()

        agent = Agent(
            name=f"TestAgent_{name}",
            instructions="Fetch data from the database source.",
            tools=[fetch_data],
            tool_use_behavior=behavior,
            model=OpenAIChatCompletionsModel(
                openai_client=provider, model="gpt-4o-mini")
        )

        try:
            import time
            start_time = time.time()

            result = await Runner.run(
                agent,
                "Get database information",
                context=context
            )

            end_time = time.time()

            results[name] = {
                "success": True,
                "output": result.final_output,
                "execution_time": end_time - start_time,
                "tool_calls": len(context.execution_log),
                "output_length": len(str(result.final_output))
            }

        except Exception as e:
            results[name] = {
                "success": False,
                "error": str(e),
                "execution_time": 0,
                "tool_calls": 0,
                "output_length": 0
            }

    # Display comparison
    print(f"\n📊 BEHAVIOR COMPARISON RESULTS:")
    print(f"{'Behavior':<20} {'Success':<8} {'Time(s)':<8} {'Tools':<6} {'Output Len':<10}")
    print("-" * 60)

    for name, data in results.items():
        if data["success"]:
            print(
                f"{name:<20} {'✅':<8} {data['execution_time']:<8.2f} {data['tool_calls']:<6} {data['output_length']:<10}")
        else:
            print(f"{name:<20} {'❌':<8} {'N/A':<8} {'N/A':<6} {'N/A':<10}")

    print(f"\n💡 Key Insights:")
    print(f"   • run_llm_again: Full LLM processing, richest output")
    print(f"   • stop_on_first_tool: Fastest, direct tool output")
    print(f"   • stop_at_tools: Selective control, balanced approach")

# =============================================================================
# DEMO 6: Production Patterns & Best Practices
# =============================================================================


async def demo_production_patterns():
    """Demonstrate production-ready tool behavior patterns"""
    print("\n" + "=" * 80)
    print("DEMO 6: Production Patterns & Best Practices")
    print("=" * 80)

    # Pattern 1: API Gateway Agent (stop_on_first_tool)
    print("🌐 Pattern 1: API Gateway Agent")
    api_agent = Agent(
        name="APIGateway",
        instructions="You are an API gateway. Route requests to appropriate data sources.",
        tools=[fetch_data],
        tool_use_behavior="stop_on_first_tool",  # Direct API responses
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    # Pattern 2: Data Pipeline Agent (StopAtTools)
    print("🔄 Pattern 2: Data Pipeline Agent")
    pipeline_agent = Agent(
        name="DataPipeline",
        instructions="Process data through ETL pipeline stages.",
        tools=[fetch_data, process_data, save_result],
        tool_use_behavior=StopAtTools(stop_at_tool_names=["save_result"]),
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    # Pattern 3: Interactive Assistant (run_llm_again)
    print("💬 Pattern 3: Interactive Assistant")
    assistant_agent = Agent(
        name="InteractiveAssistant",
        instructions="You are a helpful assistant. Use tools and provide thoughtful responses.",
        tools=[fetch_data, process_data],
        tool_use_behavior="run_llm_again",  # Full LLM processing
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini")
    )

    patterns = [
        ("API Gateway", api_agent, "Get file configuration"),
        ("Data Pipeline", pipeline_agent, "Process database data and save it"),
        ("Interactive Assistant", assistant_agent,
         "Help me understand the database data")
    ]

    for pattern_name, agent, query in patterns:
        print(f"\n🎯 Testing {pattern_name}:")
        context = ToolBehaviorContext()

        try:
            result = await Runner.run(agent, query, context=context)
            print(f"   ✅ Output: {result.final_output[:80]}...")
            print(f"   📊 Tool calls: {len(context.execution_log)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

# =============================================================================
# MAIN EXECUTION - COMPLETE TOOL BEHAVIOR MASTERY
# =============================================================================


async def main():
    """Execute complete tool behavior demonstration"""
    print("🛠️ TOOL USE BEHAVIOR - COMPREHENSIVE DEEP DIVE")
    print("=" * 100)
    print("Master all four tool_use_behavior modes with practical examples")
    print("=" * 100)

    await demo_run_llm_again()
    await demo_stop_on_first_tool()
    await demo_stop_at_tools()
    await demo_custom_tool_behavior()
    await demo_behavior_comparison()
    await demo_production_patterns()

    print("\n" + "=" * 100)
    print("🎓 TOOL BEHAVIOR MASTERY ACHIEVED")
    print("=" * 100)
    print("""
    ✅ COMPLETE TOOL_USE_BEHAVIOR COVERAGE:
    
    1. 🔄 run_llm_again (Default)
       - LLM processes all tool results
       - Rich, contextual responses
       - Best for interactive assistants
    
    2. ⏹️  stop_on_first_tool
       - Direct tool output as final result
       - Fastest execution
       - Perfect for API gateways
    
    3. 🎯 StopAtTools (Selective)
       - Stop when specific tools are called
       - Balanced control and flexibility
       - Ideal for data pipelines
    
    4. 🧠 Custom ToolsToFinalOutputFunction
       - Advanced conditional logic
       - Maximum flexibility
       - Complex workflow control
    
    🚀 PRODUCTION PATTERNS MASTERED:
    • API Gateway Pattern (direct responses)
    • Data Pipeline Pattern (selective stopping)
    • Interactive Assistant Pattern (full processing)
    • Custom Workflow Control (advanced logic)
    
    🎯 READY FOR EXPERT-LEVEL AGENT DEVELOPMENT!
    """)

if __name__ == "__main__":
    asyncio.run(main())
