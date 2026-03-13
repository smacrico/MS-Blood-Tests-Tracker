import logging
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
    PDF_LIBRARY = 'pdfplumber'
except ImportError:
    try:
        from PyPDF2 import PdfReader
        PDF_LIBRARY = 'pypdf2'
    except ImportError:
        raise ImportError("Please install either 'pdfplumber' or 'PyPDF2' for PDF processing")

class PDFReader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Using PDF library: {PDF_LIBRARY}")

    def get_page_count(self, pdf_path: Path) -> int:
        """Return number of pages in the PDF."""
        try:
            if PDF_LIBRARY == 'pdfplumber':
                with pdfplumber.open(pdf_path) as pdf:
                    return len(pdf.pages)
            else:
                with open(pdf_path, 'rb') as f:
                    reader = PdfReader(f)
                    return len(reader.pages)
        except Exception as e:
            self.logger.error(f"Failed to get page count for {pdf_path}: {e}")
            return 0

    def extract_text(self, pdf_path: Path) -> Optional[str]:
        try:
            if PDF_LIBRARY == 'pdfplumber':
                return self._extract_with_pdfplumber(pdf_path)
            else:
                return self._extract_with_pypdf2(pdf_path)
        except Exception as e:
            self.logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return None

    def _extract_with_pdfplumber(self, pdf_path: Path) -> Optional[str]:
        text_content = []
        with pdfplumber.open(pdf_path) as pdf:
            for idx, page in enumerate(pdf.pages, start=1):
                try:
                    text = page.extract_text()
                    self.logger.debug(f"Extracted text from page {idx}/{len(pdf.pages)} of {pdf_path.name}")
                    if text:
                        text_content.append(text)
                except Exception as e:
                    self.logger.warning(f"Failed to extract text from page {idx}: {e}")
        return "\n".join(text_content) if text_content else None

    def _extract_with_pypdf2(self, pdf_path: Path) -> Optional[str]:
        text_content = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for idx, page in enumerate(pdf_reader.pages, start=1):
                try:
                    text = page.extract_text()
                    self.logger.debug(f"Extracted text from page {idx}/{len(pdf_reader.pages)} of {pdf_path.name}")
                    if text:
                        text_content.append(text)
                except Exception as e:
                    self.logger.warning(f"Failed to extract text from page {idx}: {e}")
        return "\n".join(text_content) if text_content else None

    def extract_tables(self, pdf_path: Path) -> list:
        if PDF_LIBRARY != 'pdfplumber':
            self.logger.warning("Table extraction requires pdfplumber library")
            return []
        try:
            tables = []
            with pdfplumber.open(pdf_path) as pdf:
                for idx, page in enumerate(pdf.pages, start=1):
                    try:
                        page_tables = page.extract_tables()
                        if page_tables:
                            self.logger.debug(f"Found {len(page_tables)} table(s) on page {idx}/{len(pdf.pages)} of {pdf_path.name}")
                            tables.extend(page_tables)
                    except Exception as e:
                        self.logger.warning(f"Failed to extract tables from page {idx}: {e}")
            return tables
        except Exception as e:
            self.logger.error(f"Error extracting tables from {pdf_path}: {str(e)}")
            return []