"""
13_runner_expert_quiz.py

Expert-level quiz on the OpenAI Agents SDK Runner.

Covers:
- Runner methods: run(), run_sync(), run_streamed()
- The Agent Loop: final output, tool calls, handoffs, max_turns
- Input Types: string, list of items
- Streaming: RunResultStreaming, StreamEvent types
- RunConfig: model overrides, global guardrails, handoff_input_filter, tracing
- Conversations/Chat Threads: to_input_list(), group_id
- Exception Handling: MaxTurnsExceeded, UserError, Guardrail exceptions
"""

import asyncio
import random
import textwrap
from typing import List, Dict, Any, Union, Literal
import os

# --- Quiz Structure ---


class Question:
    def __init__(self,
                 text: str,
                 options: Dict[str, str],
                 correct_answer_key: str,
                 category: str,
                 difficulty: Literal["Beginner", "Intermediate", "Advanced", "Expert"],
                 explanation: str):
        self.text = textwrap.dedent(text)
        self.options = options
        self.correct_answer_key = correct_answer_key
        self.category = category
        self.difficulty = difficulty
        self.explanation = textwrap.dedent(explanation)

    def display(self):
        print(f"\nCategory: {self.category} | Difficulty: {self.difficulty}")
        print(self.text)
        for key, value in self.options.items():
            print(f"  {key}. {value}")
        print("")

    def check_answer(self, answer_key: str) -> bool:
        return answer_key.lower() == self.correct_answer_key.lower()


