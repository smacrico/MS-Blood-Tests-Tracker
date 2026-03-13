# MS Blood Test Tracker

A Python project for monitoring multiple sclerosis through automated blood test result processing. This tool reads PDF files containing blood test results and organizes them into a structured SQLite database.

## Features

- 📄 PDF parsing for blood test results
- 🗄️ SQLite database for structured storage
- 📊 Categorization by test type, date, and month
- 🔍 Query interface for retrieving test results
- 📝 Comprehensive logging and error handling
- 🏥 Support for multiple test categories (CBC, liver function, kidney function, etc.)

## Project Structure

```
ms-blood-test-tracker/
├── src/
│   ├── __init__.py
│   ├── pdf_reader.py
│   ├── database_handler.py
│   ├── data_parser.py
│   └── config.py
├── data/
│   ├── pdfs/
│   └── ms_blood_tests.db
├── logs/
│   └── app.log
├── tests/
│   └── test_parser.py
├── main.py
├── requirements.txt
├── config.yaml
└── README.md
```

## Instructions

1. Place your PDF files into `data/pdfs/`.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the application: `python main.py`
4. Results will be stored in the SQLite database: `data/ms_blood_tests.db`.

## More features, troubleshooting, and details are provided in this readme. Please review the full details above!


# Step 1: Process PDFs and extract data
python main.py --pdf-dir data\pdfs

# Step 2: Export to CSV
python main.py --export results_complete.csv

# Step 3: Query specific data (optional)
python main.py --query --patient "ΜΑΚΡΥΚΩΣΤΑΣ ΣΤΥΛΙΑΝΟΣ"
python main.py --query --category CBC
python main.py --query --start-date 2023-01-01 --end-date 2025-12-31

# chancges 7 12 2025 - save query cttegories to table
# Query CBC category - results will be displayed AND saved to database
python main.py --query --category CBC

# Query by patient name
python main.py --query --patient "John Doe"

# Query by date range
python main.py --query --start-date 2024-01-01 --end-date 2024-12-31

# Query with multiple filters
python main.py --query --category CBC --start-date 2024-01-01

# Proposed Visualizations
Proposed Visualizations:
Trend Analysis Over Time - Track key health markers across dates
Test Status Distribution - Pie chart showing Normal/High/Low/Unknown distribution
Category-wise Test Count - Bar chart of tests by category
Abnormal Results Timeline - Highlight High/Low values over time
Key Health Markers Dashboard - Focus on important tests like cholesterol, glucose, etc.