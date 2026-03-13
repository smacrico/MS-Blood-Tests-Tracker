import sqlite3

conn = sqlite3.connect('data/ms_blood_tests.db')
cursor = conn.cursor()
cursor.execute('SELECT DISTINCT test_name FROM test_results ORDER BY test_name')

with open('test_names_list.txt', 'w', encoding='utf-8') as f:
    for row in cursor.fetchall():
        f.write(row[0] + '\n')

conn.close()
print('Test names written to test_names_list.txt')
