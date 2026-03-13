#!/usr/bin/env python3
"""Test the table parser directly"""

from src.pdf_reader import PDFReader
from src.data_parser import DataParser
from pathlib import Path

pdf_path = Path("data/pdfs/blood_30012023.PDF")
reader = PDFReader()
parser = DataParser()

print("=== Testing Table Parser ===\n")

text = reader.extract_text(pdf_path)
tables = reader.extract_tables(pdf_path)

print(f"Found {len(tables)} tables\n")

# Look at first table structure
if tables:
    print(f"First table has {len(tables[0])} rows\n")
    print("First 3 rows:")
    for i, row in enumerate(tables[0][:3]):
        print(f"Row {i}: {row}\n")

# Test _parse_table_row directly
if tables and tables[0]:
    row_text = ' '.join([str(c) for c in tables[0][1] if c])  # Try row 1
    print(f"\n=== Testing _parse_table_row on Row 1 ===")
    print(f"Row text (first 500 chars): {row_text[:500]}\n")
    parsed = parser._parse_table_row(row_text, 'CBC')
    print(f"Parsed {len(parsed)} results")
    for r in parsed[:5]:
        print(f"  {r['test_name']}: {r['result_value']} {r['unit']}")

result = parser.parse_blood_test_from_tables(tables, text, pdf_path.name)

if result:
    print(f"\nPatient: {result['patient_name']}")
    print(f"Date: {result['test_date']}")
    print(f"Results: {len(result['results'])}\n")
    for r in result['results'][:10]:
        print(f"{r['test_name']}: {r['result_value']} {r['unit']} (ref: {r['reference_range']}) - {r['flag']}")
else:
    print("\nNo results returned from parse_blood_test_from_tables!")

print("\n=== Testing Text Parser ===\n")

text_result = parser.parse_blood_test_from_text(text, pdf_path.name)

if text_result:
    print(f"Patient: {text_result['patient_name']}")
    print(f"Date: {text_result['test_date']}")
    print(f"Results: {len(text_result['results'])}\n")
    for r in text_result['results'][:15]:
        print(f"{r['test_name']}: {r['result_value']} {r['unit']} (ref: {r['reference_range']}) - {r['flag']}")
else:
    print("No results from text parser!")
