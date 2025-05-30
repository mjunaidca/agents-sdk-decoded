"""
Key Benefits of Mutable Context:
- Shared State: Multiple tools can read and modify the same data
- Persistence: Changes persist across tool calls and interactions
- Efficiency: No need to create new objects constantly
- Flexibility: Context can evolve during the conversation

Common Mutable Types in Python:
- list - Can add, remove, modify elements
- dict - Can add, remove, modify key-value pairs
- set - Can add, remove elements
- Custom classes - Can modify attributes
- bytearray - Can modify individual bytes

Common Immutable Types:
- str - Cannot change characters
- tuple - Cannot change elements
- int, float, bool - Cannot change value
- frozenset - Cannot change elements

The mutable context in the Agents SDK allows your agent to maintain and modify state throughout the conversation, making it much more powerful and stateful!
"""

from agents import Agent, Runner, RunContextWrapper, function_tool
from typing import Dict, List, Any
import asyncio
from datetime import datetime

# Create a simple mutable context object


class MyContext:
    def __init__(self):
        self.user_preferences: dict[str, str] = {}
        self.call_count: int = 0

    def add_user_preferences(self, preference: str, value: str):
        self.user_preferences[preference] = value
        self.increment_call_count()

    def increment_call_count(self):
        self.call_count += 1

@function_tool
def save_user_preference(ctx: RunContextWrapper[MyContext], preference: str, value: str) -> str:
    """Save user preference to context"""
    print(f"Saving user preference: {preference} = {value}")
    ctx.context.add_user_preferences(preference, value)
    return f"Saved {preference}: {value}"


@function_tool
def get_user_preferences(ctx: RunContextWrapper[MyContext]) -> dict[str, str]:
    """Get all user preferences from context"""
    return ctx.context.user_preferences

@function_tool
def clear_user_preferences(ctx: RunContextWrapper[MyContext]) -> str:
    """Clear all user preferences"""
    print(f"Clearing user preferences: {ctx.context.user_preferences}")
    ctx.context.user_preferences.clear()
    print(f"User preferences after clearing: {ctx.context.user_preferences}")
    return "All user preferences cleared"


# Create agent with working tools
agent = Agent(
    name="PreferenceAgent",
    instructions="Help users manage their preferences. Use tools to save, retrieve, and clear preferences.",
    tools=[save_user_preference, get_user_preferences, clear_user_preferences]
)


async def test_preference_agent():
    print("=== Testing Preference Agent ===")
    
    context = MyContext()

    # Test saving preferences
    result1 = await Runner.run(agent, "Save my favorite color as blue", context=context)
    print(f"Result 1: {result1.final_output}")
    print(f"Current preferences: {context.user_preferences}")

    # Test saving another preference
    result2 = await Runner.run(agent, "Save my favorite food as pizza", context=context)
    print(f"Result 2: {result2.final_output}")
    print(f"Current preferences: {context.user_preferences}")

    # Test retrieving preferences
    result3 = await Runner.run(agent, "What are all my preferences?", context=context)
    print(f"Result 3: {result3.final_output}")

    # Test clearing preferences
    result4 = await Runner.run(agent, "Clear all my preferences", context=context)
    print(f"Result 4: {result4.final_output}")
    print(f"Final preferences: {context.user_preferences}")

# Example 2: Using context with the Runner
class SessionContext:
    def __init__(self):
        self.messages_count: int = 0
        self.topics_discussed: set[str] = set()
        self.user_mood: str = "neutral"
        self.start_time: datetime = datetime.now()

    def add_message(self):
        self.messages_count += 1

    def add_topic(self, topic: str):
        self.topics_discussed.add(topic)

    def set_mood(self, mood: str):
        self.user_mood = mood
        
    def get_session_info(self) -> str:
        return f"Messages: {self.messages_count}\nTopics: {self.topics_discussed}\nMood: {self.user_mood}"

# Tools that work with context passed to Runner


@function_tool
def track_topic(ctx: RunContextWrapper[SessionContext], topic: str) -> str:
    """Track a discussion topic"""
    ctx.context.add_topic(topic)
    return f"Tracking topic: {topic}"


@function_tool
def set_mood(ctx: RunContextWrapper[SessionContext], mood: str) -> str:
    """Set the user's current mood"""
    ctx.context.set_mood(mood)
    return f"User mood set to: {mood}"


@function_tool
def get_session_info(ctx: RunContextWrapper[SessionContext]) -> str:
    """Get current session information"""
    return ctx.context.get_session_info()


