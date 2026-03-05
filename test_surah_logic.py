"""Test surah verses logic"""
from app import app, db, Surah, Verse

def test_surah_verses():
    with app.app_context():
        # Get Surah Al-Baqarah
        surah = Surah.query.filter_by(number=2).first()
        
        if surah:
            print(f"Surah: {surah.number}")
            print(f"surah.verses exists: {bool(surah.verses)}")
            print(f"surah.verses length: {len(surah.verses) if surah.verses else 0}")
            
            # Test the template logic
            if surah.verses:
                print("Template will show verses: YES")
            else:
                print("Template will show verses: NO - will show 'ആയത്തുകൾ ഇതുവരെ ചേർത്തിട്ടില്ല'")
                
        else:
            print("Surah not found")

if __name__ == '__main__':
    test_surah_verses()