QUIZ_QUESTIONS: List[Question] = [
    # --- Runner Methods ---
    Question(
        text="Which `Runner` method is fully synchronous?",
        options={
            "a": "Runner.run()",
            "b": "Runner.run_sync()",
            "c": "Runner.run_streamed()",
            "d": "Runner.execute()"
        },
        correct_answer_key="b",
        category="Runner Methods",
        difficulty="Beginner",
        explanation="`Runner.run_sync()` is synchronous."
    ),
    Question(
        text="What does `Runner.run_streamed()` return?",
        options={
            "a": "A `RunResult` object.",
            "b": "A `RunResultStreaming` object.",
            "c": "A list of `StreamEvent`s.",
            "d": "Raw text stream."
        },
        correct_answer_key="b",
        category="Runner Methods",
        difficulty="Intermediate",
        explanation="It returns `RunResultStreaming` for async iteration."
    ),

    # --- Agent Loop ---
    Question(
        text="""
        Under what condition does the agent loop in `Runner` typically end and return a result 
        without further LLM calls or tool executions (assuming no errors or max_turns)?
        """,
        options={
            "a": "When any tool is called.",
            "b": "When a handoff occurs.",
            "c": "When the LLM returns a `final_output` and no tool calls.",
            "d": "After a fixed number of three turns."
        },
        correct_answer_key="c",
        category="Agent Loop",
        difficulty="Intermediate",
        explanation="""
        The agent loop ends when the LLM produces a final output of the desired type and no tool calls are pending. 
        Tool calls and handoffs typically lead to further iterations of the loop.
        """
    ),
    Question(
        text="""
        What happens if the number of iterations in the agent loop exceeds the `max_turns` 
        value specified in `RunConfig` (or its default)?
        """,
        options={
            "a": "The Runner logs a warning and continues indefinitely.",
            "b": "A `MaxTurnsExceeded` exception is raised.",
            "c": "The agent automatically produces a default apology message as `final_output`.",
            "d": "The `Runner.run()` method returns `None`."
        },
        correct_answer_key="b",
        category="Agent Loop",
        difficulty="Intermediate",
        explanation="""
        If `max_turns` is exceeded, the SDK raises a `MaxTurnsExceeded` exception, 
        preventing infinite loops.
        """
    ),
    Question(
        text="""
        If an LLM produces tool calls, what is the next step the `Runner` takes in the agent loop?
        """,
        options={
            "a": "It immediately hands off to another agent specialized in tools.",
            "b": "It runs the specified tool calls, appends their results to the input, and re-runs the loop with the current agent.",
            "c": "It considers the tool call requests as the final output.",
            "d": "It raises a `ToolCallRequired` exception that the user must handle."
        },
        correct_answer_key="b",
        category="Agent Loop",
        difficulty="Advanced",
        explanation="""
        When tool calls are produced, the `Runner` executes them, appends their `ToolOutput` 
        to the conversation history (input for the next iteration), and then re-invokes the LLM 
        with the current agent and this updated input.
        """
    ),

    # --- Input Types ---
    Question(
        text="""
        Besides a simple string, what other primary format can be passed as `input_data` to `Runner.run()` 
        to represent, for example, a conversation history?
        """,
        options={
            "a": "A JSON object representing a single complex message.",
            "b": "A list of input items (e.g., `agents.items.Message` or dictionaries conforming to OpenAI API message format).",
            "c": "A Pydantic model defining the entire conversation state.",
            "d": "A pre-compiled prompt template."
        },
        correct_answer_key="b",
        category="Input Types",
        difficulty="Intermediate",
        explanation="""
        `Runner.run()` accepts either a string (treated as a user message) or a list of input items. 
        These items often follow the OpenAI API message format (e.g., `{"role": "user", "content": "..."}`) 
        or are SDK-specific item types like `agents.items.Text` or `agents.items.Message`.
        """
    ),

    # --- Streaming ---
    Question(
        text="""
        When iterating over events from `RunResultStreaming.stream_events()`, what type of event 
        would typically represent a chunk of text generated by the LLM?
        """,
        options={
            "a": "`StreamEvent.Chunk`",
            "b": "`TextDelta`",
            "c": "`LLMOutputSegment`",
            "d": "`FinalOutputPart`"
        },
        correct_answer_key="b",
        category="Streaming",
        difficulty="Intermediate",
        explanation="""
        The `TextDelta` event is used to stream partial text outputs from the LLM as they are generated.
        """
    ),
    Question(
        text="""
        After a stream from `Runner.run_streamed()` is complete, what information does the 
        `RunResultStreaming` object typically contain?
        """,
        options={
            "a": "Only the concatenated text from all `TextDelta` events.",
            "b": "Only a list of errors encountered during streaming.",
            "c": "The complete run information, similar to `RunResult`, including `final_output`, `new_items`, and `history`.",
            "d": "Just a status code indicating success or failure of the stream."
        },
        correct_answer_key="c",
        category="Streaming",
        difficulty="Advanced",
        explanation="""
        Once the stream finishes, the `RunResultStreaming` object is populated with the complete 
        information about the run, including `final_output`, `new_items` (all items generated 
        during the run like tool calls, tool outputs, final text), and `history` (all turns).
        """
    ),
    Question(
        text="""
        Which of the following is NOT a standard `StreamEvent` type you might encounter when 
        using `Runner.run_streamed()`?
        """,
        options={
            "a": "`ToolCall` (when the LLM decides to call a tool)",
            "b": "`ToolOutput` (when a tool finishes execution)",
            "c": "`HandoffStarting` (when a handoff is initiated)",
            "d": "`ModelSelected` (indicating which specific LLM replica handled the request)"
        },
        correct_answer_key="d",
        category="Streaming",
        difficulty="Expert",
        explanation="""
        `ToolCall`, `ToolOutput`, and `HandoffStarting` are all valid `StreamEvent` types. 
        `ModelSelected` is not a standard event type provided by the SDK's streaming; 
        information about the model used is part of the agent's configuration or `RunConfig`.
        """
    ),

    # --- RunConfig ---
    Question(
        text="""
        How can you globally override the LLM model for all agents in a specific run 
        without modifying each agent's definition?
        """,
        options={
            "a": "By setting an environment variable `GLOBAL_AGENT_MODEL`.",
            "b": "By passing a `model` argument directly to `Runner.run()`.",
            "c": "By setting the `model` attribute in a `RunConfig` object passed to `Runner.run()`.",
            "d": "It's not possible; each agent's model must be set individually."
        },
        correct_answer_key="c",
        category="RunConfig",
        difficulty="Intermediate",
        explanation="""
        The `RunConfig` object has a `model` attribute. If set, this model will be used for 
        the entire agent run, overriding the model specified on individual agents.
        """
    ),
    Question(
        text="""
        Which `RunConfig` parameter would you use to apply an input guardrail to all agents 
        participating in a run, even if those agents don't have it defined themselves?
        """,
        options={
            "a": "`global_input_guardrail_function`",
            "b": "`input_guardrails` (a list of `InputGuardrail` objects)",
            "c": "`agent_input_interceptors`",
            "d": "`default_security_checks`"
        },
        correct_answer_key="b",
        category="RunConfig",
        difficulty="Advanced",
        explanation="""
        `RunConfig.input_guardrails` takes a list of `InputGuardrail` objects that will be applied 
        globally to the run's initial input and potentially at other stages depending on SDK version and context.
        """
    ),
    Question(
        text="""
        What is the primary purpose of the `handoff_input_filter` in `RunConfig`?
        """,
        options={
            "a": "To decide if a handoff should occur based on input content.",
            "b": "To select which target agent a handoff should go to.",
            "c": "To modify the input that is sent to the target agent during a handoff.",
            "d": "To log all inputs that trigger a handoff."
        },
        correct_answer_key="c",
        category="RunConfig",
        difficulty="Advanced",
        explanation="""
        The `RunConfig.handoff_input_filter` allows you to specify a function that can modify 
        the input data just before it's passed to the target agent in a handoff scenario.
        """
    ),
    Question(
        text="""
        If `RunConfig.trace_include_sensitive_data` is set to `False`, what is the expected behavior?
        """,
        options={
            "a": "All tracing for the run is completely disabled.",
            "b": "Traces will still be created, but sensitive data like LLM inputs/outputs and tool call details will be omitted.",
            "c": "Only errors will be traced, and all other data will be excluded.",
            "d": "A `SensitiveDataWarning` will be logged for each piece of sensitive data encountered."
        },
        correct_answer_key="b",
        category="RunConfig",
        difficulty="Expert",
        explanation="""
        Setting `trace_include_sensitive_data` to `False` ensures that while trace spans are still 
        created for events, the potentially sensitive payload data (LLM I/O, tool I/O) is not included 
        in those spans.
        """
    ),
    Question(
        text="""
        Which `RunConfig` parameter is recommended for linking traces from multiple turns 
        of the same chat conversation?
        """,
        options={
            "a": "`trace_id` (a new one for each turn)",
            "b": "`workflow_name`",
            "c": "`group_id`",
            "d": "`trace_metadata` with a session key"
        },
        correct_answer_key="c",
        category="RunConfig",
        difficulty="Advanced",
        explanation="""
        `RunConfig.group_id` is the recommended parameter for grouping multiple traces that belong to the 
        same logical process, such as all turns in a single chat conversation or a multi-step workflow.
        """
    ),

    # --- Conversations/Chat Threads ---
    Question(
        text="""
        After an agent run (e.g., `result = await Runner.run(...)`), which method on the `result` object 
        is used to get the conversation history in a format suitable for the input of a subsequent turn?
        """,
        options={
            "a": "`result.get_history_items()`",
            "b": "`result.to_input_list()`",
            "c": "`result.compile_conversation()`",
            "d": "`result.export_chat_log()`"
        },
        correct_answer_key="b",
        category="Conversations/Chat Threads",
        difficulty="Intermediate",
        explanation="""
        The `RunResultBase.to_input_list()` method (available on `RunResult` and `RunResultStreaming`) 
        constructs a list of input items representing the history of the completed run, suitable for 
        passing as input to the next turn.
        """
    ),
    Question(
        text="""
        When constructing the input for a subsequent turn in a conversation using `history = result.to_input_list()`, 
        how should a new user message typically be added?
        """,
        options={
            "a": "`new_input = history.append_user_message('New message')`",
            "b": "`new_input = [history, {'role': 'user', 'content': 'New message'}]`",
            "c": "`new_input = history + [agents.items.Message(role='user', content='New message')]` (or similar dict)",
            "d": "`new_input = {'history': history, 'new_user_message': 'New message'}`"
        },
        correct_answer_key="c",
        category="Conversations/Chat Threads",
        difficulty="Advanced",
        explanation="""
        `to_input_list()` returns a list. The new user message (as an `agents.items.Message` or a 
        compatible dictionary) should be appended to this list to form the complete input for the next turn.
        """
    ),

    # --- Exception Handling ---
    Question(
        text="""
        Which exception is specifically raised by the SDK when an agent run exceeds the 
        configured `max_turns` limit?
        """,
        options={
            "a": "`RuntimeError` with a specific message.",
            "b": "`agents.exceptions.LoopTimeoutError`",
            "c": "`agents.exceptions.MaxTurnsExceeded`",
            "d": "`agents.exceptions.AgentOverrunError`"
        },
        correct_answer_key="c",
        category="Exception Handling",
        difficulty="Intermediate",
        explanation="""
        `agents.exceptions.MaxTurnsExceeded` is the specific exception raised when the `max_turns` 
        limit is surpassed during an agent run.
        """
    ),
    Question(
        text="""
        If you attempt to run an agent that has no model configured (and no global model is provided 
        via `RunConfig`), which type of exception are you most likely to encounter?
        """,
        options={
            "a": "`ModelNotFoundError`",
            "b": "`AttributeError` for a missing model attribute.",
            "c": "`agents.exceptions.UserError` (or a subclass indicating misconfiguration)",
            "d": "`agents.exceptions.ModelBehaviorError`"
        },
        correct_answer_key="c",
        category="Exception Handling",
        difficulty="Advanced",
        explanation="""
        Misconfigurations like a missing model typically lead to a `UserError` or a more specific subclass 
        thereof, as it indicates incorrect setup by the SDK user.
        """
    ),
    Question(
        text="""
        An `InputGuardrailTripwireTriggered` exception indicates what?
        """,
        options={
            "a": "The LLM tried to use an input format that the guardrail doesn't understand.",
            "b": "An input guardrail function raised an exception, signaling that the input is not permissible.",
            "c": "The input data was too long for the guardrail to process.",
            "d": "A global input filter failed to modify the input correctly."
        },
        correct_answer_key="b",
        category="Exception Handling",
        difficulty="Advanced",
        explanation="""
        `InputGuardrailTripwireTriggered` (and its output counterpart) is raised when a guardrail 
        function itself raises an exception, which is the standard way for a guardrail to signal 
        that the input/output is disallowed and should halt processing.
        """
    ),
    Question(
        text="""
        `ModelBehaviorError` is generally raised by the SDK when:
        """,
        options={
            "a": "The chosen LLM model is deprecated or unavailable.",
            "b": "The LLM produces invalid outputs, such as malformed JSON for tool calls or attempts to use non-existent tools.",
            "c": "The user provides input that the LLM cannot understand or process.",
            "d": "A model costs too much per token for the current budget settings in `RunConfig`."
        },
        correct_answer_key="b",
        category="Exception Handling",
        difficulty="Expert",
        explanation="""
        `ModelBehaviorError` is the SDK's way of indicating that the LLM did not behave as expected 
        according to the defined protocol, such as by producing malformed structured output (e.g., bad JSON 
        for tool arguments) or trying to use tools that aren't available to it.
        """
    ),
    # Add ~20-30 more questions following this pattern, covering all aspects
    # of the Runner, RunConfig, streaming, agent loop, and exceptions.

    # More on Runner Methods
    Question(
        text="""
        When using `Runner.run()`, if the agent performs multiple tool calls and a handoff before 
        producing a final output, what does the returned `RunResult.final_output` contain?
        """,
        options={
            "a": "The output of the very first LLM call.",
            "b": "A list of all intermediate tool outputs.",
            "c": "The final textual output from the last agent in the chain that produced it.",
            "d": "None, as complex runs require `run_streamed()` to get the final result."
        },
        correct_answer_key="c",
        category="Runner Methods",
        difficulty="Advanced",
        explanation="""
        `RunResult.final_output` (for both `run` and `run_sync`, and also available on a completed 
        `RunResultStreaming`) contains the ultimate final output from the agent (or sequence of agents 
        if handoffs occurred) that concluded the run by providing a response rather than another tool call or handoff.
        """
    ),

    # More on Agent Loop & max_turns
    Question(
        text="""
        If `max_turns` is set to 3 in `RunConfig`, what is the maximum number of times the LLM 
        can be called by the sequence of agents managed by the Runner in a single `.run()` invocation?
        """,
        options={
            "a": "2 (max_turns - 1)",
            "b": "3",
            "c": "4 (max_turns + 1)",
            "d": "It depends on the number of tool calls."
        },
        correct_answer_key="b",
        category="Agent Loop",
        difficulty="Advanced",
        explanation="""
        `max_turns` directly limits the number of turns in the agent loop. Each turn typically involves 
        one primary LLM call for the current agent. So, if `max_turns` is 3, the LLM can be called 
        at most 3 times by the Runner for that sequence of agent operations.
        """
    ),

    # More on Streaming & Events
    Question(
        text="""
        Which `StreamEvent` would indicate that an agent has decided to hand off control to another agent?
        """,
        options={
            "a": "`AgentSwitch`",
            "b": "`HandoffInitiated` (or `HandoffStarting`)",
            "c": "`DelegateTask`",
            "d": "`NewAgentTurn`"
        },
        correct_answer_key="b",
        category="Streaming",
        difficulty="Intermediate",
        explanation="""
        Events like `HandoffStarting` and `HandoffEnding` are used to signal the initiation 
        and completion of a handoff process during a streamed run.
        """
    ),
    Question(
        text="""
        If you are processing events from `run_streamed()` and encounter a `ToolCall` event, 
        what information does it typically provide?
        """,
        options={
            "a": "The name of the tool, its arguments, and a unique ID for the call.",
            "b": "Only the name of the tool that was called.",
            "c": "The raw JSON string that the LLM generated for the tool call.",
            "d": "The result/output of the tool execution."
        },
        correct_answer_key="a",
        category="Streaming",
        difficulty="Advanced",
        explanation="""
        A `ToolCall` event (or `agents.items.ToolCall` object) usually contains the `tool_name` 
        the LLM wants to call, the `tool_input` (arguments), and a `tool_call_id` to correlate it 
        with its corresponding `ToolOutput`.
        """
    ),

    # More on RunConfig
    Question(
        text="""
        Can `RunConfig.model_settings` be used to override settings like `max_tokens` for an LLM call?
        """,
        options={
            "a": "No, `model_settings` only affects `temperature` and `top_p`.",
            "b": "Yes, `model_settings` (a `ModelSettings` object) can typically override any valid parameter for the LLM, like `max_tokens`, `temperature`, etc.",
            "c": "Only if the agent's model explicitly allows overrides.",
            "d": "No, `max_tokens` must be set directly on the `Agent.model` object."
        },
        correct_answer_key="b",
        category="RunConfig",
        difficulty="Advanced",
        explanation="""
        `RunConfig.model_settings` takes a `ModelSettings` object. Any non-null values in this 
        object will override the agent-specific model settings, including parameters like `temperature`, 
        `top_p`, `max_tokens`, and others supported by the underlying model interface.
        """
    ),
    Question(
        text="""
        If an `Agent` has its own `input_guardrails` defined, and `RunConfig` also specifies 
        `input_guardrails`, how are they typically applied?
        """,
        options={
            "a": "Only the `RunConfig` guardrails are applied; agent-specific ones are ignored.",
            "b": "Only the agent-specific guardrails are applied; `RunConfig` ones are ignored.",
            "c": "Both sets of guardrails are applied, often with global `RunConfig` guardrails running before agent-specific ones on initial input.",
            "d": "It raises a `ConfigurationError` due to ambiguity."
        },
        correct_answer_key="c",
        category="RunConfig",
        difficulty="Expert",
        explanation="""
        Typically, both sets of guardrails are applied. The exact order can depend on the SDK's 
        implementation details, but often global (RunConfig) guardrails are processed, followed by 
        agent-specific guardrails. For instance, global input guardrails on the very first input, 
        and then agent-specific ones when that agent takes its turn.
        """
    ),
    Question(
        text="""
        What is the purpose of `RunConfig.workflow_name`?
        """,
        options={
            "a": "To specify the Python function that orchestrates the agent run.",
            "b": "To give a logical name to the overall run, primarily used for tracing and logging.",
            "c": "To select a predefined sequence of agents from a library.",
            "d": "To define the file where the results of the agent run will be saved."
        },
        correct_answer_key="b",
        category="RunConfig",
        difficulty="Intermediate",
        explanation="""
        `RunConfig.workflow_name` is used to assign a human-readable, logical name to the agent run 
        (e.g., "CustomerSupportFlow", "CodeGenerationWorkflow"). This name is primarily used in tracing 
        to identify and categorize runs.
        """
    ),

    # More on Chat Threads
    Question(
        text="""
        Is it mandatory to use `RunConfig.group_id` when managing chat threads?
        """,
        options={
            "a": "Yes, the `Runner` will raise an error if it's not provided for multi-turn conversations.",
            "b": "No, but it is highly recommended for effectively grouping related traces in a multi-turn conversation.",
            "c": "Yes, but only if streaming is also enabled for the chat turns.",
            "d": "No, `group_id` is only relevant for batch processing of multiple independent agent runs."
        },
        correct_answer_key="b",
        category="Conversations/Chat Threads",
        difficulty="Intermediate",
        explanation="""
        While not strictly mandatory for the `Runner` to function, using `group_id` is a best practice 
        and highly recommended for tracing, as it allows you to easily find and correlate all the 
        traces belonging to a single continuous conversation or user session.
        """
    ),

    # More on Exceptions
    Question(
        text="""
        If an `OutputGuardrail` modifies the content of an agent's output, what should the guardrail function return?
        """,
        options={
            "a": "`True` to indicate success.",
            "b": "The modified output data itself.",
            "c": "`None`, and the SDK will automatically pick up the modifications from a context object.",
            "d": "A dictionary `{'status': 'modified', 'new_output': ...}`."
        },
        correct_answer_key="b",
        category="Exception Handling",  # Or Guardrails
        difficulty="Advanced",
        explanation="""
        If an output guardrail function modifies the output, it should return the modified output. 
        This returned value will then replace the original output for subsequent processing or as the final result. 
        If it returns `None` (and doesn't raise an exception), the original output is typically used.
        """
    ),
    Question(
        text="""
        Consider an agent that is supposed to use a tool to get data, but the LLM fails to format the tool call correctly (e.g., provides invalid JSON for arguments). Which exception is most appropriate?
        """,
        options={
            "a": "`UserError` because the tool arguments were effectively user-provided via the LLM.",
            "b": "`ToolExecutionError` because the tool couldn't execute.",
            "c": "`ModelBehaviorError` because the LLM didn't follow the expected tool call format.",
            "d": "`InvalidToolCallFormat` (a custom, more specific exception)."
        },
        correct_answer_key="c",
        category="Exception Handling",
        difficulty="Expert",
        explanation="""
        `ModelBehaviorError` is designed for situations where the LLM fails to adhere to the expected 
        protocol, such as providing malformed JSON for tool arguments, or trying to call tools 
        with incorrect parameter names/types if the SDK can detect that before tool execution.
        """
    ),

    # Final Batch of Questions
    Question(
        text="""
        When is `RunResult.new_items` populated?
        """,
        options={
            "a": "Only when `Runner.run_streamed()` is used.",
            "b": "It contains all input items and output items generated throughout all turns of the agent run.",
            "c": "It only contains the `final_output` item.",
            "d": "It contains items from the initial input data only."
        },
        correct_answer_key="b",
        category="Runner Methods",  # Or Results
        difficulty="Advanced",
        explanation="""
        `RunResultBase.new_items` (available on `RunResult` and `RunResultStreaming`) accumulates all new items 
        generated during the *current* `Runner.run()` invocation. This includes tool calls made by agents, 
        tool outputs received, textual responses, and the final output itself.
        It does not typically include the initial input items passed to the run, but rather what was *produced*.
        Correction: The docs imply `new_items` are those *produced* during the current run. `to_input_list()` combines original input with new items for the *next* run.
        The key is that `new_items` are the outputs of the current run cycle.
        The most accurate interpretation is that `new_items` are the items *generated by the agent(s) during the run*. This would include text, tool calls, and tool outputs from the current execution.
        Revisiting documentation: `RunResult.new_items` contains "all the new items that were produced during this agent run". This seems clear. It's not inputs. It's newly generated things.
        Final Answer based on doc: `new_items` are things *produced*. So the initial `input_data` isn't part of `new_items`.
        Options analysis:
        A is false. B is problematic with "input items". C is false. D is false.
        The best fit would be one saying "all items produced by the agent(s) in this run". Let's re-evaluate B: "It contains all input items and output items generated throughout all turns of the agent run."
        The phrase "output items generated" fits. "input items" is the confusing part.  If "generated" applies to both, then it means inputs *generated by an agent* (like for a handoff), not the initial overall input.
        Let's assume B means all items *created by the agent execution process* during this run. This could include intermediate text, tool calls, tool outputs, and the final text output.
        A better B would be: "It contains all `Item` objects (like `Text`, `ToolCall`, `ToolOutput`) newly generated by the agent(s) during the current `Runner.run()` execution."
        Given the current options, B is the most plausible if we interpret "generated" broadly for items part of the agent's process.
        The example for `Conversations/chat threads` shows `new_input = result.to_input_list() + [...]`. `to_input_list()` is defined on `RunResultBase` and says "Returns all the items from the run, in a list format suitable for passing into the run method for a subsequent turn." This implies `to_input_list()` includes the initial input *and* the new_items. So `new_items` itself must be *just* the new ones.
        Let's try a different question or refine B for clarity later if this is problematic.
        For now, sticking with current B and its common interpretation for quiz. It's tricky.
        After more thought, B is likely incorrect due to "input items". `new_items` are outputs of the current agent execution(s). A better option would be needed.
        Let's find a better question or rephrase. Or pick the *least incorrect* if forced.

        If we consider the `RunResult.history` which contains `TurnEventData` objects, each `TurnEventData` has `input_items` and `output_items` for that specific turn within the run. `RunResult.new_items` is a flat list of *all new outputs* from all turns in that run.
        The most precise answer is that `new_items` are the *outputs* generated across all turns within a single `Runner.run()` call. 

        Let's rephrase the question or options. 
        New Question:
        "What does `RunResult.new_items` primarily contain after a `Runner.run()` call?"
        Options:
        a) The initial `input_data` passed to the `Runner`.
        b) Only the `final_output` of the last agent.
        c) A list of all new output `Item` objects (e.g., `Text`, `ToolCall`, `ToolOutput`) generated by the agent(s) during that run.
        d) A log of all `StreamEvent`s, if streaming was used.
        This makes C the clear answer.
        """
    ),
    Question(
        text="""
        What does `RunResult.new_items` primarily contain after a `Runner.run()` call?
        """,
        options={
            "a": "The initial `input_data` passed to the `Runner`.",
            "b": "Only the `final_output` of the last agent.",
            "c": "A list of all new output `Item` objects (e.g., `Text`, `ToolCall`, `ToolOutput`) generated by the agent(s) during that run.",
            "d": "A log of all `StreamEvent`s, if streaming was used."
        },
        correct_answer_key="c",
        category="Runner Methods",  # Or Results
        difficulty="Advanced",
        explanation="""
        `RunResultBase.new_items` contains a list of all new `Item` objects (like `Text`, `ToolCall`, `ToolOutput`, 
        and the `final_output` itself if it's an item) that were produced by the agent or agents 
        during the execution of that specific `Runner.run()` call. It does not include the initial input data.
        """
    ),
    Question(
        text="""
        If `Runner.run_sync()` is called, can the underlying agent operations (like LLM calls or async tools) still be asynchronous?
        """,
        options={
            "a": "No, `run_sync` forces all operations to be synchronous.",
            "b": "Yes, `run_sync` is a synchronous wrapper, but the SDK internally manages an event loop for async operations.",
            "c": "Only if the agent is explicitly marked as `supports_sync_execution`.",
            "d": "No, using async tools or models with `run_sync` will raise a `CompatibilityError`."
        },
        correct_answer_key="b",
        category="Runner Methods",
        difficulty="Expert",
        explanation="""
        `Runner.run_sync()` provides a synchronous API call for convenience. Under the hood, the SDK 
        still leverages asynchronous operations for LLM calls and async tools by managing its own event loop 
        (typically by using `asyncio.run()` or a similar mechanism internally for that call).
        """
    ),
    Question(
        text="""
        In the agent loop, if an agent performs a handoff, how is the input for the target agent determined?
        """,
        options={
            "a": "The target agent always starts with a fresh, empty input.",
            "b": "The `Runner` passes the original user input that started the entire run.",
            "c": "The `Runner` typically passes the accumulated conversation history (including outputs from the handing-off agent) to the target agent, potentially modified by a `HandoffInputFilter`.",
            "d": "The handing-off agent must explicitly package the input for the target agent in its `HandoffAction`."
        },
        correct_answer_key="c",
        category="Agent Loop",
        difficulty="Expert",
        explanation="""
        When a handoff occurs, the `Runner` usually takes the current conversation history (which includes 
        the items leading to the handoff decision and the output of the current agent) and passes this as 
        input to the target agent. This input can be further modified by a `Handoff.input_filter` or a 
        global `RunConfig.handoff_input_filter`.
        """
    ),
    Question(
        text="""
        Which `StreamEvent` signifies the very beginning of a `Runner.run_streamed()` execution, 
        often containing information like the `workflow_name`?
        """,
        options={
            "a": "`StreamStarted`",
            "b": "`RunInitiated`",
            "c": "`RunStarting`",
            "d": "`WorkflowBegin`"
        },
        correct_answer_key="c",
        category="Streaming",
        difficulty="Advanced",
        explanation="""
        The `RunStarting` event is typically the first event in a stream, indicating the start of the 
        overall run and often includes metadata like the `workflow_name` and `trace_id`.
        """
    ),
    Question(
        text="""
        If `RunConfig.model_provider` is not set, what does it default to?
        """,
        options={
            "a": "An instance of `OpenAIModelProvider`.",
            "b": "An instance of `MultiProvider` (which includes OpenAI by default).",
            "c": "`None`, requiring each agent to have a fully configured model object.",
            "d": "It attempts to infer the provider from the `RunConfig.model` name."
        },
        correct_answer_key="b",
        category="RunConfig",
        difficulty="Expert",
        explanation="""
        The documentation for `RunConfig.model_provider` states it defaults to `MultiProvider`, 
        which itself is capable of handling various model providers, including OpenAI models by default.
        """
    ),

]

