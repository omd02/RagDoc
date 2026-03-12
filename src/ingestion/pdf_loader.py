from pypdf import PdfReader
from pathlib import Path


def load_pdf(file_path: str):
    """
    Load a PDF and return a list of page documents with metadata.

    Args:
        file_path (str): path to the PDF file

    Returns:
        list[dict]: list of documents containing text and metadata
    """

    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages):

        text = page.extract_text()

        if not text:
            continue

        document = {
            "text": text,
            "metadata": {
                "source": Path(file_path).name,
                "page": page_number + 1
            }
        }

        documents.append(document)

    return documents