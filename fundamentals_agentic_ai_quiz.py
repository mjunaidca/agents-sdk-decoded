"""
Fundamentals of Agentic AI Quiz
Based on OpenAI Agents SDK Documentation

Total Questions: 48 MCQs
Duration: 120 Minutes
Difficulty Level: Intermediate to Advanced

Quiz covers:
- OpenAI Agents SDK architecture and components
- Pydantic models and data validation
- Async programming patterns
- Prompt engineering and Chain-of-Thought
- Agent lifecycle and context management
- Tool integration and error handling
- Multi-agent workflows and handoffs
- Runner execution patterns
- Markdown syntax basics

Based on: https://openai.github.io/openai-agents-python/
"""

import asyncio
import time
from typing import List, Dict, Any


class AgenticAIQuiz:
    def __init__(self):
        self.questions = self._load_questions()
        self.start_time = None
        self.score = 0
        self.answers = []

    def _load_questions(self) -> List[Dict[str, Any]]:
        return [
            # Questions 1-8: Core SDK Architecture
            {
                "id": 1,
                "question": "You are building a customer service system where agents need to handle different types of requests (billing, technical, sales). Each request type requires different tools and expertise. You want to ensure proper handoff between specialized agents while maintaining conversation context. Which architectural approach best implements this requirement using the OpenAI Agents SDK?",
                "options": [
                    "A. Create a single general-purpose agent with all tools and use conditional logic in instructions",
                    "B. Use a coordinator agent with Handoff objects to route requests to specialized agents, maintaining context transfer",
                    "C. Create separate Runner instances for each request type with independent processing",
                    "D. Use multiple Tool decorators within a single agent and let the LLM decide which tools to use"
                ],
                "answer": "B",
                "explanation": "The coordinator pattern with Handoffs is the SDK's designed approach for multi-agent workflows, ensuring proper context transfer and specialization while maintaining conversation continuity.",
                "category": "Architecture"
            },
            {
                "id": 2,
                "question": "Your production system processes 1000+ user requests per hour using the OpenAI Agents SDK. Users complain about long wait times during peak hours when agents are performing complex multi-tool operations. You need to provide immediate feedback to users while maintaining system reliability. What implementation strategy addresses this requirement?",
                "options": [
                    "A. Use Runner.run_sync() with reduced max_turns to speed up processing",
                    "B. Implement streaming with Runner.run() to provide real-time feedback on agent progress and tool execution",
                    "C. Create multiple identical agents and load balance requests across them",
                    "D. Cache agent responses and return pre-computed results for similar queries"
                ],
                "answer": "B",
                "explanation": "Streaming with Runner.run() provides real-time user feedback through events like text_delta, tool_call_start, and tool_call_done, improving perceived performance even during complex operations.",
                "category": "Architecture"
            },
            {
                "id": 3,
                "question": "What happens when you call `Runner.run_sync()` with `max_turns=5` but the agent completes its task in 3 turns?",
                "options": [
                    "A. The method throws an error for unused turns",
                    "B. The method waits for 2 more user inputs to reach max_turns",
                    "C. The method returns immediately after the agent completes its task",
                    "D. The method continues running until max_turns is reached"
                ],
                "answer": "C",
                "explanation": "Runner.run_sync() returns as soon as the agent completes its task, even if fewer than max_turns have been used. max_turns is a ceiling, not a requirement.",
                "category": "Runner"
            },
            {
                "id": 4,
                "question": "You're developing a financial analysis agent that needs to be deployed across different environments (development, staging, production) with different model configurations and API endpoints. The agent's core logic and tools remain the same, but you need to easily switch between gpt-3.5-turbo for development and gpt-4o for production. How should you structure your Agent initialization to support this requirement?",
                "options": [
                    "A. Hard-code different model names in separate Agent classes for each environment",
                    "B. Create environment-specific configuration files and initialize Agent with dynamic model and settings parameters",
                    "C. Use Agent.clone() to create copies with different models after initial creation",
                    "D. Create separate tools for each environment and let the agent choose which to use"
                ],
                "answer": "B",
                "explanation": "Environment-specific configuration allows flexible Agent initialization with different models and settings while maintaining code reusability across deployments.",
                "category": "Agent"
            },
            {
                "id": 5,
                "question": "You're building a data analysis agent that needs to access multiple external APIs (weather, stock prices, news feeds). Each API has different authentication requirements, rate limits, and response formats. You want to ensure that if one API call fails, the agent can provide meaningful feedback and potentially use alternative data sources. How should you implement these API integrations?",
                "options": [
                    "A. Create a single tool function that handles all API calls with internal routing logic",
                    "B. Implement separate @function_tool decorated functions for each API with proper error handling and return structured error messages",
                    "C. Use direct HTTP calls within agent instructions without tool decoration",
                    "D. Create a single generic 'api_call' tool that accepts any URL and parameters"
                ],
                "answer": "B",
                "explanation": "Separate tool functions provide clear separation of concerns, proper error handling per API, and structured responses that allow the agent to understand and react to specific failure scenarios.",
                "category": "Tools"
            },
            {
                "id": 6,
                "question": "In a Handoff scenario, what information is typically passed between agents?",
                "options": [
                    "A. Only the current user message",
                    "B. Complete conversation history, context, and handoff-specific instructions",
                    "C. Agent configuration and model settings only",
                    "D. Tool definitions and execution results only"
                ],
                "answer": "B",
                "explanation": "Handoffs transfer comprehensive context including conversation history, current state, and specific instructions for the receiving agent to maintain continuity.",
                "category": "Handoffs"
            },
            {
                "id": 7,
                "question": "You have an agent that processes legal documents and needs to maintain different conversation contexts for different clients simultaneously. Each client's conversation should be isolated from others, but you want to reuse the same agent configuration (instructions, tools, model settings) for efficiency. What's the best approach to implement this multi-tenant scenario?",
                "options": [
                    "A. Create completely separate Agent instances for each client to ensure isolation",
                    "B. Use Agent.clone() to create instances with the same configuration but independent conversation states",
                    "C. Use a single Agent instance and manage client context manually in tool functions",
                    "D. Create different instruction sets for each client within the same Agent instance"
                ],
                "answer": "B",
                "explanation": "Agent.clone() provides the perfect solution for multi-tenant scenarios - same configuration and capabilities but completely isolated conversation states for each client.",
                "category": "Agent"
            },
            {
                "id": 8,
                "question": "Which component is responsible for managing the agent execution loop and message flow?",
                "options": [
                    "A. Agent",
                    "B. Tool",
                    "C. Runner",
                    "D. Context"
                ],
                "answer": "C",
                "explanation": "The Runner is responsible for managing the agent execution loop, orchestrating message flow, tool calls, and maintaining conversation state.",
                "category": "Runner"
            },

            # Questions 9-16: Pydantic Models and Data Validation
            {
                "id": 9,
                "question": "You're building a travel booking agent that needs to process complex reservation requests. Users provide details like departure/arrival cities, dates, passenger information, and preferences. The LLM sometimes provides invalid dates (like February 30th), missing required fields, or incorrectly formatted data. You need to ensure data quality while providing helpful error messages back to the agent. How should you implement the booking tool?",
                "options": [
                    "A. Use basic Python dictionaries and validate manually within the tool function",
                    "B. Create a comprehensive Pydantic model with field validators, custom validation logic, and return structured error responses",
                    "C. Accept all inputs as strings and parse them manually within the tool",
                    "D. Use simple type hints without validation and let the external booking API handle validation"
                ],
                "answer": "B",
                "explanation": "Pydantic models with validators provide automatic JSON schema generation for the LLM, comprehensive validation, and structured error responses that help the agent understand and correct issues.",
                "category": "Pydantic"
            },
            {
                "id": 10,
                "question": "Your e-commerce agent uses a product search tool that accepts a Pydantic model with fields like category, price_range, brand, and color. During testing, you notice that when the LLM provides an invalid price_range (like 'expensive' instead of a numeric range), the tool execution fails and the agent gets confused. What's the best way to handle this scenario while maintaining a good user experience?",
                "options": [
                    "A. Remove Pydantic validation to prevent errors",
                    "B. Catch validation errors, log them, and return a user-friendly error message that guides the agent on correct format",
                    "C. Let the LLM retry automatically until it provides valid input",
                    "D. Use default values for all invalid fields"
                ],
                "answer": "B",
                "explanation": "Proper error handling with meaningful messages allows the agent to understand what went wrong and adjust its approach, maintaining conversation flow while ensuring data quality.",
                "category": "Pydantic"
            },
            {
                "id": 11,
                "question": "You're designing a content management tool that can accept either a simple text string or a complex content object with metadata (title, body, tags, author, publish_date). Some use cases only need simple text, while others require full metadata. How should you structure the Pydantic model to handle both scenarios elegantly?",
                "options": [
                    "A. Create separate tools for simple and complex content creation",
                    "B. Use Optional fields with defaults: content: str, title: Optional[str] = None, tags: Optional[List[str]] = []",
                    "C. Accept everything as a single string and parse it internally",
                    "D. Force all inputs to use the complete metadata structure"
                ],
                "answer": "B",
                "explanation": "Optional fields with sensible defaults provide flexibility for both simple and complex use cases while maintaining type safety and clear schema documentation for the LLM.",
                "category": "Pydantic"
            },
            {
                "id": 12,
                "question": "What is the recommended pattern for handling complex nested data in tool parameters?",
                "options": [
                    "A. Use dictionaries with dynamic keys",
                    "B. Define nested Pydantic models for structured validation",
                    "C. Use JSON strings that are parsed manually",
                    "D. Avoid complex data structures in tools"
                ],
                "answer": "B",
                "explanation": "Nested Pydantic models provide structured validation, clear schemas for the LLM, and maintainable code for complex data structures.",
                "category": "Pydantic"
            },
            {
                "id": 13,
                "question": "You're building a data analytics agent that processes user queries about sales data. The tool needs to accept flexible query parameters like date ranges, product categories, regions, and aggregation types. Users might specify 'last quarter', 'Q3 2023', or '2023-07-01 to 2023-09-30' for dates. How should you design the Pydantic model to handle this flexibility while ensuring proper validation?",
                "options": [
                    "A. Accept all parameters as strings and parse them manually in the tool function",
                    "B. Use Field() with custom validators to parse and normalize different date formats, with clear descriptions for the LLM",
                    "C. Force users to use only specific date formats",
                    "D. Create separate parameters for each possible date format"
                ],
                "answer": "B",
                "explanation": "Field() with custom validators allows flexible input formats while ensuring normalized, validated data. Clear descriptions help the LLM understand acceptable formats.",
                "category": "Pydantic"
            },
            {
                "id": 14,
                "question": "You're developing a task management agent that handles project assignments. The tool needs to accept a list of team members, where each member has a name, role, email, and optional skills. The LLM sometimes provides incomplete member information or invalid email formats. How should you structure this for robust validation?",
                "options": [
                    "A. Use a simple list of strings for member names only",
                    "B. Create a TeamMember Pydantic model with email validation, then use List[TeamMember] in the tool",
                    "C. Accept a dictionary with flexible keys and validate manually",
                    "D. Use List[Dict[str, Any]] to accept any structure"
                ],
                "answer": "B",
                "explanation": "A nested TeamMember model with validation (like email format checking) ensures data quality for each list item, providing clear error messages for specific validation failures.",
                "category": "Pydantic"
            },
            {
                "id": 15,
                "question": "How does Pydantic model validation integrate with the LLM's tool calling mechanism?",
                "options": [
                    "A. Validation occurs after the LLM receives the tool output",
                    "B. The LLM receives the JSON schema and validation occurs before tool execution",
                    "C. Validation is optional and only used for debugging",
                    "D. Pydantic models are not integrated with LLM tool calling"
                ],
                "answer": "B",
                "explanation": "The LLM receives the JSON schema generated from Pydantic models, helping it provide correct arguments. Validation then occurs before tool execution.",
                "category": "Pydantic"
            },
            {
                "id": 16,
                "question": "What is the best practice for returning data from a tool function?",
                "options": [
                    "A. Return raw strings for simplicity",
                    "B. Return Pydantic models or structured data that serializes well",
                    "C. Return binary data for efficiency",
                    "D. Return None to minimize response size"
                ],
                "answer": "B",
                "explanation": "Returning structured data (like Pydantic models) ensures consistent, predictable output that the LLM can reliably interpret and reason about.",
                "category": "Pydantic"
            },

            # Questions 17-24: Async Programming and Execution Patterns
            {
                "id": 17,
                "question": "You're building a real-time customer support system where multiple agents handle different aspects of user queries simultaneously. Users expect to see typing indicators, tool execution progress, and immediate responses as agents work on their requests. The system needs to handle 100+ concurrent conversations efficiently. Which implementation approach best meets these requirements?",
                "options": [
                    "A. Use Runner.run_sync() for each conversation in separate threads for parallel processing",
                    "B. Implement async/await with Runner.run() streaming, handling multiple conversations with asyncio.gather() or create_task()",
                    "C. Process conversations sequentially to avoid concurrency issues",
                    "D. Use multiprocessing to handle each conversation in separate processes"
                ],
                "answer": "B",
                "explanation": "Async streaming with proper asyncio concurrency patterns provides real-time feedback while efficiently handling many simultaneous conversations without blocking operations.",
                "category": "Async"
            },
            {
                "id": 18,
                "question": "Your medical diagnosis agent streams responses to doctors in real-time. During a consultation, the agent uses multiple tools: patient_history_lookup, symptom_analyzer, and treatment_recommender. The doctor needs to see each step as it happens, including when tools start executing, their progress, and when they complete. However, sometimes tool calls fail due to database timeouts. How should you implement the streaming and error handling?",
                "options": [
                    "A. Use basic streaming and ignore tool execution details",
                    "B. Handle text_delta, tool_call_start, tool_call_done events with try/except around both async iteration and individual event processing",
                    "C. Only stream final results to avoid complexity",
                    "D. Use synchronous processing to avoid streaming complications"
                ],
                "answer": "B",
                "explanation": "Comprehensive event handling with proper error management provides real-time visibility into tool execution while gracefully handling failures that could occur during streaming.",
                "category": "Async"
            },
            {
                "id": 19,
                "question": "What is the correct pattern for handling errors in async agent execution?",
                "options": [
                    "A. Use try/except only around the initial run() call",
                    "B. Ignore errors to prevent blocking",
                    "C. Use try/except around both the async iteration and individual event processing",
                    "D. Errors are automatically handled by the SDK"
                ],
                "answer": "C",
                "explanation": "Proper error handling requires try/except blocks around both the async iteration and individual event processing to handle different types of failures.",
                "category": "Async"
            },
            {
                "id": 20,
                "question": "You're implementing a distributed system where multiple AI agents need to collaborate on complex research tasks. Each agent specializes in different domains (web research, data analysis, report writing) and they need to work concurrently while sharing intermediate results. The system must handle agent failures gracefully and ensure optimal resource utilization. How should you orchestrate these concurrent agent operations?",
                "options": [
                    "A. Execute agents sequentially to maintain simple control flow",
                    "B. Use asyncio.gather() for parallel execution with timeout handling via asyncio.wait_for(), implementing result sharing through structured data passing",
                    "C. Use threading for each agent to avoid async complexity",
                    "D. Create separate processes for each agent domain"
                ],
                "answer": "B",
                "explanation": "asyncio.gather() with timeout management provides efficient concurrent execution while maintaining structured communication and fault tolerance for collaborative agent workflows.",
                "category": "Async"
            },
            {
                "id": 21,
                "question": "Your financial trading agent executes market analysis tools that sometimes hang due to external API issues. The trading window is time-critical, and you need to ensure the agent can timeout problematic tool calls and continue with available data. You also need to implement exponential backoff for transient failures. How should you handle tool execution timeouts and retries in this async environment?",
                "options": [
                    "A. Let tools run indefinitely to ensure complete data collection",
                    "B. Implement asyncio.wait_for() with timeout parameters around tool calls, combined with retry logic using exponential backoff",
                    "C. Use synchronous tools with threading.Timer for timeout management",
                    "D. Process all data sequentially to avoid timeout complications"
                ],
                "answer": "B",
                "explanation": "asyncio.wait_for() provides proper async timeout handling, while exponential backoff ensures resilient handling of transient failures in time-critical scenarios.",
                "category": "Async"
            },
            {
                "id": 22,
                "question": "When streaming agent responses, how should you handle partial tool calls?",
                "options": [
                    "A. Wait for the complete tool call before processing",
                    "B. Process each chunk immediately as it arrives",
                    "C. Accumulate tool call chunks and process when tool_call_done event occurs",
                    "D. Ignore partial tool calls"
                ],
                "answer": "C",
                "explanation": "Tool calls should be accumulated across chunks and processed when the tool_call_done event indicates the complete tool call is available.",
                "category": "Async"
            },
            {
                "id": 23,
                "question": "You're developing a multi-user educational platform where each student interacts with personalized tutoring agents. Each agent maintains individual learning progress, preferences, and conversation history. The system serves 500+ concurrent students during peak hours. You need to ensure proper state isolation between students while maintaining efficient resource usage. How should you manage agent state in this async environment?",
                "options": [
                    "A. Use global variables with student ID prefixes for shared state management",
                    "B. Implement asyncio context variables for student-specific state, passing state explicitly through async function chains with proper isolation",
                    "C. Store all state in class attributes shared across all students",
                    "D. Use thread-local storage for state management"
                ],
                "answer": "B",
                "explanation": "asyncio context variables with explicit state passing ensures proper isolation between concurrent student sessions while maintaining efficient async operations and preventing state leakage.",
                "category": "Async"
            },
            {
                "id": 24,
                "question": "How should you handle agent cleanup in async contexts?",
                "options": [
                    "A. Use try/finally blocks or async context managers",
                    "B. Cleanup is automatic and not needed",
                    "C. Use atexit module for cleanup",
                    "D. Manual cleanup after each run"
                ],
                "answer": "A",
                "explanation": "try/finally blocks and async context managers ensure proper cleanup even when exceptions occur during async agent execution.",
                "category": "Async"
            },

            # Questions 25-32: Prompt Engineering and Instructions
            {
                "id": 25,
                "question": "You're developing a legal research agent that needs to analyze complex case law and provide step-by-step reasoning for its conclusions. The agent must cite sources, explain legal precedents, and show how it arrived at its recommendations. However, initial testing shows the agent often jumps to conclusions without showing its reasoning process, making it difficult for lawyers to verify the analysis. How should you structure the agent instructions to ensure comprehensive reasoning?",
                "options": [
                    "A. Add 'think step by step' at the end of instructions",
                    "B. Structure instructions with explicit sections: 'First, identify relevant legal principles. Second, analyze applicable case law. Third, examine precedents. Finally, provide your conclusion with supporting rationale.'",
                    "C. Use bullet points throughout all instructions",
                    "D. Keep instructions brief to avoid overwhelming the agent"
                ],
                "answer": "B",
                "explanation": "Structured instructions with explicit reasoning steps ensure the agent follows a methodical approach, providing the transparency and verification needed in legal contexts.",
                "category": "Prompting"
            },
            {
                "id": 26,
                "question": "You're building a healthcare agent that processes patient information including medical history, symptoms, and test results. The agent needs to provide diagnostic suggestions while ensuring patient privacy and avoiding medical liability issues. The agent should never store patient identifiers and must include appropriate disclaimers about medical advice. How should you design the agent's persona and data handling guidelines?",
                "options": [
                    "A. Include sample patient data directly in instructions for reference",
                    "B. Create explicit data privacy guidelines in the persona: 'Never store patient identifiers, anonymize all data references, include medical disclaimers, and remind users to consult healthcare professionals'",
                    "C. Avoid mentioning medical or privacy concerns in instructions",
                    "D. Use encryption for all data mentioned in instructions"
                ],
                "answer": "B",
                "explanation": "Explicit privacy and medical guidelines in the persona ensure consistent, responsible behavior that protects patient data and maintains appropriate medical boundaries.",
                "category": "Prompting"
            },
            {
                "id": 27,
                "question": "You're building a customer service agent for an e-commerce platform that needs to handle different scenarios: order inquiries, refund requests, product recommendations, and technical support. Depending on the customer's tier (bronze, silver, gold), different policies apply - gold customers get expedited service, silver customers get standard service, and bronze customers have limited options. The agent needs to adapt its responses based on customer tier and request type. How should you implement this dynamic behavior?",
                "options": [
                    "A. Modify the agent's instructions attribute directly when customer tier is identified",
                    "B. Use context-aware prompting within the conversation flow: 'Based on this customer's gold tier status, provide expedited service options and priority support'",
                    "C. Create separate agents for each customer tier and request type combination",
                    "D. Hard-code all possible tier and request combinations in the initial instructions"
                ],
                "answer": "B",
                "explanation": "Context-aware prompting allows dynamic adaptation based on real-time customer information without modifying the agent's core configuration, providing flexibility and maintaining consistency.",
                "category": "Prompting"
            },
            {
                "id": 28,
                "question": "Your financial advisory agent sometimes provides investment recommendations based on outdated market information or makes assumptions about economic conditions that aren't explicitly stated in the user's query. This leads to potentially harmful advice based on incomplete or incorrect information. You need to minimize these hallucinations while maintaining the agent's helpfulness. How should you structure the instructions?",
                "options": [
                    "A. Use vague, general instructions to avoid constraining the agent",
                    "B. Provide specific guidelines: 'Only use information explicitly provided by the user. If market data is needed, use the market_data tool. Always state assumptions clearly and ask for clarification when information is missing. Include disclaimers about investment risks.'",
                    "C. Keep instructions very short to avoid confusion",
                    "D. Include only general disclaimers without specific guidance"
                ],
                "answer": "B",
                "explanation": "Specific guidelines with clear boundaries, tool requirements, and explicit disclaimer requirements help agents stay grounded and reduce harmful hallucinations in critical domains like finance.",
                "category": "Prompting"
            },
            {
                "id": 29,
                "question": "You're designing a technical writing agent that helps software developers create documentation. The agent should write clearly, use appropriate technical terminology, include code examples when relevant, and maintain a helpful but professional tone. It should understand different documentation types (API docs, tutorials, troubleshooting guides) and adapt its writing style accordingly. How should you define this agent's persona?",
                "options": [
                    "A. Define only the technical writing capabilities without personality",
                    "B. Include comprehensive persona: 'You are a senior technical writer with expertise in software documentation. Use clear, concise language. Include relevant code examples. Adapt style to documentation type: formal for API docs, conversational for tutorials. Always prioritize clarity over brevity.'",
                    "C. Focus only on personality traits without role definition",
                    "D. Keep persona definitions generic to maintain flexibility"
                ],
                "answer": "B",
                "explanation": "A comprehensive persona including role, expertise, communication style, and context-specific behavioral guidelines provides clear framework for consistent, appropriate agent behavior across different documentation scenarios.",
                "category": "Prompting"
            },
            {
                "id": 30,
                "question": "Your project management agent receives requests like 'Schedule the meeting for next Friday but also handle the client call that's supposed to happen then, and make sure the team presentation is ready, but if the client prefers Thursday instead, prioritize that.' The request contains conflicting priorities and ambiguous requirements. How should your agent instructions address these scenarios?",
                "options": [
                    "A. Always follow the most recent instruction mentioned",
                    "B. Include explicit guidelines: 'When requests contain conflicts or ambiguities, identify the specific conflicts, ask clarifying questions about priorities, and propose alternative solutions. Example: I notice a scheduling conflict between the Friday meeting and client call. Which should take priority, or would you prefer a different time for one of them?'",
                    "C. Ignore contradictory parts of requests",
                    "D. Make random decisions when facing ambiguous requests"
                ],
                "answer": "B",
                "explanation": "Clear guidelines for identifying conflicts and seeking clarification, with examples, ensure the agent handles ambiguous requests professionally and helps users resolve unclear requirements.",
                "category": "Prompting"
            },
            {
                "id": 31,
                "question": "What is the recommended approach for instruction versioning and updates?",
                "options": [
                    "A. Update instructions directly in production",
                    "B. Version control instructions and test changes before deployment",
                    "C. Never update instructions once deployed",
                    "D. Update instructions randomly"
                ],
                "answer": "B",
                "explanation": "Version controlling instructions and testing changes ensures consistency, traceability, and prevents unexpected behavior changes in production.",
                "category": "Prompting"
            },
            {
                "id": 32,
                "question": "How should you balance specificity and flexibility in agent instructions?",
                "options": [
                    "A. Always be as specific as possible",
                    "B. Always keep instructions general",
                    "C. Provide specific core guidelines with flexibility for edge cases",
                    "D. Specificity and flexibility are mutually exclusive"
                ],
                "answer": "C",
                "explanation": "Effective instructions provide specific core guidelines for consistent behavior while allowing flexibility to handle unexpected scenarios appropriately.",
                "category": "Prompting"
            },

            # Questions 33-40: Context Management and Error Handling
            {
                "id": 33,
                "question": "You're building a long-running research agent that conducts multi-day investigations across multiple sessions. Users may disconnect and reconnect, and the agent needs to resume where it left off. The agent gathers information from various sources, maintains research notes, and builds upon previous findings. Each session can last several hours with dozens of tool calls and intermediate results. How should you handle context persistence and restoration?",
                "options": [
                    "A. Store everything in global variables that persist across sessions",
                    "B. Use the SDK's message history and implement session state management with conversation checkpoints and explicit context reconstruction tools",
                    "C. Start fresh each session to avoid complexity",
                    "D. Require users to manually re-enter all previous information"
                ],
                "answer": "B",
                "explanation": "Leveraging the SDK's built-in context management while implementing additional session state tools ensures continuity across long-running investigations without losing valuable research progress.",
                "category": "Context"
            },
            {
                "id": 34,
                "question": "Your financial trading agent is executing a complex multi-step analysis (market data retrieval, trend analysis, risk calculation, portfolio optimization) when the risk calculation tool fails due to a database timeout. The agent has already gathered valuable market data and completed trend analysis. The user needs results quickly for a time-sensitive trading decision. How should your error handling preserve the valuable work done while addressing the failure?",
                "options": [
                    "A. Restart the entire analysis from the beginning",
                    "B. Implement try/catch around tool calls, preserve successful results in context, provide partial analysis with clear indication of missing risk data, and offer retry options",
                    "C. Ignore the failure and proceed without risk calculation",
                    "D. Cache all results to disk before every tool call"
                ],
                "answer": "B",
                "explanation": "Preserving successful work while clearly communicating limitations allows users to make informed decisions with available data rather than losing all progress due to a single tool failure.",
                "category": "Error Handling"
            },
            {
                "id": 35,
                "question": "Your e-commerce agent uses an inventory_check tool that frequently times out during high-traffic periods. When this happens, the agent becomes confused and sometimes tells customers that products are unavailable even when they might be in stock. You need to maintain good customer experience while handling these infrastructure limitations. How should you implement tool error handling?",
                "options": [
                    "A. Let exceptions propagate to stop agent execution immediately",
                    "B. Catch tool timeouts, return structured error messages like 'Inventory system temporarily unavailable - please try again in a few minutes or contact support for immediate assistance', and log the issue for monitoring",
                    "C. Always tell customers products are available to avoid disappointment",
                    "D. Retry inventory checks indefinitely until they succeed"
                ],
                "answer": "B",
                "explanation": "Structured error handling with customer-friendly messages and logging maintains service quality while providing transparency about temporary limitations and alternative paths forward.",
                "category": "Error Handling"
            },
            {
                "id": 36,
                "question": "Your document processing agent uses external OCR services that sometimes fail due to poor image quality or service outages. The processing pipeline involves multiple steps: image preprocessing, OCR extraction, text analysis, and summary generation. You want to implement resilient processing that can handle transient failures without losing user documents. How should you implement retry logic?",
                "options": [
                    "A. Retry failed operations immediately without any delay",
                    "B. Implement exponential backoff retry logic within each tool function (1s, 2s, 4s delays), with maximum retry limits and fallback options for persistent failures",
                    "C. Let the LLM handle retries by asking the user to resubmit documents",
                    "D. Never retry failed operations to avoid duplicate processing"
                ],
                "answer": "B",
                "explanation": "Exponential backoff prevents overwhelming failed services while giving transient issues time to resolve, with sensible limits and fallbacks to maintain system reliability.",
                "category": "Error Handling"
            },
            {
                "id": 37,
                "question": "What information should be included in error messages returned to agents?",
                "options": [
                    "A. Full stack traces and system details",
                    "B. User-friendly error descriptions with actionable guidance",
                    "C. Only error codes",
                    "D. No error information"
                ],
                "answer": "B",
                "explanation": "Error messages should be user-friendly and provide actionable guidance that helps the agent understand what went wrong and how to proceed.",
                "category": "Error Handling"
            },
            {
                "id": 38,
                "question": "You're building a collaborative writing system where multiple specialized agents (research_agent, outline_agent, writing_agent, editing_agent) work together on long-form content. Each agent builds upon the previous agent's work, and the document evolves through multiple revisions. Users can intervene at any stage to provide feedback or request changes. How should you manage context transfer and state consistency across this multi-agent workflow?",
                "options": [
                    "A. Each agent works independently without sharing context",
                    "B. Use Handoff objects to pass comprehensive document state, revision history, and user feedback between agents, with explicit context validation at each handoff",
                    "C. Store all context in a global shared database",
                    "D. Require users to manually coordinate between agents"
                ],
                "answer": "B",
                "explanation": "Structured Handoffs with comprehensive state transfer ensure each agent has the context needed to build upon previous work while maintaining document consistency and user feedback integration.",
                "category": "Context"
            },
            {
                "id": 39,
                "question": "Your automated testing agent runs comprehensive test suites that can take 30+ minutes. The workflow includes unit tests, integration tests, security scans, and performance benchmarks. If the security scan fails, you want to continue with performance testing since they're independent, but if unit tests fail, integration tests should be skipped. How should you handle these partial failure scenarios?",
                "options": [
                    "A. Stop all testing immediately when any component fails",
                    "B. Implement workflow checkpoints with dependency mapping - continue independent tests after failures, skip dependent tests, provide comprehensive status reporting of what completed, failed, and was skipped",
                    "C. Ignore all failures and run every test regardless",
                    "D. Restart the entire test suite from the beginning after any failure"
                ],
                "answer": "B",
                "explanation": "Smart checkpoint management with dependency awareness maximizes valuable test coverage while respecting logical dependencies, providing comprehensive reporting for informed decision-making.",
                "category": "Error Handling"
            },
            {
                "id": 40,
                "question": "How should you monitor and log agent behavior for debugging purposes?",
                "options": [
                    "A. Log only final outputs",
                    "B. Implement comprehensive logging of agent decisions, tool calls, and context changes",
                    "C. Avoid logging for performance reasons",
                    "D. Log only errors"
                ],
                "answer": "B",
                "explanation": "Comprehensive logging of agent decisions, tool calls, and context changes provides the visibility needed for effective debugging and monitoring.",
                "category": "Error Handling"
            },

            # Questions 41-48: Multi-Agent Workflows and Advanced Patterns
            {
                "id": 41,
                "question": "You're designing a content moderation system for a social media platform that processes thousands of posts per hour. The system uses specialized agents: content_classifier (determines post type), safety_analyzer (checks for harmful content), sentiment_analyzer (analyzes emotional tone), and action_agent (decides on moderation actions). Posts flow through these agents based on classification results, and some posts need human review. How should you orchestrate this multi-agent workflow for optimal efficiency and accuracy?",
                "options": [
                    "A. Process all posts through every agent in sequence regardless of content type",
                    "B. Use Handoff objects with conditional routing - content_classifier determines which specialized agents are needed, with parallel processing where possible and human-in-the-loop integration for edge cases",
                    "C. Use direct function calls between agents without formal handoff mechanisms",
                    "D. Create separate workflows for each possible content type combination"
                ],
                "answer": "B",
                "explanation": "Conditional Handoff routing optimizes efficiency by only using necessary agents while maintaining flexibility for complex cases and human oversight integration.",
                "category": "Multi-Agent"
            },
            {
                "id": 42,
                "question": "Your legal document review system has three specialist agents: contracts_agent (analyzes contract terms), compliance_agent (checks regulatory requirements), and risk_agent (assesses legal risks). During a complex merger review, the contracts_agent identifies clauses that need compliance review, but the compliance_agent finds issues that require the contracts_agent to re-examine specific sections with additional context. How should you handle this iterative, bidirectional collaboration?",
                "options": [
                    "A. Create new agent instances for each iteration to avoid confusion",
                    "B. Use bidirectional Handoffs with updated context - each agent can return control to previous agents with new findings and specific focus areas for re-analysis",
                    "C. Force a linear workflow to avoid cycles",
                    "D. Combine all agents into a single multi-purpose agent"
                ],
                "answer": "B",
                "explanation": "Bidirectional Handoffs enable iterative refinement while maintaining context and focus, allowing agents to build upon each other's findings for thorough analysis.",
                "category": "Multi-Agent"
            },
            {
                "id": 43,
                "question": "You're building an automated customer onboarding system with agents for different functions: data_collection_agent (gathers customer information), verification_agent (validates identity and credentials), setup_agent (configures accounts and services), and welcome_agent (provides tutorials and initial support). Each agent has specific expertise and tools. Customer requirements vary significantly - some need simple account setup, others require complex enterprise configurations. How should you design agent specialization for this system?",
                "options": [
                    "A. Create one general-purpose agent that handles all onboarding scenarios",
                    "B. Design specialized agents with clear expertise boundaries, standard handoff protocols, and a coordinator agent that routes customers based on their specific requirements and complexity",
                    "C. Use identical agents for consistency across all customer types",
                    "D. Let customers manually choose which agents to interact with"
                ],
                "answer": "B",
                "explanation": "Specialized agents with clear boundaries and intelligent routing ensure optimal expertise application while maintaining consistent, efficient onboarding experiences tailored to customer needs.",
                "category": "Multi-Agent"
            },
            {
                "id": 44,
                "question": "Your research publication system involves a multi-week workflow where agents collaborate on literature review, data analysis, writing, and peer review coordination. Authors may request revisions, reviewers provide feedback, and the document evolves through multiple drafts over several weeks. Team members work across different time zones and may contribute asynchronously. How should you handle state persistence across this extended multi-agent workflow?",
                "options": [
                    "A. Each agent maintains completely isolated state with no sharing",
                    "B. Implement persistent context objects with version control, conversation history preservation, and state synchronization mechanisms that allow agents to resume work with full knowledge of previous contributions and current document status",
                    "C. Store all workflow state in global variables accessible to all agents",
                    "D. Require real-time collaboration only to avoid state complexity"
                ],
                "answer": "B",
                "explanation": "Persistent, versioned context management ensures continuity across extended workflows while preserving contribution history and enabling effective asynchronous collaboration.",
                "category": "Multi-Agent"
            },
            {
                "id": 45,
                "question": "What is the correct Markdown syntax for creating a link?",
                "options": [
                    "A. [text](url)",
                    "B. (text)[url]",
                    "C. <text|url>",
                    "D. {text}(url)"
                ],
                "answer": "A",
                "explanation": "The correct Markdown syntax for links is [link text](URL), where the text is in square brackets followed by the URL in parentheses.",
                "category": "Markdown"
            },
            {
                "id": 46,
                "question": "How do you display an image in Markdown?",
                "options": [
                    "A. [image](url)",
                    "B. ![alt text](image url)",
                    "C. <img src='url'>",
                    "D. {image}(url)"
                ],
                "answer": "B",
                "explanation": "Images in Markdown use the syntax ![alt text](image URL), which is similar to links but with an exclamation mark at the beginning.",
                "category": "Markdown"
            },
            {
                "id": 47,
                "question": "You're designing a smart city traffic management system where multiple AI agents coordinate traffic lights, emergency vehicle routing, public transit optimization, and incident response. The system must handle real-time events like accidents, weather changes, and special events while maintaining overall traffic flow efficiency. Each agent has different priorities and constraints, but they must work together seamlessly. What orchestration pattern best handles this complex, real-time multi-agent coordination?",
                "options": [
                    "A. Hard-code traffic management sequences based on common scenarios",
                    "B. Implement a traffic_coordinator_agent that monitors system state, prioritizes competing demands, manages handoffs based on real-time conditions, and maintains overall system optimization while allowing specialized agents to handle their domains",
                    "C. Let each agent make independent decisions without coordination",
                    "D. Use external traffic management software to control the agents"
                ],
                "answer": "B",
                "explanation": "A coordinator agent with real-time state awareness can balance competing priorities and optimize overall system performance while leveraging specialized agent expertise for domain-specific decisions.",
                "category": "Multi-Agent"
            },
            {
                "id": 48,
                "question": "Your distributed software testing system uses multiple agents (unit_test_agent, integration_test_agent, security_test_agent, performance_test_agent) that work together to validate software releases. If the unit tests fail, subsequent testing phases should be modified or skipped. If security tests find vulnerabilities, the performance agent should focus on secure configurations. The system must handle test environment failures, flaky tests, and provide comprehensive reporting even when some test phases fail. How should you design error recovery for this collaborative testing workflow?",
                "options": [
                    "A. Restart the entire test suite from the beginning whenever any agent encounters an error",
                    "B. Design adaptive fallback paths with workflow context awareness - agents can modify their strategies based on previous results, skip dependent phases when prerequisites fail, implement retry logic for transient failures, and coordinate to provide comprehensive status reporting regardless of partial failures",
                    "C. Continue all testing phases regardless of failures or dependencies",
                    "D. Stop all testing immediately when any error occurs"
                ],
                "answer": "B",
                "explanation": "Adaptive error recovery with workflow awareness maximizes test coverage value while respecting dependencies and providing comprehensive reporting for informed release decisions.",
                "category": "Multi-Agent"
            }
        ]

    async def run_quiz(self):
        """Run the complete quiz with timing and scoring."""
        print("🤖 FUNDAMENTALS OF AGENTIC AI QUIZ 🤖")
        print("=" * 50)
        print("Total Questions: 48 MCQs")
        print("Duration: 120 Minutes")
        print("Difficulty Level: Intermediate to Advanced")
        print("\nBased on OpenAI Agents SDK Documentation")
        print("https://openai.github.io/openai-agents-python/")
        print("=" * 50)

        # Quiz instructions
        print("\n📋 INSTRUCTIONS:")
        print("- Read each question carefully")
        print("- Select the best answer (A, B, C, or D)")
        print("- You can type 'skip' to skip a question")
        print("- You can type 'quit' to exit early")
        print("- Timer will track your progress")
        print("\nPress Enter to start the quiz...")
        input()

        self.start_time = time.time()

        for i, question in enumerate(self.questions, 1):
            print(f"\n{'='*20} Question {i}/48 {'='*20}")

            # Calculate elapsed time
            elapsed = time.time() - self.start_time
            remaining = 120 * 60 - elapsed  # 120 minutes in seconds

            if remaining <= 0:
                print("\n⏰ TIME'S UP! Quiz completed.")
                break

            print(
                f"⏱️ Time remaining: {int(remaining//60)}:{int(remaining % 60):02d}")
            print(f"📊 Category: {question['category']}")
            print(f"\nQ{i}: {question['question']}")
            print()

            for option in question['options']:
                print(f"   {option}")

            # Get user answer
            while True:
                user_answer = input(
                    f"\nYour answer (A/B/C/D, 'skip', or 'quit'): ").upper().strip()

                if user_answer == 'QUIT':
                    print("\nQuiz terminated by user.")
                    return self._show_results(i-1)
                elif user_answer == 'SKIP':
                    self.answers.append(None)
                    print("Question skipped.")
                    break
                elif user_answer in ['A', 'B', 'C', 'D']:
                    self.answers.append(user_answer)

                    # Check if correct
                    if user_answer == question['answer']:
                        print("✅ Correct!")
                        self.score += 1
                    else:
                        print(
                            f"❌ Incorrect. The correct answer was {question['answer']}.")

                    print(f"💡 Explanation: {question['explanation']}")
                    break
                else:
                    print("Invalid input. Please enter A, B, C, D, 'skip', or 'quit'.")

            if i < len(self.questions):
                input("\nPress Enter to continue to the next question...")

        return self._show_results(len(self.questions))

    def _show_results(self, questions_answered):
        """Display final quiz results."""
        print("\n" + "="*50)
        print("🎯 QUIZ RESULTS")
        print("="*50)

        # Calculate total time, handling case where start_time might be None
        if self.start_time is not None:
            total_time = time.time() - self.start_time
            minutes = int(total_time // 60)
            seconds = int(total_time % 60)
        else:
            total_time = 0
            minutes = 0
            seconds = 0

        print(f"📊 Questions Answered: {questions_answered}/48")
        print(f"✅ Correct Answers: {self.score}")
        print(f"📈 Score: {self.score}/{questions_answered} ({(self.score/questions_answered)*100:.1f}%)" if questions_answered > 0 else "📈 Score: 0%")
        print(f"⏱️ Time Taken: {minutes}:{seconds:02d}")

        # Performance assessment
        if questions_answered > 0:
            percentage = (self.score / questions_answered) * 100
            if percentage >= 90:
                print("\n🏆 EXCELLENT! You have mastered the OpenAI Agents SDK!")
                print("You're ready for advanced agentic AI development.")
            elif percentage >= 80:
                print("\n🎉 GREAT JOB! Strong understanding of the SDK.")
                print("Review missed concepts for complete mastery.")
            elif percentage >= 70:
                print("\n👍 GOOD WORK! Solid foundation established.")
                print("Focus on areas where you struggled for improvement.")
            elif percentage >= 60:
                print("\n📚 KEEP STUDYING! You're on the right track.")
                print("Revisit the documentation and practice more examples.")
            else:
                print("\n💪 MORE PRACTICE NEEDED!")
                print("Spend more time with the OpenAI Agents SDK documentation.")
                print("Consider working through more hands-on examples.")

        print("\n📖 Study Resources:")
        print("- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/")
        print(
            "- Prompting Guide: https://cookbook.openai.com/examples/gpt4-1_prompting_guide")
        print("- Markdown Guide: https://www.markdownguide.org/basic-syntax/")

        print("\n🎯 Focus Areas for Improvement:")
        categories = {}
        for i, question in enumerate(self.questions[:questions_answered]):
            if i < len(self.answers) and self.answers[i] is not None:
                category = question['category']
                if category not in categories:
                    categories[category] = {'correct': 0, 'total': 0}
                categories[category]['total'] += 1
                if self.answers[i] == question['answer']:
                    categories[category]['correct'] += 1

        for category, stats in categories.items():
            if stats['total'] > 0:
                cat_percentage = (stats['correct'] / stats['total']) * 100
                status = "✅" if cat_percentage >= 80 else "⚠️" if cat_percentage >= 60 else "❌"
                print(
                    f"{status} {category}: {stats['correct']}/{stats['total']} ({cat_percentage:.1f}%)")

        print("\nThank you for taking the Fundamentals of Agentic AI Quiz!")
        return {
            'score': self.score,
            'total': questions_answered,
            'percentage': (self.score/questions_answered)*100 if questions_answered > 0 else 0,
            'time_taken': total_time,
            'categories': categories
        }


async def main():
    """Main quiz execution function."""
    quiz = AgenticAIQuiz()
    results = await quiz.run_quiz()
    return results

if __name__ == "__main__":
    asyncio.run(main())
