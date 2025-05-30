"""
01_custom_exceptions_hierarchy.py

This module demonstrates defining and using a hierarchy of custom exceptions
for an agentic workflow, inheriting from the SDK's base AgentsException.
This allows for more specific error handling and diagnostics.

Key Concepts:
- Inheriting from agents.exceptions.AgentsException
- Defining specific error types (e.g., ToolProcessingError, AgentInitializationError)
- Raising and catching custom exceptions
- Including contextual information in custom exceptions
"""

from agents import Agent, Runner, function_tool, exceptions
import asyncio
import logging
import sys
import os
from typing import Any, Dict, Optional, TypedDict

# Add project root to sys.path to help resolve modules when running script directly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Reverted to original import based on documentation, hoping sys.path adjustment helps
# from agents.providers.openai_chat_completions import OpenAIChatCompletionsModel # Temporarily commented out

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Custom Exception Hierarchy
# ============================================================================


class MyAgentWorkflowException(exceptions.AgentsException):
    """Base custom exception for our specific agent workflow."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}

    def __str__(self):
        return f"{super().__str__()} (Details: {self.details})"


class AgentInitializationError(MyAgentWorkflowException):
    """Raised when an agent fails to initialize correctly."""

    def __init__(self, agent_id: str, reason: str, config: Optional[Dict[str, Any]] = None):
        message = f"Agent '{agent_id}' failed to initialize: {reason}"
        details = {"agent_id": agent_id,
                   "reason": reason, "config": config or {}}
        super().__init__(message, details)


class ToolProcessingError(MyAgentWorkflowException):
    """Raised when a tool encounters an error during execution."""

    def __init__(self, tool_name: str, error_message: str, input_args: Optional[Dict[str, Any]] = None):
        message = f"Error processing tool '{tool_name}': {error_message}"
        details = {"tool_name": tool_name,
                   "error_message": error_message, "input_args": input_args or {}}
        super().__init__(message, details)


class AgentCommunicationError(MyAgentWorkflowException):
    """Raised during errors in agent-to-agent communication."""

    def __init__(self, source_agent_id: str, target_agent_id: str, error_message: str):
        message = f"Communication error between '{source_agent_id}' and '{target_agent_id}': {error_message}"
        details = {"source_agent_id": source_agent_id,
                   "target_agent_id": target_agent_id, "error_message": error_message}
        super().__init__(message, details)


class DataValidationError(MyAgentWorkflowException):
    """Raised when input or output data validation fails."""

    def __init__(self, data_description: str, validation_errors: Dict[str, str], data: Optional[Any] = None):
        message = f"Data validation failed for '{data_description}'."
        details = {"data_description": data_description, "validation_errors": validation_errors,
                   "data_preview": str(data)[:100] if data else None}
        super().__init__(message, details)


class ConfigurationError(MyAgentWorkflowException):
    """Raised when there's an issue with agent or system configuration."""

    def __init__(self, component: str, parameter: str, issue: str):
        message = f"Configuration error in '{component}' for parameter '{parameter}': {issue}"
        details = {"component": component,
                   "parameter": parameter, "issue": issue}
        super().__init__(message, details)

# ============================================================================
# Example Agent and Tools that Might Raise Custom Exceptions
# ============================================================================

# Define a TypedDict for the tool's input structure


class FaultyDataInput(TypedDict):
    required_field: str
    numeric_value: float
    optional_field: Optional[str]


# Undecorated internal logic function for direct testing
def _internal_faulty_data_processor_logic(data: FaultyDataInput) -> Dict[str, Any]:
    """The core logic for faulty_data_processor, can be tested directly."""
    logger.info(
        f"Internal logic for '(faulty_data_processor)' called with: {data}")

    # We are now relying on the caller to provide data that conforms to FaultyDataInput.
    # The explicit checks for `required_field` presence or `numeric_value` type
    # are less critical here if the input *must* be FaultyDataInput.
    # However, for demo, we can keep a conceptual check or rely on TypedDict's nature.

    # This check demonstrates raising DataValidationError if, despite TypedDict,
    # a key considered essential by business logic is missing or None.
    # Note: `data["required_field"]` would raise KeyError if not present.
    # `data.get("required_field")` is safer if checking optional presence.
    # For a TypedDict field not marked Optional, it should always be present.
    if not data.get("required_field"):  # Example: check if it's empty, not just present
        raise DataValidationError(
            data_description="input for faulty_data_processor (internal logic)",
            validation_errors={
                "required_field": "Required field cannot be empty"},
            data=data
        )

    if data["numeric_value"] < 0:
        raise ToolProcessingError(
            tool_name="faulty_data_processor (internal logic)",
            error_message="Negative numeric values are not allowed for this operation.",
            input_args=dict(data)  # Explicitly convert TypedDict to dict
        )

    processed_data = {"status": "success", "input_received": data,
                      "result_value": data["numeric_value"] * 2}
    logger.info(
        f"Internal logic for '(faulty_data_processor)' processed data: {processed_data}")
    return processed_data


