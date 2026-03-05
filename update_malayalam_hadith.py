"""Update Bukhari and Muslim collections with proper Malayalam translations"""
import json
import os
from app import app, db, Hadith, HadithCollection

def update_malayalam_translations():
    """Update Bukhari and Muslim with proper Malayalam translations"""
    
    with app.app_context():
        print("Updating Malayalam translations for available collections...")
        
        # Load Malayalam data files
        data_dir = r"c:\DAWA - Copy\data"
        
        malayalam_files = [
            ('hadith_bukhari_ml.json', 'Sahih Al-Bukhari'),
            ('hadith_muslim_ml.json', 'Sahih Muslim')
        ]
        
        total_updated = 0
        
        for ml_file, collection_name in malayalam_files:
            ml_path = os.path.join(data_dir, ml_file)
            
            if not os.path.exists(ml_path):
                print(f"Malayalam file not found: {ml_file}")
                continue
            
            # Load Malayalam data
            with open(ml_path, 'r', encoding='utf-8') as f:
                hadith_ml = json.load(f)
            
            print(f"Processing {collection_name}: {len(hadith_ml)} hadiths")
            
            # Find collection (try both names)
            collection = HadithCollection.query.filter_by(name_en=collection_name).first()
            if not collection:
                # Try alternative name
                if 'Bukhari' in collection_name:
                    collection = HadithCollection.query.filter_by(name_en='Sahih Bukhari').first()
                elif 'Muslim' in collection_name:
                    collection = HadithCollection.query.filter_by(name_en='Sahih Muslim').first()
            
            if not collection:
                print(f"Collection not found: {collection_name}")
                continue
            
            updated_count = 0
            
            # Update hadiths with Malayalam text
            for i, hadith_ml_item in enumerate(hadith_ml):
                malayalam_text = hadith_ml_item.get('text_en', '')
                
                if malayalam_text:
                    # Find hadith by collection and number
                    hadith = Hadith.query.filter_by(
                        collection_id=collection.id,
                        hadith_number=i + 1
                    ).first()
                    
                    if hadith and hadith.text_ml != malayalam_text:
                        hadith.text_ml = malayalam_text
                        updated_count += 1
                        
                        if updated_count % 50 == 0:
                            print(f"  Updated {updated_count} hadiths...")
            
            # Commit changes
            db.session.commit()
            total_updated += updated_count
            print(f"  Updated {updated_count} hadiths for {collection_name}")
        
        print(f"Total hadiths updated with Malayalam: {total_updated}")
        return True

if __name__ == '__main__':
    print("Update Hadith Malayalam Translations")
    print("="*45)
    
    success = update_malayalam_translations()
    
    if success:
        print("\nUpdate completed successfully!")
    else:
        print("Update failed!")
