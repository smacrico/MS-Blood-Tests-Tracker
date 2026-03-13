import re

test_lines = [
    'Lp (α) - Λιποπρωτείνη (α) . . . . . . . . . . . . . . : 24.10 mg/dL < 30.00',
    'Βιταμίνη D-3 (25-ΟΗ) . . . . . . . . . . . . . . . . . : 56.6 ng/mL Έλλειψη: <11',
    'Μη- HDL χοληστερόλη(non-HDL-C) . . . . . . . : 153.0 mg/dL Σύμφωνα με τις οδηγίες του',
]

# Pattern 1: threshold with operator (< 30.00)
pattern1 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+([<>]=?)\s*(\d+\.?\d*)'

# Pattern 2: threshold in Greek text (Έλλειψη: <11)
pattern2 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)\s+[Α-ΩΆ-Ώα-ωά-ώ\s]+:\s*([<>]=?)\s*(\d+\.?\d*)'

# Pattern 3: just value and unit, no threshold
pattern3 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)'

print("Line 1 (Lp):")
for i, pattern in enumerate([pattern1, pattern2, pattern3], 1):
    match = re.search(pattern, test_lines[0])
    print(f"  Pattern {i}: {match.groups() if match else 'NO MATCH'}")

print("\nLine 2 (Vitamin D-3):")
for i, pattern in enumerate([pattern1, pattern2, pattern3], 1):
    match = re.search(pattern, test_lines[1])
    print(f"  Pattern {i}: {match.groups() if match else 'NO MATCH'}")

print("\nLine 3 (non-HDL):")
for i, pattern in enumerate([pattern1, pattern2, pattern3], 1):
    match = re.search(pattern, test_lines[2])
    print(f"  Pattern {i}: {match.groups() if match else 'NO MATCH'}")
