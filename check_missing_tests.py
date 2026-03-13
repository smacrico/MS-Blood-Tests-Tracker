import sqlite3

conn = sqlite3.connect('data/ms_blood_tests.db')
cursor = conn.cursor()

# Check for missing tests
search_terms = ['Καλσιτονίνη', 'NEUT', 'Ουδετερόφιλα', 'Neutro']
results = []

for term in search_terms:
    cursor.execute(f"SELECT DISTINCT test_name FROM test_results WHERE test_name LIKE '%{term}%'")
    found = cursor.fetchall()
    if found:
        results.extend([r[0] for r in found])

print(f'Found {len(set(results))} matching tests:')
for test in set(results):
    print(f'  {test}')

# Also search in PDF
print('\n--- Searching in PDF for these tests ---')
import pdfplumber
pdf = pdfplumber.open('data/pdfs/bloodResults_23092025.pdf')
text = ''.join([p.extract_text() for p in pdf.pages])
pdf.close()

for term in ['Καλσιτονίνη', 'NEUT', 'Ουδετερόφιλα']:
    lines = [l.strip() for l in text.split('\n') if term in l]
    if lines:
        print(f'\n{term} found in PDF:')
        for line in lines[:2]:  # Show first 2 matches
            print(f'  {line[:120]}')

conn.close()
