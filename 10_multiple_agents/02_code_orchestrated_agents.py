"""
02_code_orchestrated_agents.py

This module demonstrates code-orchestrated multi-agent systems where the flow
of agents is determined by code rather than LLM decisions. This provides more
deterministic, predictable, and cost-effective orchestration patterns.

Key Concepts:
- Structured outputs for decision making
- Agent chaining and sequential workflows
- Parallel agent execution with asyncio
- While loops with evaluator agents
- Deterministic orchestration patterns
"""

import asyncio
import logging
from typing import List, Dict, Any
from enum import Enum
from pydantic import BaseModel
from agents import Agent, Runner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================== STRUCTURED OUTPUT MODELS ==================


class TaskCategory(str, Enum):
    """Task categories for routing decisions."""
    RESEARCH = "research"
    WRITING = "writing"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    TECHNICAL = "technical"


class TaskClassification(BaseModel):
    """Structured output for task classification."""
    category: TaskCategory
    complexity: int  # 1-5 scale
    estimated_effort: str  # "low", "medium", "high"
    required_specialists: List[str]
    reasoning: str


class QualityAssessment(BaseModel):
    """Structured output for quality evaluation."""
    overall_score: int  # 1-10 scale
    criteria_scores: Dict[str, int]  # specific criteria ratings
    passes_threshold: bool
    improvement_suggestions: List[str]
    reasoning: str


class BlogPostStructure(BaseModel):
    """Structured output for blog post planning."""
    title: str
    outline: List[str]
    target_audience: str
    key_points: List[str]
    estimated_word_count: int

# ================== SPECIALIZED AGENTS ==================


# Task classifier agent
task_classifier = Agent(
    name="TaskClassifier",
    instructions="""
    You are a task classification specialist. Analyze incoming tasks and categorize them
    to determine the best routing and handling approach.
    
    Categories:
    - RESEARCH: Information gathering, investigation, analysis
    - WRITING: Content creation, editing, documentation
    - ANALYSIS: Data analysis, evaluation, assessment
    - PLANNING: Strategic planning, project management, scheduling
    - TECHNICAL: Code development, system design, troubleshooting
    
    Rate complexity 1-5 and effort as low/medium/high.
    Identify which specialists would be needed.
    """,
    output_type=TaskClassification
)

# Research specialist
research_agent = Agent(
    name="ResearchSpecialist",
    instructions="""
    You are a research specialist focused on gathering and synthesizing information.
    
    Your capabilities:
    - Literature review and information gathering
    - Source verification and fact-checking
    - Synthesis of multiple information sources
    - Identification of knowledge gaps
    
    Provide comprehensive, well-sourced research with clear conclusions.
    """
)

# Writing specialist
writing_agent = Agent(
    name="WritingSpecialist",
    instructions="""
    You are a professional writer and content creator.
    
    Your expertise:
    - Clear, engaging writing for various audiences
    - Content structure and organization
    - Tone and style adaptation
    - Editing and proofreading
    
    Create compelling, well-structured content that serves its intended purpose.
    """
)

# Analysis specialist
analysis_agent = Agent(
    name="AnalysisSpecialist",
    instructions="""
    You are a data analysis and evaluation expert.
    
    Your skills:
    - Statistical analysis and interpretation
    - Trend identification and pattern recognition
    - Comparative analysis and benchmarking
    - Insight generation and recommendations
    
    Provide clear, actionable insights based on thorough analysis.
    """
)

# Planning specialist
planning_agent = Agent(
    name="PlanningSpecialist",
    instructions="""
    You are a strategic planning and project management expert.
    
    Your expertise:
    - Strategic planning and roadmap development
    - Resource allocation and timeline estimation
    - Risk assessment and mitigation planning
    - Process optimization and workflow design
    
    Create detailed, actionable plans with clear deliverables and timelines.
    """
)

# Quality evaluator
quality_evaluator = Agent(
    name="QualityEvaluator",
    instructions="""
    You are a quality assessment specialist. Evaluate work quality across multiple criteria.
    
    Assessment criteria:
    - Accuracy and factual correctness
    - Completeness and thoroughness
    - Clarity and readability
    - Relevance and usefulness
    - Professional quality
    
    Rate each criterion 1-10 and provide overall assessment.
    Work passes if overall score >= 7 and no individual criterion < 6.
    """,
    output_type=QualityAssessment
)

# Blog post planner
blog_planner = Agent(
    name="BlogPlanner",
    instructions="""
    You are a blog content strategist. Create detailed outlines for blog posts.
    
    Consider:
    - Target audience needs and interests
    - SEO and engagement optimization
    - Logical content flow and structure
    - Key messages and takeaways
    
    Provide comprehensive outlines that writers can easily follow.
    """,
    output_type=BlogPostStructure
)

