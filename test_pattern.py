#!/usr/bin/env python3
"""Test regex pattern manually"""

import re

test_line = "ΕΡΥΘΡΑ ΑΙΜΟΣΦΑΙΡΙΑ (RBC) . . . . . . . . . . . . : 5.67 M/μl 4.50 - 6.10"

# Current pattern
pattern1 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z\s]+?)\s*\(([A-Z][A-Z0-9]{1,6})\)\s*[.:]+\s*([\d.]+)\s+([A-Za-zµμ/%#]+)\s+([\d.]+)\s*-\s*([\d.]+)'

m = re.search(pattern1, test_line)

print(f"Testing line: {test_line}\n")
print(f"Pattern: {pattern1}\n")

if m:
    print("Match found!")
    print(f"Groups: {m.groups()}")
else:
    print("NO MATCH!")
    
    # Debug: What's between value and ref_min?
    value_to_range = re.search(r'5\.67(.*?)4\.50', test_line)
    if value_to_range:
        between = value_to_range.group(1)
        print(f"\nBetween value and range: '{between}'")
        print(f"  Bytes: {between.encode('utf-8')}")
        print(f"  Characters: {[c for c in between]}")
    
    # Try a more flexible unit pattern
    flexible_pattern = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z\s]+?)\s*\(([A-Z][A-Z0-9]{1,6})\)\s*[.:]+\s*([\d.]+)\s+([^\s]+)\s+([\d.]+)\s*-\s*([\d.]+)'
    m2 = re.search(flexible_pattern, test_line)
    if m2:
        print("\n✓ Flexible pattern matched!")
        print(f"Groups: {m2.groups()}")
        print(f"  Greek name: '{m2.group(1)}'")
        print(f"  Abbr: '{m2.group(2)}'")
        print(f"  Value: '{m2.group(3)}'")
        print(f"  Unit: '{m2.group(4)}'")
        print(f"  Ref min: '{m2.group(5)}'")
        print(f"  Ref max: '{m2.group(6)}'")
