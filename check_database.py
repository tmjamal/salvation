"""Check database content"""
from app import app, db, Verse, Hadith, Story, Article, Dialogue, Surah

def check_database():
    with app.app_context():
        print("=== Database Content Check ===")
        
        # Check verses
        verse_count = Verse.query.count()
        print(f"Verses: {verse_count}")
        
        # Check hadiths
        hadith_count = Hadith.query.count()
        print(f"Hadiths: {hadith_count}")
        
        # Check stories
        story_count = Story.query.count()
        print(f"Stories: {story_count}")
        
        # Check articles
        article_count = Article.query.count()
        print(f"Articles: {article_count}")
        
        # Check dialogues
        dialogue_count = Dialogue.query.count()
        print(f"Dialogues: {dialogue_count}")
        
        # Check surahs
        surah_count = Surah.query.count()
        print(f"Surahs: {surah_count}")
        
        print("\n=== Sample Data ===")
        
        # Sample verse
        if verse_count > 0:
            verse = Verse.query.first()
            print(f"Sample verse: {verse.surah.name_malayalam} {verse.verse_number}")
        else:
            print("No verses found")
            
        # Sample hadith
        if hadith_count > 0:
            hadith = Hadith.query.first()
            print(f"Sample hadith: {hadith.collection.name_ml if hadith.collection else 'No collection'}")
        else:
            print("No hadiths found")

if __name__ == '__main__':
    check_database()
