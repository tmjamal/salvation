"""Find exact line with 827 in home.html"""
with open('c:\\PEDIA\\templates\\home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
for i, line in enumerate(lines, 1):
    if '827' in line:
        print(f"Line {i}: {line.strip()}")
