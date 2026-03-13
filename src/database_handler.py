import sqlite3
import logging
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any

class DatabaseHandler:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.conn = None
        self._connect()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {str(e)}")
            raise

    def initialize_database(self):
        """Initialize database tables"""
        try:
            cursor = self.conn.cursor()
            
            # First, migrate schema if needed (before creating indexes)
            self._migrate_schema()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    date_of_birth DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_code TEXT NOT NULL UNIQUE,
                    category_name TEXT NOT NULL,
                    description TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blood_tests (
                    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    category_id INTEGER,
                    test_date DATE NOT NULL,
                    test_month INTEGER,
                    test_year INTEGER,
                    pdf_filename TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (category_id) REFERENCES test_categories(category_id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_date DATE NOT NULL,
                    patient_name TEXT,
                    test_name TEXT NOT NULL,
                    result_value TEXT NOT NULL,
                    unit TEXT,
                    reference_range TEXT,
                    flag TEXT,
                    category_code TEXT,
                    pdf_filename TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS query_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    query_filters TEXT,
                    test_date TEXT,
                    patient_name TEXT,
                    category_name TEXT,
                    test_name TEXT,
                    result_value TEXT,
                    unit TEXT,
                    reference_range TEXT,
                    flag TEXT,
                    pdf_source TEXT
                )
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_blood_tests_date 
                ON blood_tests(test_date)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_blood_tests_patient 
                ON blood_tests(patient_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_test_results_date 
                ON test_results(test_date)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_test_results_patient 
                ON test_results(patient_name)
            ''')
            self.conn.commit()
            self.logger.info("Database initialized successfully")
            self._populate_test_categories()
        except sqlite3.Error as e:
            self.logger.error(f"Error initializing database: {str(e)}")
            raise

    def _populate_test_categories(self):
        from src.config import Config
        config = Config()
        categories = config.get_all_categories()
        cursor = self.conn.cursor()
        for code, name in categories.items():
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO test_categories (category_code, category_name)
                    VALUES (?, ?)
                ''', (code, name))
            except sqlite3.Error as e:
                self.logger.warning(f"Could not insert category {code}: {str(e)}")
        self.conn.commit()

    def insert_test_results(self, test_data: Dict[str, Any]) -> Optional[int]:
        try:
            cursor = self.conn.cursor()
            patient_id = self._get_or_create_patient(test_data['patient_name'])
            cursor.execute('''
                INSERT INTO blood_tests 
                (patient_id, test_date, test_month, test_year, pdf_filename)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                patient_id,
                test_data['test_date'],
                test_data['test_month'],
                test_data['test_year'],
                test_data['pdf_filename']
            ))
            test_id = cursor.lastrowid
            primary_category_id = None
            for result in test_data['results']:
                test_name = result['test_name'].strip()
                if len(test_name) < 2 or test_name.startswith('0 ') or test_name.startswith('50 ') or ' -,' in test_name:
                    continue
                category_code = result.get('category', 'OTHER')
                category_id = self._get_category_id(category_code)
                if primary_category_id is None and category_id is not None:
                    primary_category_id = category_id
                cursor.execute('''
                    INSERT INTO test_results 
                    (test_date, patient_name, test_name, result_value, unit, reference_range, flag, category_code, pdf_filename)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    test_data['test_date'],
                    test_data['patient_name'],
                    test_name,
                    result['result_value'],
                    result['unit'],
                    result['reference_range'],
                    result['flag'],
                    category_code,
                    test_data['pdf_filename']
                ))
            if primary_category_id is not None:
                cursor.execute('''
                    UPDATE blood_tests 
                    SET category_id = ?
                    WHERE test_id = ?
                ''', (primary_category_id, test_id))
            self.conn.commit()
            self.logger.info(f"Inserted test results for test_id: {test_id}")
            return test_id
        except sqlite3.Error as e:
            self.logger.error(f"Error inserting test results: {str(e)}")
            self.conn.rollback()
            return None

    def _get_or_create_patient(self, patient_name: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute('SELECT patient_id FROM patients WHERE name = ?', (patient_name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute('INSERT INTO patients (name) VALUES (?)', (patient_name,))
        return cursor.lastrowid

    def _get_category_id(self, category_code: str) -> Optional[int]:
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT category_id FROM test_categories WHERE category_code = ?',
            (category_code,)
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def query_results(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        query = '''
            SELECT 
                tr.test_date,
                tr.patient_name,
                tr.test_name,
                tr.result_value,
                tr.unit,
                tr.reference_range,
                tr.flag,
                tr.category_code,
                '' as category_name
            FROM test_results tr
            WHERE 1=1
        '''
        params = []
        if filters.get('patient_name'):
            query += ' AND tr.patient_name LIKE ?'
            params.append(f"%{filters['patient_name']}%")
        if filters.get('start_date'):
            query += ' AND tr.test_date >= ?'
            params.append(filters['start_date'])
        if filters.get('end_date'):
            query += ' AND tr.test_date <= ?'
            params.append(filters['end_date'])
        if filters.get('category'):
            query += ' AND tr.category_code = ?'
            params.append(filters['category'])
        query += ' ORDER BY tr.test_date DESC, tr.test_name'
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]

        # Enrich each row with full category name from code if missing or blank
        from src.config import Config
        cfg = Config()
        code_to_name = cfg.get_all_categories()
        for r in rows:
            if r.get('category_code'):
                r['category_name'] = code_to_name.get(r['category_code'], r.get('category_name', ''))
        return rows

    def export_to_csv(self, output_file: str):
        results = self.query_results({})
        if not results:
            self.logger.warning("No results to export")
            return
        from src.config import Config
        cfg = Config()
        code_to_name = cfg.get_all_categories()
        # Force enrichment and deduplicate keeping latest test_id for identical measurements
        dedup_index = {}
        for row in results:
            code = row.get('category_code')
            if code:
                row['category_name'] = code_to_name.get(code, '')
            # Key representing a unique analytical measurement
            key = (
                row.get('test_date'),
                row.get('patient_name'),
                row.get('test_name'),
                row.get('result_value'),
                row.get('unit'),
                row.get('reference_range'),
            )
            existing = dedup_index.get(key)
            # Keep the row with the highest test_id (latest ingestion) if duplicate
            if existing is None or (row.get('test_id') and existing.get('test_id', 0) < row.get('test_id', 0)):
                dedup_index[key] = row
        cleaned = list(dedup_index.values())
        # Sort by test_date desc then test_name
        cleaned.sort(key=lambda r: (r.get('test_date') or '', r.get('test_name') or ''), reverse=True)
        if not cleaned:
            self.logger.warning("All rows filtered out; nothing to export")
            return
        
        # Define column order with test_date first (no test_id, test_month, test_year)
        column_order = [
            'test_date', 'patient_name', 'category_name', 'category_code',
            'test_name', 'result_value', 'unit', 'reference_range', 'flag'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_order, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(cleaned)
        self.logger.info(f"Exported {len(cleaned)} deduplicated results to {output_file}")

    def _migrate_schema(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA table_info(test_results)")
            cols = [row[1] for row in cursor.fetchall()]
            
            # Check if we need to migrate from old schema (test_id FK) to new schema (test_date)
            if 'test_id' in cols and 'test_date' not in cols:
                self.logger.info("Migrating schema: restructuring test_results to use test_date")
                # Create new table with updated schema
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS test_results_new (
                        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_date DATE NOT NULL,
                        patient_name TEXT,
                        test_name TEXT NOT NULL,
                        result_value TEXT NOT NULL,
                        unit TEXT,
                        reference_range TEXT,
                        flag TEXT,
                        category_code TEXT,
                        pdf_filename TEXT
                    )
                ''')
                # Migrate existing data
                cursor.execute('''
                    INSERT INTO test_results_new 
                    (test_date, patient_name, test_name, result_value, unit, reference_range, flag, category_code, pdf_filename)
                    SELECT bt.test_date, p.name, tr.test_name, tr.result_value, tr.unit, 
                           tr.reference_range, tr.flag, tr.category_code, bt.pdf_filename
                    FROM test_results tr
                    JOIN blood_tests bt ON tr.test_id = bt.test_id
                    JOIN patients p ON bt.patient_id = p.patient_id
                ''')
                # Drop old table and rename new one
                cursor.execute('DROP TABLE test_results')
                cursor.execute('ALTER TABLE test_results_new RENAME TO test_results')
                # Recreate indexes
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_results_date ON test_results(test_date)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_results_patient ON test_results(patient_name)')
                self.conn.commit()
                self.logger.info("Schema migration completed successfully")
            elif 'category_code' not in cols:
                self.logger.info("Migrating schema: adding category_code column to test_results")
                cursor.execute("ALTER TABLE test_results ADD COLUMN category_code TEXT")
                self.conn.commit()
        except sqlite3.Error as e:
            self.logger.error(f"Schema migration failed: {e}")
            self.conn.rollback()

    def drop_all_tables(self):
        try:
            cursor = self.conn.cursor()
            for tbl in ["test_results", "blood_tests", "patients", "test_categories"]:
                cursor.execute(f"DROP TABLE IF EXISTS {tbl}")
            self.conn.commit()
            self.logger.info("All tables dropped successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Error dropping tables: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            self.logger.info("Database connection closed")

    def save_query_results(self, results, filters):
        """Save query results to database table"""
        cursor = self.conn.cursor()
        filter_text = ', '.join([f"{k}={v}" for k, v in filters.items()])
        
        for result in results:
            cursor.execute('''
                INSERT INTO query_results 
                (query_filters, test_date, patient_name, category_name, test_name, 
                 result_value, unit, reference_range, flag, pdf_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                filter_text,
                result['test_date'],
                result['patient_name'],
                result['category_name'],
                result['test_name'],
                result['result_value'],
                result['unit'],
                result['reference_range'],
                result['flag'],
                result.get('pdf_source', '')
            ))
        
        self.conn.commit()
        return cursor.rowcount

    def get_saved_queries(self, limit=10):
        """Retrieve saved query results"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT query_date, query_filters, COUNT(*) as result_count
            FROM query_results
            GROUP BY query_date, query_filters
            ORDER BY query_date DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    def export_query_results_to_csv(self, output_file, query_date=None):
        """Export saved query results to CSV"""
        cursor = self.conn.cursor()
        if query_date:
            cursor.execute('''
                SELECT test_date, patient_name, category_name, test_name,
                       result_value, unit, reference_range, flag, query_filters
                FROM query_results
                WHERE query_date = ?
                ORDER BY test_date, category_name, test_name
            ''', (query_date,))
        else:
            cursor.execute('''
                SELECT test_date, patient_name, category_name, test_name,
                       result_value, unit, reference_range, flag, query_filters
                FROM query_results
                ORDER BY query_date DESC, test_date, category_name, test_name
            ''')
        
        results = cursor.fetchall()
        if results:
            import csv
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Test Date', 'Patient', 'Category', 'Test', 
                               'Result', 'Unit', 'Reference', 'Flag', 'Query Filters'])
                writer.writerows(results)