# ================== CODE ORCHESTRATION PATTERNS ==================


async def pattern_structured_routing():
    """Pattern 1: Use structured outputs to route tasks to appropriate agents."""
    logger.info("\n=== Pattern 1: Structured Task Routing ===")

    tasks = [
        "Write a comprehensive blog post about sustainable energy solutions",
        "Analyze market trends in the electric vehicle industry",
        "Create a 6-month roadmap for implementing AI in customer service",
        "Research the latest developments in quantum computing"
    ]

    results = []

    for task in tasks:
        logger.info(f"\n📋 Processing task: {task}")

        # Step 1: Classify the task
        classification_result = await Runner.run(task_classifier, task)
        classification = classification_result.final_output_as(
            TaskClassification)

        logger.info(f"🏷️ Task classified as: {classification.category.value}")
        logger.info(f"   Complexity: {classification.complexity}/5")
        logger.info(f"   Effort: {classification.estimated_effort}")

        # Step 2: Route to appropriate specialist based on classification
        if classification.category == TaskCategory.RESEARCH:
            agent = research_agent
        elif classification.category == TaskCategory.WRITING:
            agent = writing_agent
        elif classification.category == TaskCategory.ANALYSIS:
            agent = analysis_agent
        elif classification.category == TaskCategory.PLANNING:
            agent = planning_agent
        else:
            agent = analysis_agent  # Default fallback

        # Step 3: Execute with chosen specialist
        result = await Runner.run(agent, task)

        logger.info(f"✅ Task completed by {agent.name}")
        results.append({
            "task": task,
            "classification": classification,
            "agent": agent.name,
            "result": result.final_output
        })

    return results


async def pattern_sequential_chaining():
    """Pattern 2: Chain multiple agents in sequence for blog post creation."""
    logger.info("\n=== Pattern 2: Sequential Agent Chaining ===")

    topic = "The Future of Remote Work in the AI Era"

    # Chain: Planning -> Research -> Writing -> Quality Check
    logger.info(f"📝 Creating blog post about: {topic}")

    # Step 1: Plan the blog post structure
    logger.info("🎯 Step 1: Planning blog structure...")
    plan_result = await Runner.run(blog_planner, f"Plan a blog post about: {topic}")
    blog_plan = plan_result.final_output_as(BlogPostStructure)

    logger.info(f"   Title: {blog_plan.title}")
    logger.info(f"   Target audience: {blog_plan.target_audience}")
    logger.info(f"   Word count: {blog_plan.estimated_word_count}")

    # Step 2: Research the topic
    logger.info("🔍 Step 2: Researching topic...")
    research_prompt = f"""
    Research the topic: {topic}
    
    Focus on these key points from the plan:
    {', '.join(blog_plan.key_points)}
    
    Target audience: {blog_plan.target_audience}
    """
    research_result = await Runner.run(research_agent, research_prompt)

    # Step 3: Write the blog post
    logger.info("✍️ Step 3: Writing blog post...")
    writing_prompt = f"""
    Write a blog post based on this plan and research:
    
    PLAN:
    Title: {blog_plan.title}
    Outline: {blog_plan.outline}
    Target audience: {blog_plan.target_audience}
    Word count goal: {blog_plan.estimated_word_count}
    
    RESEARCH:
    {research_result.final_output}
    
    Create an engaging, well-structured blog post.
    """
    blog_result = await Runner.run(writing_agent, writing_prompt)

    # Step 4: Quality evaluation
    logger.info("🔍 Step 4: Quality evaluation...")
    evaluation_result = await Runner.run(quality_evaluator,
                                         f"Evaluate this blog post:\n\n{blog_result.final_output}")
    quality_assessment = evaluation_result.final_output_as(QualityAssessment)

    logger.info(f"   Overall score: {quality_assessment.overall_score}/10")
    logger.info(f"   Passes threshold: {quality_assessment.passes_threshold}")

    return {
        "plan": blog_plan,
        "research": research_result.final_output,
        "blog_post": blog_result.final_output,
        "quality_assessment": quality_assessment
    }


