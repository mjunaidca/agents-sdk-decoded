"""
03_hybrid_orchestration.py

This module demonstrates hybrid orchestration that combines LLM intelligence
with code control. This approach provides the flexibility of LLM decision-making
where needed while maintaining predictable control through code.

Key Concepts:
- Adaptive orchestration based on task complexity
- LLM intelligence for creative/strategic decisions
- Code control for operational/deterministic steps
- Dynamic routing based on context
- Failover and fallback mechanisms
"""

import asyncio
import logging
from typing import List, Dict, Any
from enum import Enum
from pydantic import BaseModel
from agents import Agent, Runner
from agents.handoffs import handoff

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================== MODELS FOR HYBRID ORCHESTRATION ==================


class OrchestrationMode(str, Enum):
    """Orchestration approach to use."""
    LLM_DRIVEN = "llm_driven"     # Let LLM make decisions
    CODE_DRIVEN = "code_driven"   # Use deterministic code flow
    HYBRID = "hybrid"             # Mix both approaches


class TaskComplexity(str, Enum):
    """Task complexity levels."""
    SIMPLE = "simple"       # Straightforward, predictable
    MODERATE = "moderate"   # Some ambiguity, requires judgment
    COMPLEX = "complex"     # High ambiguity, creative solution needed


class OrchestrationStrategy(BaseModel):
    """Strategy for orchestrating a specific task."""
    mode: OrchestrationMode
    reasoning: str
    confidence: float  # 0.0 to 1.0
    fallback_mode: OrchestrationMode
    estimated_steps: int


class TaskAnalysis(BaseModel):
    """Analysis of task for orchestration planning."""
    complexity: TaskComplexity
    creativity_required: bool
    domain_expertise_needed: List[str]
    can_be_decomposed: bool
    time_sensitivity: str  # "low", "medium", "high"
    orchestration_strategy: OrchestrationStrategy

# ================== ORCHESTRATION CONTROLLER ==================


orchestration_planner = Agent(
    name="OrchestrationPlanner",
    instructions="""
    You are an orchestration strategy planner. Analyze tasks and determine the best 
    approach for orchestrating their execution.
    
    Consider these factors:
    - Task complexity and ambiguity
    - Creativity vs. deterministic requirements
    - Available domain expertise
    - Time sensitivity and efficiency needs
    - Decomposition possibilities
    
    Orchestration modes:
    - LLM_DRIVEN: For creative, ambiguous, or strategic tasks requiring reasoning
    - CODE_DRIVEN: For predictable, well-defined, or efficiency-critical tasks
    - HYBRID: For tasks that benefit from both approaches
    
    Provide clear reasoning for your strategy choice and confidence level.
    """,
    output_type=TaskAnalysis
)

# ================== SPECIALIZED AGENTS ==================

# Creative strategist (for LLM-driven tasks)
creative_strategist = Agent(
    name="CreativeStrategist",
    instructions="""
    You are a creative strategist and innovation expert. Handle tasks requiring:
    - Creative thinking and ideation
    - Strategic planning with ambiguous requirements
    - Novel solution development
    - Cross-domain connections and insights
    
    Use your reasoning abilities to break down complex problems and develop
    innovative approaches. Be autonomous in your decision-making while
    explaining your thought process.
    """,
    tools=[],  # Add tools as needed
    handoffs=[]  # Will be configured dynamically
)

# Process executor (for code-driven tasks)
process_executor = Agent(
    name="ProcessExecutor",
    instructions="""
    You are a process execution specialist. Handle well-defined tasks with:
    - Clear step-by-step procedures
    - Predictable workflows
    - Standardized operations
    - Quality assurance checks
    
    Follow established patterns and procedures efficiently.
    Provide structured outputs that can be easily processed.
    """
)

# Hybrid coordinator (for mixed tasks)
hybrid_coordinator = Agent(
    name="HybridCoordinator",
    instructions="""
    You are a hybrid coordination specialist. You handle tasks that require both
    creative reasoning and systematic execution:
    - Strategic planning with tactical implementation
    - Creative ideation with structured development
    - Complex analysis with clear recommendations
    
    Balance creativity with efficiency, and provide both innovative insights
    and actionable steps.
    """
)

