import sqlite3

conn = sqlite3.connect('data/ms_blood_tests.db')
cursor = conn.cursor()

# Check for HbA1c
cursor.execute("SELECT test_name, result_value, unit, reference_range FROM test_results WHERE test_name LIKE '%HbA1c%' OR test_name LIKE '%ΓΛΥΚΟΖΥΛΙΩΜΕΝΗ%'")
results = cursor.fetchall()

print(f'HbA1c results found: {len(results)}')
for r in results:
    print(f'  {r[0]}: {r[1]} {r[2]} (ref: {r[3]})')

# Also check all test names to see what we have
cursor.execute('SELECT COUNT(DISTINCT test_name) FROM test_results')
total = cursor.fetchone()[0]
print(f'\nTotal unique tests: {total}')

conn.close()
