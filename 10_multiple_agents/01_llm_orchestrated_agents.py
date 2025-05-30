"""
01_llm_orchestrated_agents.py

This module demonstrates LLM-orchestrated multi-agent systems where agents use 
AI intelligence to plan, reason, and decide on next steps. The LLM autonomously
plans task execution using tools and handoffs to specialized agents.

Key Concepts:
- LLM-driven decision making
- Autonomous task planning  
- Tool-equipped agents
- Agent handoffs for specialization
- Open-ended task handling
"""

import asyncio
import logging
from agents import Agent, Runner, function_tool
from agents.handoffs import handoff

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================== TOOLS FOR RESEARCH AGENT ==================


@function_tool
def web_search(query: str) -> str:
    """Search the web for information. This is a mock implementation."""
    logger.info(f"🔍 Web searching for: {query}")

    # Mock web search results based on query
    if "python" in query.lower():
        return """
        Web Search Results for '{query}':
        
        1. Python.org - Official Python website with documentation
        2. Real Python - Python tutorials and best practices  
        3. Python Package Index (PyPI) - Repository of Python packages
        4. Stack Overflow - Python questions and answers
        
        Python is a high-level programming language known for its simplicity and readability.
        """
    elif "ai" in query.lower() or "artificial intelligence" in query.lower():
        return """
        Web Search Results for '{query}':
        
        1. OpenAI - Leading AI research company
        2. Machine Learning Mastery - AI/ML tutorials
        3. Towards Data Science - AI articles and research
        4. Google AI - Google's AI research and tools
        
        Artificial Intelligence is revolutionizing industries through automation and intelligent decision-making.
        """
    else:
        return f"""
        Web Search Results for '{query}':
        
        1. Wikipedia article about {query}
        2. Official documentation for {query}
        3. Tutorial guides for {query}
        4. Community discussions about {query}
        
        Found relevant information about {query} from various sources.
        """


@function_tool
def file_search(filename: str, search_term: str) -> str:
    """Search through proprietary files and data. This is a mock implementation."""
    logger.info(f"📁 Searching file '{filename}' for: {search_term}")

    return f"""
    File Search Results:
    
    File: {filename}
    Search Term: {search_term}
    
    Found 3 matches:
    - Line 45: Context about {search_term} in our internal documentation
    - Line 128: Best practices for {search_term} implementation
    - Line 203: Examples of {search_term} usage in our codebase
    
    Internal knowledge indicates specific implementation details for {search_term}.
    """


@function_tool
def execute_code(code: str, language: str = "python") -> str:
    """Execute code for data analysis. This is a mock implementation for safety."""
    logger.info(f"⚡ Executing {language} code")

    if "import" in code and "pandas" in code:
        return """
        Code Execution Results:
        
        Successfully executed data analysis code.
        
        Output:
        - Loaded dataset with 1,000 rows and 15 columns
        - Performed statistical analysis
        - Generated visualization plots
        - Saved results to output.csv
        
        Summary: Data analysis completed successfully.
        """
    else:
        return f"""
        Code Execution Results:
        
        Executed {language} code successfully.
        
        Output: Code ran without errors and produced expected results.
        """

# ================== SPECIALIZED AGENTS ==================


# Writing specialist agent
writing_agent = Agent(
    name="WritingSpecialist",
    instructions="""
    You are a skilled writing specialist. Your expertise includes:
    - Creating clear, engaging content
    - Structuring articles and reports
    - Adapting tone and style to audience
    - Editing and improving text quality
    
    When you receive a writing task:
    1. Understand the target audience and purpose
    2. Create a logical structure
    3. Write clear, compelling content
    4. Ensure proper flow and transitions
    
    Always focus on clarity, engagement, and quality.
    """
)

# Planning specialist agent
planning_agent = Agent(
    name="PlanningSpecialist",
    instructions="""
    You are an expert planning specialist. Your role is to:
    - Break down complex tasks into manageable steps
    - Create detailed project plans and timelines
    - Identify required resources and dependencies
    - Anticipate potential challenges and solutions
    
    When given a task to plan:
    1. Analyze the scope and requirements
    2. Break it into logical phases
    3. Define deliverables for each phase
    4. Estimate effort and timeline
    5. Identify dependencies and risks
    
    Provide structured, actionable plans.
    """
)

# Data analysis specialist agent
data_analyst_agent = Agent(
    name="DataAnalyst",
    instructions="""
    You are a data analysis expert. Your capabilities include:
    - Statistical analysis and interpretation
    - Data visualization and reporting
    - Pattern recognition and insights
    - Recommendation based on data findings
    
    When analyzing data:
    1. Understand the business context
    2. Clean and prepare the data
    3. Apply appropriate analysis methods
    4. Generate meaningful visualizations
    5. Provide actionable insights
    
    Always explain your methodology and findings clearly.
    """,
    tools=[execute_code]
)

# ================== RESEARCH ORCHESTRATOR AGENT ==================

