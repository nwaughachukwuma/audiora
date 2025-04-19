from dataclasses import dataclass
from typing import Any, Callable, Literal, Optional

import google.generativeai as genai

from src.env_var import GEMINI_API_KEY


def get_gemini():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai


ModelName = Literal["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-pro-latest"]


@dataclass
class GeminiConfig:
    temperature: float = 0.5
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 8192
    system_prompt: str = "You're a super-intelligent and helpful AI-assistant"
    stream: bool = False
    model_name: ModelName = "gemini-2.0-flash"


def generate_content(
    prompt: list[str],
    config: GeminiConfig,
    on_finish: Optional[Callable[[str], Any]] = None,
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

    response = model.generate_content(prompt, stream=config.stream)
    if not config.stream:
        return response.text

    def _generator():
        full_text = ""
        for chunk in response:
            full_text += chunk.text
            yield chunk.text

        if on_finish:
            try:
                on_finish(full_text)
            except Exception:
                pass

    return _generator()