async def pattern_parallel_execution():
    """Pattern 3: Run multiple agents in parallel using asyncio.gather."""
    logger.info("\n=== Pattern 3: Parallel Agent Execution ===")

    # Research project that can be parallelized
    project_topic = "Impact of AI on Different Industries"

    # Define parallel research tasks
    research_tasks = [
        ("Healthcare AI Applications",
         "Research AI applications in healthcare industry"),
        ("Financial AI Solutions", "Research AI implementations in financial services"),
        ("Manufacturing AI Integration",
         "Research AI adoption in manufacturing sector"),
        ("Education AI Transformation", "Research how AI is transforming education"),
        ("Retail AI Innovation", "Research AI innovations in retail and e-commerce")
    ]

    logger.info(
        f"🚀 Running {len(research_tasks)} research tasks in parallel...")

    # Create coroutines for parallel execution
    async def research_task(topic: str, prompt: str) -> Dict[str, Any]:
        logger.info(f"   🔍 Starting research on: {topic}")
        result = await Runner.run(research_agent, prompt)
        logger.info(f"   ✅ Completed research on: {topic}")
        return {
            "topic": topic,
            "result": result.final_output
        }

    # Execute all research tasks in parallel
    start_time = asyncio.get_event_loop().time()
    research_results = await asyncio.gather(*[
        research_task(topic, prompt) for topic, prompt in research_tasks
    ])
    end_time = asyncio.get_event_loop().time()

    logger.info(
        f"⚡ Parallel execution completed in {end_time - start_time:.2f} seconds")

    # Synthesize results
    synthesis_prompt = f"""
    Synthesize research findings about {project_topic}.
    
    Research Results:
    """ + "\n\n".join([f"**{r['topic']}:**\n{r['result']}" for r in research_results])

    synthesis_result = await Runner.run(analysis_agent, synthesis_prompt)

    return {
        "individual_research": research_results,
        "synthesis": synthesis_result.final_output,
        "execution_time": end_time - start_time
    }


async def pattern_iterative_improvement():
    """Pattern 4: While loop with evaluator for iterative improvement."""
    logger.info("\n=== Pattern 4: Iterative Improvement Loop ===")

    task = "Write a technical explanation of blockchain technology for beginners"
    max_iterations = 3
    quality_threshold = 8

    current_content = None
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        logger.info(f"\n🔄 Iteration {iteration}/{max_iterations}")

        if current_content is None:
            # First iteration - create initial content
            logger.info("   ✍️ Creating initial content...")
            result = await Runner.run(writing_agent, task)
            current_content = result.final_output
        else:
            # Subsequent iterations - improve based on feedback
            logger.info("   🔧 Improving content based on feedback...")
            improvement_prompt = f"""
            Improve this content based on the previous evaluation feedback:
            
            CURRENT CONTENT:
            {current_content}
            
            IMPROVEMENT TASK:
            {task}
            
            Focus on addressing the specific improvement suggestions.
            """
            result = await Runner.run(writing_agent, improvement_prompt)
            current_content = result.final_output

        # Evaluate current content
        logger.info("   📊 Evaluating quality...")
        eval_result = await Runner.run(quality_evaluator,
                                       f"Evaluate this content:\n\n{current_content}")
        assessment = eval_result.final_output_as(QualityAssessment)

        logger.info(f"   Score: {assessment.overall_score}/10")
        logger.info(f"   Passes: {assessment.passes_threshold}")

        # Check if quality threshold is met
        if assessment.overall_score >= quality_threshold:
            logger.info(
                f"✅ Quality threshold reached! Score: {assessment.overall_score}/10")
            break
        elif iteration < max_iterations:
            logger.info(
                f"   📝 Needs improvement. Suggestions: {assessment.improvement_suggestions}")

    return {
        "final_content": current_content,
        "iterations": iteration,
        "final_assessment": assessment
    }

# ================== MAIN EXECUTION ==================


async def main():
    """Run all code orchestration pattern demonstrations."""
    print("⚙️ Code-Orchestrated Multi-Agent Systems Demo ⚙️")
    print("\nThis demonstrates deterministic orchestration patterns using code")
    print("to control agent flow, routing, and execution.\n")

    # Run all patterns
    try:
        logger.info("Starting orchestration pattern demonstrations...")

        routing_results = await pattern_structured_routing()
        logger.info(
            f"✅ Structured routing completed - processed {len(routing_results)} tasks")

        chaining_results = await pattern_sequential_chaining()
        logger.info("✅ Sequential chaining completed - blog post created")

        parallel_results = await pattern_parallel_execution()
        logger.info(
            f"✅ Parallel execution completed in {parallel_results['execution_time']:.2f}s")

        iterative_results = await pattern_iterative_improvement()
        logger.info(
            f"✅ Iterative improvement completed in {iterative_results['iterations']} iterations")

    except Exception as e:
        logger.error(f"Orchestration demo failed: {e}")

    print("\n" + "="*60)
    print("🎓 Key Takeaways from Code Orchestration:")
    print("• Structured outputs enable deterministic routing decisions")
    print("• Sequential chaining decomposes complex tasks into steps")
    print("• Parallel execution speeds up independent tasks")
    print("• Iterative loops enable quality-driven improvement")
    print("• Code orchestration provides predictable performance and cost")
    print("• Mix patterns based on your specific requirements")

if __name__ == "__main__":
    asyncio.run(main())
