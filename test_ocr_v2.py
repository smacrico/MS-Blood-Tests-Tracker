# Alternative OCR approach using PIL/Pillow directly with pdfplumber images
import pdfplumber
import pytesseract
from PIL import Image
from pathlib import Path
import io

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_with_ocr_v2(pdf_path: Path) -> str:
    """
    Extract text from PDF using OCR by converting PDF pages to images.
    Uses pdfplumber to extract images instead of pdf2image (no poppler needed).
    """
    try:
        all_text = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            print(f"  Processing {len(pdf.pages)} pages...")
            
            for page_num, page in enumerate(pdf.pages, 1):
                print(f"    Page {page_num}/{len(pdf.pages)}...", end=" ")
                
                # First try regular text extraction
                text = page.extract_text()
                if text and len(text.strip()) > 50:
                    print("text extraction")
                    all_text += text + "\n\n"
                    continue
                
                # If no text, try OCR on the page image
                try:
                    # Convert page to image
                    im = page.to_image(resolution=300)
                    # Get PIL image
                    pil_image = im.original
                    
                    # Perform OCR
                    text = pytesseract.image_to_string(pil_image, lang='ell+eng')
                    print(f"OCR ({len(text)} chars)")
                    all_text += text + "\n\n"
                except Exception as e:
                    print(f"error: {str(e)}")
                    continue
        
        return all_text
    
    except Exception as e:
        print(f"  Error: {str(e)}")
        return ""

# Test
if __name__ == "__main__":
    pdf_file = Path('data/pdfs/results_2022-2023.pdf')
    
    print(f"Testing OCR v2 on: {pdf_file.name}\n")
    text = extract_text_with_ocr_v2(pdf_file)
    
    if text:
        lines = [l for l in text.split('\n') if l.strip()]
        print(f"\n✓ Extracted {len(lines)} lines of text")
        print("\nFirst 40 lines:")
        for line in lines[:40]:
            print(f"  {line}")
    else:
        print("\n✗ No text could be extracted")
