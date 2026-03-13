import sqlite3
from pathlib import Path

db_path = Path('data') / 'ms_blood_tests.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("BLOOD TEST EXTRACTION SUMMARY")
print("=" * 80)

# Total stats
cursor.execute("SELECT COUNT(DISTINCT test_name), COUNT(*) FROM test_results")
unique, total = cursor.fetchone()
print(f"\n📊 Total Statistics:")
print(f"   - Unique test types: {unique}")
print(f"   - Total test records: {total}")

# Tests processed
cursor.execute("SELECT COUNT(DISTINCT test_date) FROM test_results")
dates = cursor.fetchone()[0]
print(f"   - Test dates: {dates}")

# Category breakdown
print(f"\n📋 By Category:")
cursor.execute("""
    SELECT category_code, COUNT(*) as count 
    FROM test_results 
    WHERE category_code IS NOT NULL AND category_code != ''
    GROUP BY category_code 
    ORDER BY count DESC
""")
for cat, count in cursor.fetchall():
    print(f"   - {cat}: {count} records")

# All unique test names
print(f"\n🧪 All {unique} Unique Test Names:")
cursor.execute("SELECT DISTINCT test_name FROM test_results ORDER BY test_name")
for i, (name,) in enumerate(cursor.fetchall(), 1):
    print(f"   {i:2}. {name}")

# Tests with special formats
print(f"\n✨ Special Format Tests Captured:")
special_tests = [
    'Καλσιτονίνη',  # Value starting with <
    'Πολυμορφοπύρηνα Ουδετερόφιλα (NEUT)',  # Greek letter in value
    'Lp (α) - Λιποπρωτείνη (α)',  # Parentheses in name
    'Βιταμίνη D-3 (25-ΟΗ)',  # Hyphen and parentheses
    'Μη- HDL χοληστερόλη (non-HDL-C)',  # Mixed Greek/English, no ref range
]

for test in special_tests:
    cursor.execute("SELECT COUNT(*) FROM test_results WHERE test_name LIKE ?", (f'%{test}%',))
    count = cursor.fetchone()[0]
    status = "✓" if count > 0 else "✗"
    print(f"   {status} {test}: {count} records")

conn.close()

print("\n" + "=" * 80)
