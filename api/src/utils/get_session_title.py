from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.services.gemini_client import GeminiConfig, generate_content
from src.utils.chat_utils import ContentCategory
from src.utils.session_manager import SessionManager


class GetSessionTitleModel(BaseModel):
    category: ContentCategory
    summary: str
    sessionId: str


async def get_session_title(request: GetSessionTitleModel, background_tasks: BackgroundTasks):
    """
    Generate session title based on a summary of the user's request
    """
    system_prompt = f"""Your task is deduce a concise, comprehensive and descriptive topic or title for the following content.

    High level summary: {request.category}
    Content category: {request.summary}

    1. Keep it succint within the length of a short phrase.
    2. Be exhaustive as possible, capturing both the category and summary.
    3. No preambles or unnecessary information, just the topic or title.
    """

    session_id = request.sessionId

    def _on_finish(title: str):
        print(f"Generated title: {title}")
        db = SessionManager(session_id, request.category)
        background_tasks.add_task(db._update_title, title)

    response = generate_content(
        prompt=["Now provide the topic or title."],
        config=GeminiConfig(
            model_name="gemini-2.0-flash",
            system_prompt=system_prompt,
            temperature=0.5,
            max_output_tokens=60,
            stream=True,
        ),
        on_finish=_on_finish,
    )

    return StreamingResponse(response, media_type="text/event-stream")
