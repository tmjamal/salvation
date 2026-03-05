"""Simple test to check slideshow generation"""
from app import app, db, Verse, Hadith, Story, Article, Dialogue
import random

def test_slideshow():
    with app.app_context():
        print("Testing slideshow generation...")
        
        # 1. Random Verse from Quran
        random_verse = None
        all_verses_count = Verse.query.count()
        print(f"Total verses: {all_verses_count}")
        if all_verses_count > 0:
            random_verse = Verse.query.offset(random.randint(0, all_verses_count - 1)).first()
            print(f"Random verse found: {random_verse.verse_number}")
        
        # 2. Random Hadith
        random_hadith = None
        all_hadiths_count = Hadith.query.count()
        print(f"Total hadiths: {all_hadiths_count}")
        if all_hadiths_count > 0:
            random_hadith = Hadith.query.offset(random.randint(0, all_hadiths_count - 1)).first()
            print(f"Random hadith found: {random_hadith.hadith_number}")
        
        # 3. Random Story
        random_story = None
        all_stories_count = Story.query.count()
        print(f"Total stories: {all_stories_count}")
        if all_stories_count > 0:
            random_story = Story.query.offset(random.randint(0, all_stories_count - 1)).first()
            print(f"Random story found: {random_story.title_ml[:50]}...")
        
        # 4. Random Article
        random_article = None
        all_articles_count = Article.query.count()
        print(f"Total articles: {all_articles_count}")
        if all_articles_count > 0:
            random_article = Article.query.offset(random.randint(0, all_articles_count - 1)).first()
            print(f"Random article found: {random_article.title_ml[:50]}...")
        
        # 5. Random Dialogue
        random_dialogue = None
        all_dialogues_count = Dialogue.query.count()
        print(f"Total dialogues: {all_dialogues_count}")
        if all_dialogues_count > 0:
            random_dialogue = Dialogue.query.offset(random.randint(0, all_dialogues_count - 1)).first()
            print(f"Random dialogue found: {random_dialogue.title_ml[:50]}...")

        slideshow_items = []
        if random_verse:
            slideshow_items.append({
                'type': 'ഖുർആൻ വചനം',
                'title': f'{random_verse.surah.name_malayalam} ({random_verse.surah.number}:{random_verse.verse_number})',
                'content': random_verse.translation_ml,
                'color': 'emerald'
            })
        if random_hadith:
            slideshow_items.append({
                'type': 'ഹദീസ്',
                'title': random_hadith.collection.name_ml if random_hadith.collection else 'ഹദീസ്',
                'content': random_hadith.text_ml,
                'color': 'sky'
            })
        if random_story:
            slideshow_items.append({
                'type': 'കഥ',
                'title': random_story.title_ml,
                'content': random_story.short_desc_ml or (random_story.full_content_ml[:150] + '...'),
                'color': 'amber'
            })
        if random_article:
            slideshow_items.append({
                'type': 'ലേഖനം',
                'title': random_article.title_ml,
                'content': random_article.summary_ml or (random_article.content_ml[:150] + '...'),
                'color': 'slate'
            })
        if random_dialogue:
            slideshow_items.append({
                'type': 'സംവാദം',
                'title': random_dialogue.title_ml,
                'content': random_dialogue.description_ml or 'പ്രമുഖ പണ്ഡിതരുടെ സംവാദങ്ങൾ.',
                'color': 'red'
            })

        random.shuffle(slideshow_items)
        
        print(f"\nFinal slideshow items count: {len(slideshow_items)}")
        for i, item in enumerate(slideshow_items):
            print(f"{i+1}. {item['type']}: {item['title'][:50]}...")

if __name__ == '__main__':
    test_slideshow()
