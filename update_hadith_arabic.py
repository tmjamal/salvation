"""Update existing Hadith records with Arabic text from DAWA - Copy"""
import json
import os
from app import app, db, Hadith, HadithCollection

def update_hadith_arabic_text():
    """Update existing Hadith records with Arabic text"""
    
    with app.app_context():
        print("Updating Hadith Arabic text...")
        
        # Load Hadith data files
        data_dir = r"c:\DAWA - Copy\data"
        
        hadith_files = [
            ('hadith_bukhari_ar.json', 'Sahih Bukhari'),
            ('hadith_muslim_ar.json', 'Sahih Muslim')
        ]
        
        total_updated = 0
        
        for ar_file, collection_name in hadith_files:
            ar_path = os.path.join(data_dir, ar_file)
            
            if not os.path.exists(ar_path):
                print(f"Arabic file not found: {ar_file}")
                continue
            
            # Load Arabic data
            with open(ar_path, 'r', encoding='utf-8') as f:
                hadith_ar = json.load(f)
            
            print(f"Processing {collection_name}: {len(hadith_ar)} hadiths")
            
            # Find collection
            collection = HadithCollection.query.filter_by(name_en=collection_name).first()
            if not collection:
                print(f"Collection not found: {collection_name}")
                continue
            
            updated_count = 0
            
            # Update hadiths
            for i, hadith_ar_item in enumerate(hadith_ar):
                arabic_text = hadith_ar_item.get('text_en', '')
                
                if arabic_text:
                    # Find hadith by collection and number
                    hadith = Hadith.query.filter_by(
                        collection_id=collection.id,
                        hadith_number=i + 1
                    ).first()
                    
                    if hadith and hadith.text_arabic != arabic_text:
                        hadith.text_arabic = arabic_text
                        updated_count += 1
                        
                        if updated_count % 100 == 0:
                            print(f"  Updated {updated_count} hadiths...")
            
            # Commit changes
            db.session.commit()
            total_updated += updated_count
            print(f"  Updated {updated_count} hadiths for {collection_name}")
        
        print(f"Total hadiths updated with Arabic text: {total_updated}")
        return True

if __name__ == '__main__':
    print("Update Hadith Arabic Text")
    print("="*40)
    
    success = update_hadith_arabic_text()
    
    if success:
        print("\nUpdate completed successfully!")
    else:
        print("Update failed!")
