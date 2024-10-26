from typing import Any, Callable, List, Optional

from src.services.openai_client import get_openai
from src.utils.chat_utils import ChatMessage, ContentType


def get_system_message(content_type: ContentType):
    return f"""
    1. You're a super-intelligent AI. Your task is to understand what audiocast a user wants to listen to.
    2. You will steer the conversation until you have enough context after which you should terminate.
    3. Keep the conversation short, say 3-5 back and forth i.e., questions and answers.
    4. As soon as the user's request is clear terminate the conversation by saying, "Ok, thanks for clarifying! Based on your specifications, you want to listen to [Best case summary of user request so far]. Please click the button below to start generating the audiocast."
    5. You can also terminate the conversation using a varied response strictly similar to (4) above.
    6. If the user's request remains unclear after 5 responses for clarity, terminate the conversation by saying, "Your request is not very specific but from what I understand, you want to listen to [Best case summary of user request so far]. Please click the button below to start generating the audiocast."


    GENERAL IDEA AND WORKFLOW:
    1. A user comes to you with a request for an audiocast of type {content_type}.
    2. You need to ask the user questions to understand what kind of audiocast they want to listen to. 
    3. Once you have enough context, within 2-3 exchanges, you should prompt the user to generate the audiocast.
    """


def chat_request(
    content_type: ContentType,
    previous_messages: List[ChatMessage],
    on_finish: Optional[Callable[[str], Any]] = None,
):
    response_stream = get_openai().chat.completions.create(
        messages=[
            {"role": "system", "content": get_system_message(content_type)},
            *[
                {"role": "user", "content": msg.content}
                if msg.role == "user"
                else {"role": "assistant", "content": msg.content}
                for msg in previous_messages
            ],
        ],
        model="gpt-4o",
        stream=True,
    )

    def generator():
        text = ""
        for chunk in response_stream:
            for item in chunk.choices:
                if not item.delta or not item.delta.content:
                    continue
                content = item.delta.content
                text += content
                yield f"{content}"

        yield "\n"

        if on_finish:
            on_finish(text)

    return generator()
