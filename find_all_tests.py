import pdfplumber
import re

# Open PDF
pdf = pdfplumber.open('data/pdfs/bloodResults_23092025.pdf')
all_text = '\n'.join([page.extract_text() for page in pdf.pages])
pdf.close()

# Find all potential test lines (Greek name followed by dots and colon)
# Pattern: Greek/Latin name ... : number unit
pattern = r'^([Α-ΩΆ-Ώα-ωά-ώA-Za-z\s\-\(\)]+?)\s*[.\s:]{3,}\s*:\s*(\d+\.?\d*)\s+([^\s]+)'

print("=== All potential test lines in PDF ===\n")
lines = all_text.split('\n')
found_tests = []

for line in lines:
    line = line.strip()
    if not line or len(line) < 10:
        continue
    
    # Look for pattern of test name ... : value unit
    if re.search(r'[.\s:]{3,}\s*:', line) and re.search(r'\d+\.?\d*', line):
        # Extract just the first 80 chars for readability
        display_line = line[:100] if len(line) > 100 else line
        
        # Try to extract test name
        match = re.match(r'^([Α-ΩΆ-Ώα-ωά-ώA-Za-z\s\-\(\)]+?)\s*[.\s:]+', line)
        if match:
            test_name = match.group(1).strip()
            if test_name and len(test_name) > 2:
                found_tests.append((test_name, display_line))

# Remove duplicates and sort
unique_tests = {}
for test_name, line in found_tests:
    if test_name not in unique_tests:
        unique_tests[test_name] = line

print(f"Found {len(unique_tests)} unique test patterns:\n")
for test_name in sorted(unique_tests.keys()):
    print(f"{test_name}")
    print(f"  Line: {unique_tests[test_name]}")
    print()
