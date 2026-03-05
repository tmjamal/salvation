#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add 10 more revert stories with correct videos
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Story, StoryCategory

def add_more_stories():
    with app.app_context():
        category = StoryCategory.query.filter_by(slug='the-reverts').first()
        
        new_stories = [
            {
                'title_ml': 'ജർമ്മൻ വനിത ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'German Woman Converts to Islam',
                'slug': 'german-woman-convert',
                'short_desc_ml': 'ജർമ്മനിയിൽ നിന്നുള്ള വനിത ഇസ്ലാം സ്വീകരിച്ചു',
                'full_content_ml': '''<h3>ജർമ്മൻ വനിതയുടെ ഇസ്ലാം സ്വീകരണ കഥ</h3>
<p>ജർമ്മനിയിൽ നിന്നുള്ള ഒരു വനിത ഇസ്ലാം സ്വീകരിച്ചു. "ഞാൻ മുസ്ലീമായപ്പോൾ എനിക്ക് ഒരു സുഹൃത്തുക്കളെ ഇല്ലായിരുന്നു" എന്നാണ് അവർ പറയുന്നത്.</p>
<p>ഖുർആൻ പഠനത്തിലൂടെയും ഇസ്ലാമിക പണ്ഡിതന്മാരുമായുള്ള ചർച്ചകളിലൂടെയും അവർ ഇസ്ലാമിലെത്തി. ഇപ്പോൾ അവർ ജർമ്മനിയിൽ ഇസ്ലാമിനെക്കുറിച്ച് പ്രവർത്തിക്കുന്നു.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=WovtKZMnANQ',
                'order': 6
            },
            {
                'title_ml': 'ബ്രിട്ടീഷ് യുവാവ് ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'British Youth Converts to Islam',
                'slug': 'british-youth-convert',
                'short_desc_ml': 'ബ്രിട്ടനിൽ നിന്നുള്ള യുവാവ് ഇസ്ലാം സ്വീകരിച്ചു',
                'full_content_ml': '''<h3>ബ്രിട്ടീഷ് യുവാവിന്റെ ഇസ്ലാം സ്വീകരണ കഥ</h3>
<p>ബ്രിട്ടനിൽ നിന്നുള്ള ഒരു യുവാവ് ഇസ്ലാം സ്വീകരിച്ചു. പ്രശസ്തനായ ബ്രിട്ടീഷ് യൂട്യൂബർ ജെ പാൽഫ്രിയുടെ കഥയാണ് ഇത്.</p>
<p>ഇസ്ലാമിന്റെ സമാധാനവും ശാസ്ത്രീയതയും അദ്ദേഹത്തെ ആകർഷിച്ചു. ഇപ്പോൾ അദ്ദേഹം തന്റെ അനുഭവം പങ്കുവെക്കുന്നു.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=WVlZqWZJRvQ',
                'order': 7
            },
            {
                'title_ml': 'ജർമ്മൻ നിരീശ്വാരവാദി ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'German Atheist Girl Converts to Islam',
                'slug': 'german-atheist-convert',
                'short_desc_ml': 'ജർമ്മനിയിലെ നിരീശ്വാരവാദിയായിരുന്ന പെൺകുട്ടി ഇസ്ലാം സ്വീകരിച്ചു',
                'full_content_ml': '''<h3>നിരീശ്വാരവാദത്തിൽ നിന്ന് ഇസ്ലാമിലേക്ക്</h3>
<p>ജർമ്മനിയിലെ ഒരു നിരീശ്വാരവാദിയായിരുന്ന പെൺകുട്ടി ഇസ്ലാം സ്വീകരിച്ചു. അവരുടെ യാത്ര ഹൃദയസ്പർശിയാണ്.</p>
<p>ഗവേഷണത്തിലൂടെയും പഠനത്തിലൂടെയും അവർ ഇസ്ലാമിലെത്തി. ഇപ്പോൾ അവർ തന്റെ കഥ പങ്കുവെക്കുന്നു.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=XuNgM8gmojQ',
                'order': 8
            },
            {
                'title_ml': 'വെള്ളക്കാരായ ബ്രിട്ടീഷ് പുരുഷന്മാർ ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'White British Men Converted to Islam',
                'slug': 'british-white-men-convert',
                'short_desc_ml': 'വെള്ളക്കാരായ ബ്രിട്ടീഷ് പുരുഷന്മാൾ ഇസ്ലാം സ്വീകരിച്ചു',
                'full_content_ml': '''<h3>ബ്രിട്ടീഷ് പുരുഷന്മാരുടെ ഇസ്ലാം സ്വീകരണം</h3>
<p>വെള്ളക്കാരായ ബ്രിട്ടീഷ് പുരുഷന്മാൾ ഇസ്ലാം സ്വീകരിച്ചു. അവരുടെ കഥകൾ പ്രചോദനാത്മകമാണ്.</p>
<p>ഇസ്ലാമിന്റെ സന്ദേശങ്ങൾ അവരെ ആകർഷിച്ചു. ഇപ്പോൾ അവർ തങ്ങളുടെ അനുഭവങ്ങൾ പങ്കുവെക്കുന്നു.</p>''',
                'video_url': 'https://www.youtube.com/shorts/7GSfeDeFWzs',
                'order': 9
            },
            {
                'title_ml': 'ബ്രിട്ടീഷ് കുടുംബം ഇസ്ലാം സ്വീകരിച്ചു',
                'title_en': 'British Family Becomes Muslim',
                'slug': 'british-family-convert',
                'short_desc_ml': 'ഒരു ബ്രിട്ടീഷ് കുടുംബം മുഴുവൻ ഇസ്ലാം സ്വീകരിച്ചു',
                'full_content_ml': '''<h3>കുടുംബത്തിന്റെ ഇസ്ലാം സ്വീകരണം</h3>
<p>ഒരു ബ്രിട്ടീഷ് കുടുംബം മുഴുവൻ ഇസ്ലാം സ്വീകരിച്ചു. അച്ഛന്റെ അത്ഭുതകരമായ കഥയാണ് ഇത്.</p>
<p>കുടുംബം ഒന്നിച്ച് ഇസ്ലാം സ്വീകരിച്ചത് ഒരു പ്രചോദനമാണ്. ഇപ്പോൾ അവർ തങ്ങളുടെ അനുഭവം പങ്കുവെക്കുന്നു.</p>''',
                'video_url': 'https://www.youtube.com/watch?v=WSG14f-163Y',
                'order': 10
            }
        ]
        
        for story_data in new_stories:
            existing = Story.query.filter_by(slug=story_data['slug']).first()
            if not existing:
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
                print(f"Added: {story_data['title_en']}")
        
        db.session.commit()
        print("Added more revert stories")

if __name__ == '__main__':
    add_more_stories()
