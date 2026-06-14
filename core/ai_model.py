# core/ai_models.py

from core.constants import (
    AI_PROVIDER_GEMINI,
    AI_PROVIDER_GROQ,
    AI_PROVIDER_OPENROUTER,
    AI_PROVIDER_OLLAMA
)


AI_MODELS = {

    AI_PROVIDER_GEMINI: [

        {
            "label": "Gemini 2.5 Flash",
            "value": "gemini-2.5-flash"
        },

        {
            "label": "Gemini 2.5 Flash Lite",
            "value": "gemini-2.5-flash-lite"
        },

        {
            "label": "Gemini 2.5 Pro",
            "value": "gemini-2.5-pro"
        },
                {
            "label": "Gemini 2.0 Flash",
            "value": "gemini-2.0-flash"
        },

        {
            "label": "Gemini 2.0 Flash Lite",
            "value": "gemini-2.0-flash-lite"
        }

    ],

    AI_PROVIDER_GROQ: [

        {
            "label": "DeepSeek R1 Distill Llama 70B",
            "value": (
                "deepseek-r1-distill-llama-70b"
            )
        },

        {
            "label": "Llama 3.3 70B",
            "value": (
                "llama-3.3-70b-versatile"
            )
        },

        {
            "label": "Qwen QWQ 32B",
            "value": (
                "qwen-qwq-32b"
            )
        }

    ],

    AI_PROVIDER_OPENROUTER: [

        {
            "label": "GPT-5",
            "value": "openai/gpt-5"
        },

        {
            "label": "Claude Sonnet 4",
            "value": (
                "anthropic/claude-sonnet-4"
            )
        },

        {
            "label": "Gemini 2.5 Pro",
            "value": (
                "google/gemini-2.5-pro"
            )
        }

    ],

    AI_PROVIDER_OLLAMA: [

        {
            "label": "Llama 3",
            "value": "llama3"
        },

        {
            "label": "Mistral",
            "value": "mistral"
        },

        {
            "label": "DeepSeek R1",
            "value": "deepseek-r1"
        }

    ]

}

DEFAULT_AI_MODELS = {
    AI_PROVIDER_GEMINI:
        "gemini-2.5-flash", 

    AI_PROVIDER_GROQ:
        "llama-3.3-70b-versatile",

    AI_PROVIDER_OPENROUTER:
        "openai/gpt-5",

    AI_PROVIDER_OLLAMA:
        "llama3"
}

def get_model_values(
    provider: str
) -> list[str]:

    return [
        model["value"]
        for model in AI_MODELS.get(
            provider,
            []
        )
    ]

def get_models_by_provider(
    provider: str
) -> list:

    return AI_MODELS.get(
        provider,
        []
    )

def is_valid_model(
    provider: str,
    model_name: str
) -> bool:

    models = AI_MODELS.get(
        provider,
        []
    )

    return any(
        model["value"] == model_name
        for model in models
    )