import sqlite3
from pathlib import Path
import pdfplumber

# Tests from the image
target_tests = [
    'Lp (α) - Λιποπρωτεΐνη (α)',
    'Lp (α)',
    'Λιποπρωτεΐνη (α)',
    'Λιποπρωτεΐνη',
    'Βιταμίνη D-3 (25-OH)',
    'Βιταμίνη D-3',
    'Μη- HDL χοληστερόλη(non-HDL-C)',
    'Μη- HDL χοληστερόλη',
    'HDL χοληστερόλη',
]

# Check database
db_path = Path('data') / 'ms_blood_tests.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Checking Database ===")
for test in target_tests:
    cursor.execute("SELECT COUNT(*) FROM test_results WHERE test_name LIKE ?", (f'%{test}%',))
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"✓ Found {count} records for: {test}")
    else:
        print(f"✗ Missing: {test}")

conn.close()

print("\n=== Searching in PDFs ===")
pdf_dir = Path('data/pdfs')
pdf_files = list(pdf_dir.glob('*.pdf')) + list(pdf_dir.glob('*.PDF'))

for pdf_file in pdf_files:
    print(f"\n--- {pdf_file.name} ---")
    with pdfplumber.open(pdf_file) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if not text:
                continue
            
            lines = text.split('\n')
            for line in lines:
                # Check for any of the target tests
                for test in ['Lp (α)', 'Λιποπρωτεΐνη', 'Βιταμίνη D-3', 'Μη- HDL', 'non-HDL']:
                    if test in line:
                        print(f"  Page {page_num}: {line.strip()}")
                        break
