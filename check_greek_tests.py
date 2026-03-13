import sqlite3

conn = sqlite3.connect('data/ms_blood_tests.db')
cursor = conn.cursor()

# Get all distinct test names
cursor.execute('SELECT DISTINCT test_name FROM test_results ORDER BY test_name')
all_tests = [r[0] for r in cursor.fetchall()]

# Filter for Greek characters
greek_tests = [t for t in all_tests if any(ord(c) > 900 and ord(c) < 1200 for c in t)]

print(f'\nGreek test names extracted ({len(greek_tests)} total):')
for t in greek_tests:
    cursor.execute('SELECT result_value, unit, reference_range FROM test_results WHERE test_name = ? LIMIT 1', (t,))
    row = cursor.fetchone()
    if row:
        print(f'  {t}: {row[0]} {row[1]} (ref: {row[2]})')
    else:
        print(f'  {t}')

print(f'\n\nAll test names extracted ({len(all_tests)} total):')
for t in all_tests:
    print(f'  {t}')

conn.close()
