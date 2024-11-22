from io import BytesIO

from pypdf import PdfReader


class ReadContent:
    def _read_pdf(self, content: bytes) -> tuple[str, PdfReader]:
        pdf_reader = PdfReader(BytesIO(content))

        pages: list[str] = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            # Split into paragraphs and clean
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            pages.append("\n\n".join(paragraphs))

        text_content = "\n\n".join(pages).strip()
        return text_content, pdf_reader

    def _read_txt(self, content: bytes) -> str:
        return content.decode()
