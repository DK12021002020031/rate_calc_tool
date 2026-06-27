import os
import json

try:
    import openai
except ImportError:
    openai = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def call_llm(prompt, model="gpt-4.1-mini"):
    if openai is None:
        raise RuntimeError("openai package is not installed.")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    if not prompt:
        return "No prompt provided."

    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.7,
    )
    if response and response.choices:
        return response.choices[0].message.content.strip()
    return "No response from LLM."


def calculate_rate(base_rate, modifier, hours):
    if base_rate is None or modifier is None or hours is None:
        raise ValueError("All parameters are required.")

    if hours < 0:
        return 0
    elif hours == 0:
        return base_rate
    else:
        return base_rate * (1 + modifier) * hours


def tool_summary(text):
    if not text:
        return "Nothing to summarize."

    if len(text) < 50:
        return text
    else:
        return text[:47].rstrip() + "..."


def main():
    example_prompt = "Summarize the benefits of using tool functions with LLM calls."
    print("Calling LLM with prompt:", example_prompt)

    try:
        llm_result = call_llm(example_prompt)
        print("LLM result:\n", llm_result)
    except Exception as exc:
        print("LLM call failed:", exc)
        llm_result = None

    short_summary = tool_summary(llm_result or "")
    print("Summary:\n", short_summary)

    rate = calculate_rate(base_rate=50, modifier=0.1, hours=8)
    print("Calculated rate:", rate)


if __name__ == "__main__":
    main()
