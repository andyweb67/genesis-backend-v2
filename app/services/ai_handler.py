import openai
import anthropic
import os
from core.config import settings
from routers.admin import genesis_settings

openai.api_key = settings.OPENAI_API_KEY
anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def call_gpt(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.9,
        max_tokens=500
    )
    return response.choices[0].message['content']

def call_claude(prompt: str) -> str:
    response = anthropic_client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=500,
        temperature=0.2,
        system="You are a legal compliance assistant focused on good faith standards and insurance fairness.",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

def smart_ai_call(prompt: str, use_model: str = None, temperature: float = None) -> str:
    """
    Calls the selected AI model based on dynamic admin settings.
    """
    # Pull defaults from Admin settings if not explicitly provided
    model = use_model if use_model else genesis_settings.get("model", "gpt")
    temp = temperature if temperature else genesis_settings.get("temperature", 0.2)

    # Simulated AI call for now (replace with real OpenAI / Anthropic call later)
    if model == "gpt":
        return f"(GPT-4 Response - temp={temp}): {prompt[:100]}..."
    elif model == "claude":
        return f"(Claude Response - temp={temp}): {prompt[:100]}..."
    else:
        return f"(Unknown Model - temp={temp}): {prompt[:100]}..."
