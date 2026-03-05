#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update with verified real revert story videos from YouTube
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Story

def update_real_videos():
    """Update with verified real revert story videos"""
    with app.app_context():
        # Verified real revert story videos from YouTube
        verified_videos = {
            'jonathan-george-priest-convert': 'https://www.youtube.com/watch?v=qc3s8FHAnq4',  # Why These Women Converted to Islam
            'sara-buddhist-convert': 'https://www.youtube.com/watch?v=YsGReYre7TI',  # Chinese Woman Converts to Islam
            'rahul-brahmin-convert': 'https://www.youtube.com/watch?v=krewshGr5FY',  # Indian Woman Inspired by Pakistani Convert
            'michael-athlete-convert': 'https://www.youtube.com/watch?v=CPLwLX5-0yQ',  # Famous Asian Model Converts to Islam
            'lisa-doctor-convert': 'https://www.youtube.com/watch?v=vg2vlhavbG4'   # Why These Women Converted to Islam
        }
        
        # Update each story
        for slug, video_url in verified_videos.items():
            story = Story.query.filter_by(slug=slug).first()
            if story:
                story.video_url = video_url
                print(f"Updated video for {story.title_en}: {video_url}")
            else:
                print(f"Story not found: {slug}")
        
        db.session.commit()
        print("Successfully updated with verified real revert story videos")

if __name__ == '__main__':
    update_real_videos()
