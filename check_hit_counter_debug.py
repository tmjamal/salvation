"""Check hit counter status"""
from app import app, db, PageHit
from flask import request

def check_hit_counter():
    with app.app_context():
        # Check current total hits
        total_hits = PageHit.query.count()
        print(f"Current total hits: {total_hits}")
        
        # Check today's hits
        from datetime import datetime
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_hits = PageHit.query.filter(PageHit.visit_date >= today).count()
        print(f"Today's hits: {today_hits}")
        
        # Check recent hits
        recent_hits = PageHit.query.order_by(PageHit.visit_date.desc()).limit(5).all()
        print("Recent hits:")
        for hit in recent_hits:
            print(f"  - {hit.visit_date}: {hit.page_url}")
        
        # Test tracking function
        print("\nTesting track_page_hit function...")
        try:
            with app.test_request_context():
                # Simulate a home page visit
                from app import track_page_hit
                track_page_hit('http://test.com/home', 'Test Home Page')
                db.session.commit()
                print("Track page hit executed successfully")
        except Exception as e:
            print(f"Error in track_page_hit: {e}")

if __name__ == '__main__':
    check_hit_counter()
