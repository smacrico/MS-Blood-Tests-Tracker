#!/usr/bin/env python3
"""Test the table parser - write output to file"""

from src.pdf_reader import PDFReader
from src.data_parser import DataParser
from pathlib import Path
import json

pdf_path = Path("data/pdfs/blood_30012023.PDF")
reader = PDFReader()
parser = DataParser()

text = reader.extract_text(pdf_path)
tables = reader.extract_tables(pdf_path)

# Write text to file to check encoding
with open("debug_extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Test row parsing
if tables and tables[0]:
    row_text = ' '.join([str(c) for c in tables[0][1] if c])
    
    # Write row text to file
    with open("debug_row_text.txt", "w", encoding="utf-8") as f:
        f.write(row_text)
    
    # Test parsing
    parsed = parser._parse_table_row(row_text, 'CBC')
    
    with open("debug_parse_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "row_text_length": len(row_text),
            "parsed_count": len(parsed),
            "results": parsed
        }, f, ensure_ascii=False, indent=2)

print(f"Created debug files:")
print("- debug_extracted_text.txt")
print("- debug_row_text.txt")
print("- debug_parse_results.json")
