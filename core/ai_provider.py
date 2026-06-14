import requests

from google import genai

from core.constants import (
    FINANCIAL_AI_SYSTEM_PROMPT,
    AI_PROVIDER_GEMINI,
    AI_PROVIDER_GROQ,
    AI_PROVIDER_OLLAMA,
    AI_PROVIDER_OPENROUTER
)


def call_gemini(
    api_key: str,
    model_name: str,
    prompt: str,
    temperature: float = 0.7
) -> str:

    client = genai.Client(
        api_key=api_key
    )

    full_prompt = f"""
        {FINANCIAL_AI_SYSTEM_PROMPT}

        User:
        {prompt}
        """

    try:

        response = client.models.generate_content(
            model=model_name,
            contents=full_prompt
        )

        return response.text

    except Exception as e:

        raise ValueError(
            f"Gagal menghubungi Gemini: {str(e)}"
        )


def call_openrouter(
    api_key: str,
    model_name: str,
    prompt: str,
    temperature: float = 0.7
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
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": FINANCIAL_AI_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        raise ValueError(
            f"Gagal menghubungi OpenRouter: {str(e)}"
        )


def call_groq(
    api_key: str,
    model_name: str,
    prompt: str,
    temperature: float = 0.7
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
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": FINANCIAL_AI_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        raise ValueError(
            f"Gagal menghubungi Groq: {str(e)}"
        )


def call_ollama(
    model_name: str,
    prompt: str,
    temperature: float = 0.7
) -> str:

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,

        "prompt": f"""
    {FINANCIAL_AI_SYSTEM_PROMPT}

    User:
    {prompt}
    """,

        "stream": False,

        "options": {
            "temperature": temperature
        }
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except Exception as e:

        raise ValueError(
            f"Gagal menghubungi Ollama: {str(e)}"
        )


def generate_ai_response(
    provider: str,
    api_key: str | None,
    model_name: str,
    prompt: str,
    temperature: float = 0.7
) -> str:

    if provider == AI_PROVIDER_GEMINI:

        if not api_key:
            raise ValueError(
                "Gemini membutuhkan API Key."
            )

        return call_gemini(
            api_key=api_key,
            model_name=model_name,
            prompt=prompt, 
            temperature=temperature
        )

    if provider == AI_PROVIDER_OPENROUTER:

        if not api_key:
            raise ValueError(
                "OpenRouter membutuhkan API Key."
            )

        return call_openrouter(
            api_key=api_key,
            model_name=model_name,
            prompt=prompt, 
            temperature=temperature
        )

    if provider == AI_PROVIDER_GROQ:

        if not api_key:
            raise ValueError(
                "Groq membutuhkan API Key."
            )

        return call_groq(
            api_key=api_key,
            model_name=model_name,
            prompt=prompt, 
            temperature=temperature
        )

    if provider == AI_PROVIDER_OLLAMA:

        return call_ollama(
            model_name=model_name,
            prompt=prompt, 
            temperature=temperature
        )

    raise ValueError(
        f"Provider AI tidak didukung: {provider}"
    )