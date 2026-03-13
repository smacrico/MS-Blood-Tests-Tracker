import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path
import pdfplumber

# Set Tesseract path (default Windows installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_with_ocr(pdf_path: Path) -> str:
    """
    Extract text from PDF using OCR for scanned/image-based PDFs.
    Falls back to regular extraction if OCR fails.
    """
    try:
        # First, try regular text extraction
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text()
            if text and len(text.strip()) > 50:  # If we got meaningful text
                print(f"  Using regular text extraction for {pdf_path.name}")
                all_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        all_text += page_text + "\n\n"
                return all_text
        
        # If no text found, use OCR
        print(f"  Using OCR extraction for {pdf_path.name}...")
        
        # Convert PDF pages to images
        images = convert_from_path(pdf_path, dpi=300)
        
        all_text = ""
        for i, image in enumerate(images, 1):
            print(f"    Processing page {i}/{len(images)}...")
            # Perform OCR on the image with Greek language support
            text = pytesseract.image_to_string(image, lang='ell+eng')  # Greek + English
            all_text += text + "\n\n"
        
        return all_text
    
    except Exception as e:
        print(f"  Error during OCR extraction: {str(e)}")
        return ""

# Test on one of the scanned PDFs
if __name__ == "__main__":
    pdf_file = Path('data/pdfs/results_2022-2023.pdf')
    
    print(f"Testing OCR on: {pdf_file.name}\n")
    text = extract_text_with_ocr(pdf_file)
    
    if text:
        lines = [l for l in text.split('\n') if l.strip()]
        print(f"\n✓ Extracted {len(lines)} lines of text")
        print("\nFirst 30 lines:")
        for line in lines[:30]:
            print(f"  {line}")
    else:
        print("\n✗ No text could be extracted")
