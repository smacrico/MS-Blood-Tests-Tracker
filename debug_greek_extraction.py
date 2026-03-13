import pdfplumber
import re
from src.data_parser import DataParser

# Open PDF
pdf = pdfplumber.open('data/pdfs/bloodResults_23092025.pdf')
text = '\n'.join([page.extract_text() for page in pdf.pages])
pdf.close()

# Find lines with Greek test names
greek_tests = ['Ουρία', 'Κρεατινίνη', 'Χοληστερίνη', 'Τριγλυκερίδια']
print("=== Lines with Greek test names ===")
for greek_test in greek_tests:
    lines = [l.strip() for l in text.split('\n') if greek_test in l]
    for line in lines:
        print(f"\n{greek_test}:")
        print(f"  {line}")

# Test parser
parser = DataParser()
result = parser.parse_blood_test_from_text(text, 'bloodResults_23092025.pdf')

print("\n\n=== Extracted Results with Greek Names ===")
if result and 'results' in result:
    greek_results = [r for r in result['results'] if any(ord(c) > 127 for c in r['test_name'])]
    print(f"Found {len(greek_results)} results with Greek characters:")
    for r in greek_results:
        print(f"  {r['test_name']}: {r['result_value']} {r['unit']} (ref: {r['reference_range']})")
else:
    print("No results extracted")

# Check what test names are being extracted
print("\n\n=== All Extracted Test Names ===")
if result and 'results' in result:
    test_names = sorted(set([r['test_name'] for r in result['results']]))
    for name in test_names:
        print(f"  {name}")
