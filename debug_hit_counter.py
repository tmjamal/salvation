"""Debug hit counter with detailed logging"""
from app import app, db, PageHit, track_page_hit
from flask import request

def debug_hit_counter():
    print("=== DEBUG HIT COUNTER ===")
    
    with app.app_context():
        # Check current hits
        total_hits = PageHit.query.count()
        print(f"Current total hits: {total_hits}")
        
        # Test with manual hit
        print("\nTesting manual hit creation...")
        try:
            with app.test_request_context():
                # Mock request data
                request.environ = {
                    'HTTP_X_FORWARDED_FOR': '127.0.0.1',
                    'REMOTE_ADDR': '127.0.0.1',
                    'HTTP_USER_AGENT': 'Test Browser',
                    'HTTP_REFERER': 'http://test.com'
                }
                
                # Test the function
                track_page_hit('http://test.com/debug', 'Debug Test Page')
                
                # Check if hit was added
                new_total = PageHit.query.count()
                print(f"New total hits: {new_total}")
                print(f"Hits added: {new_total - total_hits}")
                
                if new_total > total_hits:
                    print("SUCCESS: Hit tracking is working!")
                else:
                    print("FAILED: Hit tracking not working")
                    
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    debug_hit_counter()
