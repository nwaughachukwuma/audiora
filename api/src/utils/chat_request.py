from typing import Any, Callable, List, Optional

from src.services.openai_client import get_openai
from src.utils.chat_utils import ContentCategory, SessionChatItem


def get_system_message(content_category: ContentCategory):
    return f"""
    1. You're a super-intelligent AI. Your task is to understand what audiocast a user wants to listen to.
    2. You will steer the conversation providing eliciting questions until you have enough context.
    3. Keep the conversation exchange short, say 3-5 back and forth i.e., questions and answers.
    4. As soon as you have enough context and the user's request is clear terminate the conversation by saying "Ok, thanks for clarifying! You want to listen to [Best case summary of user request so far]. Please click the button below to start generating the audiocast."
    6. If the user's request remains unclear after 5 responses for clarity, terminate the conversation by saying "Your request is not very specific but from what I understand, you want to listen to [Best case summary of user request so far]. Please click the button below to start generating the audiocast."


    GENERAL IDEA AND WORKFLOW:
    1. A user comes to you with a request for an audiocast of type {content_category}.
    2. You need to ask the user questions (elicitation) to understand what kind of audiocast they want to listen to.
    3. Once you have enough context, within 3-5 exchanges, you should terminate the conversation.

    IMPORTANT NOTES:
    1. Your task is to understand the user's request only by eliciting questions.
    2. Do not generate the audiocast or any other content yourself.
    3. Strictly keep the conversation short with 3-5 exchanges.
    """


def chat_request(
    content_category: ContentCategory,
    previous_messages: List[SessionChatItem],
    on_finish: Optional[Callable[[str], Any]] = None,
):
    response_stream = get_openai().chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": get_system_message(content_category)},
            *[
                {"role": "user", "content": msg.content}
                if msg.role == "user"
                else {"role": "assistant", "content": msg.content}
                for msg in previous_messages
            ],
        ],
        stream=True,
    )

    def generator():
        text = ""
        for chunk in response_stream:
            for item in chunk.choices:
                if item.delta and item.delta.content:
                    content = item.delta.content
                    text += content
                    yield content

        if on_finish:
            on_finish(text)

    return generator()
