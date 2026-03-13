import re

test_lines = [
    'Lp (α) - Λιποπρωτείνη (α) . . . . . . . . . . . . . . : 24.10 mg/dL < 30.00',
    'Βιταμίνη D-3 (25-ΟΗ) . . . . . . . . . . . . . . . . . : 56.6 ng/mL Έλλειψη: <11',
    'Μη- HDL χοληστερόλη(non-HDL-C) . . . . . . . : 153.0 mg/dL Σύμφωνα με τις οδηγίες του',
]

# Current pattern (simplified)
current_pattern = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s]+?)\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+([<>]=?)\s*(\d+\.?\d*)'

# Updated pattern with parentheses, hyphens
updated_pattern = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+([<>]=?)\s*(\d+\.?\d*)'

print("Testing current pattern:")
for line in test_lines:
    match = re.search(current_pattern, line)
    if match:
        print(f"✓ Matched: {match.groups()}")
    else:
        print(f"✗ No match: {line[:50]}")

print("\nTesting updated pattern (with parentheses and hyphens):")
for line in test_lines:
    match = re.search(updated_pattern, line)
    if match:
        print(f"✓ Matched: {match.groups()}")
    else:
        print(f"✗ No match: {line[:50]}")
