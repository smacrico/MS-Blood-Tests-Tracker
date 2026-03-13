import pdfplumber
from pathlib import Path

# Check a different PDF to see its format
pdf_file = Path('data/pdfs/proccessed/blood_10072025.PDF')

print(f"=== Examining {pdf_file.name} ===\n")

with pdfplumber.open(pdf_file) as pdf:
    print(f"Total pages: {len(pdf.pages)}\n")
    
    for page_num, page in enumerate(pdf.pages[:2], 1):  # First 2 pages
        print(f"--- Page {page_num} ---")
        
        # Check tables
        tables = page.extract_tables()
        if tables:
            print(f"Found {len(tables)} table(s)")
            for i, table in enumerate(tables[:1], 1):  # First table
                print(f"\nTable {i} (first 5 rows):")
                for row in table[:5]:
                    print(f"  {row}")
        
        # Check text
        text = page.extract_text()
        if text:
            lines = text.split('\n')[:30]  # First 30 lines
            print(f"\nText (first 30 lines):")
            for line in lines:
                if line.strip():
                    print(f"  {line}")
        
        print("\n")
