"""
🎯 OPENAI AGENTS SDK - EXPERT TECHNICAL QUIZ
120 Comprehensive Questions Covering ALL Agent Concepts + Tool Behavior Mastery

This quiz tests complete mastery of:
- Agent Architecture & Design Patterns
- Context Management & State Handling
- Structured Outputs (Strict vs Non-Strict)
- Tool Integration & Behavior Control (EXPANDED)
- Agent Composition & Delegation
- Guardrails & Security
- Lifecycle Hooks & Monitoring
- Dynamic Instructions & System Prompts
- Error Handling & Production Patterns
- Advanced Handoffs & Routing
- Tool Use Behavior Mastery (NEW)
- MCP Integration & Configuration

Difficulty Levels: Beginner (25) → Intermediate (35) → Advanced (35) → Expert (25)
"""

import asyncio
import time
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class QuestionDifficulty(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class QuestionCategory(str, Enum):
    AGENT_BASICS = "Agent Basics"
    CONTEXT_MANAGEMENT = "Context Management"
    STRUCTURED_OUTPUTS = "Structured Outputs"
    TOOL_INTEGRATION = "Tool Integration"
    TOOL_BEHAVIOR = "Tool Use Behavior"  # NEW CATEGORY
    HANDOFFS_DELEGATION = "Handoffs & Delegation"
    GUARDRAILS_SECURITY = "Guardrails & Security"
    LIFECYCLE_HOOKS = "Lifecycle & Hooks"
    DYNAMIC_INSTRUCTIONS = "Dynamic Instructions"
    ERROR_HANDLING = "Error Handling"
    PRODUCTION_PATTERNS = "Production Patterns"
    MCP_INTEGRATION = "MCP Integration"  # NEW CATEGORY


@dataclass
class QuizQuestion:
    id: int
    category: QuestionCategory
    difficulty: QuestionDifficulty
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    code_example: Optional[str] = None
    expert_insight: Optional[str] = None


@dataclass
class QuizResult:
    total_questions: int
    correct_answers: int
    percentage: float
    time_taken: float
    category_scores: Dict[str, Dict[str, int]]
    difficulty_scores: Dict[str, Dict[str, int]]
    mastery_level: str
    recommendations: List[str]


class AgentExpertQuiz:
    """Comprehensive OpenAI Agents SDK Expert Quiz Engine"""

    def __init__(self):
        self.questions = self._load_all_questions()
        self.user_answers: Dict[int, str] = {}
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def _load_all_questions(self) -> List[QuizQuestion]:
        """Load all 120 comprehensive questions including new tool behavior concepts"""
        questions = []

        # BEGINNER QUESTIONS (1-25) - Agent Basics & Fundamentals
        questions.extend([
            QuizQuestion(
                id=1, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="What is the primary purpose of the 'instructions' parameter in an Agent?",
                options=[
                    "A) To define the agent's name and description",
                    "B) To serve as the system prompt that guides the agent's behavior",
                    "C) To specify which tools the agent can use",
                    "D) To configure the model's temperature settings"
                ],
                correct_answer="B",
                explanation="The 'instructions' parameter serves as the system prompt that defines how the agent should behave and respond to user inputs.",
                expert_insight="Instructions can be static strings, callable functions, or async functions for dynamic behavior."
            ),

            QuizQuestion(
                id=2, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="Which method is used to execute an agent asynchronously?",
                options=[
                    "A) Agent.run()",
                    "B) Runner.execute()",
                    "C) Runner.run()",
                    "D) Agent.execute()"
                ],
                correct_answer="C",
                explanation="Runner.run() is the primary async method for executing agents in the OpenAI Agents SDK.",
                code_example="result = await Runner.run(agent, 'Hello, world!')"
            ),

            QuizQuestion(
                id=3, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.BEGINNER,
                question="What is the default value for tool_use_behavior in an Agent?",
                options=[
                    "A) 'stop_on_first_tool'",
                    "B) 'run_llm_again'",
                    "C) StopAtTools([])",
                    "D) None"
                ],
                correct_answer="B",
                explanation="The default tool_use_behavior is 'run_llm_again', which means the LLM processes tool results before generating the final output.",
                expert_insight="This default provides the richest, most contextual responses but uses more tokens."
            ),

            QuizQuestion(
                id=4, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.BEGINNER,
                question="What is the purpose of context in the OpenAI Agents SDK?",
                options=[
                    "A) To store conversation history",
                    "B) To provide shared mutable state across agent interactions",
                    "C) To configure model parameters",
                    "D) To define agent permissions"
                ],
                correct_answer="B",
                explanation="Context provides shared mutable state that can be accessed and modified by agents, tools, and guardrails throughout the execution.",
                code_example="@dataclass\nclass MyContext:\n    counter: int = 0\n    data: list = field(default_factory=list)"
            ),

            QuizQuestion(
                id=5, category=QuestionCategory.TOOL_INTEGRATION, difficulty=QuestionDifficulty.BEGINNER,
                question="How do you create a function tool in the OpenAI Agents SDK?",
                options=[
                    "A) Using the @tool decorator",
                    "B) Using the @function_tool decorator",
                    "C) Using the Tool() class constructor",
                    "D) Using the create_tool() function"
                ],
                correct_answer="B",
                explanation="The @function_tool decorator is used to convert regular Python functions into tools that agents can use.",
                code_example="@function_tool\nasync def my_tool(context: RunContextWrapper, param: str) -> str:\n    return f'Result: {param}'"
            ),

            QuizQuestion(
                id=6, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.BEGINNER,
                question="What happens when tool_use_behavior is set to 'stop_on_first_tool'?",
                options=[
                    "A) The agent stops after calling any tool",
                    "B) The first tool's output becomes the final output without LLM processing",
                    "C) Only the first tool in the list can be called",
                    "D) The agent stops if the first tool fails"
                ],
                correct_answer="B",
                explanation="With 'stop_on_first_tool', the first tool call's output is used directly as the final result without further LLM processing.",
                expert_insight="This is fastest for direct API responses but provides no LLM interpretation of results."
            ),

            QuizQuestion(
                id=7, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="Which parameter controls the LLM model used by an agent?",
                options=[
                    "A) model_name",
                    "B) llm",
                    "C) model",
                    "D) ai_model"
                ],
                correct_answer="C",
                explanation="The 'model' parameter specifies which LLM model implementation to use for the agent.",
                code_example="model=OpenAIChatCompletionsModel(openai_client=client, model='gpt-4o-mini')"
            ),

            QuizQuestion(
                id=8, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.BEGINNER,
                question="What type is StopAtTools in the OpenAI Agents SDK?",
                options=[
                    "A) A class that inherits from BaseModel",
                    "B) A TypedDict with stop_at_tool_names field",
                    "C) A regular dictionary",
                    "D) An enum"
                ],
                correct_answer="B",
                explanation="StopAtTools is a TypedDict that contains a stop_at_tool_names field with a list of tool names.",
                code_example="StopAtTools(stop_at_tool_names=['save_result', 'generate_report'])"
            ),

            QuizQuestion(
                id=9, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="What does Runner.run_sync() do?",
                options=[
                    "A) Runs multiple agents simultaneously",
                    "B) Provides a synchronous wrapper around Runner.run()",
                    "C) Synchronizes agent state across instances",
                    "D) Runs agents in strict mode only"
                ],
                correct_answer="B",
                explanation="Runner.run_sync() is a synchronous wrapper that internally calls the async Runner.run() method.",
                expert_insight="Use run_sync() when you need to call agents from non-async code."
            ),

            QuizQuestion(
                id=10, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.BEGINNER,
                question="What is required for a Pydantic model to work in strict mode?",
                options=[
                    "A) It must inherit from StrictBaseModel",
                    "B) It must use only basic types with concrete defaults",
                    "C) It must have a __strict__ = True attribute",
                    "D) It must use the @strict decorator"
                ],
                correct_answer="B",
                explanation="Strict mode requires basic types (str, int, bool, float) with concrete defaults, avoiding Union/Optional types.",
                code_example="class StrictModel(BaseModel):\n    name: str = ''\n    age: int = 0\n    model_config = ConfigDict(extra='forbid')"
            ),

            # Questions 11-25 continue with beginner level...
            QuizQuestion(
                id=11, category=QuestionCategory.MCP_INTEGRATION, difficulty=QuestionDifficulty.BEGINNER,
                question="What does MCP stand for in the OpenAI Agents SDK?",
                options=[
                    "A) Model Context Protocol",
                    "B) Multi-Client Platform",
                    "C) Message Control Protocol",
                    "D) Model Configuration Parameters"
                ],
                correct_answer="A",
                explanation="MCP stands for Model Context Protocol, which standardizes how AI models interact with external tools and data sources.",
                expert_insight="MCP enables seamless integration with external systems while maintaining security and consistency."
            ),

            QuizQuestion(
                id=12, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="What is the purpose of model_settings in an Agent?",
                options=[
                    "A) To specify which model to use",
                    "B) To configure model-specific parameters like temperature",
                    "C) To set the model's API key",
                    "D) To define model permissions"
                ],
                correct_answer="B",
                explanation="model_settings configures model-specific tuning parameters such as temperature, top_p, etc.",
                code_example="model_settings=ModelSettings(temperature=0.7, top_p=0.9)"
            ),

            QuizQuestion(
                id=13, category=QuestionCategory.TOOL_INTEGRATION, difficulty=QuestionDifficulty.BEGINNER,
                question="What is the first parameter of every function tool?",
                options=[
                    "A) agent: Agent",
                    "B) context: RunContextWrapper",
                    "C) self",
                    "D) input: str"
                ],
                correct_answer="B",
                explanation="Every function tool must have context: RunContextWrapper as its first parameter.",
                expert_insight="The context parameter provides access to shared state and agent information."
            ),

            QuizQuestion(
                id=14, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.BEGINNER,
                question="What is ToolsToFinalOutputFunction in the OpenAI Agents SDK?",
                options=[
                    "A) A decorator for tool functions",
                    "B) A TypeAlias for custom tool behavior functions",
                    "C) A class for tool validation",
                    "D) A configuration object"
                ],
                correct_answer="B",
                explanation="ToolsToFinalOutputFunction is a TypeAlias for callable functions that determine when to stop tool execution and what the final output should be.",
                expert_insight="This enables sophisticated custom logic for tool execution control."
            ),

            QuizQuestion(
                id=15, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="What does the handoff_description parameter do?",
                options=[
                    "A) Describes how handoffs work technically",
                    "B) Provides a description of the agent for use in handoffs",
                    "C) Sets the handoff timeout",
                    "D) Configures handoff permissions"
                ],
                correct_answer="B",
                explanation="handoff_description provides a human-readable description of what the agent does, used when the agent is a handoff target.",
                expert_insight="Good handoff descriptions help LLMs decide when to delegate to specific agents."
            ),

            QuizQuestion(
                id=16, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.BEGINNER,
                question="What happens to context between agent runs?",
                options=[
                    "A) Context is automatically reset",
                    "B) Context persists and maintains state",
                    "C) Context is copied to a new instance",
                    "D) Context becomes read-only"
                ],
                correct_answer="B",
                explanation="Context persists between agent runs, maintaining its state and allowing for stateful interactions.",
                expert_insight="This persistence enables multi-turn conversations and stateful workflows."
            ),

            QuizQuestion(
                id=17, category=QuestionCategory.TOOL_INTEGRATION, difficulty=QuestionDifficulty.BEGINNER,
                question="How do you add tools to an agent?",
                options=[
                    "A) agent.add_tool(tool)",
                    "B) agent.tools.append(tool)",
                    "C) tools=[tool1, tool2] in Agent constructor",
                    "D) agent.register_tool(tool)"
                ],
                correct_answer="C",
                explanation="Tools are added to an agent by passing a list to the tools parameter in the Agent constructor.",
                code_example="agent = Agent(name='MyAgent', tools=[tool1, tool2])"
            ),

            QuizQuestion(
                id=18, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="What is the return type of Runner.run()?",
                options=[
                    "A) str",
                    "B) RunResult",
                    "C) Agent",
                    "D) dict"
                ],
                correct_answer="B",
                explanation="Runner.run() returns a RunResult object containing the execution results and metadata.",
                expert_insight="RunResult contains final_output, new_items, and other execution details."
            ),

            QuizQuestion(
                id=19, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.BEGINNER,
                question="What does 'extra=\"forbid\"' do in a Pydantic model config?",
                options=[
                    "A) Prevents the model from being used",
                    "B) Forbids extra fields not defined in the model",
                    "C) Disables validation",
                    "D) Makes all fields required"
                ],
                correct_answer="B",
                explanation="extra='forbid' prevents additional fields not defined in the model schema from being accepted.",
                expert_insight="This is a security best practice that prevents unexpected data injection."
            ),

            QuizQuestion(
                id=20, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="Which of these is NOT a valid Agent parameter?",
                options=[
                    "A) instructions",
                    "B) tools",
                    "C) context",
                    "D) model"
                ],
                correct_answer="C",
                explanation="'context' is not an Agent parameter. Context is passed to Runner.run(), not the Agent constructor.",
                expert_insight="Context is runtime state, while Agent parameters define the agent's configuration."
            ),

            QuizQuestion(
                id=21, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.BEGINNER,
                question="What does ToolsToFinalOutputResult.is_final_output indicate?",
                options=[
                    "A) Whether the tool execution was successful",
                    "B) Whether this is the final output or if the LLM should run again",
                    "C) Whether the output is valid",
                    "D) Whether more tools should be called"
                ],
                correct_answer="B",
                explanation="is_final_output determines whether the current result should be the final output or if the LLM should process tool results further.",
                expert_insight="This is the key control mechanism in custom tool behavior functions."
            ),

            QuizQuestion(
                id=22, category=QuestionCategory.MCP_INTEGRATION, difficulty=QuestionDifficulty.BEGINNER,
                question="What is the purpose of MCPConfig.convert_schemas_to_strict?",
                options=[
                    "A) To validate MCP server connections",
                    "B) To attempt converting MCP schemas to strict-mode compatibility",
                    "C) To enforce security on MCP tools",
                    "D) To cache MCP tool definitions"
                ],
                correct_answer="B",
                explanation="convert_schemas_to_strict attempts to convert MCP tool schemas to be compatible with OpenAI's strict mode requirements.",
                expert_insight="This is a best-effort conversion; some complex schemas may not be convertible."
            ),

            QuizQuestion(
                id=23, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="What method returns all tools available to an agent?",
                options=[
                    "A) agent.tools",
                    "B) agent.get_tools()",
                    "C) agent.get_all_tools()",
                    "D) agent.list_tools()"
                ],
                correct_answer="C",
                explanation="get_all_tools() returns both function tools and MCP tools available to the agent.",
                expert_insight="This method combines tools from multiple sources into a unified list."
            ),

            QuizQuestion(
                id=24, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.BEGINNER,
                question="In a custom tool behavior function, what parameters does it receive?",
                options=[
                    "A) (agent, tools)",
                    "B) (context, tool_results)",
                    "C) (context, agent, tools)",
                    "D) (tool_results, final_output)"
                ],
                correct_answer="B",
                explanation="Custom tool behavior functions receive (context: RunContextWrapper, tool_results: list[FunctionToolResult]) as parameters.",
                code_example="async def custom_behavior(context: RunContextWrapper, tool_results: list) -> ToolsToFinalOutputResult:"
            ),

            QuizQuestion(
                id=25, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.BEGINNER,
                question="What does the reset_tool_choice parameter control?",
                options=[
                    "A) Whether tools can be called multiple times",
                    "B) Whether tool choice is reset to default after each call",
                    "C) Whether tools are validated before calling",
                    "D) Whether tool errors are reset"
                ],
                correct_answer="B",
                explanation="reset_tool_choice controls whether the agent's tool choice is reset to default behavior after each tool call.",
                expert_insight="Setting this to False can lead to tool call loops in some scenarios."
            ),
        ])

        # INTERMEDIATE QUESTIONS (26-60) - Deeper Understanding
        questions.extend([
            QuizQuestion(
                id=26, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What causes the error 'additionalProperties should not be set for object types'?",
                options=[
                    "A) Missing default values in Pydantic models",
                    "B) Union/Optional types generating anyOf schemas",
                    "C) Incorrect model configuration",
                    "D) Wrong Pydantic version"
                ],
                correct_answer="B",
                explanation="Union/Optional types generate anyOf schemas which are incompatible with OpenAI's strict mode requirements.",
                expert_insight="This is the most common strict mode compatibility issue in production."
            ),

            QuizQuestion(
                id=27, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the key difference between 'run_llm_again' and 'stop_on_first_tool' in terms of performance?",
                options=[
                    "A) run_llm_again is faster",
                    "B) stop_on_first_tool is faster but provides less context",
                    "C) No performance difference",
                    "D) stop_on_first_tool uses more memory"
                ],
                correct_answer="B",
                explanation="stop_on_first_tool is faster because it skips LLM processing of tool results, but provides no contextual interpretation.",
                expert_insight="Use stop_on_first_tool for direct API responses, run_llm_again for rich interactions."
            ),

            QuizQuestion(
                id=28, category=QuestionCategory.DYNAMIC_INSTRUCTIONS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you create dynamic instructions that change based on context?",
                options=[
                    "A) Use a string template with variables",
                    "B) Pass a callable function as instructions",
                    "C) Use the @dynamic_instructions decorator",
                    "D) Set instructions to None and use hooks"
                ],
                correct_answer="B",
                explanation="Dynamic instructions are created by passing a callable function that receives context and agent parameters.",
                code_example="def dynamic_instructions(context, agent):\n    return f'You are {agent.name}. User role: {context.context.role}'"
            ),

            QuizQuestion(
                id=29, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="When would you use StopAtTools instead of stop_on_first_tool?",
                options=[
                    "A) When you want to stop after any tool call",
                    "B) When you want selective control over which tools trigger stopping",
                    "C) When you want faster execution",
                    "D) When you want to prevent tool calls"
                ],
                correct_answer="B",
                explanation="StopAtTools allows you to specify exactly which tools should trigger stopping, providing selective control over execution flow.",
                expert_insight="Perfect for data pipelines where certain tools represent completion points."
            ),

            QuizQuestion(
                id=30, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the difference between mutable and immutable context patterns?",
                options=[
                    "A) Mutable allows state changes, immutable creates new instances",
                    "B) Mutable is faster, immutable is safer",
                    "C) Mutable uses dataclasses, immutable uses regular classes",
                    "D) No practical difference"
                ],
                correct_answer="A",
                explanation="Mutable context allows direct state modification, while immutable patterns create new context instances for each change.",
                expert_insight="Immutable patterns provide better debugging and state tracking but require more memory."
            ),

            # Continue with more intermediate questions (31-60)...
            QuizQuestion(
                id=31, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What happens if a custom tool behavior function returns is_final_output=False?",
                options=[
                    "A) The agent stops execution",
                    "B) The LLM continues processing and may call more tools",
                    "C) An error is raised",
                    "D) The last tool result becomes final output"
                ],
                correct_answer="B",
                explanation="When is_final_output=False, the LLM continues processing and may decide to call additional tools or generate a response.",
                expert_insight="This allows for sophisticated multi-step workflows with conditional stopping logic."
            ),

            QuizQuestion(
                id=32, category=QuestionCategory.MCP_INTEGRATION, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you access MCP tools in an agent?",
                options=[
                    "A) Through the mcp_servers parameter",
                    "B) They are automatically included with function tools",
                    "C) Using agent.get_mcp_tools()",
                    "D) Both A and C"
                ],
                correct_answer="D",
                explanation="MCP tools are configured via mcp_servers parameter and can be accessed using agent.get_mcp_tools().",
                expert_insight="MCP tools are fetched dynamically and combined with function tools at runtime."
            ),

            QuizQuestion(
                id=33, category=QuestionCategory.HANDOFFS_DELEGATION, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you convert an agent into a tool for other agents?",
                options=[
                    "A) agent.to_tool()",
                    "B) agent.as_tool(tool_name, description)",
                    "C) Tool.from_agent(agent)",
                    "D) function_tool(agent)"
                ],
                correct_answer="B",
                explanation="Use agent.as_tool(tool_name, description) to convert an agent into a tool callable by other agents.",
                expert_insight="This enables hierarchical agent architectures where agents can use other agents as tools."
            ),

            QuizQuestion(
                id=34, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the recommended pattern for API gateway agents?",
                options=[
                    "A) Use run_llm_again for rich responses",
                    "B) Use stop_on_first_tool for direct API responses",
                    "C) Use custom tool behavior for validation",
                    "D) Use StopAtTools for selective routing"
                ],
                correct_answer="B",
                explanation="API gateways benefit from stop_on_first_tool to provide direct, fast responses without LLM interpretation overhead.",
                expert_insight="This pattern minimizes latency and token usage for simple data retrieval scenarios."
            ),

            QuizQuestion(
                id=35, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you enable non-strict mode for flexible schemas?",
                options=[
                    "A) Set strict=False in Agent constructor",
                    "B) Use AgentOutputSchema(Model, strict_json_schema=False)",
                    "C) Add @non_strict decorator to the model",
                    "D) Set model_config strict=False"
                ],
                correct_answer="B",
                explanation="Non-strict mode is enabled by wrapping the model with AgentOutputSchema and setting strict_json_schema=False.",
                expert_insight="Non-strict mode allows Union types and dynamic schemas but is slower."
            ),

            # Continue with questions 36-60...
            QuizQuestion(
                id=36, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="In production data pipelines, which tool_use_behavior is most appropriate?",
                options=[
                    "A) run_llm_again for data interpretation",
                    "B) stop_on_first_tool for speed",
                    "C) StopAtTools to stop at save/export operations",
                    "D) Custom function for complex validation"
                ],
                correct_answer="C",
                explanation="Data pipelines benefit from StopAtTools to automatically stop when data is saved or exported, indicating completion.",
                expert_insight="This pattern ensures pipelines complete at the right stage without unnecessary processing."
            ),

            QuizQuestion(
                id=37, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What does the clone() method do?",
                options=[
                    "A) Creates an exact copy of the agent",
                    "B) Creates a new agent with modified parameters",
                    "C) Duplicates the agent's state",
                    "D) Creates a backup of the agent"
                ],
                correct_answer="B",
                explanation="clone() creates a new agent instance with specified parameters changed while keeping others the same.",
                code_example="new_agent = base_agent.clone(instructions='New instructions', temperature=0.9)"
            ),

            QuizQuestion(
                id=38, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the main advantage of custom tool behavior functions?",
                options=[
                    "A) They're faster than built-in behaviors",
                    "B) They provide maximum flexibility for complex workflow control",
                    "C) They're easier to implement",
                    "D) They use fewer tokens"
                ],
                correct_answer="B",
                explanation="Custom tool behavior functions allow sophisticated conditional logic for determining when and how to stop tool execution.",
                expert_insight="Use custom functions for complex workflows that require conditional stopping based on multiple factors."
            ),

            QuizQuestion(
                id=39, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="Which Pydantic v2 decorator is used for field validation?",
                options=[
                    "A) @validator",
                    "B) @field_validator with @classmethod",
                    "C) @validates",
                    "D) @field_check"
                ],
                correct_answer="B",
                explanation="Pydantic v2 uses @field_validator with @classmethod for field validation, replacing v1's @validator.",
                code_example="@field_validator('email')\n@classmethod\ndef validate_email(cls, v):\n    if '@' not in v:\n        raise ValueError('Invalid email')\n    return v"
            ),

            QuizQuestion(
                id=40, category=QuestionCategory.MCP_INTEGRATION, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the purpose of mcp_config in an Agent?",
                options=[
                    "A) To configure MCP server connections",
                    "B) To set MCP tool permissions",
                    "C) To configure MCP schema conversion and behavior",
                    "D) To cache MCP responses"
                ],
                correct_answer="C",
                explanation="mcp_config configures how MCP schemas are processed, including strict mode conversion attempts.",
                expert_insight="This allows fine-tuning of MCP integration behavior for different use cases."
            ),

            # Continue with more intermediate questions through 60...
            QuizQuestion(
                id=41, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What happens when you combine StopAtTools with multiple tool names?",
                options=[
                    "A) The agent stops only when all tools are called",
                    "B) The agent stops when any of the specified tools is called",
                    "C) Only the first tool in the list can trigger stopping",
                    "D) The tools are called in sequence"
                ],
                correct_answer="B",
                explanation="StopAtTools stops execution when ANY of the tools in the stop_at_tool_names list is called.",
                expert_insight="This provides flexible stopping conditions for workflows with multiple completion points."
            ),

            QuizQuestion(
                id=42, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you share state between multiple tool calls?",
                options=[
                    "A) Use global variables",
                    "B) Use the context object",
                    "C) Use return values",
                    "D) Use class attributes"
                ],
                correct_answer="B",
                explanation="The context object is the proper way to share state between tool calls and across agent interactions.",
                expert_insight="Context provides thread-safe state sharing in async environments."
            ),

            QuizQuestion(
                id=43, category=QuestionCategory.TOOL_INTEGRATION, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What happens if a function tool raises an exception?",
                options=[
                    "A) The agent stops immediately",
                    "B) The exception is passed to the LLM as tool output",
                    "C) The tool is retried automatically",
                    "D) The agent switches to a different tool"
                ],
                correct_answer="B",
                explanation="Tool exceptions are converted to error messages and passed to the LLM as tool output for handling.",
                expert_insight="The LLM can then decide how to handle the error or try alternative approaches."
            ),

            QuizQuestion(
                id=44, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you implement conditional stopping based on tool results content?",
                options=[
                    "A) Use StopAtTools with tool names",
                    "B) Use stop_on_first_tool",
                    "C) Use a custom tool behavior function that analyzes results",
                    "D) Use run_llm_again with special instructions"
                ],
                correct_answer="C",
                explanation="Custom tool behavior functions can analyze tool result content and implement sophisticated conditional stopping logic.",
                expert_insight="This enables stopping based on result content, not just which tool was called."
            ),

            QuizQuestion(
                id=45, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What does Runner.run_streamed() return?",
                options=[
                    "A) RunResult",
                    "B) RunResultStreaming",
                    "C) AsyncIterator[StreamEvent]",
                    "D) Stream[RunResult]"
                ],
                correct_answer="B",
                explanation="Runner.run_streamed() returns a RunResultStreaming object that provides access to streaming events.",
                expert_insight="Use .stream_events() to access the streaming events iterator."
            ),

            # Continue through question 60...
            QuizQuestion(
                id=46, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the best practice for interactive assistant agents?",
                options=[
                    "A) Use stop_on_first_tool for speed",
                    "B) Use run_llm_again for rich, contextual responses",
                    "C) Use StopAtTools for control",
                    "D) Use custom behavior for validation"
                ],
                correct_answer="B",
                explanation="Interactive assistants benefit from run_llm_again to provide rich, contextual responses that interpret and explain tool results.",
                expert_insight="This pattern provides the best user experience for conversational interfaces."
            ),

            QuizQuestion(
                id=47, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the correct way to handle enums in strict mode?",
                options=[
                    "A) Use Union[str, str, str] for options",
                    "B) Use Literal['option1', 'option2', 'option3']",
                    "C) Use Optional[Enum]",
                    "D) Use str with validation"
                ],
                correct_answer="B",
                explanation="Literal types work perfectly in strict mode and provide type-safe enumeration of allowed values.",
                code_example="status: Literal['pending', 'confirmed', 'shipped'] = 'pending'"
            ),

            QuizQuestion(
                id=48, category=QuestionCategory.HANDOFFS_DELEGATION, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you implement conditional handoffs?",
                options=[
                    "A) Use if statements in instructions",
                    "B) Create custom Handoff classes with condition logic",
                    "C) Use tool_use_behavior",
                    "D) Use guardrails"
                ],
                correct_answer="B",
                explanation="Custom Handoff classes can implement condition logic to determine when handoffs should occur.",
                expert_insight="This enables intelligent routing based on input content or context state."
            ),

            QuizQuestion(
                id=49, category=QuestionCategory.MCP_INTEGRATION, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How are MCP tools combined with function tools?",
                options=[
                    "A) They replace function tools",
                    "B) They are kept separate",
                    "C) They are combined into a unified tool list",
                    "D) They require special configuration"
                ],
                correct_answer="C",
                explanation="MCP tools and function tools are combined into a unified list accessible through get_all_tools().",
                expert_insight="This provides a seamless experience where agents can use tools from multiple sources."
            ),

            QuizQuestion(
                id=50, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the key consideration when choosing between different tool_use_behavior modes?",
                options=[
                    "A) Number of tools available",
                    "B) Model type being used",
                    "C) Balance between speed, control, and response richness",
                    "D) Context size limitations"
                ],
                correct_answer="C",
                explanation="The choice depends on balancing execution speed, workflow control needs, and desired response richness.",
                expert_insight="Consider your use case: API gateway (speed), data pipeline (control), or assistant (richness)."
            ),

            # Continue with questions 51-60...
            QuizQuestion(
                id=51, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you handle errors in custom tool behavior functions?",
                options=[
                    "A) Return is_final_output=True with error message",
                    "B) Raise an exception",
                    "C) Return is_final_output=False to continue",
                    "D) All of the above depending on error type"
                ],
                correct_answer="D",
                explanation="Error handling in custom tool behavior depends on the error type: fatal errors should stop (A), recoverable errors can continue (C), or raise exceptions for system errors (B).",
                expert_insight="Implement sophisticated error handling based on error severity and recovery possibilities."
            ),

            QuizQuestion(
                id=52, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the purpose of RunContextWrapper?",
                options=[
                    "A) To wrap the context for serialization",
                    "B) To provide a consistent interface for accessing context",
                    "C) To add validation to context access",
                    "D) To enable context caching"
                ],
                correct_answer="B",
                explanation="RunContextWrapper provides a consistent interface for accessing context across different parts of the SDK.",
                expert_insight="It abstracts context access and provides additional metadata about the run."
            ),

            QuizQuestion(
                id=53, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="When should you use non-strict schemas over strict schemas?",
                options=[
                    "A) For production applications",
                    "B) For performance-critical systems",
                    "C) For prototyping with dynamic/unknown data structures",
                    "D) For simple data extraction"
                ],
                correct_answer="C",
                explanation="Non-strict schemas are ideal for prototyping when data structure is unknown or highly dynamic.",
                expert_insight="Use non-strict for discovery, then migrate to strict for production."
            ),

            QuizQuestion(
                id=54, category=QuestionCategory.AGENT_BASICS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What is the purpose of the get_system_prompt() method?",
                options=[
                    "A) To retrieve the agent's instructions",
                    "B) To generate dynamic system prompts based on context",
                    "C) To validate system prompts",
                    "D) To cache system prompts"
                ],
                correct_answer="B",
                explanation="get_system_prompt() generates the actual system prompt, handling both static and dynamic instructions.",
                expert_insight="This method resolves callable instructions into actual prompt text."
            ),

            QuizQuestion(
                id=55, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the difference between hosted tools and function tools regarding tool_use_behavior?",
                options=[
                    "A) No difference",
                    "B) Hosted tools ignore tool_use_behavior settings",
                    "C) Function tools ignore tool_use_behavior settings",
                    "D) They use different behavior configurations"
                ],
                correct_answer="B",
                explanation="Hosted tools (like file search) are always processed by the LLM and ignore tool_use_behavior settings, which only affect function tools.",
                expert_insight="This is important for mixed tool environments where some tools need LLM processing."
            ),

            QuizQuestion(
                id=56, category=QuestionCategory.HANDOFFS_DELEGATION, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What information does handoff_description provide?",
                options=[
                    "A) Technical implementation details",
                    "B) Human-readable description for LLM decision-making",
                    "C) Performance characteristics",
                    "D) Security requirements"
                ],
                correct_answer="B",
                explanation="handoff_description provides human-readable information that helps LLMs decide when to delegate to specific agents.",
                expert_insight="Good descriptions include what the agent does and when to use it."
            ),

            QuizQuestion(
                id=57, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the main advantage of strict schemas over non-strict?",
                options=[
                    "A) More flexible data structures",
                    "B) Faster validation and OpenAI optimization",
                    "C) Support for Union types",
                    "D) Better error messages"
                ],
                correct_answer="B",
                explanation="Strict schemas provide faster validation and are optimized for OpenAI's function calling infrastructure.",
                expert_insight="Strict schemas can be 2-3x faster and use fewer tokens."
            ),

            QuizQuestion(
                id=58, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="How do you implement tool result caching in custom behavior functions?",
                options=[
                    "A) Use built-in caching",
                    "B) Store results in context and check before processing",
                    "C) Use external caching service",
                    "D) Caching is automatic"
                ],
                correct_answer="B",
                explanation="Implement caching by storing tool results in context and checking for cached results in custom behavior functions.",
                expert_insight="This pattern reduces redundant tool calls and improves performance."
            ),

            QuizQuestion(
                id=59, category=QuestionCategory.DYNAMIC_INSTRUCTIONS, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="Can dynamic instructions be async functions?",
                options=[
                    "A) No, only sync functions are supported",
                    "B) Yes, both sync and async functions are supported",
                    "C) Only async functions are supported",
                    "D) It depends on the model type"
                ],
                correct_answer="B",
                explanation="Dynamic instructions can be either synchronous or asynchronous functions, providing flexibility for different use cases.",
                code_example="async def async_instructions(context, agent):\n    data = await fetch_external_data()\n    return f'Instructions based on: {data}'"
            ),

            QuizQuestion(
                id=60, category=QuestionCategory.MCP_INTEGRATION, difficulty=QuestionDifficulty.INTERMEDIATE,
                question="What's the benefit of MCP schema conversion to strict mode?",
                options=[
                    "A) Better security",
                    "B) Faster execution and better OpenAI compatibility",
                    "C) More features available",
                    "D) Easier debugging"
                ],
                correct_answer="B",
                explanation="Converting MCP schemas to strict mode provides faster execution and better compatibility with OpenAI's optimized function calling.",
                expert_insight="This is a best-effort conversion that improves performance when successful."
            ),
        ])

        # ADVANCED QUESTIONS (61-95) - Expert-Level Understanding
        questions.extend([
            QuizQuestion(
                id=61, category=QuestionCategory.GUARDRAILS_SECURITY, difficulty=QuestionDifficulty.ADVANCED,
                question="What's the difference between InputGuardrail and OutputGuardrail?",
                options=[
                    "A) InputGuardrail validates user input, OutputGuardrail validates agent output",
                    "B) InputGuardrail is faster than OutputGuardrail",
                    "C) InputGuardrail is for security, OutputGuardrail is for compliance",
                    "D) No functional difference"
                ],
                correct_answer="A",
                explanation="InputGuardrail validates and potentially blocks user input before processing, while OutputGuardrail validates agent output before returning to user.",
                expert_insight="Use InputGuardrail for threat detection, OutputGuardrail for compliance and data leakage prevention."
            ),

            QuizQuestion(
                id=62, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution ordering with custom behavior functions?",
                options=[
                    "A) Tools are automatically ordered",
                    "B) Use dependency tracking in context with custom logic",
                    "C) Use StopAtTools with ordered names",
                    "D) Use separate agents for dependent operations"
                ],
                correct_answer="B",
                explanation="Implement dependency tracking in context and use custom tool behavior functions to enforce execution ordering based on dependencies.",
                expert_insight="This pattern ensures complex workflows execute in the correct sequence."
            ),

            QuizQuestion(
                id=63, category=QuestionCategory.LIFECYCLE_HOOKS, difficulty=QuestionDifficulty.ADVANCED,
                question="Which AgentHooks method is called when a tool execution fails?",
                options=[
                    "A) on_tool_error()",
                    "B) after_tool_call() with error parameter",
                    "C) on_agent_error()",
                    "D) Tool errors don't trigger hooks"
                ],
                correct_answer="A",
                explanation="on_tool_error() is specifically called when tool execution encounters an error.",
                expert_insight="This hook is crucial for monitoring and debugging tool failures in production."
            ),

            QuizQuestion(
                id=64, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement circuit breaker patterns with custom tool behavior?",
                options=[
                    "A) Use try-catch in tools",
                    "B) Track failure rates in context and stop execution when threshold exceeded",
                    "C) Use external circuit breaker libraries",
                    "D) Circuit breakers are automatic"
                ],
                correct_answer="B",
                explanation="Implement circuit breaker logic by tracking failure rates in context and using custom tool behavior to stop execution when failure thresholds are exceeded.",
                expert_insight="This prevents cascading failures and provides graceful degradation."
            ),

            QuizQuestion(
                id=65, category=QuestionCategory.PRODUCTION_PATTERNS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement retry logic for unreliable tools?",
                options=[
                    "A) Use try-catch in the tool function",
                    "B) Implement retry logic in AgentHooks",
                    "C) Use tool_use_behavior with custom function",
                    "D) Configure retry in model_settings"
                ],
                correct_answer="B",
                explanation="AgentHooks provide the appropriate lifecycle events to implement sophisticated retry logic.",
                expert_insight="Combine on_tool_error() with custom retry state in context for robust retry mechanisms."
            ),

            QuizQuestion(
                id=66, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement conditional tool execution based on previous results?",
                options=[
                    "A) Use if statements in tool functions",
                    "B) Use custom tool behavior to analyze result history and control continuation",
                    "C) Use separate agents for each condition",
                    "D) Use StopAtTools with dynamic names"
                ],
                correct_answer="B",
                explanation="Custom tool behavior functions can analyze the history of tool results and implement sophisticated conditional logic for continued execution.",
                expert_insight="This enables adaptive workflows that change behavior based on intermediate results."
            ),

            QuizQuestion(
                id=67, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you create a schema that works in both strict and non-strict modes?",
                options=[
                    "A) Use only basic types",
                    "B) Design with strict constraints, then wrap with AgentOutputSchema for non-strict",
                    "C) Use Union types with proper defaults",
                    "D) It's not possible"
                ],
                correct_answer="B",
                explanation="Design schemas with strict mode constraints, then use AgentOutputSchema wrapper to enable non-strict mode when needed.",
                expert_insight="This approach provides maximum compatibility and performance flexibility."
            ),

            QuizQuestion(
                id=68, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool result transformation pipelines?",
                options=[
                    "A) Transform results in tool functions",
                    "B) Use custom tool_use_behavior with transformation logic",
                    "C) Implement transformation in hooks",
                    "D) Use separate transformation agents"
                ],
                correct_answer="B",
                explanation="Custom tool_use_behavior functions can implement sophisticated result transformation pipelines before determining final output.",
                expert_insight="This pattern enables complex data processing workflows within agent execution."
            ),

            QuizQuestion(
                id=69, category=QuestionCategory.DYNAMIC_INSTRUCTIONS, difficulty=QuestionDifficulty.ADVANCED,
                question="How can dynamic instructions access agent execution history?",
                options=[
                    "A) Through the agent parameter",
                    "B) Through context.execution_history",
                    "C) Through context.context custom fields",
                    "D) History is not accessible"
                ],
                correct_answer="C",
                explanation="Execution history must be manually tracked in custom context fields, as it's not automatically provided.",
                expert_insight="Implement custom history tracking in context for sophisticated dynamic instruction patterns."
            ),

            QuizQuestion(
                id=70, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement load balancing across multiple tool instances?",
                options=[
                    "A) Use random selection",
                    "B) Implement load balancing logic in custom tool behavior with performance tracking",
                    "C) Use multiple tool definitions",
                    "D) Load balancing is automatic"
                ],
                correct_answer="B",
                explanation="Custom tool behavior functions can implement load balancing by tracking tool performance and distributing calls accordingly.",
                expert_insight="Track response times and success rates in context to enable intelligent load distribution."
            ),

            # Continue with more advanced questions through 95...
            QuizQuestion(
                id=71, category=QuestionCategory.HANDOFFS_DELEGATION, difficulty=QuestionDifficulty.ADVANCED,
                question="What's the most efficient way to implement agent routing based on input classification?",
                options=[
                    "A) Use multiple if-else statements in instructions",
                    "B) Create custom Handoff classes with classification logic",
                    "C) Use a separate classification agent",
                    "D) Use tool_use_behavior for routing"
                ],
                correct_answer="B",
                explanation="Custom Handoff classes with built-in classification logic provide the most efficient routing without additional LLM calls.",
                expert_insight="This pattern avoids the overhead of separate classification steps while maintaining clean separation of concerns."
            ),

            QuizQuestion(
                id=72, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool calls that modify agent behavior mid-execution?",
                options=[
                    "A) Modify the agent object directly",
                    "B) Use context to store behavior modifications and custom tool behavior to apply them",
                    "C) Return special control codes from tools",
                    "D) Use separate agents for different behaviors"
                ],
                correct_answer="B",
                explanation="Store behavior modifications in context, then use custom tool behavior functions to apply them during execution.",
                expert_insight="This pattern enables adaptive agent behavior based on runtime conditions."
            ),

            QuizQuestion(
                id=73, category=QuestionCategory.GUARDRAILS_SECURITY, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement cascading guardrails with different security levels?",
                options=[
                    "A) Use multiple agents with different guardrails",
                    "B) Implement conditional logic within guardrail validate() methods",
                    "C) Use guardrail inheritance",
                    "D) Configure guardrails in model_settings"
                ],
                correct_answer="B",
                explanation="Implement conditional logic within guardrail validate() methods based on context security levels.",
                expert_insight="This allows dynamic security enforcement based on user roles, content sensitivity, and risk scores."
            ),

            QuizQuestion(
                id=74, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution timeouts with custom behavior?",
                options=[
                    "A) Use asyncio.timeout in tool functions",
                    "B) Track execution time in context and stop via custom behavior",
                    "C) Use external timeout services",
                    "D) Timeouts are automatic"
                ],
                correct_answer="B",
                explanation="Track tool execution times in context and use custom tool behavior to enforce timeouts and stop execution when limits are exceeded.",
                expert_insight="This provides fine-grained control over execution time limits for different workflow stages."
            ),

            QuizQuestion(
                id=75, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.ADVANCED,
                question="What's the best pattern for implementing context versioning?",
                options=[
                    "A) Use context.version field with manual tracking",
                    "B) Implement immutable context with version history",
                    "C) Use separate context classes for each version",
                    "D) Context versioning is not supported"
                ],
                correct_answer="B",
                explanation="Immutable context patterns with version history provide the best debugging and rollback capabilities.",
                expert_insight="This pattern is essential for complex workflows where state rollback might be necessary."
            ),

            QuizQuestion(
                id=76, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement A/B testing for different tool execution strategies?",
                options=[
                    "A) Use random selection in tools",
                    "B) Implement strategy selection in custom tool behavior with tracking",
                    "C) Use separate agents for each strategy",
                    "D) A/B testing is not supported"
                ],
                correct_answer="B",
                explanation="Use custom tool behavior to implement strategy selection and tracking, enabling sophisticated A/B testing of different execution approaches.",
                expert_insight="This enables data-driven optimization of tool execution strategies."
            ),

            QuizQuestion(
                id=77, category=QuestionCategory.LIFECYCLE_HOOKS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement distributed tracing across multiple agents?",
                options=[
                    "A) Use agent names as trace IDs",
                    "B) Implement trace ID propagation through context",
                    "C) Use the built-in tracing system",
                    "D) Tracing is automatic"
                ],
                correct_answer="C",
                explanation="The OpenAI Agents SDK includes a built-in tracing system for distributed agent execution tracking.",
                expert_insight="Use trace_id and group_id in run configuration for comprehensive distributed tracing."
            ),

            QuizQuestion(
                id=78, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool result aggregation across multiple calls?",
                options=[
                    "A) Use global variables",
                    "B) Implement aggregation logic in custom tool behavior with context storage",
                    "C) Use external aggregation services",
                    "D) Aggregation is automatic"
                ],
                correct_answer="B",
                explanation="Custom tool behavior functions can implement sophisticated aggregation logic, storing intermediate results in context.",
                expert_insight="This enables complex data collection and analysis workflows within agent execution."
            ),

            QuizQuestion(
                id=79, category=QuestionCategory.PRODUCTION_PATTERNS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement circuit breaker patterns for external service calls?",
                options=[
                    "A) Use try-catch in tools",
                    "B) Implement circuit breaker logic in context with hooks",
                    "C) Use tool_use_behavior",
                    "D) Configure timeouts in model_settings"
                ],
                correct_answer="B",
                explanation="Implement circuit breaker state in context and use hooks to monitor and control service call patterns.",
                expert_insight="Track failure rates and implement exponential backoff using context state and hook lifecycle events."
            ),

            QuizQuestion(
                id=80, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution rollback on failure?",
                options=[
                    "A) Use database transactions",
                    "B) Track operations in context and implement rollback logic in custom behavior",
                    "C) Use external rollback services",
                    "D) Rollback is automatic"
                ],
                correct_answer="B",
                explanation="Track all operations in context and implement rollback logic in custom tool behavior functions to undo operations on failure.",
                expert_insight="This ensures data consistency in complex workflows with multiple side effects."
            ),

            # Continue with questions 81-95...
            QuizQuestion(
                id=81, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement schema evolution while maintaining backward compatibility?",
                options=[
                    "A) Use Union types for different versions",
                    "B) Implement version-aware schema selection",
                    "C) Use optional fields with defaults",
                    "D) Schema evolution is not supported"
                ],
                correct_answer="C",
                explanation="Use optional fields with sensible defaults to maintain backward compatibility while evolving schemas.",
                expert_insight="This approach works in both strict and non-strict modes when properly implemented."
            ),

            QuizQuestion(
                id=82, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution monitoring and metrics collection?",
                options=[
                    "A) Use external monitoring tools",
                    "B) Implement metrics collection in custom tool behavior with context tracking",
                    "C) Use logging statements",
                    "D) Monitoring is automatic"
                ],
                correct_answer="B",
                explanation="Custom tool behavior functions can collect detailed metrics about tool execution, storing them in context for analysis.",
                expert_insight="This enables real-time performance monitoring and optimization of tool usage patterns."
            ),

            QuizQuestion(
                id=83, category=QuestionCategory.DYNAMIC_INSTRUCTIONS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement instruction templates with dynamic variable substitution?",
                options=[
                    "A) Use string formatting in dynamic instructions",
                    "B) Use template engines like Jinja2",
                    "C) Implement custom template logic with context data",
                    "D) All of the above"
                ],
                correct_answer="D",
                explanation="All approaches are valid - choose based on complexity needs, from simple string formatting to sophisticated template engines.",
                expert_insight="Template engines provide the most flexibility for complex instruction generation patterns."
            ),

            QuizQuestion(
                id=84, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution caching with custom behavior?",
                options=[
                    "A) Cache in tool functions",
                    "B) Implement caching logic in custom tool behavior with hash-based keys",
                    "C) Use external caching service",
                    "D) Caching is automatic"
                ],
                correct_answer="B",
                explanation="Implement caching in custom tool behavior using hash-based keys of tool parameters and context state for efficient result reuse.",
                expert_insight="This pattern reduces external API calls and improves performance for repeated operations."
            ),

            QuizQuestion(
                id=85, category=QuestionCategory.HANDOFFS_DELEGATION, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement agent pools with automatic scaling?",
                options=[
                    "A) Use multiple agent instances",
                    "B) Implement pool management in custom Handoff classes",
                    "C) Use external orchestration",
                    "D) Automatic scaling is built-in"
                ],
                correct_answer="B",
                explanation="Custom Handoff classes can implement sophisticated pool management with automatic scaling based on load metrics.",
                expert_insight="Track performance metrics and queue lengths to implement intelligent scaling decisions."
            ),

            QuizQuestion(
                id=86, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution prioritization?",
                options=[
                    "A) Tools execute in definition order",
                    "B) Implement priority logic in custom tool behavior with context-based scheduling",
                    "C) Use separate agents for different priorities",
                    "D) Prioritization is automatic"
                ],
                correct_answer="B",
                explanation="Custom tool behavior can implement sophisticated prioritization logic based on context state, urgency, and resource availability.",
                expert_insight="This enables efficient resource utilization in complex workflows with competing demands."
            ),

            QuizQuestion(
                id=87, category=QuestionCategory.GUARDRAILS_SECURITY, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement rate limiting per user or context?",
                options=[
                    "A) Use external rate limiting services",
                    "B) Implement rate limiting logic in guardrails with context tracking",
                    "C) Rate limiting is automatic",
                    "D) Use model_settings for rate limiting"
                ],
                correct_answer="B",
                explanation="Implement rate limiting in guardrails using context to track usage patterns per user or session.",
                expert_insight="Combine with sliding window algorithms for sophisticated rate limiting patterns."
            ),

            QuizQuestion(
                id=88, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution batching for efficiency?",
                options=[
                    "A) Call tools individually",
                    "B) Implement batching logic in custom tool behavior with context accumulation",
                    "C) Use external batching services",
                    "D) Batching is automatic"
                ],
                correct_answer="B",
                explanation="Custom tool behavior can accumulate tool calls in context and execute them in batches for improved efficiency.",
                expert_insight="This pattern reduces API overhead and improves throughput for bulk operations."
            ),

            QuizQuestion(
                id=89, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.ADVANCED,
                question="What's the best pattern for implementing context inheritance hierarchies?",
                options=[
                    "A) Use class inheritance",
                    "B) Use composition with nested context objects",
                    "C) Use mixins for shared behavior",
                    "D) All approaches are valid depending on use case"
                ],
                correct_answer="D",
                explanation="Different patterns suit different needs: inheritance for is-a relationships, composition for has-a, mixins for shared behavior.",
                expert_insight="Choose based on your specific domain model and complexity requirements."
            ),

            QuizQuestion(
                id=90, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution sandboxing for security?",
                options=[
                    "A) Use external sandboxing",
                    "B) Implement security checks in custom tool behavior with context validation",
                    "C) Sandboxing is automatic",
                    "D) Use separate processes"
                ],
                correct_answer="B",
                explanation="Custom tool behavior can implement security checks and validation before tool execution, using context to track security state.",
                expert_insight="This provides fine-grained security control over tool execution in multi-tenant environments."
            ),

            QuizQuestion(
                id=91, category=QuestionCategory.LIFECYCLE_HOOKS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement custom metrics collection for business KPIs?",
                options=[
                    "A) Use external analytics tools",
                    "B) Implement KPI tracking in hooks with context aggregation",
                    "C) Use logging for metrics",
                    "D) Metrics collection is automatic"
                ],
                correct_answer="B",
                explanation="Use lifecycle hooks to collect business-specific metrics and aggregate them in context for KPI tracking.",
                expert_insight="This enables real-time business intelligence from agent interactions."
            ),

            QuizQuestion(
                id=92, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution dependency graphs?",
                options=[
                    "A) Tools execute independently",
                    "B) Implement dependency tracking in custom tool behavior with graph resolution",
                    "C) Use external workflow engines",
                    "D) Dependencies are automatic"
                ],
                correct_answer="B",
                explanation="Custom tool behavior can implement sophisticated dependency graph resolution, ensuring tools execute in the correct order based on dependencies.",
                expert_insight="This enables complex workflows with conditional execution paths and parallel processing."
            ),

            QuizQuestion(
                id=93, category=QuestionCategory.PRODUCTION_PATTERNS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement blue-green deployment for agent updates?",
                options=[
                    "A) Use version numbers in agent names",
                    "B) Implement version routing in handoffs with gradual rollout",
                    "C) Use external deployment tools",
                    "D) Blue-green deployment is not applicable"
                ],
                correct_answer="B",
                explanation="Implement version-aware routing in handoffs to gradually shift traffic from old to new agent versions.",
                expert_insight="This enables safe agent updates with rollback capabilities."
            ),

            QuizQuestion(
                id=94, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement tool execution audit trails?",
                options=[
                    "A) Use logging statements",
                    "B) Implement comprehensive audit tracking in custom tool behavior with context storage",
                    "C) Use external audit systems",
                    "D) Audit trails are automatic"
                ],
                correct_answer="B",
                explanation="Custom tool behavior can implement detailed audit tracking, storing execution history, parameters, and results in context.",
                expert_insight="This provides complete traceability for compliance and debugging purposes."
            ),

            QuizQuestion(
                id=95, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.ADVANCED,
                question="How do you implement schema-driven API generation from agent outputs?",
                options=[
                    "A) Use Pydantic's schema generation",
                    "B) Implement custom schema extraction",
                    "C) Use OpenAPI generation tools",
                    "D) All of the above"
                ],
                correct_answer="D",
                explanation="Multiple approaches work: Pydantic schemas, custom extraction, or OpenAPI tools - choose based on integration needs.",
                expert_insight="This enables automatic API documentation and client generation from agent schemas."
            ),
        ])

        # EXPERT QUESTIONS (96-120) - Master-Level Understanding
        questions.extend([
            QuizQuestion(
                id=96, category=QuestionCategory.PRODUCTION_PATTERNS, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement multi-tenant agent isolation with shared infrastructure?",
                options=[
                    "A) Use separate agent instances per tenant",
                    "B) Implement tenant isolation in context with security boundaries",
                    "C) Use external tenant management",
                    "D) Multi-tenancy is not supported"
                ],
                correct_answer="B",
                explanation="Implement tenant isolation using context-based security boundaries while sharing agent infrastructure for efficiency.",
                expert_insight="This pattern enables SaaS-style agent deployment with proper security isolation."
            ),

            QuizQuestion(
                id=97, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement distributed tool execution across multiple nodes?",
                options=[
                    "A) Use remote procedure calls",
                    "B) Implement distributed coordination in custom tool behavior with context synchronization",
                    "C) Use external orchestration platforms",
                    "D) Distributed execution is automatic"
                ],
                correct_answer="B",
                explanation="Implement distributed coordination using custom tool behavior to manage tool execution across multiple nodes with proper synchronization.",
                expert_insight="This enables horizontal scaling of tool execution while maintaining consistency."
            ),

            QuizQuestion(
                id=98, category=QuestionCategory.LIFECYCLE_HOOKS, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement distributed consensus for multi-agent decision making?",
                options=[
                    "A) Use voting mechanisms in hooks",
                    "B) Implement consensus algorithms in context with agent coordination",
                    "C) Use external consensus services",
                    "D) Consensus is automatic"
                ],
                correct_answer="B",
                explanation="Implement consensus algorithms (like Raft or PBFT) in context with hooks coordinating agent participation.",
                expert_insight="This enables reliable multi-agent systems with fault tolerance and consistency guarantees."
            ),

            QuizQuestion(
                id=99, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement quantum-resistant cryptography for tool communications?",
                options=[
                    "A) Use standard encryption",
                    "B) Implement post-quantum cryptographic algorithms in custom tool behavior",
                    "C) Quantum resistance is automatic",
                    "D) Not applicable to agent systems"
                ],
                correct_answer="B",
                explanation="Implement post-quantum cryptographic algorithms in custom tool behavior to secure tool communications against future quantum computing threats.",
                expert_insight="This future-proofs agent systems against quantum computing advances."
            ),

            QuizQuestion(
                id=100, category=QuestionCategory.GUARDRAILS_SECURITY, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement zero-trust security architecture for agent interactions?",
                options=[
                    "A) Use authentication in guardrails",
                    "B) Implement comprehensive security validation at every interaction point",
                    "C) Use external security services",
                    "D) Zero-trust is not applicable"
                ],
                correct_answer="B",
                explanation="Implement security validation at every agent interaction, tool call, and data access point using guardrails and context.",
                expert_insight="This ensures security even if individual components are compromised."
            ),

            QuizQuestion(
                id=101, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement self-healing tool execution with automatic recovery?",
                options=[
                    "A) Manual intervention for failures",
                    "B) Implement autonomous healing algorithms in custom tool behavior with failure detection",
                    "C) Use external monitoring tools",
                    "D) Self-healing is automatic"
                ],
                correct_answer="B",
                explanation="Implement autonomous healing algorithms in custom tool behavior that detect failures, diagnose root causes, and automatically apply recovery strategies.",
                expert_insight="This creates truly autonomous agent systems that can maintain themselves without human intervention."
            ),

            QuizQuestion(
                id=102, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement event sourcing for complete agent interaction history?",
                options=[
                    "A) Log all interactions",
                    "B) Implement event store with context state reconstruction",
                    "C) Use external event sourcing systems",
                    "D) Event sourcing is not supported"
                ],
                correct_answer="B",
                explanation="Implement event sourcing by storing all state changes as events and reconstructing context state from event history.",
                expert_insight="This enables complete auditability and time-travel debugging capabilities."
            ),

            QuizQuestion(
                id=103, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement formal verification for tool execution guarantees?",
                options=[
                    "A) Use testing and monitoring",
                    "B) Implement formal specification languages with automated verification in custom behavior",
                    "C) Manual verification",
                    "D) Formal verification is not applicable"
                ],
                correct_answer="B",
                explanation="Implement formal specification languages and automated verification tools in custom tool behavior to mathematically prove execution properties.",
                expert_insight="This provides the highest level of assurance for safety-critical tool execution."
            ),

            QuizQuestion(
                id=104, category=QuestionCategory.STRUCTURED_OUTPUTS, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement real-time schema migration during agent execution?",
                options=[
                    "A) Stop and restart agents",
                    "B) Implement version-aware schema handling with graceful migration",
                    "C) Use external migration tools",
                    "D) Real-time migration is not possible"
                ],
                correct_answer="B",
                explanation="Implement version-aware schema handling that can gracefully migrate between schema versions during execution.",
                expert_insight="This enables zero-downtime schema updates in production systems."
            ),

            QuizQuestion(
                id=105, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement differential privacy for tool result sanitization?",
                options=[
                    "A) Remove sensitive data manually",
                    "B) Implement differential privacy algorithms in custom tool behavior",
                    "C) Use external privacy tools",
                    "D) Differential privacy is not applicable"
                ],
                correct_answer="B",
                explanation="Implement differential privacy algorithms in custom tool behavior to add controlled noise to results while preserving utility and protecting individual privacy.",
                expert_insight="This enables privacy-preserving analytics and reporting from agent systems."
            ),

            QuizQuestion(
                id=106, category=QuestionCategory.DYNAMIC_INSTRUCTIONS, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement self-modifying agent instructions based on learning?",
                options=[
                    "A) Manual instruction updates",
                    "B) Implement learning algorithms that modify instruction generation logic",
                    "C) Use external ML systems",
                    "D) Self-modification is not supported"
                ],
                correct_answer="B",
                explanation="Implement learning algorithms in dynamic instruction functions that adapt based on performance feedback and outcomes.",
                expert_insight="This creates truly adaptive agents that improve their instructions over time."
            ),

            QuizQuestion(
                id=107, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement federated learning for collaborative tool optimization?",
                options=[
                    "A) Share tool updates directly",
                    "B) Implement federated learning protocols in custom tool behavior for privacy-preserving optimization",
                    "C) Use external federated learning platforms",
                    "D) Federated learning is not applicable"
                ],
                correct_answer="B",
                explanation="Implement federated learning protocols in custom tool behavior to collaboratively improve tool execution across multiple agent deployments without sharing sensitive data.",
                expert_insight="This enables collective intelligence while maintaining privacy and security boundaries."
            ),

            QuizQuestion(
                id=108, category=QuestionCategory.HANDOFFS_DELEGATION, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement agent swarm intelligence with emergent behavior?",
                options=[
                    "A) Use predefined coordination patterns",
                    "B) Implement swarm algorithms with local interaction rules leading to global behavior",
                    "C) Use external swarm platforms",
                    "D) Swarm intelligence is not supported"
                ],
                correct_answer="B",
                explanation="Implement swarm intelligence algorithms where simple local interaction rules between agents lead to complex emergent global behaviors.",
                expert_insight="This enables self-organizing agent systems that solve complex problems through collective intelligence."
            ),

            QuizQuestion(
                id=109, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement homomorphic encryption for privacy-preserving tool computation?",
                options=[
                    "A) Use external encryption services",
                    "B) Implement encryption/decryption in custom tool behavior with encrypted context",
                    "C) Encryption is automatic",
                    "D) Homomorphic encryption is not supported"
                ],
                correct_answer="B",
                explanation="Implement homomorphic encryption in custom tool behavior to enable computation on encrypted data while preserving privacy.",
                expert_insight="This enables privacy-preserving AI services where sensitive data never exists in plaintext."
            ),

            QuizQuestion(
                id=110, category=QuestionCategory.PRODUCTION_PATTERNS, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement chaos engineering for agent system resilience testing?",
                options=[
                    "A) Use external chaos tools",
                    "B) Implement controlled failure injection in hooks and context",
                    "C) Manual failure testing",
                    "D) Chaos engineering is not applicable"
                ],
                correct_answer="B",
                explanation="Implement controlled failure injection using hooks and context to test system resilience under various failure conditions.",
                expert_insight="This ensures agent systems can handle real-world failures gracefully."
            ),

            QuizQuestion(
                id=111, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement CRDT (Conflict-free Replicated Data Types) for distributed tool state?",
                options=[
                    "A) Use external CRDT libraries",
                    "B) Implement CRDT logic in custom tool behavior with automatic conflict resolution",
                    "C) Manual conflict resolution",
                    "D) CRDTs are not applicable"
                ],
                correct_answer="B",
                explanation="Implement CRDT algorithms in custom tool behavior to enable automatic conflict resolution in distributed tool execution.",
                expert_insight="This enables eventually consistent distributed tool execution without coordination overhead."
            ),

            QuizQuestion(
                id=112, category=QuestionCategory.CONTEXT_MANAGEMENT, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement temporal logic for context state verification?",
                options=[
                    "A) Use simple state checks",
                    "B) Implement temporal logic specifications with model checking",
                    "C) Use external verification tools",
                    "D) Temporal logic is not applicable"
                ],
                correct_answer="B",
                explanation="Implement temporal logic specifications to formally verify that context state transitions satisfy required temporal properties.",
                expert_insight="This ensures that agent systems maintain required invariants over time and across state transitions."
            ),

            QuizQuestion(
                id=113, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement Byzantine fault tolerance for tool consensus?",
                options=[
                    "A) Use voting mechanisms",
                    "B) Implement BFT algorithms in custom tool behavior with malicious tool detection",
                    "C) Use external BFT systems",
                    "D) BFT is not applicable"
                ],
                correct_answer="B",
                explanation="Implement Byzantine fault tolerance algorithms in custom tool behavior to handle potentially malicious or faulty tools in the system.",
                expert_insight="This ensures system integrity even when some tools behave maliciously or unpredictably."
            ),

            QuizQuestion(
                id=114, category=QuestionCategory.GUARDRAILS_SECURITY, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement secure multi-party computation for collaborative agent tasks?",
                options=[
                    "A) Share data directly between agents",
                    "B) Implement SMPC protocols for privacy-preserving collaborative computation",
                    "C) Use external SMPC services",
                    "D) SMPC is not applicable"
                ],
                correct_answer="B",
                explanation="Implement secure multi-party computation protocols to enable agents to collaborate on computations without revealing their private inputs.",
                expert_insight="This enables privacy-preserving collaboration between agents from different organizations or trust domains."
            ),

            QuizQuestion(
                id=115, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement tool execution with quantum computing integration?",
                options=[
                    "A) Use classical computing only",
                    "B) Implement quantum-classical hybrid execution in custom tool behavior",
                    "C) Quantum integration is automatic",
                    "D) Not applicable to current systems"
                ],
                correct_answer="B",
                explanation="Implement quantum-classical hybrid execution patterns in custom tool behavior to leverage quantum computing for specific computational tasks.",
                expert_insight="This enables next-generation agent systems that can leverage quantum advantages for specific problem domains."
            ),

            QuizQuestion(
                id=116, category=QuestionCategory.DYNAMIC_INSTRUCTIONS, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement instruction optimization based on performance feedback?",
                options=[
                    "A) Manual instruction tuning",
                    "B) Implement feedback loops with performance tracking in context",
                    "C) Use external optimization tools",
                    "D) Optimization is automatic"
                ],
                correct_answer="B",
                explanation="Implement feedback loops that track performance metrics and automatically adjust instructions based on results.",
                expert_insight="This enables self-improving agent systems that optimize over time."
            ),

            QuizQuestion(
                id=117, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement tool execution with neuromorphic computing integration?",
                options=[
                    "A) Use traditional computing only",
                    "B) Implement neuromorphic-classical hybrid execution in custom tool behavior",
                    "C) Neuromorphic integration is automatic",
                    "D) Not applicable to agent systems"
                ],
                correct_answer="B",
                explanation="Implement neuromorphic-classical hybrid execution patterns in custom tool behavior to leverage neuromorphic computing for specific tasks.",
                expert_insight="This enables energy-efficient agent systems that can leverage neuromorphic advantages for pattern recognition and learning tasks."
            ),

            QuizQuestion(
                id=118, category=QuestionCategory.PRODUCTION_PATTERNS, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement agent mesh networking with automatic discovery?",
                options=[
                    "A) Use service discovery protocols",
                    "B) Implement mesh coordination in handoffs with dynamic agent registration",
                    "C) Use external service mesh",
                    "D) Mesh networking is not supported"
                ],
                correct_answer="B",
                explanation="Implement mesh coordination where agents can dynamically discover and connect to other agents through intelligent handoff mechanisms.",
                expert_insight="This enables self-organizing agent networks that adapt to changing topologies."
            ),

            QuizQuestion(
                id=119, category=QuestionCategory.TOOL_BEHAVIOR, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement tool execution with edge computing optimization?",
                options=[
                    "A) Use cloud computing only",
                    "B) Implement edge-cloud hybrid execution in custom tool behavior with latency optimization",
                    "C) Edge optimization is automatic",
                    "D) Not applicable to agent systems"
                ],
                correct_answer="B",
                explanation="Implement edge-cloud hybrid execution patterns in custom tool behavior to optimize for latency and bandwidth constraints.",
                expert_insight="This enables responsive agent systems that can adapt to network conditions and computational constraints."
            ),

            QuizQuestion(
                id=120, category=QuestionCategory.LIFECYCLE_HOOKS, difficulty=QuestionDifficulty.EXPERT,
                question="How do you implement self-healing agent systems with automatic recovery?",
                options=[
                    "A) Manual intervention for failures",
                    "B) Implement autonomous healing algorithms with failure detection and recovery strategies",
                    "C) Use external monitoring tools",
                    "D) Self-healing is automatic"
                ],
                correct_answer="B",
                explanation="Implement autonomous healing algorithms that detect failures, diagnose root causes, and automatically apply recovery strategies.",
                expert_insight="This creates truly autonomous agent systems that can maintain themselves without human intervention."
            ),
        ])

        return questions

    def run_quiz(self, num_questions: Optional[int] = None, difficulty_filter: Optional[QuestionDifficulty] = None,
                 category_filter: Optional[QuestionCategory] = None, randomize: bool = True) -> QuizResult:
        """Run the comprehensive agent quiz with optional filtering"""

        # Filter questions based on criteria
        filtered_questions = self.questions

        if difficulty_filter:
            filtered_questions = [
                q for q in filtered_questions if q.difficulty == difficulty_filter]

        if category_filter:
            filtered_questions = [
                q for q in filtered_questions if q.category == category_filter]

        # Select questions
        if num_questions and num_questions < len(filtered_questions):
            if randomize:
                filtered_questions = random.sample(
                    filtered_questions, num_questions)
            else:
                filtered_questions = filtered_questions[:num_questions]

        if randomize:
            random.shuffle(filtered_questions)

        print("🎯 OPENAI AGENTS SDK - EXPERT TECHNICAL QUIZ")
        print("=" * 80)
        print(f"📊 Questions: {len(filtered_questions)}")
        print(
            f"🎯 Difficulty: {difficulty_filter.value if difficulty_filter else 'All Levels'}")
        print(
            f"📂 Category: {category_filter.value if category_filter else 'All Categories'}")
        print("⏱️  No time limit - Focus on accuracy and understanding")
        print("=" * 80)

        input("\nPress Enter to begin the quiz...")
        self.start_time = time.time()

        for i, question in enumerate(filtered_questions, 1):
            self._ask_question(i, len(filtered_questions), question)

        self.end_time = time.time()
        return self._calculate_results(filtered_questions)

    def _ask_question(self, current: int, total: int, question: QuizQuestion):
        """Ask a single question with comprehensive formatting"""
        print(f"\n{'='*20} QUESTION {current}/{total} {'='*20}")
        print(f"📂 Category: {question.category.value}")
        print(f"🔥 Difficulty: {question.difficulty.value}")
        print(f"🆔 ID: {question.id}")

        print(f"\n❓ {question.question}")

        # Show code example if present
        if question.code_example:
            print(f"\n💻 Code Example:")
            print(f"```python\n{question.code_example}\n```")

        # Show options
        print(f"\nOptions:")
        for option in question.options:
            print(f"   {option}")

        # Get user answer
        while True:
            answer = input(f"\nYour answer (A/B/C/D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                break
            print("Please enter A, B, C, or D")

        self.user_answers[question.id] = answer

        # Immediate feedback
        is_correct = answer == question.correct_answer
        if is_correct:
            print("✅ Correct!")
        else:
            print(f"❌ Wrong. Correct answer: {question.correct_answer}")

        print(f"\n💡 Explanation: {question.explanation}")

        if question.expert_insight:
            print(f"\n🎓 Expert Insight: {question.expert_insight}")

        print("-" * 80)

    def _calculate_results(self, questions: List[QuizQuestion]) -> QuizResult:
        """Calculate comprehensive quiz results with detailed analysis"""
        total_questions = len(questions)
        correct_answers = 0
        category_scores: Dict[str, Dict[str, int]] = {}
        difficulty_scores: Dict[str, Dict[str, int]] = {}

        # Calculate scores
        for question in questions:
            user_answer = self.user_answers.get(question.id, "")
            is_correct = user_answer == question.correct_answer

            if is_correct:
                correct_answers += 1

            # Category tracking
            cat = question.category.value
            if cat not in category_scores:
                category_scores[cat] = {"correct": 0, "total": 0}
            category_scores[cat]["total"] += 1
            if is_correct:
                category_scores[cat]["correct"] += 1

            # Difficulty tracking
            diff = question.difficulty.value
            if diff not in difficulty_scores:
                difficulty_scores[diff] = {"correct": 0, "total": 0}
            difficulty_scores[diff]["total"] += 1
            if is_correct:
                difficulty_scores[diff]["correct"] += 1

        percentage = (correct_answers / total_questions) * 100
        time_taken = (self.end_time or 0) - (self.start_time or 0)

        # Determine mastery level
        if percentage >= 95:
            mastery_level = "🏆 EXPERT MASTER"
        elif percentage >= 90:
            mastery_level = "🥇 EXPERT LEVEL"
        elif percentage >= 85:
            mastery_level = "🥈 ADVANCED+"
        elif percentage >= 80:
            mastery_level = "🥉 ADVANCED"
        elif percentage >= 75:
            mastery_level = "📚 INTERMEDIATE+"
        elif percentage >= 70:
            mastery_level = "📖 INTERMEDIATE"
        elif percentage >= 60:
            mastery_level = "🔄 DEVELOPING"
        else:
            mastery_level = "📚 NEEDS STUDY"

        # Generate recommendations
        recommendations = self._generate_recommendations(
            category_scores, difficulty_scores, percentage)

        return QuizResult(
            total_questions=total_questions,
            correct_answers=correct_answers,
            percentage=percentage,
            time_taken=time_taken,
            category_scores=category_scores,
            difficulty_scores=difficulty_scores,
            mastery_level=mastery_level,
            recommendations=recommendations
        )

    def _generate_recommendations(self, category_scores: Dict[str, Dict[str, int]], difficulty_scores: Dict[str, Dict[str, int]], percentage: float) -> List[str]:
        """Generate personalized study recommendations"""
        recommendations = []

        # Overall performance recommendations
        if percentage < 60:
            recommendations.append(
                "🔄 Complete review of OpenAI Agents SDK fundamentals required")
            recommendations.append(
                "📖 Start with basic Agent creation and Runner execution patterns")
        elif percentage < 75:
            recommendations.append(
                "📚 Focus on intermediate concepts and practical implementation")
            recommendations.append(
                "💻 Practice building multi-agent systems with handoffs")
        elif percentage < 85:
            recommendations.append(
                "🚀 Study advanced patterns like guardrails and lifecycle hooks")
            recommendations.append(
                "🏭 Focus on production deployment and monitoring patterns")
        elif percentage < 95:
            recommendations.append(
                "🎯 Master expert-level concepts like distributed systems patterns")
            recommendations.append(
                "🔬 Explore cutting-edge topics like formal verification and swarm intelligence")
        else:
            recommendations.append(
                "🎉 Outstanding mastery! Consider contributing to the community")
            recommendations.append(
                "🌟 Mentor others and explore research applications")

        # Category-specific recommendations
        weak_categories = []
        for category, scores in category_scores.items():
            cat_percentage = (scores["correct"] / scores["total"]) * 100
            if cat_percentage < 70:
                weak_categories.append(category)

        if weak_categories:
            recommendations.append(
                f"🎯 Focus on weak areas: {', '.join(weak_categories)}")

        # Difficulty-specific recommendations
        for difficulty, scores in difficulty_scores.items():
            diff_percentage = (scores["correct"] / scores["total"]) * 100
            if diff_percentage < 60:
                recommendations.append(
                    f"📖 Review {difficulty} level concepts thoroughly")

        return recommendations

    def show_results(self, result: QuizResult):
        """Display comprehensive quiz results"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE QUIZ RESULTS & ANALYSIS")
        print("=" * 80)

        # Overall performance
        print(
            f"🎯 Overall Score: {result.correct_answers}/{result.total_questions} ({result.percentage:.1f}%)")
        print(f"⏱️  Time Taken: {result.time_taken/60:.1f} minutes")
        print(
            f"⚡ Average per question: {result.time_taken/result.total_questions:.1f} seconds")
        print(f"🎖️  Mastery Level: {result.mastery_level}")

        # Category breakdown
        print(f"\n📈 CATEGORY PERFORMANCE:")
        for category, scores in result.category_scores.items():
            percentage = (scores["correct"] / scores["total"]) * 100
            status = "✅" if percentage >= 80 else "⚠️" if percentage >= 60 else "❌"
            print(
                f"   {status} {category}: {scores['correct']}/{scores['total']} ({percentage:.0f}%)")

        # Difficulty breakdown
        print(f"\n🔥 DIFFICULTY PERFORMANCE:")
        for difficulty, scores in result.difficulty_scores.items():
            percentage = (scores["correct"] / scores["total"]) * 100
            status = "✅" if percentage >= 80 else "⚠️" if percentage >= 60 else "❌"
            print(
                f"   {status} {difficulty}: {scores['correct']}/{scores['total']} ({percentage:.0f}%)")

        # Recommendations
        print(f"\n📚 PERSONALIZED RECOMMENDATIONS:")
        for i, rec in enumerate(result.recommendations, 1):
            print(f"   {i}. {rec}")

        # Next steps
        print(f"\n🎯 NEXT STEPS:")
        if result.percentage >= 90:
            print("   🚀 Ready for production OpenAI Agents SDK development")
            print("   🎯 Consider advanced topics like distributed agent systems")
            print("   🌟 Explore research applications and contribute to community")
        elif result.percentage >= 80:
            print("   📚 Review missed concepts and practice advanced patterns")
            print("   🏭 Focus on production deployment and monitoring")
            print("   🔄 Retake quiz focusing on weak areas")
        else:
            print("   📖 Comprehensive study of OpenAI Agents SDK documentation")
            print("   💻 Build practical projects to reinforce learning")
            print("   🔄 Retake quiz after additional study")

        print("\n" + "=" * 80)
        print("🎓 Quiz completed! Use this analysis to guide your continued learning.")
        print("=" * 80)


def main():
    """Main quiz execution with options"""
    quiz = AgentExpertQuiz()

    print("🎯 OPENAI AGENTS SDK - EXPERT TECHNICAL QUIZ")
    print("Choose your quiz mode:")
    print("1. Full Quiz (120 questions)")
    print("2. Quick Assessment (25 questions)")
    print("3. Category Focus")
    print("4. Difficulty Focus")
    print("5. Tool Behavior Focus (NEW)")

    choice = input("\nEnter your choice (1-5): ").strip()

    if choice == "1":
        result = quiz.run_quiz()
    elif choice == "2":
        result = quiz.run_quiz(num_questions=25, randomize=True)
    elif choice == "3":
        print("\nAvailable categories:")
        for i, category in enumerate(QuestionCategory, 1):
            print(f"{i}. {category.value}")
        cat_choice = int(input("Choose category (1-12): ")) - 1
        category = list(QuestionCategory)[cat_choice]
        result = quiz.run_quiz(category_filter=category)
    elif choice == "4":
        print("\nAvailable difficulties:")
        for i, difficulty in enumerate(QuestionDifficulty, 1):
            print(f"{i}. {difficulty.value}")
        diff_choice = int(input("Choose difficulty (1-4): ")) - 1
        difficulty = list(QuestionDifficulty)[diff_choice]
        result = quiz.run_quiz(difficulty_filter=difficulty)
    elif choice == "5":
        result = quiz.run_quiz(category_filter=QuestionCategory.TOOL_BEHAVIOR)
    else:
        print("Invalid choice. Running full quiz.")
        result = quiz.run_quiz()

    quiz.show_results(result)


if __name__ == "__main__":
    main()
