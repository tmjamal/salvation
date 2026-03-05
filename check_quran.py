"""Check Quran data for Surah Al-Baqarah"""
from app import app, db, Surah, Verse

def check_quran_data():
    with app.app_context():
        print("=== Quran Data Check ===")
        
        # Find Surah Al-Baqarah (should be surah number 2)
        baqarah = Surah.query.filter_by(number=2).first()
        
        if baqarah:
            print(f"Found Surah Number: {baqarah.number}")
            print(f"Total Verses: {baqarah.total_verses}")
            
            # Check verses for this surah
            verses = Verse.query.filter_by(surah_id=baqarah.id).all()
            print(f"Verses in database: {len(verses)}")
            
            if verses:
                print("First 5 verses:")
                for i, verse in enumerate(verses[:5], 1):
                    print(f"  {i}. {verse.verse_number}")
            else:
                print("NO VERSES FOUND for Surah Al-Baqarah!")
                
        else:
            print("Surah Al-Baqarah not found!")
            
        # Check all surahs
        all_surahs = Surah.query.all()
        print(f"\nTotal Surahs in database: {len(all_surahs)}")
        
        # Check which surahs have verses
        surahs_with_verses = 0
        for surah in all_surahs:
            verse_count = Verse.query.filter_by(surah_id=surah.id).count()
            if verse_count > 0:
                surahs_with_verses += 1
                
        print(f"Surahs with verses: {surahs_with_verses}")
        print(f"Surahs without verses: {len(all_surahs) - surahs_with_verses}")

if __name__ == '__main__':
    check_quran_data()