# Domain experts
research_expert = Agent(
    name="ResearchExpert",
    instructions="Research specialist focused on information gathering and analysis."
)

writing_expert = Agent(
    name="WritingExpert",
    instructions="Writing specialist for content creation and editing."
)

technical_expert = Agent(
    name="TechnicalExpert",
    instructions="Technical specialist for system design and implementation."
)

business_expert = Agent(
    name="BusinessExpert",
    instructions="Business specialist for strategy and commercial insights."
)

# ================== HYBRID ORCHESTRATION ENGINE ==================


class HybridOrchestrator:
    """Main orchestration engine that adapts approach based on task analysis."""

    def __init__(self):
        self.domain_experts = {
            "research": research_expert,
            "writing": writing_expert,
            "technical": technical_expert,
            "business": business_expert
        }

    async def analyze_task(self, task: str) -> TaskAnalysis:
        """Analyze a task to determine optimal orchestration strategy."""
        logger.info(f"🧠 Analyzing task for orchestration strategy...")

        analysis_result = await Runner.run(orchestration_planner, task)
        analysis = analysis_result.final_output_as(TaskAnalysis)

        logger.info(f"   Complexity: {analysis.complexity.value}")
        logger.info(
            f"   Strategy: {analysis.orchestration_strategy.mode.value}")
        logger.info(
            f"   Confidence: {analysis.orchestration_strategy.confidence:.2f}")

        return analysis

    async def execute_llm_driven(self, task: str, analysis: TaskAnalysis) -> Dict[str, Any]:
        """Execute task using LLM-driven orchestration."""
        logger.info("🤖 Executing with LLM-driven orchestration...")

        # Configure creative strategist with relevant experts
        available_experts = []
        for domain in analysis.domain_expertise_needed:
            if domain in self.domain_experts:
                available_experts.append(self.domain_experts[domain])

        # Configure handoffs dynamically
        creative_strategist.handoffs = [
            handoff(agent=expert) for expert in available_experts]

        # Let the LLM autonomously plan and execute
        enhanced_task = f"""
        Task: {task}
        
        Available domain experts: {[e.name for e in available_experts]}
        
        You have full autonomy to:
        1. Plan your approach strategically
        2. Delegate to domain experts as needed
        3. Iterate and refine based on results
        4. Synthesize final outcomes
        
        Use your creative and strategic thinking to deliver the best possible result.
        """

        result = await Runner.run(
            creative_strategist,
            enhanced_task,
            max_turns=analysis.orchestration_strategy.estimated_steps
        )

        return {
            "mode": "llm_driven",
            "result": result.final_output,
            "turns": analysis.orchestration_strategy.estimated_steps
        }

    async def execute_code_driven(self, task: str, analysis: TaskAnalysis) -> Dict[str, Any]:
        """Execute task using code-driven orchestration."""
        logger.info("⚙️ Executing with code-driven orchestration...")

        steps = []
        current_result = task

        # Step 1: Decompose task if possible
        if analysis.can_be_decomposed:
            logger.info("   📋 Step 1: Task decomposition...")
            decomposition_prompt = f"Break down this task into clear, actionable steps: {task}"
            decomp_result = await Runner.run(process_executor, decomposition_prompt)
            steps.append(("decomposition", decomp_result.final_output))
            current_result = decomp_result.final_output

        # Step 2: Execute with appropriate domain expert
        if analysis.domain_expertise_needed:
            for domain in analysis.domain_expertise_needed:
                if domain in self.domain_experts:
                    logger.info(f"   🎯 Step: {domain} expert execution...")
                    expert_result = await Runner.run(
                        self.domain_experts[domain],
                        f"Handle this {domain} task: {current_result}"
                    )
                    steps.append(
                        (f"{domain}_execution", expert_result.final_output))
                    current_result = expert_result.final_output

        # Step 3: Final synthesis
        logger.info("   🔄 Step: Final synthesis...")
        synthesis_prompt = f"""
        Synthesize and finalize results for: {task}
        
        Execution steps completed:
        {chr(10).join([f"{i+1}. {step[0]}: {step[1][:200]}..." for i, step in enumerate(steps)])}
        
        Provide final, complete result.
        """
        final_result = await Runner.run(process_executor, synthesis_prompt)

        return {
            "mode": "code_driven",
            "steps": steps,
            "result": final_result.final_output,
            "total_steps": len(steps) + 1
        }

    async def execute_hybrid(self, task: str, analysis: TaskAnalysis) -> Dict[str, Any]:
        """Execute task using hybrid orchestration."""
        logger.info("🔀 Executing with hybrid orchestration...")

        phases = []

        # Phase 1: Creative strategic planning (LLM-driven)
        logger.info("   🎨 Phase 1: Creative strategic planning...")
        strategy_prompt = f"""
        Develop a creative strategy for: {task}
        
        Consider:
        - Innovative approaches and possibilities
        - Strategic framework and vision
        - Key insights and opportunities
        - High-level action plan
        
        Focus on strategic thinking and creativity.
        """
        strategy_result = await Runner.run(creative_strategist, strategy_prompt)
        phases.append(("strategic_planning", strategy_result.final_output))

        # Phase 2: Systematic execution planning (Code-driven)
        logger.info("   📊 Phase 2: Systematic execution planning...")
        execution_plan_prompt = f"""
        Create detailed execution plan based on this strategy:
        
        STRATEGY:
        {strategy_result.final_output}
        
        ORIGINAL TASK:
        {task}
        
        Provide:
        - Specific action steps
        - Timeline and dependencies
        - Resource requirements
        - Quality checkpoints
        """
        execution_plan = await Runner.run(process_executor, execution_plan_prompt)
        phases.append(("execution_planning", execution_plan.final_output))

        # Phase 3: Domain expert implementation (Code-driven)
        logger.info("   🎯 Phase 3: Domain expert implementation...")
        expert_results = []

        for domain in analysis.domain_expertise_needed:
            if domain in self.domain_experts:
                expert_prompt = f"""
                Execute your part of this plan:
                
                OVERALL STRATEGY:
                {strategy_result.final_output}
                
                EXECUTION PLAN:
                {execution_plan.final_output}
                
                Focus on {domain}-specific implementation.
                """
                expert_result = await Runner.run(self.domain_experts[domain], expert_prompt)
                expert_results.append((domain, expert_result.final_output))

        phases.append(("expert_implementation", expert_results))

        # Phase 4: Creative synthesis and refinement (LLM-driven)
        logger.info("   ✨ Phase 4: Creative synthesis...")
        synthesis_prompt = f"""
        Synthesize all work into final deliverable:
        
        ORIGINAL TASK: {task}
        STRATEGY: {strategy_result.final_output}
        EXECUTION PLAN: {execution_plan.final_output}
        EXPERT RESULTS: {expert_results}
        
        Create final, polished result that meets all requirements.
        Apply creative insights to enhance quality and impact.
        """
        final_result = await Runner.run(creative_strategist, synthesis_prompt)
        phases.append(("creative_synthesis", final_result.final_output))

        return {
            "mode": "hybrid",
            "phases": phases,
            "result": final_result.final_output,
            "total_phases": len(phases)
        }

    async def orchestrate_task(self, task: str) -> Dict[str, Any]:
        """Main orchestration method with fallback handling."""
        logger.info(f"\n🎯 Orchestrating task: {task}")

        try:
            # Step 1: Analyze task
            analysis = await self.analyze_task(task)

            # Step 2: Execute with primary strategy
            primary_mode = analysis.orchestration_strategy.mode

            if primary_mode == OrchestrationMode.LLM_DRIVEN:
                result = await self.execute_llm_driven(task, analysis)
            elif primary_mode == OrchestrationMode.CODE_DRIVEN:
                result = await self.execute_code_driven(task, analysis)
            else:  # HYBRID
                result = await self.execute_hybrid(task, analysis)

            result["analysis"] = analysis
            result["primary_mode"] = primary_mode.value
            result["fallback_used"] = False

            return result

        except Exception as e:
            logger.warning(f"Primary orchestration failed: {e}")
            logger.info(
                f"Attempting fallback with {analysis.orchestration_strategy.fallback_mode.value}...")

            # Try fallback strategy
            try:
                if analysis.orchestration_strategy.fallback_mode == OrchestrationMode.CODE_DRIVEN:
                    result = await self.execute_code_driven(task, analysis)
                else:
                    result = await self.execute_llm_driven(task, analysis)

                result["analysis"] = analysis
                result["primary_mode"] = primary_mode.value
                result["fallback_used"] = True
                result["fallback_mode"] = analysis.orchestration_strategy.fallback_mode.value

                return result

            except Exception as fallback_error:
                logger.error(
                    f"Fallback orchestration also failed: {fallback_error}")
                return {
                    "mode": "error",
                    "error": str(fallback_error),
                    "analysis": analysis,
                    "fallback_used": True
                }

