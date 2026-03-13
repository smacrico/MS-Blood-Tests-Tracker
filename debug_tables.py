#!/usr/bin/env python3
"""Debug script to inspect table structure from blood test PDFs."""

import pdfplumber
from pathlib import Path

pdf_path = Path("data/pdfs/blood_30012023.PDF")

print(f"=== Analyzing {pdf_path.name} ===\n")

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        print(f"\n{'='*60}")
        print(f"PAGE {page_num}")
        print(f"{'='*60}")
        
        tables = page.extract_tables()
        
        if tables:
            for table_num, table in enumerate(tables, 1):
                print(f"\n--- Table {table_num} ---")
                print(f"Dimensions: {len(table)} rows x {len(table[0]) if table else 0} columns")
                
                # Print first 20 rows
                for row_idx, row in enumerate(table[:20], 1):
                    print(f"Row {row_idx}: {row}")
        else:
            print("No tables found on this page")
