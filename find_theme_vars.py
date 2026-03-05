"""Find theme variables in CSS"""
with open('c:\\PEDIA\\static\\css\\style.css', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Find all theme-related variables
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'theme-primary' in line or 'theme-secondary' in line or 'theme-shade' in line:
        print(f"Line {i}: {line.strip()}")

print("\n=== Checking for CSS variable definitions ===")
# Look for CSS variable definitions
for i, line in enumerate(lines, 1):
    if '--theme-primary' in line or '--theme-secondary' in line:
        print(f"Line {i}: {line.strip()}")
