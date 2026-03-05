"""Search for hardcoded hit counter values"""
import os
import re

def search_hardcoded_hits():
    hits_found = []
    
    # Search in all files
    for root, dirs, files in os.walk('c:\\PEDIA'):
        for file in files:
            if file.endswith(('.html', '.py', '.js', '.css')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Look for hit counter patterns
                    patterns = [
                        r'827',
                        r'hits?\s*[:\-\+]?\s*\d+',
                        r'visitors?\s*[:\-\+]?\s*\d+',
                        r'സന്ദർശനങ്ങൾ.*\d+',
                        r'total_hits.*\d+'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            hits_found.append({
                                'file': file_path,
                                'matches': matches
                            })
                            
                except Exception as e:
                    pass
    
    return hits_found

if __name__ == '__main__':
    results = search_hardcoded_hits()
    print("=== SEARCH RESULTS ===")
    for result in results:
        print(f"File: {result['file']}")
        for match in result['matches']:
            print(f"  Found: {match}")
        print()
