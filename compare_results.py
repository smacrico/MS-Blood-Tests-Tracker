import sqlite3
from pathlib import Path

# Get current test names
db_path = Path('data') / 'ms_blood_tests.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT test_name FROM test_results ORDER BY test_name")
current_tests = {row[0] for row in cursor.fetchall()}
cursor.execute("SELECT COUNT(DISTINCT test_name) FROM test_results")
unique_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM test_results")
total_count = cursor.fetchone()[0]
conn.close()

print(f"Current database:")
print(f"  Total records: {total_count}")
print(f"  Unique test names: {unique_count}")
print(f"\nAll test names ({len(current_tests)}):")
for test in sorted(current_tests):
    print(f"  {test}")
