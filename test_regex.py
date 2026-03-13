import re

line = 'ΕΡΥΘΡΑ ΑΙΜΟΣΦΑΙΡΙΑ (RBC) . . . : 5.67 M/μl 4.50 - 6.10'

# Test: non-greedy greek name
pattern = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z\s]+?)\s*\(([A-Z][A-Z0-9]{1,6})\)\s*[.:]+\s+(\d+\.?\d*)\s+([^\s]+)\s+(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'
m = re.search(pattern, line)
print(f"Non-greedy + \\s+: {m.groups() if m else 'NO MATCH'}")

# Test: Debugging - what does the name capture?
name_test = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z\s]+?)\s*\(RBC\)'
m_name = re.search(name_test, line)
if m_name:
    print(f"Name captured: '{m_name.group(1)}'")

# Test: Full pattern step by step
print("\nStep-by-step:")
p1 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z\s]+?)'
print(f"  Greek name: {re.search(p1, line).group(1) if re.search(p1, line) else 'NO'}")

p2 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z\s]+?)\s*\(([A-Z]+)\)'
m2 = re.search(p2, line)
print(f"  Greek + (ABBR): {m2.groups() if m2 else 'NO'}")

p3 = r'([Α-ΩA-ZΆ-Ώα-ωά-ώA-Za-z\s]+?)\s*\(([A-Z]+)\)\s*[.:]+\s+(\d+\.?\d*)'
m3 = re.search(p3, line)
print(f"  + dots + number: {m3.groups() if m3 else 'NO'}")