# Simple agent without dynamic instructions
session_agent = Agent(
    name="SessionAgent",
    instructions="Help users track topics and mood. Be helpful and engaging. Always use the tools to update the context.",
    tools=[track_topic, set_mood, get_session_info]
)


async def test_session_agent():
    print("\n=== Testing Session Agent ===")

    # Create context
    context = SessionContext()

    interactions = [
        "I want to learn about Python programming",
        "I'm getting frustrated with coding",
        "Can you help me with data structures?",
        "What's my current session info?"
    ]

    for i, message in enumerate(interactions):
        context.add_message()

        print(f"\n--- Interaction {i+1} ---")
        print(f"Messages count: {context.messages_count}")
        print(f"User message: {message}")

        # Run the agent (context is available but tools work independently)
        result = await Runner.run(session_agent, message, context=context)

        print(f"Agent response: {result.final_output}")


    print(f"\nFinal session state:")
    print(f"Messages: {context.messages_count}")
    print(f"Topics: {context.topics_discussed}")
    print(f"Mood: {context.user_mood}")


# Example 3: Advanced Context Usage with Proper Context Access
class AdvancedContext:
    def __init__(self):
        self.user_profile: Dict[str, Any] = {}
        self.conversation_memory: List[str] = []
        self.task_queue: List[str] = []
        self.completed_tasks: List[str] = []

    def add_memory(self, memory: str):
        self.conversation_memory.append(memory)
        # Keep only last 10 memories
        if len(self.conversation_memory) > 10:
            self.conversation_memory.pop(0)

    def add_task(self, task: str):
        self.task_queue.append(task)

    def complete_task(self, task: str):
        if task in self.task_queue:
            self.task_queue.remove(task)
            self.completed_tasks.append(task)
            return True
        return False



@function_tool
def remember_fact(ctx: RunContextWrapper[AdvancedContext], fact: str) -> str:
    """Remember an important fact about the conversation"""
    ctx.context.add_memory(fact)
    return f"Remembered: {fact}"


@function_tool
def add_task(ctx: RunContextWrapper[AdvancedContext], task: str) -> str:
    """Add a task to the user's task queue"""
    ctx.context.add_task(task)
    return f"Added task: {task}"


@function_tool
def complete_task(ctx: RunContextWrapper[AdvancedContext], task: str) -> str:
    """Mark a task as completed"""
    if ctx.context.complete_task(task):
        return f"Completed task: {task}"
    else:
        return f"Task not found: {task}"


@function_tool
def get_status(ctx: RunContextWrapper[AdvancedContext]) -> Dict[str, Any]:
    """Get current status including memories, tasks, and profile"""
    return {
        "memories": ctx.context.conversation_memory,
        "pending_tasks": ctx.context.task_queue,
        "completed_tasks": ctx.context.completed_tasks,
        "profile": ctx.context.user_profile
    }


@function_tool
def update_profile(ctx: RunContextWrapper[AdvancedContext], key: str, value: str) -> str:
    """Update user profile information"""
    ctx.context.user_profile[key] = value
    return f"Updated profile: {key} = {value}"


# Advanced agent with memory and task management
advanced_agent = Agent(
    name="AdvancedAgent",
    instructions="""You are an advanced assistant with memory and task management capabilities. 
    Use your tools to:
    - Remember important facts about our conversation
    - Help users manage their tasks
    - Keep track of user profile information
    - Provide status updates when requested
    
    Be proactive in using these capabilities to provide better assistance.""",
    tools=[remember_fact, add_task, complete_task, get_status, update_profile]
)


async def test_advanced_agent():
    print("\n=== Testing Advanced Agent with Context ===")

    interactions = [
        "Hi, I'm John and I'm a software engineer working on Python projects",
        "I need to finish my machine learning project by Friday",
        "Also remind me to call my mom later",
        "I just finished the data preprocessing part of my ML project",
        "What's my current status?"
    ]
    
    context = AdvancedContext()

    for i, message in enumerate(interactions):
        print(f"\n--- Interaction {i+1} ---")
        print(f"User: {message}")

        result = await Runner.run(advanced_agent, message, context=context)
        print(f"Agent: {result.final_output}")

        # Show context state after each interaction
        print(f"Context state:")
        print(f"  Memories: {context.conversation_memory}")
        print(f"  Pending tasks: {context.task_queue}")
        print(f"  Completed tasks: {context.completed_tasks}")
        print(f"  Profile: {context.user_profile}")


async def main():
    # await test_preference_agent()
    # await test_session_agent()
    await test_advanced_agent()

if __name__ == "__main__":
    asyncio.run(main())
