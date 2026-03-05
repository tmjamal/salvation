#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data restoration script for Salvation website
Restores stories, articles, Quran verses, and Hadith
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app import app, db
from datetime import datetime

def restore_sample_data():
    """Restore sample Islamic content"""
    with app.app_context():
        print("🕌 Restoring Salvation website data...")
        
        # Import models
        from app import StoryCategory, Story, ArticleCategory, Article, Verse, Hadith, PageHit
        
        # 1. Create Story Categories
        print("📖 Creating story categories...")
        story_categories = [
            StoryCategory(
                name_en='Islamic Stories',
                name_ml='ഇസ്ലാമിക കഥകൾ',
                slug='islamic-stories',
                description_ml='ഇസ്ലാമിക കഥകളും ശേഷങ്ങൾ',
                icon='🕌',
                image_url='https://images.unsplash.com/photo-1542816871-8f6f4b6c6c0b5d.jpg'
            ),
            StoryCategory(
                name_en='Prophet Stories',
                name_ml='പ്രവാചകകഥകൾ',
                slug='prophet-stories',
                description_ml='പ്രവാചകന്മാരുടെ ജീവിതകഥകൾ',
                icon='👳',
                image_url='https://images.unsplash.com/photo-1546428777-8c2b1b9a5e5c.jpg'
            ),
            StoryCategory(
                name_en='Companion Stories',
                name_ml='സഹാബാകളുടെ കഥകൾ',
                slug='companion-stories',
                description_ml='സഹാബാകളുടെ ജീവിതവും സംഭാവനകളും',
                icon='👥',
                image_url='https://images.unsplash.com/photo-1506905925346-21bda4d32df4.jpg'
            )
        ]
        
        for cat in story_categories:
            existing = StoryCategory.query.filter_by(slug=cat.slug).first()
            if not existing:
                db.session.add(cat)
        
        # 2. Create Article Categories
        print("📝 Creating article categories...")
        article_categories = [
            ArticleCategory(
                name_en='Islamic Beliefs',
                name_ml='ഇസ്ലാമിക വിശ്വാസങ്ങൾ',
                slug='islamic-beliefs',
                description_ml='ഇസ്ലാമിന്റെ അടിസ്ഥാന വിശ്വാസങ്ങൾ',
                icon='🌙',
                image_url='https://images.unsplash.com/photo-1598427783068-4a962018d48b.jpg'
            ),
            ArticleCategory(
                name_en='Prayer & Worship',
                name_ml='നമസ്കാരവും ആരാധനയും',
                slug='prayer-worship',
                description_ml='നമസ്കാരം, റോസ, സകാത്ത് തുടങ്ങിയവ',
                icon='🙏',
                image_url='https://images.unsplash.com/photo-1594736797933-d0acc24019e5.jpg'
            ),
            ArticleCategory(
                name_en='Islamic Ethics',
                name_ml='ഇസ്ലാമിക ധാർമ്മികത',
                slug='islamic-ethics',
                description_ml='ഇസ്ലാമിക നൈതികതയും നന്മയും',
                icon='💚',
                image_url='https://images.unsplash.com/photo-1589391886645-d51941baf7fb.jpg'
            )
        ]
        
        for cat in article_categories:
            existing = ArticleCategory.query.filter_by(slug=cat.slug).first()
            if not existing:
                db.session.add(cat)
        
        # 3. Add Sample Stories
        print("📖 Adding sample stories...")
        islamic_cat = StoryCategory.query.filter_by(slug='islamic-stories').first()
        prophet_cat = StoryCategory.query.filter_by(slug='prophet-stories').first()
        
        stories = [
            Story(
                category_id=islamic_cat.id if islamic_cat else 1,
                title_en='The Power of Prayer',
                title_ml='പ്രാർത്ഥനയുടെ ശക്തി',
                slug='power-of-prayer',
                short_desc_ml='പ്രാർത്ഥനയുടെ മഹത്വവും പ്രാധാന്യവും',
                full_content_ml='<h2>പ്രാർത്ഥനയുടെ ശക്തി</h2><p>അല്ലാഹുവിനോടുള്ള പ്രാർത്ഥന ഒരു മുസ്ലിമിന്റെ ജീവിതത്തിൽ ഏറ്റവും പ്രധാനമായ കാര്യമാണ്. അവന്റെ അടുത്തേക്ക് എത്തുന്നതിനുള്ള മാർഗമാണ് പ്രാർത്ഥന.</p><p>പ്രവാചകൻ (സ) പറഞ്ഞു: "പ്രാർത്ഥന ഇസ്ലാമിന്റെ തൂൺ ആണ്."</p>',
                video_url='https://www.youtube.com/watch?v=example',
                image_url='https://images.unsplash.com/photo-1542816871-8f6f4b6c6c0b5d.jpg',
                order=1
            ),
            Story(
                category_id=prophet_cat.id if prophet_cat else 2,
                title_en='Prophet Muhammad (PBUH)',
                title_ml='പ്രവാചകൻ മുഹമ്മദ് (സ)',
                slug='prophet-muhammad',
                short_desc_ml='മനുഷ്യരക്ക് അയകപ്പെട്ട അവസാനത്തെ പ്രവാചകൻ',
                full_content_ml='<h2>പ്രവാചകൻ മുഹമ്മദ് (സ)</h2><p>അല്ലാഹു മനുഷ്യരക്കായി അയച്ച അവസാനത്തെ പ്രവാചകനാണ് മുഹമ്മദ് ഇബ്നു അബ്ദുല്ല (സ). അദ്ദേഹത്തിന്റെ ജീവിതം മനുഷ്യത്വത്തിന് മാതൃകയാണ്.</p>',
                video_url='https://www.youtube.com/watch?v=example',
                image_url='https://images.unsplash.com/photo-1546428777-8c2b1b9a5e5c.jpg',
                order=2
            )
        ]
        
        for story in stories:
            existing = Story.query.filter_by(slug=story.slug).first()
            if not existing:
                db.session.add(story)
        
        # 4. Add Sample Articles
        print("📝 Adding sample articles...")
        beliefs_cat = ArticleCategory.query.filter_by(slug='islamic-beliefs').first()
        prayer_cat = ArticleCategory.query.filter_by(slug='prayer-worship').first()
        
        articles = [
            Article(
                category_id=beliefs_cat.id if beliefs_cat else 1,
                title_ml='ഇസ്ലാമിന്റെ അടിസ്ഥാനങ്ങൾ',
                slug='basics-of-islam',
                summary_ml='ഇസ്ലാമിന്റെ അടിസ്ഥാന വിശ്വാസങ്ങളെ കുറിച്ച്',
                content_ml='<h2>ഇസ്ലാമിന്റെ അടിസ്ഥാനങ്ങൾ</h2><p>ഇസ്ലാം അഞ്ച് അടിസ്ഥാന തത്വങ്ങളിൽ അധിഷ്ഠിതമാണ്:</p><ol><li>ഖുർആൻ</li><li>സുന്നത്ത്</li><li>ഇഖ്ലാസ്</li><li>തൗഹീദ്</li><li>അഖീദ</li></ol>',
                author='സ്രഷ്ടാവിന്റെ മാർഗദർശനം',
                image_url='https://images.unsplash.com/photo-1594736797933-d0acc24019e5.jpg',
                is_featured=True
            ),
            Article(
                category_id=prayer_cat.id if prayer_cat else 2,
                title_ml='നമസ്കാരത്തിന്റെ പ്രാധാന്യം',
                slug='importance-of-prayer',
                summary_ml='നമസ്കാരത്തിന്റെ ഇസ്ലാമിലെ സ്ഥാനം',
                content_ml='<h2>നമസ്കാരത്തിന്റെ പ്രാധാന്യം</h2><p>നമസ്കാരം ഇസ്ലാമിലെ രണ്ടാമത്തെ തൂണാണ്. അല്ലാഹുവിനോടുള്ള ആരാധനയിൽ ഏറ്റവും പ്രധാനമായത് നമസ്കാരമാണ്.</p>',
                author='സ്രഷ്ടാവിന്റെ മാർഗദർശനം',
                image_url='https://images.unsplash.com/photo-1594736797933-d0acc24019e5.jpg',
                is_featured=False
            )
        ]
        
        for article in articles:
            existing = Article.query.filter_by(slug=article.slug).first()
            if not existing:
                db.session.add(article)
        
        # 5. Add Quran Verses (Sample)
        print("📖 Adding Quran verses...")
        verses = [
            Verse(
                surah_id=1,
                verse_number=1,
                text_arabic='بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ',
                translation_ml='അനുഗ്രഹിക്കുന്നതും കരുണാനിധനായ അല്ലാഹുവിന്റെ നാമത്തിൽ',
                tafsir_ml='എല്ലാ നന്മകളും ചെയ്യുന്നതും എല്ലാ സൃഷ്ടികൾക്കും കരുണ ചെയ്യുന്നതുമായ അല്ലാഹുവിന്റെ നാമത്തിൽ'
            ),
            Verse(
                surah_id=1,
                verse_number=2,
                text_arabic='الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ',
                translation_ml='സർവ്വലോകരക്ഷിതാവായ അല്ലാഹുവിന് സ്തുതി',
                tafsir_ml='ലോകങ്ങളുടെ രക്ഷിതാവും നിയന്താവുമായ അല്ലാഹുവിന് എല്ലാ സ്തുതിയും'
            ),
            Verse(
                surah_id=1,
                verse_number=3,
                text_arabic='الرَّحْمَٰنِ الرَّحِيمِ',
                translation_ml='അനുഗ്രഹിക്കുന്നവനും കരുണാനിധിയുമായ അല്ലാഹു',
                tafsir_ml='അനുഗ്രഹം നൽകുന്നവനും കരുണ ചെയ്യുന്നവനുമായ അല്ലാഹു'
            ),
            Verse(
                surah_id=1,
                verse_number=4,
                text_arabic='مَالِكِ يَوْمِ الدِّينِ',
                translation_ml='വിധിനാളിന്റെ ഉടമസ്ഥൻ',
                tafsir_ml='പ്രളയ ദിനത്തിന്റെ ഉടമസ്ഥനും വിധികർത്താവുമായ അല്ലാഹു'
            )
        ]
        
        for verse in verses:
            existing = Verse.query.filter_by(surah_id=verse.surah_id, verse_number=verse.verse_number).first()
            if not existing:
                db.session.add(verse)
        
        # 6. Add Hadith (Sample)
        print("📜 Adding Hadith...")
        hadiths = [
            Hadith(
                text_arabic='إِنَّمَا الْأَعْمَالُ بِالنِّيَّاتِ',
                translation_ml='പ്രവൃത്തികൾ നിയതികൾ അനുസരിച്ചാണ്',
                tafsir_ml='ഒരു പ്രവൃത്തിയുടെ മൂല്യം അത് ചെയ്യുന്നയാളുടെ ഉദ്ദേശം അനുസരിച്ചായിരിക്കും',
                narrator='ഉമർ (റ)',
                source='ബുഖാരി',
                category='നിയതികൾ'
            ),
            Hadith(
                text_arabic='مَنْ قَالَ لَا إِلَٰهَ إِلَّا اللَّهُ دَخَلَ الْجَنَّةَ',
                translation_ml='അല്ലാഹുവിനു പുറമെ ദൈവമില്ലെന്ന് പറയുന്നയാൾ സ്വർഗ്ഗത്തിൽ പ്രവേശിക്കും',
                tafsir_ml='വിശുദ്ധമായ ഈ വാക്യം സത്യമായി പറയുകയും അതനുസരിച്ച് ജീവിക്കുകയും ചെയ്യുന്നയാൾക്ക് സ്വർഗ്ഗം ലഭിക്കും',
                narrator='അബു ഹുറൈറ (റ)',
                source='മുസ്ലിം',
                category='വിശ്വാസം'
            )
        ]
        
        for hadith in hadiths:
            existing = Hadith.query.filter_by(text_arabic=hadith.text_arabic).first()
            if not existing:
                db.session.add(hadith)
        
        # Commit all changes
        db.session.commit()
        print("✅ Data restoration completed successfully!")
        print("🕌 Your Salvation website now has Islamic content!")
        
        # Print summary
        print("\n📊 Added Content Summary:")
        print(f"📖 Story Categories: {len(story_categories)}")
        print(f"📝 Article Categories: {len(article_categories)}")
        print(f"📖 Stories: {len(stories)}")
        print(f"📝 Articles: {len(articles)}")
        print(f"📖 Quran Verses: {len(verses)}")
        print(f"📜 Hadith: {len(hadiths)}")

if __name__ == '__main__':
    restore_sample_data()
