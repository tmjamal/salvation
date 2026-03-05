"""Check Hadith database content to see language issue"""
from app import app, db, Hadith, HadithCollection

def check_hadith_content():
    """Check what language content is in the database"""
    
    with app.app_context():
        print("Checking Hadith database content...")
        
        collections = HadithCollection.query.all()
        
        for collection in collections:
            print(f"\n=== {collection.name_en} (ID: {collection.id}) ===")
            
            # Get first few hadiths from this collection
            hadiths = Hadith.query.filter_by(collection_id=collection.id).limit(3).all()
            
            for hadith in hadiths:
                print(f"\nHadith {hadith.hadith_number}:")
                arabic_preview = hadith.text_arabic[:50] if hadith.text_arabic else 'None'
                malayalam_preview = hadith.text_ml[:50] if hadith.text_ml else 'None'
                print(f"Arabic length: {len(hadith.text_arabic) if hadith.text_arabic else 0}")
                print(f"Malayalam length: {len(hadith.text_ml) if hadith.text_ml else 0}")
                
                # Check if Malayalam text contains English words
                if hadith.text_ml:
                    # Simple check for English words
                    english_words = ['the', 'and', 'of', 'to', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 'are', 'with', 'as', 'his', 'they', 'I']
                    text_lower = hadith.text_ml.lower()
                    english_count = sum(1 for word in english_words if word in text_lower)
                    
                    if english_count > 5:
                        print(f"Appears to be English text ({english_count} English words found)")
                    else:
                        print(f"Appears to be Malayalam text")

if __name__ == '__main__':
    check_hadith_content()
