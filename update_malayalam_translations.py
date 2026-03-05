"""Update Malayalam translations using the actual Malayalam Quran data"""
import json
import os
from app import app, db, Verse, Surah

def update_malayalam_translations():
    """Update verses with proper Malayalam translations from the DAWA - Copy data"""
    
    with app.app_context():
        print("Updating Malayalam translations...")
        
        # Load Malayalam Quran data
        quran_ml_file = r"c:\DAWA - Copy\data\quran_ml.json"
        
        if not os.path.exists(quran_ml_file):
            print("Malayalam Quran file not found!")
            return False
            
        with open(quran_ml_file, 'r', encoding='utf-8') as f:
            quran_ml = json.load(f)
        
        print(f"Loaded {len(quran_ml)} Surahs from Malayalam file")
        
        updated_count = 0
        
        # Process each Surah
        for surah_ml in quran_ml:
            surah_num = surah_ml['number']
            verses_ml = surah_ml.get('verses', [])
            
            print(f"Processing Surah {surah_num}")
            
            # Create verse translation mapping
            translation_dict = {verse['number']: verse.get('text_en', '') for verse in verses_ml}
            
            # Update verses in database
            for verse_num, malayalam_text in translation_dict.items():
                # Find verses for this Surah number
                verses = Verse.query.join(Surah).filter(Surah.number == surah_num, Verse.verse_number == verse_num).all()
                
                for verse in verses:
                    if verse.translation_ml != malayalam_text:
                        verse.translation_ml = malayalam_text
                        updated_count += 1
                        print(f"  Updated verse {verse_num}")
        
        # Commit changes
        db.session.commit()
        
        print(f"Updated {updated_count} Malayalam translations!")
        return True

if __name__ == '__main__':
    update_malayalam_translations()
