"""
06_models_quiz.py

This module provides a comprehensive quiz on OpenAI Agents SDK Models.
Focus: Test understanding of model types, configuration, providers, and optimization.

Learning Objectives:
- Assess knowledge of core model concepts and SDK features
- Validate understanding of multi-provider integration
- Test ability to apply cost and performance optimization
- Evaluate readiness for production deployment

Key Concepts:
- Model selection (OpenAI, LiteLLM, custom)
- ModelSettings parameters and use cases
- Provider integration and fallback strategies
- Cost optimization and performance tuning
- Troubleshooting and production best practices

Based on: Modules 01-05
"""

import asyncio

# ================== QUIZ QUESTIONS & ANSWERS ==================


async def run_models_quiz():
    """Run an interactive quiz on OpenAI Agents SDK Models."""
    print("🤖 OpenAI Agents SDK - Models Quiz 🤖")
    print("\nWelcome to the Models module quiz!")
    print("This quiz will test your understanding of model configuration, integration, and optimization.")
    print("Let's begin!\n")

    questions = [
        {
            "question": "What are the two primary default model types in the OpenAI Agents SDK, and what are their key differences?",
            "options": [
                "OpenAIResponsesModel (advanced features, OpenAI only) vs OpenAIChatCompletionsModel (standard features, OpenAI + compatible)",
                "OpenAIFineTuningModel (custom models) vs OpenAIBaseModel (generic models)",
                "OpenAIReasoningModel (complex logic) vs OpenAICreativeModel (text generation)",
                "OpenAICompletionModel (legacy) vs OpenAIChatModel (modern)"
            ],
            "answer": 0,
            "explanation": "OpenAIResponsesModel leverages the newer /v1/responses API for advanced features, while OpenAIChatCompletionsModel uses the standard /v1/chat/completions API for broader compatibility."
        },
        {
            "question": "How does LiteLLM enhance model integration in the OpenAI Agents SDK?",
            "options": [
                "It provides a universal interface to 100+ models from various providers (Anthropic, Google, Mistral, etc.)",
                "It optimizes OpenAI models for lower latency and cost",
                "It enables fine-tuning of custom models directly within the SDK",
                "It restricts model usage to only approved providers for enhanced security"
            ],
            "answer": 0,
            "explanation": "LiteLLM acts as a translation layer, allowing the SDK to interact with a wide range of LLM providers using a consistent API."
        },
        {
            "question": "Which ModelSettings parameter controls the randomness and creativity of model responses?",
            "options": [
                "temperature (0.0 = deterministic, 2.0 = very random)",
                "max_tokens (limits output length)",
                "top_p (nucleus sampling for vocabulary diversity)",
                "frequency_penalty (reduces word repetition)"
            ],
            "answer": 0,
            "explanation": "Temperature directly influences the probability distribution of token selection, with higher values leading to more random and creative outputs."
        },
        {
            "question": "In a Triage-Specialist pattern, what is the primary goal of using two different models?",
            "options": [
                "Cost optimization (cheap model for simple tasks, expensive for complex) and performance",
                "Increased creativity for all responses",
                "Simplified tool usage and integration",
                "Enhanced security through provider diversification"
            ],
            "answer": 0,
            "explanation": "The Triage-Specialist pattern significantly reduces costs (60-80%) by routing simple requests to a cheaper model (e.g., gpt-3.5-turbo) and complex requests to a more powerful model (e.g., gpt-4o)."
        },
        {
            "question": "How is request timeout typically configured in the OpenAI Agents SDK?",
            "options": [
                "At the AsyncOpenAI client level (e.g., AsyncOpenAI(timeout=30.0))",
                "Within ModelSettings (e.g., ModelSettings(timeout=30))",
                "Globally via an environment variable (e.g., AGENT_TIMEOUT=30)",
                "It cannot be configured and uses a fixed default value"
            ],
            "answer": 0,
            "explanation": "Network timeouts are configured on the HTTP client (AsyncOpenAI), not within ModelSettings, which controls model behavior parameters."
        },
        {
            "question": "What is the recommended approach for integrating a custom OpenAI-compatible API provider?",
            "options": [
                "Create an AsyncOpenAI client with the provider's base_url and api_key, then use set_default_openai_client()",
                "Use LiteLLM with a custom provider prefix (e.g., litellm/custom/my-model)",
                "Modify the SDK source code to add a new provider type",
                "This is not supported; only LiteLLM providers can be added"
            ],
            "answer": 0,
            "explanation": "The SDK allows setting a custom AsyncOpenAI client, enabling integration with any OpenAI-compatible API endpoint by specifying base_url, api_key, and other client parameters."
        },
        {
            "question": "Which ModelSettings parameter is crucial for enabling structured outputs or forcing the model to use a specific tool?",
            "options": [
                "tool_choice ('auto', 'required', 'none', or specific tool name)",
                "max_tokens (indirectly by limiting response format)",
                "reasoning (for models that support structured reasoning)",
                "metadata (for passing schema information)"
            ],
            "answer": 0,
            "explanation": "tool_choice directly controls how the model interacts with tools, allowing you to force tool usage, prevent it, or let the model decide."
        },
        {
            "question": "What is a key benefit of using environment variables for API keys and provider configuration?",
            "options": [
                "Enhanced security (keeps secrets out of code) and deployment flexibility (different configs for dev/staging/prod)",
                "Faster model response times due to optimized configuration loading",
                "Automatic provider failover and load balancing",
                "Simplified debugging and error tracking"
            ],
            "answer": 0,
            "explanation": "Environment variables are a best practice for managing sensitive data like API keys and allow for easy configuration changes across different deployment environments without code modification."
        },
        {
            "question": "In a multi-provider workflow, what is a common strategy for handling API errors or rate limits from the primary provider?",
            "options": [
                "Implement a fallback mechanism to switch to a secondary provider or a less capable model",
                "Immediately terminate the request and return an error to the user",
                "Retry the request indefinitely until it succeeds",
                "Log the error and wait for manual intervention"
            ],
            "answer": 0,
            "explanation": "Robust systems implement fallback strategies, such as trying a different provider or a model with lower resource requirements, to ensure service availability and graceful degradation."
        },
        {
            "question": "Which of the following is NOT a parameter available in ModelSettings?",
            "options": [
                "stop_sequences (this would be 'stop' if available, but neither is currently in ModelSettings)",
                "temperature",
                "max_tokens",
                "tool_choice"
            ],
            "answer": 0,
            "explanation": "ModelSettings does not include a 'stop' or 'stop_sequences' parameter. Stop sequences are a concept related to model generation but are not configured via this class in the SDK."
        }
    ]

    score = 0
    total_questions = len(questions)

    for i, item in enumerate(questions):
        print(f"--- Question {i+1}/{total_questions} ---")
        print(f"Q: {item['question']}\n")
        for opt_idx, option in enumerate(item['options']):
            print(f"   {chr(65+opt_idx)}. {option}")

        while True:
            try:
                answer_char = input("\nYour answer (A, B, C, D): ").upper()
                answer_idx = ord(answer_char) - 65
                if 0 <= answer_idx < len(item['options']):
                    break
                else:
                    print("Invalid option. Please enter A, B, C, or D.")
            except Exception:
                print("Invalid input. Please enter a letter (A, B, C, D).")

        if answer_idx == item['answer']:
            print("\n✅ Correct!")
            score += 1
        else:
            print(
                f"\n❌ Incorrect. The correct answer was {chr(65+item['answer'])}.")

        print(f"💡 Explanation: {item['explanation']}\n")
        input("Press Enter to continue...")
        print("-"*30 + "\n")

    print("=== Quiz Complete! ===")
    print(
        f"Your final score: {score}/{total_questions} ({score/total_questions*100:.2f}%)")

    if score == total_questions:
        print("🎉 Excellent! You have mastered the OpenAI Agents SDK Models module! 🎉")
    elif score >= total_questions * 0.7:
        print("👍 Great job! You have a strong understanding of the Models module.")
    elif score >= total_questions * 0.5:
        print("🙂 Good effort. Review the explanations and revisit the modules for a deeper understanding.")
    else:
        print(
            "😕 Keep practicing. Revisit the modules (01-05) to strengthen your knowledge.")

    print("\nThank you for taking the quiz!")

# ================== MAIN EXECUTION ==================


async def main():
    """Run the models quiz."""
    await run_models_quiz()

if __name__ == "__main__":
    asyncio.run(main())
