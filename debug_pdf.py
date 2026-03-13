#!/usr/bin/env python
"""Debug script to inspect PDF structure and test parsing patterns."""
import pdfplumber
from pathlib import Path
import re

pdf_path = Path('data/pdfs/blood_30012023.PDF')

print(f"=== Analyzing {pdf_path.name} ===\n")

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}\n")
    
    for page_num, page in enumerate(pdf.pages, start=1):
        print(f"\n{'='*60}")
        print(f"PAGE {page_num}")
        print('='*60)
        
        # Extract text
        text = page.extract_text()
        if text:
            lines = text.splitlines()
            print(f"\nFirst 50 lines of text:")
            for i, line in enumerate(lines[:50], start=1):
                print(f"{i:3d}: {line}")
        
        # Extract tables
        tables = page.extract_tables()
        if tables:
            print(f"\n\nFound {len(tables)} table(s) on page {page_num}")
            for t_idx, table in enumerate(tables, start=1):
                print(f"\n--- Table {t_idx} (rows: {len(table)}) ---")
                for row_idx, row in enumerate(table[:10]):  # Show first 10 rows
                    print(f"Row {row_idx}: {row}")
        
        # Test patterns for hormone/lipid tests
        if text:
            print(f"\n\n=== Pattern Testing on Page {page_num} ===")
            
            # Look for common hormone/lipid indicators
            indicators = [
                r'(?i)(thyroid|hormone|lipid|cholesterol|tsh|hdl|ldl|triglyceride)',
                r'(?i)(testosterone|estradiol|cortisol|prolactin)',
                r'(?i)(vitamine?|vitamin)',
            ]
            
            for pattern in indicators:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    print(f"\nFound indicators: {set(matches)}")
                    # Show context
                    for match in re.finditer(pattern, text, re.IGNORECASE):
                        start = max(0, match.start() - 100)
                        end = min(len(text), match.end() + 100)
                        context = text[start:end].replace('\n', ' | ')
                        print(f"  Context: ...{context}...")

print("\n\n=== Analysis Complete ===")
