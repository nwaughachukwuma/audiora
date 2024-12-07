import asyncio

from src.utils.decorators.base import use_cache_manager
from src.utils.make_seed import get_hash
from src.utils.session_manager import SessionManager
from src.utils.summarize_custom_sources import summarize_custom_sources

from .base_utils import CustomSourceManager
from .generate_url_source import GenerateCustomSourceRequest, generate_custom_source


class ManageAttachments:
    def __init__(self, session_id: str):
        self.session_id = session_id

    async def get_attachments_summary(self, db: SessionManager, attachments: list[str] | None):
        """
        Manage custom sources uploaded by the user
        """
        sources_summary: str | None = None
        if attachments:
            attachments.sort(key=lambda x: x.lower())

            @use_cache_manager(get_hash(attachments))
            async def handler():
                summary = await summarize_custom_sources(attachments)
                db._update_source(summary)
                return summary

            sources_summary = await handler()

        return sources_summary

    async def store_attachments(self, attachments: list[str]):
        """
        Store attachments as custom sources of type links
        """
        cs_manager = CustomSourceManager(self.session_id)

        async def _handler(url: str):
            custom_source = cs_manager._get_custom_source_by_url(url)
            if not custom_source:
                request = GenerateCustomSourceRequest(url=url, sessionId=self.session_id)
                return generate_custom_source(request)

        await asyncio.gather(*[_handler(url) for url in attachments], return_exceptions=True)
        return True
