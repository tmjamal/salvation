"""Check hit counter data"""
from app import app, db, PageHit

def check_hits():
    with app.app_context():
        print("=== Hit Counter Check ===")
        
        # Total hits
        total_hits = PageHit.query.count()
        print(f"Total hits: {total_hits}")
        
        # Today's hits
        from datetime import datetime
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_hits = PageHit.query.filter(PageHit.visit_date >= today).count()
        print(f"Today's hits: {today_hits}")
        
        # Recent hits
        recent_hits = PageHit.query.order_by(PageHit.visit_date.desc()).limit(5).all()
        print("\nRecent hits:")
        for hit in recent_hits:
            print(f"  - {hit.page_url} - {hit.visit_date}")
        
        # Popular pages
        from sqlalchemy import func
        popular_pages = db.session.query(
            PageHit.page_url,
            PageHit.page_title,
            func.count(PageHit.id).label('hits')
        ).group_by(PageHit.page_url, PageHit.page_title).order_by(func.count(PageHit.id).desc()).limit(5).all()
        
        print("\nPopular pages:")
        for page in popular_pages:
            print(f"  - {page.hits} hits: {page.page_url}")

if __name__ == '__main__':
    check_hits()
