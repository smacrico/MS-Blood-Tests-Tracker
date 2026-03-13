import re

line = 'ΓΛΥΚΟΖΥΛΙΩΜΕΝΗ HBA1c . . . . . . . . . . . . . : 5.0 % >= 1 έτους:'

# Current pattern from text parser (threshold-based)
pattern2 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z\s\-]+?)\s*(?:\(([A-Z\-]+)\))?\s*[.\s:]+(\d+\.?\d*)\s+([^\s]+)\s+.*?([<>])\s*(\d+\.?\d*)'
m = re.search(pattern2, line)
if m:
    print('Current pattern match:', m.groups())
    greek_name, abbr, val, unit, operator, threshold = m.groups()
    print(f'Greek name: "{greek_name}"')
    print(f'Abbr: {abbr}')
    if abbr:
        test_name = f"{greek_name.strip()} ({abbr.strip()})"
    else:
        test_name = greek_name.strip()
    print(f'Test name would be: "{test_name}"')
else:
    print('NO MATCH with current pattern')

# Try pattern that includes numbers and handles >= operator
pattern_with_numbers = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z0-9\s]+?)\s*[.\s:]+(\d+\.?\d*)\s+([^\s]+)\s+.*?([<>]=?)\s*(\d+)'
m2 = re.search(pattern_with_numbers, line)
if m2:
    print('\nPattern with numbers and >=:', m2.groups())
    test_name, val, unit, operator, threshold = m2.groups()
    print(f'Test name: "{test_name.strip()}"')
    print(f'Value: {val} {unit}')
    print(f'Reference: {operator} {threshold}')
