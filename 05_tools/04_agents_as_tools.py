# Agents as Tools Example
# https://openai.github.io/openai-agents-python/tools/

import asyncio
from agents import Agent, Runner

# Specialized agent for Spanish translation
spanish_agent = Agent(
    name="Spanish Translator",
    instructions="You are an expert Spanish translator. Translate the user's message to Spanish accurately and naturally."
)

# Specialized agent for French translation
french_agent = Agent(
    name="French Translator",
    instructions="You are an expert French translator. Translate the user's message to French accurately and naturally."
)

# Specialized agent for German translation
german_agent = Agent(
    name="German Translator",
    instructions="You are an expert German translator. Translate the user's message to German accurately and naturally."
)

# Specialized agent for code generation
code_agent = Agent(
    name="Code Generator",
    instructions="""You are a code generation expert. Generate clean, well-documented code based on the user's requirements.
    Always include comments and follow best practices."""
)

# Specialized agent for text analysis
analysis_agent = Agent(
    name="Text Analyzer",
    instructions="""You are a text analysis expert. Analyze the given text for:
    - Sentiment
    - Key themes
    - Writing style
    - Word count and readability
    Provide a comprehensive analysis."""
)


async def main():
    # Create orchestrator agent that uses other agents as tools
    orchestrator_agent = Agent(
        name="Multi-Purpose Assistant",
        instructions="""You are a versatile assistant that coordinates with specialized experts.
        
        Available specialists:
        - Translation experts for Spanish, French, and German
        - Code generation expert for programming tasks
        - Text analysis expert for content analysis
        
        Analyze the user's request and delegate to the appropriate specialist(s).
        If multiple translations are requested, call multiple translation tools.
        Always provide the results in a clear, organized format.""",
        tools=[
            spanish_agent.as_tool(
                tool_name="translate_to_spanish",
                tool_description="Translate text to Spanish using an expert translator"
            ),
            french_agent.as_tool(
                tool_name="translate_to_french",
                tool_description="Translate text to French using an expert translator"
            ),
            german_agent.as_tool(
                tool_name="translate_to_german",
                tool_description="Translate text to German using an expert translator"
            ),
            code_agent.as_tool(
                tool_name="generate_code",
                tool_description="Generate code based on requirements using a programming expert"
            ),
            analysis_agent.as_tool(
                tool_name="analyze_text",
                tool_description="Perform comprehensive text analysis using an expert analyzer"
            )
        ]
    )

    print("=== Multi-Language Translation Test ===")
    result1 = await Runner.run(
        orchestrator_agent,
        input="Translate 'Hello, how are you today?' to Spanish, French, and German."
    )
    print(result1.final_output)
    print("\n" + "="*60 + "\n")

    print("=== Code Generation Test ===")
    result2 = await Runner.run(
        orchestrator_agent,
        input="Generate a Python function that calculates the factorial of a number using recursion."
    )
    print(result2.final_output)
    print("\n" + "="*60 + "\n")

    print("=== Text Analysis Test ===")
    result3 = await Runner.run(
        orchestrator_agent,
        input="Analyze this text: 'The weather today is absolutely wonderful! I love how the sun is shining and the birds are singing. It makes me feel so happy and energetic.'"
    )
    print(result3.final_output)
    print("\n" + "="*60 + "\n")

    print("=== Combined Task Test ===")
    result4 = await Runner.run(
        orchestrator_agent,
        input="First, analyze the sentiment of 'I am feeling great today!', then translate it to Spanish and French."
    )
    print(result4.final_output)

if __name__ == "__main__":
    asyncio.run(main())
