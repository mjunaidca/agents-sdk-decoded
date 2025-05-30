from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, InputGuardrail, GuardrailFunctionOutput, RunConfig, InputGuardrailTripwireTriggered
import asyncio
from pydantic import BaseModel


class MathQuestion(BaseModel):
    is_math_question: bool
    reasoning: str


@dataclass
class UserContext:
    uid: str
    is_pro_user: bool


def create_prompt(ctx: RunContextWrapper[str], agent: Agent[str]) -> str:
    print(f"Creating prompt for {ctx.context}")
    return f"You are a helpful assistant that provides concise answers. You are talking to {ctx.context}."


agent_guardrail_agent = Agent[str](
    name="GuardrailAgent",
    instructions="You answer about Math",
    output_type=MathQuestion
)


async def guardrail_function(ctx: RunContextWrapper[str], agent: Agent[str], input_data: str) -> GuardrailFunctionOutput:
    print(f"Guardrail function called with input: {input_data}")
    print(f"Agent: {agent}")
    print(f"Context: {ctx}")
    # if input_data.startswith("What is"):
    #     return GuardrailFunctionOutput(output_info="MathQuestion", tripwire_triggered=True)
    # else:
    return GuardrailFunctionOutput(output_info="NotMathQuestion", tripwire_triggered=False)

# Example 1: Basic string instructions
agent_basic = Agent[str](
    name="BasicAgent",
    instructions=create_prompt,
    input_guardrails=[InputGuardrail(
        guardrail_function=guardrail_function,
        name="GuardrailAgent",
    )]
)


async def global_guardrail_function(ctx: RunContextWrapper[str], agent: Agent[str], input_data: str) -> GuardrailFunctionOutput:
    print(f"Global Guardrail function called with input: {input_data}")
    print(f"Agent: {agent}")
    print(f"Context: {ctx}")
    return GuardrailFunctionOutput(output_info="GlobalNotMathQuestion", tripwire_triggered=True)


async def test_basic():
    try:
        name = "junaid"
        result1 = await Runner.run(agent_basic, "What is my name?", context=name,
                                run_config=RunConfig(input_guardrails=[InputGuardrail(guardrail_function=global_guardrail_function, name="GlobalGuardrailAgent")]))
        print("Basic Agent:", result1.final_output)
        
    except InputGuardrailTripwireTriggered as e:
        print("Tripwire triggered")
        print(e.guardrail_result)


async def main():
    await test_basic()

if __name__ == "__main__":
    asyncio.run(main())
