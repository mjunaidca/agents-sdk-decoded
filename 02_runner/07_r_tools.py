"""
07_runner_and_tools_loop.py

Focuses on the Runner's role in handling tool calls within the agent loop.

- Runner identifying LLM tool call requests.
- Runner executing the specified tool.
- Runner appending ToolOutput to the input for the next loop iteration.
- Demonstrating tool_use_behavior options from the Runner's perspective:
    - 'run_llm_again' (default): LLM processes tool output.
    - 'stop_on_first_tool': Tool output becomes final_output immediately.
    - StopAtTools: Loop stops if a specified tool is called; its output is final.

Based on: https://openai.github.io/openai-agents-python/running_agents/#the-agent-loop
And Agent.tool_use_behavior documentation.
"""

import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from agents.agent import StopAtTools

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the OpenAI client
provider = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# --- Tools for Demo ---


@function_tool
async def get_stock_price(ticker_symbol: str) -> str:
    """Gets the current stock price for a given ticker symbol."""
    print(f"[Tool Call: get_stock_price for {ticker_symbol}]")
    if ticker_symbol.upper() == "ACME":
        return "The stock price for ACME is $123.45."
    elif ticker_symbol.upper() == "WIDGET":
        return "The stock price for WIDGET is $78.90."
    return f"Stock price for {ticker_symbol} is not available."


@function_tool
async def save_analysis_report(report_content: str) -> str:
    """Saves a financial analysis report."""
    print(
        f"[Tool Call: save_analysis_report with content: '{report_content[:50]}...']")
    # In a real scenario, this would save to a file or database
    return f"Report successfully saved. Content preview: '{report_content[:30]}...'"

# --- Agent for Demo ---
financial_analyst_agent = Agent(
    name="FinancialAnalyst",
    instructions=(
        "You are a financial analyst. Use get_stock_price to find stock prices. "
        "After analyzing, use save_analysis_report to save your findings. "
        "When saving, provide a brief summary as the report content."
    ),
    model=OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=provider),
    tools=[get_stock_price, save_analysis_report]
)


async def demo_tool_behavior_run_llm_again():
    print("\n--- Demo: tool_use_behavior = 'run_llm_again' (default) ---")
    # Default behavior: LLM processes tool output and generates a final response.
    agent = financial_analyst_agent.clone(tool_use_behavior='run_llm_again')
    user_input = "What is the stock price for ACME?"
    print(f"Input: {user_input}")
    result = await Runner.run(agent, user_input)
    print(f"Final Output: {result.final_output}")
    # Expected: LLM gets stock price, then formulates a sentence like "The stock price for ACME is $123.45."


async def demo_tool_behavior_stop_on_first_tool():
    print("\n--- Demo: tool_use_behavior = 'stop_on_first_tool' ---")
    # LLM calls the tool, and the tool's direct output becomes the final_output.
    agent = financial_analyst_agent.clone(
        tool_use_behavior='stop_on_first_tool')
    user_input = "Get ACME's stock price."
    print(f"Input: {user_input}")
    result = await Runner.run(agent, user_input)
    print(f"Final Output (Directly from tool): {result.final_output}")
    # Expected: "The stock price for ACME is $123.45." (raw output from get_stock_price)


async def demo_tool_behavior_stop_at_tools():
    print(
        "\n--- Demo: tool_use_behavior = StopAtTools(['save_analysis_report']) ---")
    # Loop continues, LLM processes tool outputs, until 'save_analysis_report' is called.
    # The output of 'save_analysis_report' becomes the final_output.
    agent = financial_analyst_agent.clone(
        tool_use_behavior=StopAtTools(
            stop_at_tool_names=['save_analysis_report'])
    )
    user_input = "Find WIDGET stock price and save an analysis stating its price."
    print(f"Input: {user_input}")
    result = await Runner.run(agent, user_input)
    print(
        f"Final Output (Directly from save_analysis_report): {result.final_output}")
    # Expected: "Report successfully saved. Content preview: 'The stock price for WIDGET is...'"


async def main():
    print("--- Running 07_runner_and_tools_loop.py ---")
    await demo_tool_behavior_run_llm_again()
    await demo_tool_behavior_stop_on_first_tool()
    await demo_tool_behavior_stop_at_tools()
    print("\n--- Finished 07_runner_and_tools_loop.py ---")

if __name__ == "__main__":
    asyncio.run(main())