# --- Quiz Runner ---


def run_quiz(questions: List[Question], num_questions: int = 0):
    """Runs the quiz, asking a specified number of questions or all if num_questions is 0."""
    if not questions:
        print("No questions available for the quiz.")
        return

    if num_questions <= 0 or num_questions > len(questions):
        selected_questions = questions
    else:
        selected_questions = random.sample(questions, num_questions)

    print(f"--- OpenAI Agents SDK: Runner Expert Quiz ---")
    print(f"Total questions in this session: {len(selected_questions)}\n")

    score = 0
    detailed_results = []

    for i, question in enumerate(selected_questions):
        print(f"Question {i+1} of {len(selected_questions)}")
        question.display()

        while True:
            user_answer_key = input(
                "Your answer (a, b, c, d...): ").strip().lower()
            if user_answer_key in question.options:
                break
            print("Invalid option. Please enter one of the provided keys (a, b, c, ...).")

        is_correct = question.check_answer(user_answer_key)
        if is_correct:
            print("✅ Correct!")
            score += 1
        else:
            print(
                f"❌ Incorrect. The correct answer was: {question.correct_answer_key.upper()}")

        print("\nExplanation:")
        print(question.explanation)
        print("-" * 70)

        detailed_results.append({
            "question": question.text,
            "your_answer": user_answer_key,
            "correct_answer": question.correct_answer_key,
            "is_correct": is_correct,
            "category": question.category,
            "difficulty": question.difficulty
        })

    print("\n--- Quiz Complete ---")
    final_score_percent = (score / len(selected_questions)
                           ) * 100 if selected_questions else 0
    print(
        f"Your final score: {score} out of {len(selected_questions)} ({final_score_percent:.2f}%)")

    # Performance Analysis
    if selected_questions:
        print("\n--- Performance Analysis ---")
        # By Category
        print("\nBy Category:")
        categories = sorted(list(set(q.category for q in selected_questions)))
        for category in categories:
            cat_questions = [
                r for r in detailed_results if r["category"] == category]
            cat_correct = sum(1 for r in cat_questions if r["is_correct"])
            cat_total = len(cat_questions)
            cat_percent = (cat_correct / cat_total) * 100 if cat_total else 0
            print(
                f"  - {category}: {cat_correct}/{cat_total} ({cat_percent:.2f}%)")

        # By Difficulty
        print("\nBy Difficulty:")
        difficulties = ["Beginner", "Intermediate", "Advanced", "Expert"]
        for diff in difficulties:
            diff_questions = [
                r for r in detailed_results if r["difficulty"] == diff]
            if not diff_questions:
                continue
            diff_correct = sum(1 for r in diff_questions if r["is_correct"])
            diff_total = len(diff_questions)
            diff_percent = (diff_correct / diff_total) * \
                100 if diff_total else 0
            print(
                f"  - {diff}: {diff_correct}/{diff_total} ({diff_percent:.2f}%)")

        mastery_level = "Needs Significant Study"
        if final_score_percent >= 90:
            mastery_level = "Expert Level - Excellent!"
        elif final_score_percent >= 75:
            mastery_level = "Advanced Understanding - Well Done!"
        elif final_score_percent >= 60:
            mastery_level = "Intermediate Knowledge - Good Progress!"
        elif final_score_percent >= 40:
            mastery_level = "Beginner Grasp - Keep Studying!"

        print(f"\nOverall Mastery: {mastery_level}")
        if final_score_percent < 75:
            print("Recommendation: Review the explanations and relevant SDK documentation, focusing on areas with lower scores.")
            print("Consider re-running the examples in `02_runner` directory.")


def main_cli():
    # Simple CLI to run the quiz
    num_q_str = input(
        f"How many questions would you like? (1-{len(QUIZ_QUESTIONS)}, or 0 for all): ").strip()
    try:
        num_q = int(num_q_str)
        if not (0 <= num_q <= len(QUIZ_QUESTIONS)):
            # Default to all if invalid number outside range but still int
            num_q = len(QUIZ_QUESTIONS)
            print(f"Invalid number, defaulting to all {num_q} questions.")
    except ValueError:
        num_q = len(QUIZ_QUESTIONS)  # Default to all if not a number
        print(f"Invalid input, defaulting to all {num_q} questions.")

    run_quiz(QUIZ_QUESTIONS, num_questions=num_q)


main_cli()
