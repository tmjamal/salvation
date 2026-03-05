#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check existing stories and categories
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Story, StoryCategory

def check_stories():
    """Check existing stories and categories"""
    with app.app_context():
        print("Categories:")
        for cat in StoryCategory.query.all():
            print(f'- {cat.name_en}')
        
        print("\nStories:")
        for story in Story.query.all():
            print(f'- {story.title_en}')

if __name__ == '__main__':
    check_stories()
