"""Generate Malayalam translations for missing Hadith collections"""
import json
import os
from app import app, db, Hadith, HadithCollection

def generate_malayalam_for_missing_collections():
    """Generate Malayalam translations for collections that don't have them"""
    
    with app.app_context():
        print("Generating Malayalam translations for missing collections...")
        
        # Collections that need Malayalam translations
        collections_needing_ml = [
            'Jami at-Tirmidhi',
            'Sunan an-Nasai', 
            'Sunan Ibn Majah',
            'Sunan Abu Dawud'
        ]
        
        for collection_name in collections_needing_ml:
            collection = HadithCollection.query.filter_by(name_en=collection_name).first()
            if not collection:
                print(f"Collection not found: {collection_name}")
                continue
            
            print(f"\nProcessing {collection_name} (ID: {collection.id})...")
            
            # Get all hadiths from this collection
            hadiths = Hadith.query.filter_by(collection_id=collection.id).all()
            print(f"Found {len(hadiths)} hadiths")
            
            updated_count = 0
            
            for hadith in hadiths:
                # Simple Malayalam translation placeholder
                # In a real implementation, you'd use Google Translate API
                current_text = hadith.text_ml
                
                # Check if it's English (simple heuristic)
                english_words = ['the', 'and', 'of', 'to', 'in', 'is', 'it', 'you', 'that', 'he']
                text_lower = current_text.lower()
                english_count = sum(1 for word in english_words if word in text_lower)
                
                if english_count > 5:  # Likely English text
                    # Create a simple Malayalam placeholder
                    malayalam_placeholder = f"ഹദീസ് {hadith.hadith_number}: {collection_name} - വിവർത്തനം ലഭ്യമാക്കുന്നു"
                    
                    if hadith.text_ml != malayalam_placeholder:
                        hadith.text_ml = malayalam_placeholder
                        updated_count += 1
                        
                        if updated_count % 100 == 0:
                            print(f"  Updated {updated_count} hadiths...")
            
            # Commit changes
            db.session.commit()
            print(f"  Updated {updated_count} hadiths with Malayalam placeholders")
        
        print("\nMalayalam placeholder generation completed!")
        return True

if __name__ == '__main__':
    print("Generate Malayalam for Missing Hadith Collections")
    print("="*55)
    
    success = generate_malayalam_for_missing_collections()
    
    if success:
        print("\nProcess completed!")
    else:
        print("Process failed!")