@function_tool
def faulty_data_processor(data: FaultyDataInput) -> Dict[str, Any]:
    """A tool that processes data. Wraps the internal logic."""
    # The @function_tool and TypedDict handle input validation against the schema.
    # The call to internal logic assumes data is already validated to conform to FaultyDataInput.
    logger.info(
        f"Tool '(faulty_data_processor)' called by agent/runner with validated data: {data}")
    return _internal_faulty_data_processor_logic(data)


class ConfigurableAgent(Agent):
    """An agent that requires specific configuration and uses tools."""

    def __init__(self, agent_id: str, config: Dict[str, Any], **kwargs):
        if not config.get("api_key"):
            raise AgentInitializationError(
                agent_id=agent_id,
                reason="Missing 'api_key' in configuration.",
                config=config
            )

        if config.get("invalid_setting", False):
            raise ConfigurationError(
                component=f"Agent {agent_id}",
                parameter="invalid_setting",
                issue="This setting has an invalid value or is deprecated."
            )

        super().__init__(
            name=agent_id,
            instructions="You are a configurable agent. Use your tools as instructed.",
            tools=[faulty_data_processor],
            # model=OpenAIChatCompletionsModel(model="gpt-4o-mini"), # Temporarily commented out
            **kwargs
        )
        self.agent_id = agent_id
        self.config = config
        logger.info(
            f"Agent '{self.agent_id}' initialized successfully with config: {self.config}")

# ============================================================================
# Demonstration of Raising and Catching Custom Exceptions
# ============================================================================


async def run_agent_with_error_handling(agent: Agent, user_input: str):
    """Runs the agent and demonstrates catching custom exceptions."""
    logger.info(
        f"\n--- Running agent '{agent.name}' with input: '{user_input}' ---")
    try:
        result = await Runner.run(agent, user_input)
        logger.info(f"Agent '{agent.name}' finished successfully.")
        # Safely access result output for logging
        if hasattr(result, 'output') and result.output:
            logger.info(f"Agent output: {result.output}")
        elif hasattr(result, 'outputs') and result.outputs:
            logger.info(f"Agent outputs: {result.outputs}")
        elif hasattr(result, 'messages') and result.messages:
            logger.info(
                f"Last message: {result.messages[-1].content if result.messages else 'N/A'}")
        else:
            logger.info(
                "Agent run completed, but no standard history/output attribute found on RunResult for logging.")

    except AgentInitializationError as e:
        logger.error(f"CAUGHT AgentInitializationError: {e}")
        logger.error(
            f"   Error Details: Agent ID - {e.details.get('agent_id')}, Reason - {e.details.get('reason')}")
    except ToolProcessingError as e:
        logger.error(f"CAUGHT ToolProcessingError: {e}")
        logger.error(
            f"   Error Details: Tool - {e.details.get('tool_name')}, Input - {e.details.get('input_args')}")
    except DataValidationError as e:
        logger.error(f"CAUGHT DataValidationError: {e}")
        logger.error(
            f"   Validation Errors: {e.details.get('validation_errors')}")
    except ConfigurationError as e:
        logger.error(f"CAUGHT ConfigurationError: {e}")
        logger.error(
            f"   Error Details: Component - {e.details.get('component')}, Parameter - {e.details.get('parameter')}")
    except MyAgentWorkflowException as e:  # Catch base custom exception
        logger.error(f"CAUGHT MyAgentWorkflowException (general): {e}")
    except exceptions.AgentsException as e:  # Catch any other SDK exception
        logger.error(f"CAUGHT AgentsException (SDK base): {e}")
    except Exception as e:
        logger.error(f"CAUGHT UNEXPECTED EXCEPTION: {type(e).__name__} - {e}")


