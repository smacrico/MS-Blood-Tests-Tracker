import sys
sys.path.append('.')

from src.pdf_reader import PDFReader
from src.data_parser import DataParser
from src.config import Config
from pathlib import Path

# Test on the new format PDF
pdf_file = Path('data/pdfs/proccessed/blood_10072025.PDF')
config = Config()
reader = PDFReader()
parser = DataParser()

print(f"Testing extraction on: {pdf_file.name}\n")

# Read PDF
text = reader.extract_text(pdf_file)
tables = reader.extract_tables(pdf_file)
print(f"Extracted {len(tables) if tables else 0} tables\n")

# Parse from tables
table_results = []
for table in tables:
    results = parser.parse_blood_test_from_tables(table)
    if results:
        table_results.extend(results)

print(f"=== Table Results: {len(table_results)} ===")
seen_names = set()
for r in table_results:
    if r['test_name'] not in seen_names:
        print(f"  {r['test_name']}: {r['result_value']} {r['unit']} ({r['reference_range']})")
        seen_names.add(r['test_name'])

# Parse from text
text_results = []
if text:
    results = parser.parse_blood_test_from_text(text)
    if results:
        text_results.extend(results)

print(f"\n=== Text Results: {len(text_results)} ===")
seen_names = set()
for r in text_results:
    if r['test_name'] not in seen_names:
        print(f"  {r['test_name']}: {r['result_value']} {r['unit']} ({r['reference_range']})")
        seen_names.add(r['test_name'])

print(f"\n=== Total: {len(table_results) + len(text_results)} tests ===")
