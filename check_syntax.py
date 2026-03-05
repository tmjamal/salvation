"""Check template syntax"""
def check_template_syntax():
    with open('c:\\PEDIA\\templates\\surah_detail.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count if blocks
    if_count = content.count('{% if')
    endif_count = content.count('{% endif')
    for_count = content.count('{% for')
    endfor_count = content.count('{% endfor}')
    
    print("Template syntax check:")
    print("  {% if blocks: " + str(if_count))
    print("  {% endif blocks: " + str(endif_count))
    print("  {% for blocks: " + str(for_count))
    print("  {% endfor blocks: " + str(endfor_count))
    
    if if_count != endif_count:
        print("MISMATCH: if and endif blocks don't match!")
    else:
        print("if/endif blocks match")
        
    if for_count != endfor_count:
        print("MISMATCH: for and endfor blocks don't match!")
    else:
        print("for/endfor blocks match")
    
    # Find all if blocks
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if '{% if' in line:
            print(f"Line {i}: {line.strip()}")
        if '{% endif' in line:
            print(f"Line {i}: {line.strip()}")

if __name__ == '__main__':
    check_template_syntax()
