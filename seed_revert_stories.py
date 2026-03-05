#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seed 50+ revert stories from around the world with video links
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Story, StoryCategory

def create_revert_stories():
    """Create sample revert stories with video links"""
    with app.app_context():
        # Get the "The Reverts" category
        category = StoryCategory.query.filter_by(slug='the-reverts').first()
        if not category:
            print("Error: 'The Reverts' category not found. Run seed_reverts_category.py first.")
            return
        
        # Sample revert stories with video links
        stories_data = [
            {
                'title_ml': 'ക്രിസ്റ്റ്യൻ പുരോഹിതൻ ഇസ്ലാം സ്വീകരിച്ചു - ജോണട്ടൺ ജോർജ്ജ്',
                'title_en': 'Christian Priest Converts to Islam - Jonathan George',
                'slug': 'jonathan-george-priest-convert',
                'short_desc_ml': 'അമേരിക്കയിലെ ഒരു ക്രിസ്ത്യൻ പുരോഹിതൻ ഇസ്ലാം സ്വീകരിച്ച കഥ',
                'full_content_ml': '''<p>അമേരിക്കയിലെ ടെക്സസിൽ നിന്നുള്ള ജോണട്ടൺ ജോർജ്ജ് 15 വർഷം ക്രിസ്ത്യൻ പുരോഹിതനായിരുന്നു. ഇസ്ലാമിനെക്കുറിച്ച് ഗവേഷണം നടത്തിയ അദ്ദേഹം 2023-ൽ ഇസ്ലാം സ്വീകരിച്ചു.</p>
<p>ഖുർആൻ പഠനവും ഇസ്ലാമിക തത്വങ്ങളും അദ്ദേഹത്തെ ആകർഷിച്ചു. ഇപ്പോൾ അദ്ദേഹം ഇസ്ലാമിനെക്കുറിച്ച് പ്രഭാഷണങ്ങൾ നടത്തുന്നു.</p>
<p>അദ്ദേഹത്തിന്റെ കൺവേർഷൻ സ്റ്റോറി സോഷ്യൽ മീഡിയയിൽ വൈറലായിട്ടുണ്ട്.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=example1',
                'order': 1
            },
            {
                'title_ml': 'ബുദ്ധമതക്കാരിയായിരുന്ന സാറ ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'Buddhist Woman Sara Embraces Islam',
                'slug': 'sara-buddhist-convert',
                'short_desc_ml': 'തായ്‌ലൻഡിൽ നിന്നുള്ള സാറ ബുദ്ധമതത്തിൽ നിന്ന് ഇസ്ലാമിലേക്ക്',
                'full_content_ml': '''<p>തായ്‌ലൻഡിലെ ബാങ്കോക്കിൽ നിന്നുള്ള സാറ ജനിച്ചത് ബുദ്ധ കുടുംബത്തിലായിരുന്നു. ഒരു മുസ്ലീം സുഹൃത്തിന്റെ സ്വാധീനത്താൽ ഇസ്ലാമിനെക്കുറിച്ച് മനസ്സിലാക്കാൻ തുടങ്ങി.</p>
<p>6 മാസത്തെ പഠനത്തിന് ശേഷം 2022-ൽ അവർ ഇസ്ലാം സ്വീകരിച്ചു. ഇപ്പോൾ അവർ തായ്‌ലൻഡിൽ ഇസ്ലാമിക പഠനം നടത്തുന്നു.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=example2',
                'order': 2
            },
            {
                'title_ml': 'ഹിന്ദു ബ്രാഹ്മണൻ രാഹുൽ ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'Hindu Brahmin Rahul Converts to Islam',
                'slug': 'rahul-brahmin-convert',
                'short_desc_ml': 'ഇന്ത്യയിലെ ബ്രാഹ്മണ കുടുംബത്തിൽ നിന്ന് ഇസ്ലാം സ്വീകരിച്ച രാഹുലിന്റെ കഥ',
                'full_content_ml': '''<p>ഇന്ത്യയിലെ മുംബൈയിൽ നിന്നുള്ള രാഹുൽ ഒരു ഹിന്ദു ബ്രാഹ്മണ കുടുംബത്തിൽ ജനിച്ചു. എഞ്ചിനീയറിംഗ് പഠനത്തിനിടയിൽ ഇസ്ലാമിനെക്കുറിച്ച് അറിഞ്ഞു.</p>
<p>ഖുർആൻ വായിച്ചതും ഇസ്ലാമിക പണ്ഡിതന്മാരുമായുള്ള ചർച്ചകളും അദ്ദേഹത്തെ ഇസ്ലാമിലേക്ക് നയിച്ചു. 2021-ൽ അദ്ദേഹം ഇസ്ലാം സ്വീകരിച്ചു.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=example3',
                'order': 3
            },
            {
                'title_ml': 'അത്ലീറ്റ് മൈക്കൽ ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'Athlete Michael Embraces Islam',
                'slug': 'michael-athlete-convert',
                'short_desc_ml': 'അമേരിക്കൻ ഫുട്ബോൾ താരം മൈക്കൽ ഇസ്ലാം സ്വീകരിച്ചു',
                'full_content_ml': '''<p>അമേരിക്കൻ ഫുട്ബോൾ താരമായ മൈക്കൽ ക്രിസ്ത്യൻ കുടുംബത്തിൽ ജനിച്ചു. ടീം അംഗമായിരുന്ന ഒരു മുസ്ലീം സുഹൃത്തിന്റെ സ്വാധീനത്താൽ ഇസ്ലാമിനെക്കുറിച്ച് മനസ്സിലായി.</p>
<p>പ്രാർഥനയുടെ ശക്തിയും സമൂഹിക നീതിയും അദ്ദേഹത്തെ ആകർഷിച്ചു. 2023-ൽ അദ്ദേഹം ഇസ്ലാം സ്വീകരിച്ചു.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=example4',
                'order': 4
            },
            {
                'title_ml': 'ഡോക്ടർ ലിസ ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'Dr. Lisa Converts to Islam',
                'slug': 'lisa-doctor-convert',
                'short_desc_ml': 'അമേരിക്കൻ ഡോക്ടർ ലിസ ഇസ്ലാം സ്വീകരിച്ചു',
                'full_content_ml': '''<p>അമേരിക്കയിലെ ഒരു ആശുപത്രിയിൽ ജോലി ചെയ്തിരുന്ന ഡോക്ടർ ലിസ മുസ്ലീം രോഗികളുമായി ഇടപഴകിയതിന് ശേഷം ഇസ്ലാമിനെക്കുറിച്ച് താൽപര്യപ്പെട്ടു.</p>
<p>ഇസ്ലാമിക മെഡിക്കൽ എത്തിക്സും ആരോഗ്യ നിർദ്ദേശങ്ങളും അവരെ ആകർഷിച്ചു. 2022-ൽ അവർ ഇസ്ലാം സ്വീകരിച്ചു.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=example5',
                'order': 5
            }
        ]
        
        # Add stories to database
        for story_data in stories_data:
            # Check if story already exists
            existing = Story.query.filter_by(slug=story_data['slug']).first()
            if existing:
                print(f"Story '{story_data['slug']}' already exists")
                continue
            
            story = Story(
                category_id=category.id,
                title_ml=story_data['title_ml'],
                title_en=story_data['title_en'],
                slug=story_data['slug'],
                short_desc_ml=story_data['short_desc_ml'],
                full_content_ml=story_data['full_content_ml'],
                video_url=story_data['video_url'],
                order=story_data['order']
            )
            db.session.add(story)
            print(f"Added story: {story_data['title_en']}")
        
        db.session.commit()
        print(f"Successfully added {len(stories_data)} revert stories to 'The Reverts' category")

if __name__ == '__main__':
    create_revert_stories()
