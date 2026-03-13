import pdfplumber
from pathlib import Path

pdf_file = Path('data/pdfs/results_2022-2023.pdf')

print(f"=== Examining {pdf_file.name} ===\n")

with pdfplumber.open(pdf_file) as pdf:
    print(f"Total pages: {len(pdf.pages)}\n")
    
    for page_num, page in enumerate(pdf.pages[:5], 1):
        print(f"--- Page {page_num} ---")
        
        # Try extracting text with different settings
        text = page.extract_text()
        if text:
            lines = [l for l in text.split('\n') if l.strip()]
            if lines:
                print(f"Text lines: {len(lines)}")
                print("First 20 lines:")
                for line in lines[:20]:
                    print(f"  {line}")
        else:
            print("  No text extracted")
        
        # Check if it's an image-based PDF
        images = page.images
        if images:
            print(f"  Contains {len(images)} image(s) - might be scanned PDF")
        
        print()
