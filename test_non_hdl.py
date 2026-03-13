import re

line = 'Μη- HDL χοληστερόλη(non-HDL-C) . . . . . . . : 153.0 mg/dL Σύμφωνα με τις οδηγίες του'

# Current pattern (with space before parenthesis)
pattern1 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*(?:\(([A-Z0-9\-]+)\))?\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)'

# Updated pattern (no space required before parenthesis, make abbreviation optional)
pattern2 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*(?:\(([A-Za-z0-9\-]+)\))?\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)'

print("Testing current pattern:")
match = re.search(pattern1, line)
if match:
    print(f"  Matched: {match.groups()}")
else:
    print(f"  NO MATCH")

print("\nTesting updated pattern (allow lowercase in abbr):")
match = re.search(pattern2, line)
if match:
    print(f"  Matched: {match.groups()}")
else:
    print(f"  NO MATCH")

# Try to match as simple name without abbreviation extraction
pattern3 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-\(\)]+?)\s*[.\s:]+([<>]?\d+\.?\d*)[α-ωά-ώ]*\s*([^\s]+)'
print("\nTesting as simple name pattern:")
match = re.search(pattern3, line)
if match:
    print(f"  Matched: {match.groups()}")
    print(f"  Test name would be: '{match.group(1).strip()}'")
else:
    print(f"  NO MATCH")
