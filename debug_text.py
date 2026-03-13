#!/usr/bin/env python3
"""Debug script to inspect text content from blood test PDFs."""

import pdfplumber
from pathlib import Path

pdf_path = Path("data/pdfs/blood_30012023.PDF")

print(f"=== Analyzing {pdf_path.name} ===\n")

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        print(f"\n{'='*60}")
        print(f"PAGE {page_num}")
        print(f"{'='*60}\n")
        
        text = page.extract_text()
        
        if text:
            lines = text.split('\n')
            print(f"Total lines: {len(lines)}\n")
            
            # Print all lines for Page 2
            if page_num == 2:
                for i, line in enumerate(lines, 1):
                    print(f"{i:3d}: {line}")
            else:
                # For other pages, print first 20 lines
                for i, line in enumerate(lines[:20], 1):
                    print(f"{i:3d}: {line}")
        else:
            print("No text found on this page")
