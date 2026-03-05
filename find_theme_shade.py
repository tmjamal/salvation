"""Find theme-shade class definition"""
with open('c:\\PEDIA\\static\\css\\style.css', 'r', encoding='utf-8') as f:
    content = f.read()
    
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'theme-shade' in line and not line.strip().startswith('/*'):
        print(f"Line {i}: {line.strip()}")