async def main():
    """Main function to demonstrate custom exception handling."""
    print("🚀 Demonstrating Custom Exception Hierarchy in Agent Workflows 🚀")

    # Scenario 1: Agent Initialization Error (direct instantiation)
    logger.info("\n--- Scenario 1: Agent Initialization Error ---")
    try:
        faulty_agent_config = {"some_setting": "value"}  # Missing api_key
        ConfigurableAgent(agent_id="faulty-init-agent",
                          config=faulty_agent_config)
    except AgentInitializationError as e:
        logger.error(f"CAUGHT AgentInitializationError: {e}")
        logger.error(f"   Config provided: {e.details.get('config')}")
    except Exception as e:
        logger.error(f"UNEXPECTED error during Scenario 1: {e}")

    # Scenario 2: Configuration Error (direct instantiation)
    logger.info("\n--- Scenario 2: Configuration Error ---")
    try:
        faulty_agent_config_2 = {
            "api_key": "dummy_key", "invalid_setting": True}
        ConfigurableAgent(agent_id="faulty-config-agent",
                          config=faulty_agent_config_2)
    except ConfigurationError as e:
        logger.error(f"CAUGHT ConfigurationError: {e}")
    except Exception as e:
        logger.error(f"UNEXPECTED error during Scenario 2: {e}")

    # Scenario 3: Data Validation Error (direct tool logic call)
    logger.info(
        "\n--- Scenario 3: Data Validation Error (Direct Tool Logic Call) ---")
    try:
        # Test with an input that should make the internal logic's validation fail
        # TypedDict requires all non-Optional keys. To test missing required_field leading to empty string:
        invalid_for_logic = FaultyDataInput(
            required_field="", numeric_value=10.0, optional_field=None)
        _internal_faulty_data_processor_logic(data=invalid_for_logic)
    except DataValidationError as e:
        logger.error(
            f"CAUGHT DataValidationError from direct tool logic call: {e}")
    except TypeError as e:
        # Should not happen if FaultyDataInput is constructed correctly
        logger.error(f"CAUGHT TypeError from direct tool logic call: {e}")
    except Exception as e:
        logger.error(
            f"UNEXPECTED error during Scenario 3 direct tool logic call: {type(e).__name__} - {e}")

    # Scenario 4: Tool Processing Error (direct tool logic call)
    logger.info(
        "\n--- Scenario 4: Tool Processing Error (Direct Tool Logic Call) ---")
    try:
        negative_value_input = FaultyDataInput(
            required_field="present", numeric_value=-5.0, optional_field=None)
        _internal_faulty_data_processor_logic(data=negative_value_input)
    except ToolProcessingError as e:
        logger.error(
            f"CAUGHT ToolProcessingError from direct tool logic call: {e}")
    except Exception as e:
        logger.error(
            f"UNEXPECTED error during Scenario 4 direct tool logic call: {type(e).__name__} - {e}")

    # Initialize a working agent for agent-run scenarios
    try:
        agent_config = {"api_key": "fake_key_for_demo", "feature_flag_x": True}
        working_agent = ConfigurableAgent(
            agent_id="worker-001", config=agent_config)
    except MyAgentWorkflowException as e:
        logger.error(f"Failed to initialize working_agent: {e}")
        return  # Cannot proceed

    # Scenario 5: Successful Agent Run (formerly Scenario 3 for agent interaction)
    # Now, the agent will call the tool, and we observe the outcome from Runner.run()
    # We are less focused on *which* custom exception is caught here, but that the run completes or fails gracefully.
    logger.info(
        "\n--- Scenario 5: Agent attempts tool call that might raise DataValidationError ---")
    await run_agent_with_error_handling(
        working_agent,
        # Missing required_field
        "Call the 'faulty_data_processor' tool with this exact JSON input: { \"numeric_value\": 10 }"
    )

    # Scenario 6: Agent Run where tool might raise ToolProcessingError (formerly Scenario 4)
    logger.info(
        "\n--- Scenario 6: Agent attempts tool call that might raise ToolProcessingError ---")
    await run_agent_with_error_handling(
        working_agent,
        "Call the 'faulty_data_processor' tool with this exact JSON input: { \"required_field\": \"present\", \"numeric_value\": -5 }"
    )

    # Scenario 7: Successful Agent Run with Tool (formerly Scenario 5)
    logger.info("\n--- Scenario 7: Successful Agent Run with Tool ---")
    await run_agent_with_error_handling(
        working_agent,
        "Call the 'faulty_data_processor' tool with this exact JSON input: { \"required_field\": \"present\", \"numeric_value\": 20 }"
    )

    # Scenario 8: Simulating AgentCommunicationError (Conceptual)
    logger.info("\n--- Scenario 8: Agent Communication Error (Conceptual) ---")
    try:
        raise AgentCommunicationError(
            source_agent_id="agent-A",
            target_agent_id="agent-B",
            error_message="Target agent timed out."
        )
    except AgentCommunicationError as e:
        logger.error(f"CAUGHT AgentCommunicationError (conceptual): {e}")

    print("\n✅ Custom Exception Handling Demonstration Complete.")
    print("Review logs for details on caught exceptions.")

if __name__ == "__main__":
    # Note: This example uses a fake OpenAI API key for the OpenAIChatCompletionsModel.
    # It won't make actual API calls if the LLM isn't strictly needed to trigger the custom exceptions.
    # The focus is on the exception hierarchy and handling, not LLM interaction itself.
    # For scenarios where the LLM *must* be called to reach the exception, a real key would be needed.
    asyncio.run(main())
