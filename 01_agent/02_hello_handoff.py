import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, GuardrailFunctionOutput, InputGuardrail, function_tool
from pydantic import BaseModel

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

load_dotenv(find_dotenv())

provider = AsyncOpenAI(base_url="https://api.openai.com/v1",
                       api_key=os.getenv("OPENAI_API_KEY"))


@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)


guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent: Agent, input_data):
    print("RECEIVED AGENT IN GD", agent.name)
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    print("RESULT", result)
    final_output = result.final_output_as(HomeworkOutput)
    print("FINAL OUTPUT", final_output)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )
    
async def main():
    agent = Agent(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question",
        # model=OpenAIChatCompletionsModel(openai_client=provider, model="gpt-4o-mini"),
        handoffs=[history_tutor_agent, math_tutor_agent],
        input_guardrails=[InputGuardrail(homework_guardrail)],

    )

    result = await Runner.run(agent, "I have homework about the french revolution. Can you help me?")
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":
    print("\n[STARTING AGENT]\n")
    asyncio.run(main())
