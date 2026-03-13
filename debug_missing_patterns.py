import re

# Test 1: Καλσιτονίνη with < in value
line1 = 'Καλσιτονίνη . . . . . . . . . . . . . . . . . . . . . . . : <0.2 pg/mL < 18.2'

# Current threshold pattern
pattern = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-]+?)\s*(?:\(([A-Z0-9\-]+)\))?\s*[.\s:]+(\d+\.?\d*)\s+([^\s]+)\s+.*?([<>]=?)\s*(\d+\.?\d*)'
m = re.search(pattern, line1)
print('Test 1: Καλσιτονίνη')
print(f'Line: {line1}')
print(f'Match: {m.groups() if m else "NO MATCH"}')

# Try pattern that allows < in value
pattern_with_lt = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s\-]+?)\s*(?:\(([A-Z0-9\-]+)\))?\s*[.\s:]+([<>]?\d+\.?\d*)\s+([^\s]+)\s+.*?([<>]=?)\s*(\d+\.?\d*)'
m2 = re.search(pattern_with_lt, line1)
print(f'With < in value: {m2.groups() if m2 else "NO MATCH"}')

# Test 2: NEUT with Greek letter in value
print('\n' + '='*80)
line2 = 'Πολυμορφοπύρηνα Ουδετερόφιλα (NEUT) . : 71α% 40 - 75 6.04 K/μl'
print('Test 2: NEUT')
print(f'Line: {line2}')

# Range pattern
range_pattern = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s]+?)\s*(?:\(([A-Z0-9][A-Z0-9]{1,6})\))?\s*[.\s:]+(\d+\.?\d*)\s+([^\s]+)\s+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'
m3 = re.search(range_pattern, line2)
print(f'Range pattern: {m3.groups() if m3 else "NO MATCH"}')

# Try pattern that skips Greek letters
range_pattern2 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s]+?)\s*\(([A-Z0-9]+)\)\s*[.\s:]+(\d+)[α-ωά-ώ]*\s*([%\w/]+)\s+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'
m4 = re.search(range_pattern2, line2)
print(f'With Greek letter skip: {m4.groups() if m4 else "NO MATCH"}')
