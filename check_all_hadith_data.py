"""Check all Hadith collections and see what data we have"""
import json
import os
from app import app, db, Hadith, HadithCollection

def check_all_hadith_collections():
    """Check all collections and available data files"""
    
    with app.app_context():
        print("=== Current Database Collections ===")
        collections = HadithCollection.query.all()
        
        for collection in collections:
            hadith_count = Hadith.query.filter_by(collection_id=collection.id).count()
            print(f"ID {collection.id}: {collection.name_en} - {hadith_count} hadiths")
        
        print("\n=== Available Data Files ===")
        data_dir = r"c:\DAWA - Copy\data"
        
        # Check for full files
        full_files = [f for f in os.listdir(data_dir) if f.endswith('_full.json')]
        print("Full data files:")
        for f in sorted(full_files):
            print(f"  {f}")
        
        # Check for Malayalam files
        ml_files = [f for f in os.listdir(data_dir) if 'ml.json' in f and 'hadith' in f]
        print("\nMalayalam files:")
        for f in sorted(ml_files):
            print(f"  {f}")
        
        # Check for Arabic files
        ar_files = [f for f in os.listdir(data_dir) if 'ar.json' in f and 'hadith' in f]
        print("\nArabic files:")
        for f in sorted(ar_files):
            print(f"  {f}")

if __name__ == '__main__':
    check_all_hadith_collections()