# ================== DEMONSTRATION SCENARIOS ==================


async def demo_adaptive_orchestration():
    """Demonstrate adaptive orchestration for different task types."""
    logger.info("\n=== Demo: Adaptive Orchestration ===")

    orchestrator = HybridOrchestrator()

    test_tasks = [
        # Simple, predictable task -> Code-driven
        "Convert this data into a standardized CSV format with proper headers",

        # Creative, strategic task -> LLM-driven
        "Develop an innovative marketing strategy for a new AI startup targeting small businesses",

        # Complex, mixed task -> Hybrid
        "Design and implement a comprehensive employee onboarding program that improves retention and productivity"
    ]

    results = []

    for task in test_tasks:
        logger.info(f"\n{'='*60}")
        result = await orchestrator.orchestrate_task(task)
        results.append(result)

        logger.info(
            f"✅ Task completed using {result.get('mode', 'unknown')} orchestration")
        if result.get('fallback_used'):
            logger.info(
                f"   (Fallback to {result.get('fallback_mode')} was used)")

    return results


async def demo_failover_resilience():
    """Demonstrate failover and resilience mechanisms."""
    logger.info("\n=== Demo: Failover and Resilience ===")

    orchestrator = HybridOrchestrator()

    # Task designed to potentially trigger fallback
    challenging_task = """
    Create a comprehensive digital transformation roadmap for a traditional 
    manufacturing company that includes AI integration, cloud migration, 
    workforce training, and change management strategy.
    """

    result = await orchestrator.orchestrate_task(challenging_task)

    logger.info(f"Result mode: {result.get('mode')}")
    logger.info(f"Fallback used: {result.get('fallback_used', False)}")

    return result

# ================== MAIN EXECUTION ==================


async def main():
    """Run hybrid orchestration demonstrations."""
    print("🔀 Hybrid Multi-Agent Orchestration Demo 🔀")
    print("\nThis demonstrates adaptive orchestration that combines LLM intelligence")
    print("with code control for optimal flexibility and predictability.\n")

    try:
        # Run demonstrations
        adaptive_results = await demo_adaptive_orchestration()
        logger.info(
            f"✅ Adaptive orchestration completed - {len(adaptive_results)} tasks")

        resilience_result = await demo_failover_resilience()
        logger.info("✅ Failover resilience demonstrated")

    except Exception as e:
        logger.error(f"Hybrid orchestration demo failed: {e}")

    print("\n" + "="*60)
    print("🎓 Key Takeaways from Hybrid Orchestration:")
    print("• Adaptive strategies based on task analysis and complexity")
    print("• LLM intelligence for creative and ambiguous tasks")
    print("• Code control for predictable and efficiency-critical tasks")
    print("• Dynamic routing with fallback mechanisms")
    print("• Best of both worlds: flexibility + predictability")
    print("• Resilient execution with error recovery")

if __name__ == "__main__":
    asyncio.run(main())
