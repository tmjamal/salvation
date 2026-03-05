"""Import complete Quran from the DAWA - Copy data files"""
import json
import os
from app import app, db, Surah, Verse

def import_complete_quran():
    """Import complete Quran with Arabic text and Malayalam translation"""
    
    with app.app_context():
        print("Starting complete Quran import...")
        
        # Load Quran data files
        data_dir = r"c:\DAWA - Copy\data"
        
        # Load Arabic Quran
        quran_ar_file = os.path.join(data_dir, "quran_ar.json")
        quran_ml_file = os.path.join(data_dir, "quran_ml.json")
        
        if not os.path.exists(quran_ar_file) or not os.path.exists(quran_ml_file):
            print("Quran data files not found!")
            return False
            
        with open(quran_ar_file, 'r', encoding='utf-8') as f:
            quran_ar = json.load(f)
            
        with open(quran_ml_file, 'r', encoding='utf-8') as f:
            quran_ml = json.load(f)
        
        print(f"Loaded {len(quran_ar)} Surahs from Arabic file")
        print(f"Loaded {len(quran_ml)} Surahs from Malayalam file")
        
        imported_verses = 0
        updated_verses = 0
        
        # Process each Surah
        for surah_ar in quran_ar:
            surah_num = surah_ar['number']
            
            # Find corresponding Malayalam Surah
            surah_ml = next((s for s in quran_ml if s['number'] == surah_num), None)
            
            if not surah_ml:
                print(f"Malayalam Surah {surah_num} not found")
                continue
                
            # Find Surah in database
            surah = Surah.query.filter_by(number=surah_num).first()
            if not surah:
                print(f"Surah {surah_num} not found in database")
                continue
            
            print(f"Processing Surah {surah_num}: {surah.name_malayalam}")
            
            # Process verses
            verses_ar = surah_ar.get('verses', [])
            verses_ml = surah_ml.get('verses', [])
            
            for verse_ar in verses_ar:
                verse_num = verse_ar['number']
                arabic_text = verse_ar.get('text_ar', '')
                
                # Find Malayalam translation
                verse_ml = next((v for v in verses_ml if v['number'] == verse_num), None)
                malayalam_text = verse_ml.get('text_en', '') if verse_ml else ''
                
                # Check if verse exists
                existing_verse = Verse.query.filter_by(
                    surah_id=surah.id,
                    verse_number=verse_num
                ).first()
                
                if existing_verse:
                    # Update existing verse
                    existing_verse.text_arabic = arabic_text
                    existing_verse.translation_ml = malayalam_text
                    updated_verses += 1
                else:
                    # Add new verse
                    new_verse = Verse(
                        surah_id=surah.id,
                        verse_number=verse_num,
                        text_arabic=arabic_text,
                        translation_ml=malayalam_text
                    )
                    db.session.add(new_verse)
                    imported_verses += 1
            
            # Commit every 5 Surahs to avoid memory issues
            if surah_num % 5 == 0:
                db.session.commit()
                print(f"Progress: Surah {surah_num}, Imported: {imported_verses}, Updated: {updated_verses}")
        
        # Final commit
        db.session.commit()
        
        print(f"✅ Quran import completed!")
        print(f"📊 Total new verses imported: {imported_verses}")
        print(f"📊 Total verses updated: {updated_verses}")
        print(f"📊 Total verses processed: {imported_verses + updated_verses}")
        
        return True

def check_current_database():
    """Check current database status"""
    with app.app_context():
        surahs = Surah.query.all()
        total_verses = 0
        surahs_with_content = 0
        
        for surah in surahs:
            verse_count = Verse.query.filter_by(surah_id=surah.id).count()
            total_verses += verse_count
            if verse_count > 0:
                surahs_with_content += 1
            print(f"Surah {surah.number}: {verse_count} verses")
        
        print(f"\n📊 Database Summary:")
        print(f"Total Surahs: {len(surahs)}")
        print(f"Surahs with content: {surahs_with_content}")
        print(f"Total verses: {total_verses}")

if __name__ == '__main__':
    print("Quran Import from DAWA - Copy")
    print("1. Check current database")
    print("2. Import complete Quran")
    
    choice = "2"  # Auto-run import
    
    if choice == "1":
        check_current_database()
    elif choice == "2":
        import_complete_quran()
        print("\n" + "="*50)
        print("After import:")
        check_current_database()
    else:
        print("Invalid choice")
