from dataclasses import dataclass
from typing import Any, Callable, Literal, Optional

from google import genai
from google.genai import types

from src.env_var import GEMINI_API_KEY

ModelName = Literal["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]


class GeminiClient:
    _client = genai.Client(api_key=GEMINI_API_KEY)
    _models = _client.models
    _types = types
    _Content = types.Content
    _Part = types.Part


@dataclass
class GeminiConfig:
    temperature: float = 0.5
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    max_output_tokens: int = 8192
    system_prompt: str = "You're a super-intelligent and helpful AI-assistant"
    stream: bool = False
    model_name: ModelName = "gemini-2.0-flash"


def generate_content(
    prompt: list[Any],
    config: GeminiConfig,
    on_finish: Optional[Callable[[str], Any]] = None,
):
    def stream_response():
        responses = GeminiClient._models.generate_content_stream(
            model=config.model_name,
            contents=prompt,
            config=GeminiClient._types.GenerateContentConfig(
                temperature=config.temperature,
                max_output_tokens=config.max_output_tokens,
                response_mime_type="text/plain",
                system_instruction=config.system_prompt,
                top_p=config.top_p,
                top_k=config.top_k,
            ),
        )

        def _generator():
            full_text = ""
            for res in responses:
                if not res.candidates:
                    continue
                for candidate in res.candidates:
                    if not candidate.content or not candidate.content.parts:
                        continue
                    for part in candidate.content.parts:
                        if part.text:
                            full_text += part.text
                            yield part.text

            if on_finish:
                try:
                    on_finish(full_text)
                except Exception:
                    pass

        return _generator()

    def non_stream_response():
        response = GeminiClient._models.generate_content(
            model=config.model_name,
            contents=prompt,
            config=GeminiClient._types.GenerateContentConfig(
                temperature=config.temperature,
                max_output_tokens=config.max_output_tokens,
                response_mime_type="text/plain",
                system_instruction=config.system_prompt,
            ),
        )

        if not response.text:
            raise ValueError(f"No response returned from Gemini API using {config.model_name}")

        if on_finish:
            try:
                on_finish(response.text)
            except Exception:
                pass

        return response.text

    return stream_response() if config.stream else non_stream_response()
