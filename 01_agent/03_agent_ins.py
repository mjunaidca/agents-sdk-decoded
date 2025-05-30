from datetime import datetime
from agents import Agent, Runner
import asyncio

# Example 1: Basic string instructions
agent_basic = Agent(
    name="BasicAgent",
    instructions="You are a helpful assistant that provides concise answers."
)

# Example 2: Detailed string instructions
agent_detailed = Agent(
    name="DetailedAgent", 
    instructions="""You are an expert Python developer.
    - Always provide working code examples
    - Explain your reasoning step by step
    - Keep responses under 200 words
    - Use best practices and modern Python syntax"""
)

# Example 3: Simple callable instructions
def dynamic_instructions(context, agent):
    print("RECEIVED CONTEXT", context)
    print("RECEIVED AGENT", agent)
    """Generate instructions based on context"""
    return f"You are {agent.name}. Respond professionally and helpfully."

agent_callable = Agent(
    name="DynamicAgent",
    instructions=dynamic_instructions
)

# Example 4: Context-aware callable instructions
def context_aware_instructions(context, agent):
    print("RECEIVED CONTEXT", context)
    print("RECEIVED AGENT", agent)
    """Instructions that adapt based on conversation context"""
    # You can access context.messages to see conversation history
    message_count = len(getattr(context, 'messages', []))
    
    if message_count == 0:
        return "You are a friendly assistant. Introduce yourself and ask how you can help."
    elif message_count < 3:
        return "You are a helpful assistant. Be encouraging and detailed in your responses."
    else:
        return "You are an experienced assistant. Be concise but thorough."

agent_context_aware = Agent(
    name="ContextAwareAgent",
    instructions=context_aware_instructions
)

async def test_callable_instructions():
    result1 = await Runner.run(agent_callable, "Hello!")
    print("Callable Agent:", result1.final_output)
    
    result2 = await Runner.run(agent_context_aware, "What's the weather like?")
    print("Context Aware Agent:", result2.final_output)
    

async def test_string_instructions():
    result1 = await Runner.run(agent_basic, "What is Python?")
    print("Basic Agent:", result1.final_output)
    
    result2 = await Runner.run(agent_detailed, "How do I create a list comprehension?")
    print("Detailed Agent:", result2.final_output)

# Example 5: Async callable instructions
async def async_instructions(context, agent):
    """Async function that generates instructions"""
    # Simulate async operation (like fetching from database)
    await asyncio.sleep(0.1)
    current_time = asyncio.get_event_loop().time()
    parsed_time = datetime.fromtimestamp(current_time)
    return f"""You are {agent.name}, an AI assistant with real-time capabilities.
    Current timestamp: {parsed_time}
    Provide helpful and timely responses."""

agent_async = Agent(
    name="AsyncAgent",
    instructions=async_instructions
)

async def test_async_instructions():
    result = await Runner.run(agent_async, "What time is it?")
    print("Async Agent:", result.final_output)
    
    
from agents import Agent, Runner
import asyncio

# Example 7: Stateful callable instructions
class InstructionGenerator:
    def __init__(self):
        self.interaction_count = 0
    
    def __call__(self, context, agent):
        self.interaction_count += 1
        
        if self.interaction_count == 1:
            return "You are a learning assistant. This is our first interaction - be welcoming!"
        elif self.interaction_count <= 3:
            return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation."
        else:
            return f"You are an experienced learning assistant. We've had {self.interaction_count} interactions - be efficient."

instruction_gen = InstructionGenerator()

agent_stateful = Agent(
    name="StatefulAgent",
    instructions=instruction_gen
)

async def test_stateful_instructions():
    for i in range(4):
        result = await Runner.run(agent_stateful, f"Question {i+1}: Tell me about Python")
        print(f"Interaction {i+1}:", result.final_output[:100] + "...")


def main():
    print("\n[1. STRING INSTRUCTIONS]")
    # # Test this
    asyncio.run(test_string_instructions())
    
    print("\n[2. CALLABLE INSTRUCTIONS]")
    asyncio.run(test_callable_instructions())
    
    print("\n[3. ASYNC INSTRUCTIONS]")
    asyncio.run(test_async_instructions())
    
    print("\n[4. STATEFUL INSTRUCTIONS]")
    asyncio.run(test_stateful_instructions())
    
    
if __name__ == "__main__":
    main()