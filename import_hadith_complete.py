"""Import complete Hadith data with Arabic and Malayalam text from DAWA - Copy"""
import json
import os
from app import app, db, Hadith, HadithCollection

def import_hadith_data():
    """Import Hadith data with Arabic and Malayalam text"""
    
    with app.app_context():
        print("Starting Hadith import with Arabic and Malayalam text...")
        
        # Load Hadith data files
        data_dir = r"c:\DAWA - Copy\data"
        
        hadith_files = [
            ('hadith_bukhari_ar.json', 'hadith_bukhari_ml.json', 'സഹീഹ് ബുഖാരി', 'Sahih Bukhari', '📘'),
            ('hadith_muslim_ar.json', 'hadith_muslim_ml.json', 'സഹീഹ് മുസ്‌ലിം', 'Sahih Muslim', '📗')
        ]
        
        total_imported = 0
        
        for ar_file, ml_file, name_ml, name_en, icon in hadith_files:
            ar_path = os.path.join(data_dir, ar_file)
            ml_path = os.path.join(data_dir, ml_file)
            
            if not os.path.exists(ar_path) or not os.path.exists(ml_path):
                print(f"Files not found for {name_ml}")
                continue
            
            # Load Arabic and Malayalam data
            with open(ar_path, 'r', encoding='utf-8') as f:
                hadith_ar = json.load(f)
            
            with open(ml_path, 'r', encoding='utf-8') as f:
                hadith_ml = json.load(f)
            
            print(f"Processing collection: {len(hadith_ar)} Arabic, {len(hadith_ml)} Malayalam")
            
            # Find or create collection
            collection = HadithCollection.query.filter_by(name_ml=name_ml).first()
            if not collection:
                collection = HadithCollection(
                    name_ml=name_ml,
                    name_en=name_en,
                    slug=name_en.lower().replace(' ', '-'),
                    description_ml=f"{name_ml} ഹദീസ് ശേഖരം",
                    icon=icon
                )
                db.session.add(collection)
                db.session.flush()  # Get the ID
            
            imported_count = 0
            
            # Process hadiths (match by reference)
            for i, hadith_ar_item in enumerate(hadith_ar):
                if i < len(hadith_ml):
                    hadith_ml_item = hadith_ml[i]
                    
                    # Extract reference info
                    reference = hadith_ar_item.get('reference', '')
                    hadith_number = reference.split('Hadith ')[-1] if 'Hadith ' in reference else str(i + 1)
                    
                    # Extract chapter info
                    chapter_ml = reference.split('Book ')[-1].split(',')[0] if 'Book ' in reference else ''
                    
                    # Check if hadith already exists
                    existing_hadith = Hadith.query.filter_by(
                        collection_id=collection.id,
                        hadith_number=hadith_number
                    ).first()
                    
                    if existing_hadith:
                        # Update existing
                        existing_hadith.text_arabic = hadith_ar_item.get('text_en', '')
                        existing_hadith.text_ml = hadith_ml_item.get('text_en', '')
                        existing_hadith.hadith_number = hadith_number
                        existing_hadith.chapter_ml = chapter_ml
                        existing_hadith.grade = 'സഹീഹ്'
                    else:
                        # Add new hadith
                        new_hadith = Hadith(
                            collection_id=collection.id,
                            text_arabic=hadith_ar_item.get('text_en', ''),
                            text_ml=hadith_ml_item.get('text_en', ''),
                            hadith_number=hadith_number,
                            chapter_ml=chapter_ml,
                            grade='സഹീഹ്'
                        )
                        db.session.add(new_hadith)
                        imported_count += 1
            
            # Commit after each collection
            db.session.commit()
            total_imported += imported_count
            print(f"  Imported {imported_count} new hadiths")
        
        print(f"Total hadiths imported: {total_imported}")
        return True

def check_hadith_summary():
    """Check current Hadith database summary"""
    with app.app_context():
        collections = HadithCollection.query.all()
        total_hadiths = 0
        
        for collection in collections:
            hadith_count = Hadith.query.filter_by(collection_id=collection.id).count()
            total_hadiths += hadith_count
            print(f"Collection {collection.id}: {hadith_count} hadiths")
        
        print(f"\nTotal collections: {len(collections)}")
        print(f"Total hadiths: {total_hadiths}")

if __name__ == '__main__':
    print("Hadith Import with Arabic and Malayalam Text")
    print("="*50)
    
    success = import_hadith_data()
    
    if success:
        print("\n" + "="*50)
        print("Database Summary:")
        check_hadith_summary()
    else:
        print("Import failed!")
