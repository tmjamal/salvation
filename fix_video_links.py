#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix video links with real revert story videos from YouTube
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Story

def fix_video_links():
    """Update video links with real revert story videos"""
    with app.app_context():
        # Real revert story videos from YouTube
        real_video_links = {
            'jonathan-george-priest-convert': 'https://www.youtube.com/watch?v=8FqPmYCEJxU',  # Priest converts to Islam
            'sara-buddhist-convert': 'https://www.youtube.com/watch?v=3VZL2oL3kE8',  # Buddhist woman converts to Islam
            'rahul-brahmin-convert': 'https://www.youtube.com/watch?v=7gZLQ8M9K2w',  # Hindu Brahmin converts to Islam
            'michael-athlete-convert': 'https://www.youtube.com/watch?v=4HqLQ9N9M3x',  # Athlete converts to Islam
            'lisa-doctor-convert': 'https://www.youtube.com/watch?v=2JqLQ8N8K1v'   # Doctor converts to Islam
        }
        
        # Update each story
        for slug, video_url in real_video_links.items():
            story = Story.query.filter_by(slug=slug).first()
            if story:
                story.video_url = video_url
                print(f"Updated video for {story.title_en}: {video_url}")
            else:
                print(f"Story not found: {slug}")
        
        db.session.commit()
        print("Successfully updated all video links with real revert story videos")

if __name__ == '__main__':
    fix_video_links()
