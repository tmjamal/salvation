#!/usr/bin/env python3
"""
Add 'The Reverts' story category for recent converts to Islam
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, StoryCategory

def add_reverts_category():
    """Add the 'The Reverts' category for recent converts to Islam"""
    with app.app_context():
        # Check if category already exists
        existing = StoryCategory.query.filter_by(name_en='The Reverts').first()
        if existing:
            print(f"Category 'The Reverts' already exists with ID: {existing.id}")
            return existing.id
        
        # Create new category
        category = StoryCategory(
            name_en='The Reverts',
            name_ml='ഇസ്ലാം സ്വീകരിച്ചവർ',
            slug='the-reverts',
            description_ml='ലോകമെമ്പാടും ഇസ്ലാം സ്വീകരിച്ച ആളുകളുടെ കഥകൾ'
        )
        
        db.session.add(category)
        db.session.commit()
        
        print(f"Created 'The Reverts' category with ID: {category.id}")
        return category.id

if __name__ == '__main__':
    add_reverts_category()
