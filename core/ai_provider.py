import requests

from google import genai

from core.constants import (
    AI_SYSTEM_PROMPT,
    AI_PROVIDER_GEMINI,
    AI_PROVIDER_GROQ,
    AI_PROVIDER_OLLAMA,
    AI_PROVIDER_OPENROUTER
)


def call_gemini(
    api_key: str,
    model_name: str,
    prompt: str
) -> str:

    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return response.text


def call_openrouter(
    api_key: str,
    model_name: str,
    prompt: str
) -> str:

    url = (
        "https://openrouter.ai/api/v1/"
        "chat/completions"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": AI_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]


def call_groq(
    api_key: str,
    model_name: str,
    prompt: str
) -> str:

    url = (
        "https://api.groq.com/openai/v1/"
        "chat/completions"
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": AI_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]


def call_ollama(
    model_name: str,
    prompt: str
) -> str:

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        url,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]


def generate_ai_response(
    provider: str,
    api_key: str | None,
    model_name: str,
    prompt: str
) -> str:

    if provider == AI_PROVIDER_GEMINI:

        if not api_key:
            raise ValueError(
                "Gemini membutuhkan API Key."
            )

        return call_gemini(
            api_key=api_key,
            model_name=model_name,
            prompt=prompt
        )

    if provider == AI_PROVIDER_OPENROUTER:

        if not api_key:
            raise ValueError(
                "OpenRouter membutuhkan API Key."
            )

        return call_openrouter(
            api_key=api_key,
            model_name=model_name,
            prompt=prompt
        )

    if provider == AI_PROVIDER_GROQ:

        if not api_key:
            raise ValueError(
                "Groq membutuhkan API Key."
            )

        return call_groq(
            api_key=api_key,
            model_name=model_name,
            prompt=prompt
        )

    if provider == AI_PROVIDER_OLLAMA:

        return call_ollama(
            model_name=model_name,
            prompt=prompt
        )

    raise ValueError(
        f"Provider AI tidak didukung: {provider}"
    )