import re
from typing import Dict, Any
from PyPDF2 import PdfReader

def sanitize_key(key: str) -> str:
    """
    Sanitize a document key to be valid for Azure Search.
    Only allows letters, digits, underscore (_), dash (-), or equal sign (=).
    Replaces invalid characters with an underscore.
    """
    return re.sub(r'[^A-Za-z0-9_\-=]', '_', key)

def extract_metadata(pdf_path: str) -> Dict[str, Any]:
    """
    Extract metadata from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary containing extracted metadata (title, authors, year, content)
    """
    reader = PdfReader(pdf_path)
    first_page = reader.pages[0]
    text = first_page.extract_text()

    # Extract title (first line)
    title = text.split('\n')[0] if text else "Unknown Title"

    # Extract authors (second line)
    authors = "Unknown Authors"
    lines = text.split('\n')
    if len(lines) > 1:
        authors = lines[1]

    # Extract year (first occurrence of 19xx or 20xx)
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    year = int(year_match.group()) if year_match else 2023

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "content": text
    }

def safe_document_id(filename: str) -> str:
    """
    Returns a sanitized document id for Azure Search from a filename.
    """
    return sanitize_key(filename)
