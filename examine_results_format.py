import pdfplumber
from pathlib import Path

# Check the new format PDF
pdf_file = Path('data/pdfs/results_2022-2023.pdf')

print(f"=== Examining {pdf_file.name} ===\n")

with pdfplumber.open(pdf_file) as pdf:
    print(f"Total pages: {len(pdf.pages)}\n")
    
    for page_num in [0, 1]:  # First 2 pages
        page = pdf.pages[page_num]
        print(f"--- Page {page_num + 1} ---")
        
        # Check tables
        tables = page.extract_tables()
        if tables:
            print(f"Found {len(tables)} table(s)")
            for i, table in enumerate(tables[:1], 1):
                print(f"\nTable {i} (first 10 rows):")
                for row in table[:10]:
                    print(f"  {row}")
        
        # Check text
        text = page.extract_text()
        if text:
            lines = text.split('\n')[:40]
            print(f"\nText (first 40 lines):")
            for line in lines:
                if line.strip():
                    print(f"  {line}")
        
        print("\n")