# Main research agent with tools and handoffs
research_orchestrator = Agent(
    name="ResearchOrchestrator",
    instructions="""
    You are an intelligent research orchestrator agent. Your role is to autonomously
    plan and execute complex research tasks by using available tools and delegating 
    to specialized agents.
    
    Available capabilities:
    - Web search for online information
    - File search for internal/proprietary data
    - Code execution for data analysis
    - Handoffs to specialized agents (writing, planning, data analysis)
    
    For any research task:
    1. PLAN: Analyze the task and create a research strategy
    2. GATHER: Use web_search and file_search to collect information
    3. ANALYZE: Use execute_code for any data analysis needs
    4. DELEGATE: Hand off specialized work to expert agents:
       - Complex writing tasks -> WritingSpecialist
       - Strategic planning -> PlanningSpecialist  
       - Data analysis -> DataAnalyst
    5. SYNTHESIZE: Combine all findings into comprehensive results
    
    Always explain your reasoning and decision-making process.
    Be autonomous but transparent about your approach.
    """,
    tools=[web_search, file_search, execute_code],
    handoffs=[
        handoff(agent=writing_agent),
        handoff(agent=planning_agent),
        handoff(agent=data_analyst_agent)
    ]
)

# ================== EXAMPLE SCENARIOS ==================


async def demo_autonomous_research():
    """Demonstrate autonomous research with LLM orchestration."""
    logger.info("\n=== Demo: Autonomous Research Orchestration ===")

    # Complex research task that requires multiple steps and specializations
    research_task = """
    I need a comprehensive analysis of implementing AI agents in customer service.
    This should include:
    1. Current market trends and technologies
    2. Implementation planning and timeline
    3. Data analysis of potential ROI
    4. A well-written executive summary
    
    Please research this thoroughly and provide a complete analysis.
    """

    logger.info(f"Research Task: {research_task}")

    try:
        # Let the LLM orchestrate the entire research process
        result = await Runner.run(
            research_orchestrator,
            research_task,
            max_turns=8  # Allow multiple turns for complex orchestration
        )

        logger.info("✅ Research completed successfully!")
        logger.info(f"Final Result: {result.final_output}")

        # Show the orchestration details
        logger.info(f"\nOrchestration Details:")
        logger.info(f"- Total turns: 8 (max allowed)")
        logger.info(f"- Tools used: Check the logs for tool usage")
        logger.info(f"- Handoffs: Check for any agent handoffs")

        return result

    except Exception as e:
        logger.error(f"Research orchestration failed: {e}")
        return None


async def demo_specialized_delegation():
    """Demonstrate how the orchestrator delegates to specialized agents."""
    logger.info("\n=== Demo: Specialized Agent Delegation ===")

    writing_task = """
    I have research data about Python programming trends. I need you to:
    1. Research additional context about Python's popularity
    2. Create a strategic plan for a Python training program
    3. Write a compelling blog post about Python's future
    
    Delegate the specialized tasks to the appropriate experts.
    """

    try:
        result = await Runner.run(
            research_orchestrator,
            writing_task,
            max_turns=6
        )

        logger.info("✅ Delegation demo completed!")
        logger.info(f"Result: {result.final_output}")

        return result

    except Exception as e:
        logger.error(f"Delegation demo failed: {e}")
        return None


async def demo_iterative_improvement():
    """Demonstrate iterative improvement through LLM orchestration."""
    logger.info("\n=== Demo: Iterative Improvement ===")

    improvement_task = """
    Create a research report about machine learning in healthcare.
    After creating the initial version:
    1. Critique your own work
    2. Identify areas for improvement
    3. Research additional data if needed
    4. Refine and improve the report
    
    Use your autonomous planning capabilities to create the best possible output.
    """

    try:
        result = await Runner.run(
            research_orchestrator,
            improvement_task,
            max_turns=10  # Allow more turns for iterative improvement
        )

        logger.info("✅ Iterative improvement completed!")
        logger.info(f"Final refined result: {result.final_output}")

        return result

    except Exception as e:
        logger.error(f"Iterative improvement failed: {e}")
        return None

# ================== MAIN EXECUTION ==================


async def main():
    """Run all LLM orchestration demonstrations."""
    print("🤖 LLM-Orchestrated Multi-Agent Systems Demo 🤖")
    print("\nThis demonstrates how LLMs can autonomously orchestrate complex tasks")
    print("using intelligence to plan, reason, and delegate to specialized agents.\n")

    # Run all demonstrations
    await demo_autonomous_research()
    await demo_specialized_delegation()
    await demo_iterative_improvement()

    print("\n" + "="*60)
    print("🎓 Key Takeaways from LLM Orchestration:")
    print("• LLMs can autonomously plan complex multi-step workflows")
    print("• Tools enable agents to gather data and take actions")
    print("• Handoffs allow delegation to specialized expert agents")
    print("• Iterative improvement through self-critique and refinement")
    print("• Open-ended tasks benefit from LLM intelligence and reasoning")
    print("• Monitor and iterate on prompts for better orchestration")

if __name__ == "__main__":
    asyncio.run(main())
