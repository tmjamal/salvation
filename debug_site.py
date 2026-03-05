"""Debug script to check what's happening with the site"""
import requests
import json

def test_site():
    try:
        # Test home page
        response = requests.get('http://127.0.0.1:5000')
        print(f"Home page status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"Page length: {len(content)} characters")
            
            # Check for key elements
            if 'slideshow_items' in content:
                print("OK: Slideshow items found in template")
            else:
                print("ERROR: Slideshow items NOT found in template")
                
            if 'heroSlideshow' in content:
                print("OK: Hero slideshow element found")
            else:
                print("ERROR: Hero slideshow element NOT found")
                
            if 'toggleTab' in content:
                print("OK: Tab function found")
            else:
                print("ERROR: Tab function NOT found")
                
            # Check for slideshow data
            if 'slideshow_items' in content and '[]' not in content:
                print("OK: Slideshow has data")
            else:
                print("ERROR: Slideshow might be empty")
        else:
            print(f"ERROR: {response.status_code}")
            
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == '__main__':
    test_site()
