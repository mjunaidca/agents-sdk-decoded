from agents import Agent, Runner, GuardrailFunctionOutput, RunConfig, output_guardrail, RunContextWrapper
from typing import Any

from pydantic.dataclasses import dataclass
from __future__ import annotations

from pydantic import BaseModel


class Animal(BaseModel):
    type_animal: Cat | Dog

class Cat(BaseModel):
    name: str

class Dog(BaseModel):
    name: str
    
@dataclass
class Test:
    name: str
    
    def call_some_method(self) -> Test:
        return Test(name="Modified")




# @output_guardrail
# async def modifying_guardrail(ctx: RunContextWrapper, agent: Agent, output: Any):
#     return GuardrailFunctionOutput(output_info="Guardrail says: Modified!", tripwire_triggered=False)


# agent = Agent(name="Test", instructions="Output 'Original'", output_guardrails=[modifying_guardrail])
# result = Runner.run_sync(agent, "Hello")
# print(result.final_output)