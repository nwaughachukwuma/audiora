from dataclasses import dataclass
from typing import Literal

import google.generativeai as genai

from env_var import GEMINI_API_KEY


def get_gemini():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai


ModelName = Literal[
    "gemini-1.5-flash-002", "gemini-1.5-pro-002", "gemini-1.5-pro-latest"
]


@dataclass
class GeminiConfig:
    temperature: float = 0.5
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 8192
    system_prompt: str = "You're a super-intelligent and helpful AI-assistant"
    stream: bool = False
    model_name: ModelName = "gemini-1.5-pro-002"


def generate_content(
    prompt: list[str],
    config: GeminiConfig,
):
    model = get_gemini().GenerativeModel(
        model_name=config.model_name,
        generation_config={
            "temperature": config.temperature,
            "max_output_tokens": config.max_output_tokens,
            "response_mime_type": "text/plain",
        },
        system_instruction=config.system_prompt,
    )

    response = model.generate_content(prompt)
    return response.text
