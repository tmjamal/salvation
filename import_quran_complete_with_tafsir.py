"""Import complete Quran with verses and tafsir from DAWA - Copy data files"""
import json
import os
from app import app, db, Surah, Verse

def load_tafsir(surah_number):
    """Load tafsir for a specific Surah"""
    tafsir_file = rf"c:\DAWA - Copy\data\tafsir\{surah_number}.json"
    if os.path.exists(tafsir_file):
        with open(tafsir_file, 'r', encoding='utf-8') as f:
            tafsir_data = json.load(f)
            return tafsir_data.get('ayahs', [])
    return []

def import_complete_quran_with_tafsir():
    """Import complete Quran with Arabic text, Malayalam translation, and tafsir"""
    
    with app.app_context():
        print("Starting complete Quran import with Tafsir...")
        
        # Load Quran data files
        data_dir = r"c:\DAWA - Copy\data"
        
        quran_ar_file = os.path.join(data_dir, "quran_ar.json")
        quran_ml_file = os.path.join(data_dir, "quran_ml.json")
        
        if not os.path.exists(quran_ar_file) or not os.path.exists(quran_ml_file):
            print("Quran data files not found!")
            return False
            
        with open(quran_ar_file, 'r', encoding='utf-8') as f:
            quran_ar_data = json.load(f)
            quran_ar = quran_ar_data.get('data', {}).get('surahs', [])
            
        with open(quran_ml_file, 'r', encoding='utf-8') as f:
            quran_ml_data = json.load(f)
            quran_ml = quran_ml_data  # Malayalam file has different structure
        
        print(f"Loaded {len(quran_ar)} Surahs from Arabic file")
        print(f"Loaded {len(quran_ml)} Surahs from Malayalam file")
        
        imported_verses = 0
        updated_verses = 0
        tafsir_added = 0
        
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
            
            print(f"Processing Surah {surah_num}")
            
            # Load tafsir for this Surah
            tafsir_ayahs = load_tafsir(surah_num)
            tafsir_dict = {ayah['ayah']: ayah.get('text', '') for ayah in tafsir_ayahs}
            
            # Process verses
            verses_ar = surah_ar.get('verses', [])
            verses_ml = surah_ml.get('verses', [])
            
            for verse_ar in verses_ar:
                verse_num = verse_ar['number']
                arabic_text = verse_ar.get('text_ar', '')
                
                # Find Malayalam translation
                verse_ml = next((v for v in verses_ml if v['number'] == verse_num), None)
                malayalam_text = verse_ml.get('text_en', '') if verse_ml else ''
                
                # Get tafsir for this verse
                tafsir_text = tafsir_dict.get(verse_num, '')
                
                # Check if verse exists
                existing_verse = Verse.query.filter_by(
                    surah_id=surah.id,
                    verse_number=verse_num
                ).first()
                
                if existing_verse:
                    # Update existing verse
                    existing_verse.text_arabic = arabic_text
                    existing_verse.translation_ml = malayalam_text
                    existing_verse.tafsir_ml = tafsir_text
                    updated_verses += 1
                    if tafsir_text:
                        tafsir_added += 1
                else:
                    # Add new verse
                    new_verse = Verse(
                        surah_id=surah.id,
                        verse_number=verse_num,
                        text_arabic=arabic_text,
                        translation_ml=malayalam_text,
                        tafsir_ml=tafsir_text
                    )
                    db.session.add(new_verse)
                    imported_verses += 1
                    if tafsir_text:
                        tafsir_added += 1
            
            # Commit every 5 Surahs to avoid memory issues
            if surah_num % 5 == 0:
                db.session.commit()
                print(f"Progress: Surah {surah_num}, Imported: {imported_verses}, Updated: {updated_verses}, Tafsir: {tafsir_added}")
        
        # Final commit
        db.session.commit()
        
        print(f"Complete Quran import finished!")
        print(f"Total new verses imported: {imported_verses}")
        print(f"Total verses updated: {updated_verses}")
        print(f"Total verses with tafsir: {tafsir_added}")
        print(f"Total verses processed: {imported_verses + updated_verses}")
        
        return True

def check_database_summary():
    """Check current database summary"""
    with app.app_context():
        surahs = Surah.query.all()
        total_verses = 0
        surahs_with_content = 0
        verses_with_tafsir = 0
        
        for surah in surahs:
            verse_count = Verse.query.filter_by(surah_id=surah.id).count()
            tafsir_count = Verse.query.filter(Verse.surah_id == surah.id, Verse.tafsir_ml.isnot(None), Verse.tafsir_ml != '').count()
            
            total_verses += verse_count
            verses_with_tafsir += tafsir_count
            
            if verse_count > 0:
                surahs_with_content += 1
                
            print(f"Surah {surah.number:3d}: {verse_count:3d} verses, {tafsir_count:3d} with tafsir")
        
        print(f"\nDatabase Summary:")
        print(f"Total Surahs: {len(surahs)}")
        print(f"Surahs with content: {surahs_with_content}")
        print(f"Total verses: {total_verses}")
        print(f"Verses with tafsir: {verses_with_tafsir}")
        if total_verses > 0:
            print(f"Tafsir coverage: {verses_with_tafsir/total_verses*100:.1f}%")

if __name__ == '__main__':
    print("Complete Quran Import with Tafsir from DAWA - Copy")
    print("="*60)
    
    # Run import
    success = import_complete_quran_with_tafsir()
    
    if success:
        print("\n" + "="*60)
        print("Database Summary After Import:")
        check_database_summary()
    else:
        print("Import failed!")
