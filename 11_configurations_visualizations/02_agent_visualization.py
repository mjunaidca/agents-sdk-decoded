"""
02_agent_visualization.py

This module demonstrates agent visualization capabilities in the OpenAI Agents SDK.
Shows how to generate graphical representations of agent relationships using Graphviz.

Key Visualization Features:
- Basic agent visualization
- Multi-agent systems with handoffs
- Tool visualization
- Graph customization options
- Saving and viewing graphs

Based on: https://openai.github.io/openai-agents-python/visualization/
"""

import asyncio
import tempfile
import os
from pathlib import Path

try:
    import graphviz
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

from agents import Agent, function_tool
from agents.handoffs import handoff

if GRAPHVIZ_AVAILABLE:
    from agents.extensions.visualization import draw_graph

# ================== TOOLS FOR EXAMPLES ==================


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    return f"The weather in {city} is sunny with 25°C."


@function_tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Found relevant information about: {query}"


@function_tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    return f"Email sent to {to} with subject '{subject}'"


@function_tool
def calculate(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        # Simple evaluation for demo (in production, use a safer approach)
        result = eval(expression.replace("^", "**"))
        return f"Result: {result}"
    except:
        return "Error: Invalid mathematical expression"


@function_tool
def get_stock_price(symbol: str) -> str:
    """Get current stock price for a symbol."""
    return f"Current price of {symbol}: $150.25 (+2.3%)"

# ================== VISUALIZATION EXAMPLES ==================


def demo_installation_check():
    """Check if visualization dependencies are available."""
    print("=== Demo: Installation Check ===")

    if GRAPHVIZ_AVAILABLE:
        print("✅ Graphviz Python package is available")

        # Check if graphviz system package is installed
        try:
            import subprocess
            result = subprocess.run(
                ['dot', '-V'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ Graphviz system package is installed")
                print(f"   Version: {result.stderr.strip()}")
                return True
            else:
                print("❌ Graphviz system package not found")
                print(
                    "💡 Install with: brew install graphviz (macOS) or apt-get install graphviz (Ubuntu)")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Graphviz system package not found")
            print(
                "💡 Install with: brew install graphviz (macOS) or apt-get install graphviz (Ubuntu)")
            return False
    else:
        print("❌ Graphviz Python package not available")
        print("💡 Install with: pip install 'openai-agents[viz]'")
        return False


def demo_simple_agent_visualization():
    """Demonstrate basic agent visualization."""
    print("\n=== Demo: Simple Agent Visualization ===")

    if not GRAPHVIZ_AVAILABLE:
        print("❌ Graphviz not available. Skipping visualization demo.")
        return None

    # Create a simple agent with tools
    simple_agent = Agent(
        name="WeatherAgent",
        instructions="You are a weather assistant. Use the get_weather tool to provide weather information.",
        tools=[get_weather]
    )

    try:
        print("🎨 Creating visualization for simple agent...")

        # Generate the graph
        graph = draw_graph(simple_agent)

        print("✅ Simple agent visualization created")
        print(f"   Agent: {simple_agent.name}")
        print(f"   Tools: {len(simple_agent.tools)} tool(s)")
        print(f"   Handoffs: {len(simple_agent.handoffs)} handoff(s)")

        # Show the DOT source
        print("\n📄 Generated DOT source (first 200 chars):")
        print(graph.source[:200] + "..." if len(graph.source)
              > 200 else graph.source)

        return graph

    except Exception as e:
        print(f"❌ Error creating simple visualization: {e}")
        return None


def demo_multi_agent_visualization():
    """Demonstrate multi-agent system visualization."""
    print("\n=== Demo: Multi-Agent System Visualization ===")

    if not GRAPHVIZ_AVAILABLE:
        print("❌ Graphviz not available. Skipping visualization demo.")
        return None

    # Create specialized agents
    research_agent = Agent(
        name="ResearchAgent",
        instructions="I specialize in web research and information gathering.",
        tools=[search_web]
    )

    communication_agent = Agent(
        name="CommunicationAgent",
        instructions="I handle email communication and messaging.",
        tools=[send_email]
    )

    finance_agent = Agent(
        name="FinanceAgent",
        instructions="I provide financial data and stock information.",
        tools=[get_stock_price, calculate]
    )

    # Create triage agent with handoffs
    triage_agent = Agent(
        name="TriageAgent",
        instructions="""
        I am a triage agent that routes requests to specialized agents.
        - For research tasks, I handoff to ResearchAgent
        - For communication tasks, I handoff to CommunicationAgent  
        - For financial tasks, I handoff to FinanceAgent
        """,
        tools=[get_weather],  # Triage agent has its own tools too
        handoffs=[
            handoff(agent=research_agent),
            handoff(agent=communication_agent),
            handoff(agent=finance_agent)
        ]
    )

    try:
        print("🎨 Creating visualization for multi-agent system...")

        # Generate the graph
        graph = draw_graph(triage_agent)

        print("✅ Multi-agent visualization created")
        print(f"   Main agent: {triage_agent.name}")
        print(f"   Handoff agents: {len(triage_agent.handoffs)}")
        print(
            f"   Total tools across system: {len(triage_agent.tools) + sum(len(agent.tools) for agent in [research_agent, communication_agent, finance_agent])}")

        # Analyze the visualization
        print("\n📊 System Architecture:")
        print(
            f"   - Triage Agent: {len(triage_agent.tools)} tools, {len(triage_agent.handoffs)} handoffs")
        print(f"   - Research Agent: {len(research_agent.tools)} tools")
        print(
            f"   - Communication Agent: {len(communication_agent.tools)} tools")
        print(f"   - Finance Agent: {len(finance_agent.tools)} tools")

        return graph

    except Exception as e:
        print(f"❌ Error creating multi-agent visualization: {e}")
        return None


def demo_complex_agent_visualization():
    """Demonstrate complex agent system with multiple levels."""
    print("\n=== Demo: Complex Agent System Visualization ===")

    if not GRAPHVIZ_AVAILABLE:
        print("❌ Graphviz not available. Skipping visualization demo.")
        return None

    # Level 3: Specialist agents
    weather_specialist = Agent(
        name="WeatherSpecialist",
        instructions="I provide detailed weather forecasts and analysis.",
        tools=[get_weather]
    )

    calculation_specialist = Agent(
        name="CalculationSpecialist",
        instructions="I perform complex mathematical calculations.",
        tools=[calculate]
    )

    # Level 2: Department agents
    data_agent = Agent(
        name="DataAgent",
        instructions="I handle data processing and analysis tasks.",
        tools=[search_web],
        handoffs=[
            handoff(agent=weather_specialist),
            handoff(agent=calculation_specialist)
        ]
    )

    communication_dept = Agent(
        name="CommunicationDept",
        instructions="I manage all communication and outreach.",
        tools=[send_email]
    )

    # Level 1: Main orchestrator
    orchestrator = Agent(
        name="MainOrchestrator",
        instructions="""
        I am the main orchestrator that coordinates all business operations.
        I route tasks to appropriate departments and specialists.
        """,
        tools=[get_stock_price],  # Orchestrator has its own capabilities
        handoffs=[
            handoff(agent=data_agent),
            handoff(agent=communication_dept)
        ]
    )

    try:
        print("🎨 Creating visualization for complex agent system...")

        # Generate the graph
        graph = draw_graph(orchestrator)

        print("✅ Complex system visualization created")

        # Analyze the complex system
        print("\n🏗️ System Hierarchy:")
        print(f"   Level 1 - Orchestrator: {orchestrator.name}")
        print(
            f"   Level 2 - Departments: {len(orchestrator.handoffs)} departments")
        print(
            f"   Level 3 - Specialists: {len(data_agent.handoffs)} specialists")

        print("\n📈 System Metrics:")
        total_agents = 1 + len(orchestrator.handoffs) + \
            len(data_agent.handoffs)
        total_tools = (len(orchestrator.tools) +
                       len(data_agent.tools) + len(communication_dept.tools) +
                       len(weather_specialist.tools) + len(calculation_specialist.tools))

        print(f"   - Total agents: {total_agents}")
        print(f"   - Total tools: {total_tools}")
        print(f"   - Max depth: 3 levels")

        return graph

    except Exception as e:
        print(f"❌ Error creating complex visualization: {e}")
        return None


def demo_graph_customization():
    """Demonstrate graph customization options."""
    print("\n=== Demo: Graph Customization ===")

    if not GRAPHVIZ_AVAILABLE:
        print("❌ Graphviz not available. Skipping customization demo.")
        return

    # Create a test agent
    test_agent = Agent(
        name="CustomizationTest",
        instructions="Test agent for demonstrating customization.",
        tools=[get_weather, calculate]
    )

    try:
        print("🎨 Demonstrating graph customization options...")

        # 1. Basic graph
        basic_graph = draw_graph(test_agent)
        print("✅ Basic graph created")

        # 2. Show customization options
        print("\n🎛️ Customization Options:")
        print("   1. View in separate window: graph.view()")
        print("   2. Save to file: draw_graph(agent, filename='my_graph')")
        print("   3. Access DOT source: graph.source")
        print("   4. Render in different formats: graph.render(..., format='svg')")

        # 3. Demonstrate source access
        print(f"\n📄 DOT Source Info:")
        print(f"   - Source length: {len(basic_graph.source)} characters")
        print(f"   - Contains nodes: {'node [' in basic_graph.source}")
        print(f"   - Contains edges: {'->' in basic_graph.source}")

        return basic_graph

    except Exception as e:
        print(f"❌ Error in customization demo: {e}")
        return None


def demo_save_and_export():
    """Demonstrate saving and exporting graphs."""
    print("\n=== Demo: Save and Export ===")

    if not GRAPHVIZ_AVAILABLE:
        print("❌ Graphviz not available. Skipping save demo.")
        return

    # Create an agent for export demo
    export_agent = Agent(
        name="ExportDemo",
        instructions="Agent for demonstrating export functionality.",
        tools=[get_weather, send_email]
    )

    try:
        print("💾 Demonstrating save and export options...")

        # Create temporary directory for saving
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # 1. Save as PNG
            png_path = temp_path / "agent_graph"
            try:
                graph = draw_graph(export_agent, filename=str(png_path))
                png_file = png_path.with_suffix('.png')

                if png_file.exists():
                    print(f"✅ PNG saved successfully")
                    print(f"   Path: {png_file}")
                    print(f"   Size: {png_file.stat().st_size} bytes")
                else:
                    print("❌ PNG file not created")

            except Exception as e:
                print(f"❌ Error saving PNG: {e}")

            # 2. Show other format options
            print("\n📁 Export Format Options:")
            print("   - PNG: draw_graph(agent, filename='graph')")
            print("   - SVG: graph.render('graph', format='svg')")
            print("   - PDF: graph.render('graph', format='pdf')")
            print("   - DOT: save graph.source to .dot file")

            # 3. Demonstrate DOT source export
            dot_file = temp_path / "agent_graph.dot"
            try:
                with open(dot_file, 'w') as f:
                    f.write(graph.source)
                print(f"✅ DOT source saved to {dot_file}")
                print(f"   Size: {dot_file.stat().st_size} bytes")
            except Exception as e:
                print(f"❌ Error saving DOT source: {e}")

        print("\n💡 Tips for production use:")
        print("   - Save graphs to version control for documentation")
        print("   - Use SVG format for web applications")
        print("   - Include graphs in architectural documentation")
        print("   - Generate graphs automatically in CI/CD pipelines")

    except Exception as e:
        print(f"❌ Error in save/export demo: {e}")


def demo_understanding_visualization():
    """Explain how to understand the generated visualizations."""
    print("\n=== Demo: Understanding Visualizations ===")

    print("🔍 How to Read Agent Visualizations:")
    print()

    print("📊 Graph Elements:")
    print("   🟦 __start__ (blue ellipse): Entry point of execution")
    print("   🟨 Agent boxes (yellow rectangles): AI agents")
    print("   🟩 Tool ellipses (green): Available functions/tools")
    print("   🟦 __end__ (blue ellipse): Execution termination point")
    print()

    print("🔗 Connections:")
    print("   ➡️ Solid arrows: Agent handoffs (delegation)")
    print("   ⚫ Dotted arrows: Tool access (bidirectional)")
    print("   📍 Start → Agent: Initial execution flow")
    print("   📍 Agent → End: Final output (no handoffs)")
    print()

    print("🏗️ Architecture Patterns:")
    print("   🔸 Linear: Start → Agent → Tool → End")
    print("   🔸 Hub & Spoke: Central agent with multiple tool handoffs")
    print("   🔸 Hierarchical: Multi-level agent delegation")
    print("   🔸 Network: Complex interconnected agent systems")
    print()

    print("💡 Analysis Tips:")
    print("   • Count agents to understand system complexity")
    print("   • Follow arrows to trace execution flow")
    print("   • Identify bottlenecks (agents with many connections)")
    print("   • Look for isolated components (potential issues)")
    print("   • Check tool distribution across agents")


def demo_best_practices():
    """Demonstrate best practices for agent visualization."""
    print("\n=== Demo: Visualization Best Practices ===")

    practices = [
        "🎯 Use clear, descriptive agent names",
        "📝 Keep agent instructions concise for better readability",
        "🔧 Group related tools with appropriate agents",
        "🏗️ Design hierarchical structures for complex systems",
        "📊 Generate visualizations during system design",
        "🔄 Update visualizations when architecture changes",
        "📚 Include visualizations in documentation",
        "🧪 Use visualizations to identify optimization opportunities",
        "👥 Share visualizations with team members for review",
        "🎨 Save visualizations in multiple formats for different uses"
    ]

    print("Visualization best practices:")
    for practice in practices:
        print(f"   {practice}")

    print("\n🚫 Common Pitfalls to Avoid:")
    print("   • Creating overly complex single-agent systems")
    print("   • Missing tool-agent relationships")
    print("   • Circular handoff dependencies")
    print("   • Agents with unclear responsibilities")
    print("   • Missing documentation for complex flows")

    print("\n🔧 Optimization Strategies:")
    print("   • Balance agent specialization vs. generalization")
    print("   • Minimize handoff depth for better performance")
    print("   • Group frequently used tools together")
    print("   • Consider parallel execution opportunities")
    print("   • Design for testability and monitoring")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all visualization demonstrations."""
    print("🎨 OpenAI Agents SDK - Agent Visualization Guide 🎨")
    print("\nThis demonstrates how to visualize agent architectures")
    print("using Graphviz for better understanding and documentation.\n")

    # Check if visualization is available
    if not demo_installation_check():
        print("\n❌ Visualization dependencies not available.")
        print("💡 Install with: pip install 'openai-agents[viz]'")
        print("💡 Also install Graphviz system package for your OS")
        return

    # Run visualization demos
    print("\n" + "="*60)
    simple_graph = demo_simple_agent_visualization()

    print("\n" + "="*60)
    multi_graph = demo_multi_agent_visualization()

    print("\n" + "="*60)
    complex_graph = demo_complex_agent_visualization()

    print("\n" + "="*60)
    demo_graph_customization()

    print("\n" + "="*60)
    demo_save_and_export()

    print("\n" + "="*60)
    demo_understanding_visualization()

    print("\n" + "="*60)
    demo_best_practices()

    print("\n" + "="*60)
    print("🎓 Key Visualization Takeaways:")
    print("• Visualizations help understand agent architecture")
    print("• Use graphs for system design and documentation")
    print("• Different complexity levels serve different purposes")
    print("• Save visualizations in multiple formats")
    print("• Include visualizations in team reviews")
    print("• Update visualizations when systems evolve")

    # Optional: Try to view one graph if available
    if GRAPHVIZ_AVAILABLE and simple_graph:
        try:
            print("\n🖼️ To view a graph in a separate window, use: graph.view()")
            print(
                "💡 Example: simple_graph.view() # (if graphviz system package is installed)")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(main())
